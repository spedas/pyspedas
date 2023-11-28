import os
import numpy as np
import pandas as pd
import pytplot

import pyspedas
from .config import CONFIG
from pytplot import store_data, options

# MTH5 installation is checked in __init__
from mth5.clients.make_mth5 import FDSN
from mth5.mth5 import MTH5

from pyspedas.mth5.utilities import mth5_time_str

from datetime import datetime

def load_fdsn(trange=None, network=None, station=None, nodownload=False):
    """
    Load FDSN data using MTH5 interface.

    Parameters:
        trange : list of str
            Time range of interest.
        network : str
            Network name.
        station : str
            Station name.

    Returns:
        List of tplot variables created.
    """

    # If trange is not specified we don't know what to load
    if trange is None:
        pyspedas.logging.info("trange not specified")
        return

    if not network:
        pyspedas.logging.info("Network not specified")
        return

    if not station:
        pyspedas.logging.info("Station not specified")
        return

    # Determine where data will be stored
    mth5dir = CONFIG['local_data_dir']
    # if os.environ.get('SPEDAS_DATA_DIR'):
    #     mth5dir = os.environ['SPEDAS_DATA_DIR']

    # Get MTH5 file from the server
    # we use "*F*" channel instead of "*" to extract magnetic data
    # TODO: modify according to SEED manual appendix A: https://www.fdsn.org/pdf/SEEDManual_V2.4_Appendix-A.pdf
    request_df = pd.DataFrame(
        {
            "network": [network],
            "station": [station],
            "location": ["--"],
            "channel": ["*F*"],
            "start": [mth5_time_str(trange[0])],  # ["2019-11-14T00:00:00"],
            "end":  [mth5_time_str(trange[1])]  # ["2019-11-15T00:00:00"]
        }
    )

    # print(request_df)

    # Create time variables that correspond to the request time period
    request_start = datetime.fromisoformat(request_df.start[0])
    request_end = datetime.fromisoformat(request_df.end[0])

    mth5_filename = f"{network}_{station}_{trange[0]}_{trange[1]}.h5".replace(":", "").replace("-", "")
    mth5_pathfile = os.path.join(mth5dir, mth5_filename)

    # Implementation of caching
    if nodownload and os.path.isfile(mth5_pathfile):
        mth5_path = mth5_pathfile
    else:
        # Initialize FDSN object
        fdsn_object = FDSN(mth5_version='0.2.0', client="IRIS")
        try:
            mth5_path = fdsn_object.make_mth5_from_fdsn_client(request_df, interact=False, path=mth5dir)
            if os.path.isfile(mth5_pathfile):
                pytplot.logger.info(f"Removing cached {mth5_pathfile}")
                os.remove(mth5_pathfile)
            pytplot.logger.info(f"Creating cached {mth5_pathfile}")
            os.rename(mth5_path, mth5_pathfile)
            mth5_path = mth5_pathfile
        except Exception:
            # This code is obsolete with updated MTH5
            # Hande mth5 object initialization error. This error may occur if MTH5 file was not closed.
            pyspedas.logger.error("Cannot initialize mth5 object")
            mth5filename = fdsn_object.make_filename(request_df)
            mth5file = os.path.join(mth5dir, mth5filename)
            # attempt find the open file identifier and close it
            if os.path.exists(mth5file):
                # h5py must be installed as a requirement of MTH5
                import h5py
                fids = h5py.h5f.get_obj_ids(types=h5py.h5f.OBJ_FILE)
                for fid in fids:
                    # Test if the open file handler is the one we want to close
                    if os.path.basename(fid.name.decode('utf8')) == mth5filename:
                        h5py.File(fid).close()
                        pyspedas.logger.info(f"mth5 file {mth5filename} object is now closed.")
            raise

    # Using MTH5 as a context manager
    with MTH5() as mth5_object:
        mth5_object.open_mth5(mth5_path)
        surveys = mth5_object.surveys_group.groups_list

        # mth5_object = MTH5()
        # mth5_object.open_mth5(mth5_path)
        # surveys = mth5_object.surveys_group.groups_list
        # # print(surveys)

        # Create new data for time, x, y and z
        # TODO: is there a better way to create a new time array?
        time = np.array([])
        attributes = [('hx', 'bx'), ('hy', 'by'), ('hz', 'bz')]
        variables = {'x': np.array([]), 'y': np.array([]), 'z':np.array([])}

        attr_dict = {}  # metadata
        units = set()  # basic units
        measurements_type = set()  # basic type of measurements

        # loop over surveys and runs
        for survey in surveys:
            station_data = mth5_object.get_station(station_name=station, survey=survey)
            attr_dict["metadata"] = station_data.metadata

            # TODO: Check orientation reference frame
            # "orientation.reference_frame": "geographic"

            # Loop over runs
            for run_name in station_data.metadata.run_list:
                # Get the data
                run_data = station_data.get_run(run_name=run_name)

                # Check run time coverage
                run_start =  datetime.fromisoformat(run_data.metadata.time_period.start).replace(tzinfo=None)
                run_end = datetime.fromisoformat(run_data.metadata.time_period.end).replace(tzinfo=None)

                # Skip processing if run is outside requested time range
                if run_start > request_end or run_end < request_start:
                    continue

                # Get the run table summary
                # TODO: figure out why time cut does not work
                run_ts = run_data.to_runts(start=request_df.start[0], end=request_df.end[0])

                # Determine is we have all components
                # can channels_recorded_magnetic be missing from the dataset?
                # TODO: What to do with the runs without 3 components - operate only with 3 components for now...
                if 'channels_recorded_magnetic' in run_ts.dataset.attrs:
                    if len(run_ts.dataset.channels_recorded_magnetic) != 3:
                        pyspedas.logger.info("Run has less than 3 components")
                        continue
                else:
                    pyspedas.logger.warning("Run dataset has no channels_recorded_magnetic attribute")
                    continue

                # Check if the filters are available to calibrate data
                if len(run_ts.filters)  == 0:
                    pyspedas.logger.warning("Filters were not added to run_ts")
                    continue

                # Convert counts to physical units
                run_ts = run_ts.calibrate()

                # Copy numpy arrays to ensure that data is in memory after mth5 is closed
                if time.size == 0:
                    time = run_ts.dataset.time.to_numpy()
                else:
                    time = np.append(time, run_ts.dataset.time.to_numpy())

                # Check if all required attributes are present
                all_attributes_present = all(
                    hasattr(run_ts.dataset, attr_h) or hasattr(run_ts.dataset, attr_b)
                    for attr_h, attr_b in attributes
                )
                if all_attributes_present:
                    for (attr_h, attr_b), var_name in zip(attributes, variables.keys()):
                        if hasattr(run_ts.dataset, attr_h):
                            data = getattr(run_ts.dataset, attr_h)
                        elif hasattr(run_ts.dataset, attr_b):
                            data = getattr(run_ts.dataset, attr_b)
                        else:
                            pyspedas.logger.warning(f"Neither {attr_h} nor {attr_b} found in run dataset")
                            continue

                        variables[var_name] = np.append(variables[var_name], data.to_numpy())

                        try:
                            units.add(data.units)
                            measurements_type.add(data.type)
                        except AttributeError:
                            pyspedas.logger.warning(f"Problem with adding {attr_h}/{attr_b} dataset units or type")

                    # After the loop, you can reassign the modified arrays back to x, y, z
                    # x, y, z = variables['x'], variables['y'], variables['z']
                else:
                    pyspedas.logger.warning("Some of the attributes are not present in run_ts dataset")
                    continue

                # x = np.append(x, run_ts.dataset.hx.to_numpy())
                # y = np.append(y, run_ts.dataset.hy.to_numpy())
                # z = np.append(z, run_ts.dataset.hz.to_numpy())
                #
                # try:
                #     units.add(run_ts.dataset.hx.units)
                #     units.add(run_ts.dataset.hy.units)
                #     units.add(run_ts.dataset.hz.units)
                # except AttributeError:
                #     pyspedas.logger.warning("Problem with adding run dataset units")
                #
                # try:
                #     measurements_type.add(run_ts.dataset.hx.type)
                #     measurements_type.add(run_ts.dataset.hx.type)
                #     measurements_type.add(run_ts.dataset.hx.type)
                # except AttributeError:
                #     pyspedas.logger.warning("Problem with adding run dataset type")

        # TODO: Should data be sorted before saving
        data = {'x': time, 'y': np.vstack((variables['x'], variables['y'], variables['z'])).T}
        tplot_variable = 'fdsn_' + network + '_' + station

        # TODO: Add metadata

        # TODO: Clip time according to original times, add noclip parameter

        store_data(tplot_variable, data=data, attr_dict=attr_dict)
        tplot_options = {
            "name": f"FDSN: {network}, station: {station}",  # network and stations
            "ytitle": f"{','.join(list(measurements_type))}",  # measurment
            "ysubtitle": f"{','.join(list(units))}"  # units
        }

        options(tplot_variable, opt_dict=tplot_options)

        # It is crucial to close mth5 file
        # mth5_object.close_mth5()
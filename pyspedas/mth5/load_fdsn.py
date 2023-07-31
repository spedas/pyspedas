import os
import numpy as np
import pandas as pd
import pyspedas
from .config import CONFIG
from pytplot import store_data, options

# MTH5 installation is checked in __init__
from mth5.clients.make_mth5 import FDSN
from mth5.mth5 import MTH5

from pyspedas.mth5.utilities import mth5_time_str

def load_fdsn(trange=None, network=None, station=None):
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

    fdsn_object = FDSN(mth5_version='0.2.0', client="IRIS")

    # Determine where data will be stored
    mth5dir = CONFIG['local_data_dir']
    # if os.environ.get('SPEDAS_DATA_DIR'):
    #     mth5dir = os.environ['SPEDAS_DATA_DIR']

    # Get MTH5 file from the server
    # TODO: channel should not be a "*" - we use "*F*"
    request_df = pd.DataFrame(
        {
            "network": [network],
            "station": [station],
            "location": ["--"],
            "channel": ["*F*"],
            "start": [mth5_time_str(trange[0])], #  ["2019-11-14T00:00:00"],
            "end":  [mth5_time_str(trange[1])] # ["2019-11-15T00:00:00"]
        }
    )

    try:
        mth5_path = fdsn_object.make_mth5_from_fdsn_client(request_df, interact=False, path=mth5dir)
    except Exception:
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

    # TODO: change to context manager as below:
    # with mth5_object.open_mth5(mth5_path) as mth5_object_ref
    # with mth5_object.open_mth5(mth5_path) as m

    mth5_object = MTH5()
    mth5_object.open_mth5(mth5_path)
    surveys = mth5_object.surveys_group.groups_list
    # print(surveys)

    # Create new data for time, x, y and z
    # TODO: is there a better way to create a new time array?
    time = np.array([])
    x = np.array([])
    y = np.array([])
    z = np.array([])

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

            # Get the run table summary
            run_ts = run_data.to_runts()

            # Determine is we have all components
            # TODO: What to do with the runs without 3 components - operate only with 3 components for now...
            # TODO: can channels_recorded_magnetic be missing from the dataset?
            if len(run_ts.dataset.channels_recorded_magnetic) != 3:
                continue

            # Copy numpy arrays to ensure that data is in memory after mth5 is closed
            if not time:
                time = run_ts.dataset.time.to_numpy()
            else:
                time = np.append(time, run_ts.dataset.time.to_numpy())

            # TODO: can channels_recorded_magnetic not be hx, hy, hz? Just in case add the check
            x = np.append(x, run_ts.dataset.hx.to_numpy())
            y = np.append(y, run_ts.dataset.hy.to_numpy())
            z = np.append(z, run_ts.dataset.hz.to_numpy())

            try:
                units.add(run_ts.dataset.hx.units)
                units.add(run_ts.dataset.hy.units)
                units.add(run_ts.dataset.hz.units)
            except AttributeError:
                pyspedas.logger.warning("Problem with adding  run dataset units")

            try:
                measurements_type.add(run_ts.dataset.hx.type)
                measurements_type.add(run_ts.dataset.hx.type)
                measurements_type.add(run_ts.dataset.hx.type)
            except AttributeError:
                pyspedas.logger.warning("Problem with adding run dataset type")

    # TODO: Should data be sorted before saving
    data = {'x': time, 'y': np.vstack((x, y, z)).T}
    tplot_variable = 'fdsn_' + network + '_' + station

    # TODO: Add metadata


    store_data(tplot_variable, data=data, attr_dict=attr_dict)
    tplot_options = {
        "name": f"FDSN: {network}, station: {station}",  # network and stations
        "ytitle": f"{','.join(list(measurements_type))}",  # measurment
        "ysubtitle": f"{','.join(list(units))}"  # units
    }

    options(tplot_variable, opt_dict=tplot_options)

    # It is crucial to close mth5 file
    mth5_object.close_mth5()
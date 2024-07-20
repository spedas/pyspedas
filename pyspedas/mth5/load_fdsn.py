import os

import mth5
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
from pyspedas.mth5.utilities import _list_of_fdsn_channels

from datetime import datetime


def _disable_loguru_warnings(record):
    if record["extra"].get("no_warning"):
        return record["level"].no != mth5.logger.level("WARNING").no
    return True

def _request_df_from_input(trange, network, station):
    """
    Create a request_df from input parameters.

    Parameters
    ----------
        trange : list of str
            Time range of interest.
        network : str
            Network name.
        station : str
            Station name.

    Returns
    -------
    request_df : pandas.DataFrame
        Request dataframe.
    """

    # Get MTH5 file from the server
    # we use "*F*" channel instead of "*" to extract magnetic data
    # TODO: modify according to SEED manual appendix A: https://www.fdsn.org/pdf/SEEDManual_V2.4_Appendix-A.pdf
    channel_list = _list_of_fdsn_channels()
    # channel_list = "*F*"

    # Create request_df from input parameters
    request_df = pd.DataFrame(
        {
            "network": [network],
            "station": [station],
            "location": ["--"],
            "channel": [channel_list],
            "start": [mth5_time_str(trange[0])],  # ["2019-11-14T00:00:00"],
            "end": [mth5_time_str(trange[1])]  # ["2019-11-15T00:00:00"]
        }
    )

    return request_df


def _validate_date_format(date_string):
    """
    Validate if a date string is in the correct format.

    Parameters
    ----------
    date_string : str
        The date string to validate. Expected format: YYYY-MM-DDThh:mm:ss.

    Raises
    ------
    ValueError
        If the date string is not in the expected format.
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Expected format: YYYY-MM-DDThh:mm:ss")


def load_fdsn(trange=None, network=None, station=None,
              nodownload=False, noexception=False, print_request=False,
              nowarnings=False, request_df=None):
    """
    Load FDSN data using MTH5 interface.

    Parameters
    ----------
    trange : list of str
        Time range of interest.
    network : str
        Network name.
    station : str
        Station name.
    nodownload : bool, default=False
        If h5 file is already created do not load another one.
    noexception : bool, default=False
        If true, do not raise an exception produced by FDSN.
    print_request : bool, default=False
        Print request_df structure, which can be useful for debugging the request.
    nowarnings : bool, default=False
        If true, disable loguru warnings.
    request_df : pandas.DataFrame, optional
        Custom request_df dataframe for the `make_mth5_from_fdsn_client` method of the `FDSN` class.
        This parameter is optional, and it is not advised to use it unless the user knows exactly what to do.
        request_df must contain the following:

        - One `station`, one `network`, and one `location` as a list.
        - A list of 3 strings for `channels`.
        - The `start` and `end` date fields must contain a list of one string.

        See `pyspedas.mth5.load_fdsn._request_df_from_input` implementation for reference.

    Returns
    -------
    tplot_variable : str or None
        Tplot variable name. Tplot variable is created if data is loaded successfully, None otherwise.
    """

    # mth5.logger.remove()
    mth5.logger._core.extra["no_warning"] = nowarnings

    # If trange is not specified we don't know what to load
    if trange is None:
        pyspedas.logging.error("trange not specified")
        return

    if not network:
        pyspedas.logging.error("Network not specified")
        return

    if not station:
        pyspedas.logging.error("Station not specified")
        return

    # Handle request_df
    if request_df is None:
        request_df = _request_df_from_input(trange, network, station)
    else:
        network = request_df.network
        station = request_df.station
        trange = [request_df.start[0], request_df.end[0]]

    if print_request:
        print(request_df.to_string())

    # Create time variables that correspond to the request time period
    request_start = datetime.fromisoformat(request_df.start[0])
    request_end = datetime.fromisoformat(request_df.end[0])

    # Validate time period
    _validate_date_format(request_df.start[0])
    _validate_date_format(request_df.end[0])

    # Determine where data will be stored
    mth5dir = CONFIG['local_data_dir']
    # if os.environ.get('SPEDAS_DATA_DIR'):
    #     mth5dir = os.environ['SPEDAS_DATA_DIR']

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
                pytplot.logger.info(f"Deleting cached {mth5_pathfile}")
                os.remove(mth5_pathfile)
            pytplot.logger.info(f"Creating cached {mth5_pathfile}")
            os.rename(mth5_path, mth5_pathfile)
            mth5_path = mth5_pathfile
        except Exception as e:
            # Hande mth5 object initialization error.
            pyspedas.logger.error(f"Cannot initialize mth5 object:\n{e}")

            # # Check if file was the cache file was created
            # if 'mth5_path' in locals() and os.path.isfile(mth5_path):
            #     pytplot.logger.info(f"Cache was created and will be deleted: {mth5_path}")
            #     os.remove(mth5_path)

            # Exit code by flag
            if noexception:
                return
            raise
        finally:
            mth5_tmp = fdsn_object.make_filename(request_df)
            mth5_file = os.path.join(mth5dir, mth5_tmp)
            if os.path.isfile(mth5_file):
                pytplot.logger.info(f"Deleting mth5 temporary h5 file {mth5_tmp}")
                os.remove(mth5_file)

    # Using MTH5 as a context manager
    with MTH5() as mth5_object:
        mth5_object.open_mth5(mth5_path)
        surveys = mth5_object.surveys_group.groups_list

        # mth5_object = MTH5()
        # mth5_object.open_mth5(mth5_path)
        # surveys = mth5_object.surveys_group.groups_list
        # # print(surveys)

        # Create new data for time, x, y and z
        time = np.array([])
        attributes = [('hx', 'bx'), ('hy', 'by'), ('hz', 'bz')]
        variables = {'x': np.array([]), 'y': np.array([]), 'z': np.array([])}

        attr_dict = {'filename': mth5_path}  # metadata with filename
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
                run_start = datetime.fromisoformat(run_data.metadata.time_period.start).replace(tzinfo=None)
                run_end = datetime.fromisoformat(run_data.metadata.time_period.end).replace(tzinfo=None)

                # Skip processing if run is outside requested time range
                if run_start > request_end or run_end < request_start or request_end <= request_start:
                    continue

                # Get the run table summary
                # Time clips according to original times
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
                if len(run_ts.filters) == 0:
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

        # TODO: Should data be sorted before saving
        data = {'x': time, 'y': np.vstack((variables['x'], variables['y'], variables['z'])).T}
        tplot_variable = 'fdsn_' + network + '_' + station

        # Handle legends
        legend_names = ['x', 'y', 'z']
        try:
            legend_names = station_data.metadata.channels_recorded
        except AttributeError or UnboundLocalError:
            pyspedas.logger.error("station_data was not defined correctly")
            # Also raise this exception if noexception flag is set
            if not noexception:
                raise

        tplot_variable_created = False
        try:
            store_data(tplot_variable, data=data, attr_dict=attr_dict)
            tplot_variable_created = True
        except IndexError:
            pyspedas.logger.error(f"Cannot create empty tplot variabe {tplot_variable}")
        except Exception as E:
            pyspedas.logger.error(f"Unexpected error {E} while creating tplot variable {tplot_variable}")
            if not noexception:
                raise

        if tplot_variable_created:
            tplot_options = {
                "name": f"FDSN: {network}, station: {station}",  # network and stations
                "ytitle": f"{','.join(list(measurements_type))}",  # measurement
                "ysubtitle": f"{','.join(list(units))}",  # units
                "legend_names": legend_names
            }

            options(tplot_variable, opt_dict=tplot_options)

            # TODO: For potential future implementation
            #     filename : bool, default=False
            #         If true, return filename as a second return parameter

            return tplot_variable

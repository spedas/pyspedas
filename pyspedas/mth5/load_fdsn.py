import os
import numpy as np
import pandas as pd
import pyspedas
from .config import CONFIG
from pytplot import store_data

def load_fdsn(trange=['2019-11-14', '2019-11-15'], network=None, station=None):
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

    mth5dir = CONFIG['local_data_dir']
    # if os.environ.get('SPEDAS_DATA_DIR'):
    #     mth5dir = os.environ['SPEDAS_DATA_DIR']

    if not network:
        pyspedas.logging.info("Network not specified")
        return

    if not station:
        pyspedas.logging.info("Station not specified")
        return

    fdsn_object = FDSN(mth5_version='0.2.0', client="IRIS")

    # Get MTH5 file from the server
    # TODO: convert trange to a proper start and end time
    # TODO: channel should not be a "*" - we use "*F*"
    request_df = pd.DataFrame(
        {
            "network": [network],
            "station": [station],
            "location": ["--"],
            "channel": ["*F*"],
            "start": [trange[0]], #  ["2019-11-14T00:00:00"],
            "end":  [trange[1]] # ["2019-11-15T00:00:00"]
        }
    )

    try:
        mth5_path = fdsn_object.make_mth5_from_fdsn_client(request_df, interact=False, path=mth5dir)
    except:
        pyspedas.logger.error("Cannot initialize mth5 object")
        filename = fdsn_object.make_filename(request_df)
        # attempt to open and close
        if os.path.exists(mth5dir + filename):
            # This code does not seem to be working
            # TODO: figure out how to close mth5 object if error
            with open(mth5dir + filename) as f: f.close()
            pyspedas.logger.info("mth5 file object is closed")
        return

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

    # loop over surveys and runs
    for survey in surveys:
        station_data = mth5_object.get_station(station_name=station, survey=survey)

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

    # TODO: Should data be sorted before saving
    data = {'x': time, 'y': np.vstack((x, y, z)).T}
    tplot_variable = 'fdsn_' + network + '_' + station

    # TODO: Add metadata
    store_data(tplot_variable, data=data)

    # It is crucial to close mth5 file
    mth5_object.close_mth5()
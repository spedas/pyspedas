import os

import mth5
import numpy as np
import pandas as pd
import pyspedas
from .config import CONFIG
from pyspedas.tplot_tools import store_data, options

# MTH5 installation is checked in __init__
from mth5.clients.fdsn import FDSN
from mth5.mth5 import MTH5

from pyspedas.mth5.utilities import mth5_time_str
from pyspedas.mth5.utilities import _list_of_fdsn_channels

from datetime import datetime
from packaging.version import Version


# Physical field definitions, keyed by datatype ('mag', 'elec').
# The only place that knows magnetic vs. electric.
# print_name: human-readable field name used in log messages, e.g. 'magnetic'.
# components: MTH5 component names per output column, in order of preference,
#     e.g. ('hx', 'bx') -> use hx if present, otherwise bx.
# name: run_ts.dataset attribute listing the recorded components,
#     e.g. 'channels_recorded_magnetic' -> ['hx', 'hy', 'hz'].
# labels: names of the output columns, e.g. ['x', 'y', 'z'].
# instrument: SEED instrument code to request, e.g. 'F' -> channels LFE, LFN, LFZ.
_FIELDS = {
    'mag': {'print_name': 'magnetic', 'instrument': 'F', 'components': [('hx', 'bx'), ('hy', 'by'), ('hz', 'bz')],
            'name': 'channels_recorded_magnetic', 'labels': ['x', 'y', 'z']},
    'elec': {'print_name': 'electric', 'instrument': 'Q', 'components': [('ex',), ('ey',)],
             'name': 'channels_recorded_electric', 'labels': ['x', 'y']},
}


def _disable_loguru_warnings(record):
    if record["extra"].get("no_warning"):
        return record["level"].no != mth5.logger.level("WARNING").no
    return True

def _request_df_from_input(trange, network, station, instruments='F'):
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
        instruments : str, default='F'
            SEED instrument codes to request, e.g. 'F' (magnetic) or 'FQ' (magnetic and electric).

    Returns
    -------
    request_df : pandas.DataFrame
        Request dataframe.
    """

    # Get MTH5 file from the server
    # we use "*F*" channel instead of "*" to extract magnetic data
    channel_list = _list_of_fdsn_channels(instruments=instruments)
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
              nowarnings=False, request_df=None, downloadonly=False, datatype='mag'):
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
        - A list of one comma-separated string of SEED channel codes for `channel`, e.g. 'LFE,LFN,LFZ'.
        - The `start` and `end` date fields must contain a list of one string.

        See `pyspedas.mth5.load_fdsn._request_df_from_input` implementation for reference.
        The extracted fields and the cache file name follow `datatype`, not the channels in request_df:
        request the channels that match `datatype` (e.g. electric 'LQ?' channels for 'elec'),
        otherwise no tplot variable is created for the missing field.
    downloadonly : bool, default=False
        If true, return the path to the downloaded/cached MTH5 file instead of loading
        its data into a tplot variable.
    datatype : str or list of str, default='mag'
        Physical field(s) to load:

        - 'mag': magnetic field, tplot variable `fdsn_mag_<network>_<station>`.
        - 'elec': electric field, tplot variable `fdsn_elec_<network>_<station>`.
        - ['mag', 'elec']: both.
        - 'legacy': magnetic field only, as in earlier versions: tplot variable
          `fdsn_<network>_<station>` and magnetic-only cache file. Cannot be combined with other values.

        Only the requested fields are downloaded. The cache file name ends with the SEED instrument
        codes: `..._F.h5` ('mag'), `..._Q.h5` ('elec'), `..._FQ.h5` (['mag', 'elec']).
        An electric-only request can fail in mth5 0.6.9 and earlier when a station run has no electric
        channels in the requested period; a warning is logged. Use ['mag', 'elec'] if it fails.

    Returns
    -------
    tplot_variable : list of str, str or None
        Tplot variable names (a list) for 'mag'/'elec'; a single name (str) for 'legacy';
        None if no tplot variable was created.
        If `downloadonly` is true, the path to the downloaded/cached MTH5 file is returned instead.
        If runs differ in coordinate system, units, or measurement type, additional tplot
        variables with `_1`, `_2`, ... suffixes are created; for 'legacy' only the primary (base)
        name is returned.
    """

    # mth5.logger.remove()
    mth5.logger._core.extra["no_warning"] = nowarnings

    # If trange is not specified we don't know what to load
    if trange is None:
        pyspedas.logging.error("trange not specified")
        return

    if len(trange) != 2:
        pyspedas.logging.error("trange must have exactly 2 elements")
        return

    if not network:
        pyspedas.logging.error("Network not specified")
        return

    if not station:
        pyspedas.logging.error("Station not specified")
        return

    # Normalize datatype to a list, e.g. 'mag' -> ['mag']
    datatypes = [datatype] if isinstance(datatype, str) else list(datatype)
    legacy = datatypes == ['legacy']
    if legacy:
        # legacy extracts magnetic data exactly as earlier versions did
        datatypes = ['mag']
    elif not datatypes or any(d not in _FIELDS for d in datatypes):
        # 'legacy' combined with other values also ends up here
        pyspedas.logging.error(f"Invalid datatype {datatype}. Use 'mag', 'elec', ['mag', 'elec'] or 'legacy'")
        return

    # SEED instrument codes to request, sorted so the cache name does not depend on datatype order,
    # e.g. ['mag'] -> 'F', ['elec'] -> 'Q', ['elec', 'mag'] -> 'FQ'
    instruments = ''.join(sorted({_FIELDS[d]['instrument'] for d in datatypes}))

    # mth5 0.6.9 and earlier: StationGroup.update_metadata fails with a pydantic ValidationError
    # when a run has none of the requested channels, e.g. an electric-only request at a station
    # whose electric channel epochs are split (8P/CAS04). Magnetic channels usually span all runs.
    # 0.6.9 is the latest affected version known (no fixed release yet); update it if a later
    # release is still affected.
    if instruments == 'Q' and Version(mth5.__version__) <= Version("0.6.9"):
        pyspedas.logger.warning(
            f"Electric-only requests can fail in mth5 {mth5.__version__} when a station run has no "
            "electric channels in the requested period. Use datatype=['mag', 'elec'] if it fails."
        )

    # Handle request_df
    if request_df is None:
        request_df = _request_df_from_input(trange, network, station, instruments=instruments)
    else:
        network = request_df.network[0]
        station = request_df.station[0]
        trange = [request_df.start[0], request_df.end[0]]

    if print_request:
        print(request_df.to_string())

    # Validate time period
    _validate_date_format(request_df.start[0])
    _validate_date_format(request_df.end[0])

    # Create time variables that correspond to the request time period
    request_start = datetime.fromisoformat(request_df.start[0])
    request_end = datetime.fromisoformat(request_df.end[0])

    if request_end <= request_start:
        pyspedas.logging.error(f'End time {request_end} earlier or equal to start time {request_start}')
        return

    # Determine where data will be stored
    mth5dir = CONFIG['local_data_dir']
    # if os.environ.get('SPEDAS_DATA_DIR'):
    #     mth5dir = os.environ['SPEDAS_DATA_DIR']

    # Non-legacy cache files get an instrument suffix (e.g. _FQ) so a magnetic-only legacy file is never reused
    cache_suffix = '' if legacy else f"_{instruments}"
    mth5_filename = f"{network}_{station}_{trange[0]}_{trange[1]}{cache_suffix}.h5".replace(":", "").replace("-", "")
    mth5_pathfile = os.path.join(mth5dir, mth5_filename)

    # Implementation of caching
    if nodownload and os.path.isfile(mth5_pathfile):
        mth5_path = mth5_pathfile
    else:
        # Initialize FDSN object
        fdsn_object = FDSN(mth5_version='0.2.0', client="EARTHSCOPE")
        try:
            mth5_path = fdsn_object.make_mth5_from_fdsn_client(request_df, interact=False, path=mth5dir)
            if os.path.isfile(mth5_pathfile):
                pyspedas.logger.info(f"Deleting cached {mth5_pathfile}")
                os.remove(mth5_pathfile)
            pyspedas.logger.info(f"Creating cached {mth5_pathfile}")
            os.rename(mth5_path, mth5_pathfile)
            mth5_path = mth5_pathfile
        except Exception as e:
            # Handle mth5 object initialization error.
            pyspedas.logger.error(f"Cannot initialize mth5 object:\n{e}")

            # # Check if file was the cache file was created
            # if 'mth5_path' in locals() and os.path.isfile(mth5_path):
            #     pyspedas.logger.info(f"Cache was created and will be deleted: {mth5_path}")
            #     os.remove(mth5_path)

            # Exit code by flag
            if noexception:
                return
            raise
        finally:
            mth5_tmp = fdsn_object.make_filename(request_df)
            mth5_file = os.path.join(mth5dir, mth5_tmp)
            if os.path.isfile(mth5_file):
                pyspedas.logger.info(f"Deleting mth5 temporary h5 file {mth5_tmp}")
                os.remove(mth5_file)

    if downloadonly:
        return mth5_path

    # Using MTH5 as a context manager
    with MTH5() as mth5_object:
        mth5_object.open_mth5(mth5_path)
        surveys = mth5_object.surveys_group.groups_list

        # mth5_object = MTH5()
        # mth5_object.open_mth5(mth5_path)
        # surveys = mth5_object.surveys_group.groups_list
        # # print(surveys)

        # Initialize run-record collection (one list of processed runs per datatype) before merging,
        # e.g. {'mag': [run_record, ...], 'elec': [...]}.
        run_records = {datatype: [] for datatype in datatypes}
        last_station_metadata = None

        # loop over surveys and runs
        for survey in surveys:
            station_data = mth5_object.get_station(station_name=station, survey=survey)
            last_station_metadata = station_data.metadata

            # Record the station coordinate system for every run in this survey.
            # Example: "orientation.reference_frame": "geographic"
            try:
                reference_frame = station_data.metadata.orientation.reference_frame
                coord_sys = getattr(reference_frame, "value", reference_frame)
                coord_sys = str(coord_sys).lower()
            except AttributeError:
                coord_sys = None

            # Loop over runs
            for run_name in station_data.metadata.run_list:
                # Get the data
                run_data = station_data.get_run(run_name=run_name)

                # Check run time coverage
                # The times in the metadata may already be strings, or objects that are convertible to strings,
                # depending on which versions of mth5, obspy, and mt-metadata are being used.
                # We'll just call str() on whatever we get back and hope for the best...
                run_start = datetime.fromisoformat(str(run_data.metadata.time_period.start)).replace(tzinfo=None)
                run_end = datetime.fromisoformat(str(run_data.metadata.time_period.end)).replace(tzinfo=None)

                # Skip processing if run is outside requested time range
                if run_start > request_end or run_end < request_start or request_end <= request_start:
                    continue

                # Get the run table summary
                # Time clips according to original times
                run_ts = run_data.to_runts(start=request_df.start[0], end=request_df.end[0])

                # Determine which requested fields have at least one component to work with.
                # A run with fewer recorded channels than the field's columns is still
                # processed; the missing channel(s) are filled with NaN below.
                run_datatypes = []  # datatypes this run can provide, e.g. ['mag']
                for datatype in datatypes:  # e.g. 'mag', 'elec'
                    field = _FIELDS[datatype]
                    n_columns = len(field['labels'])
                    # e.g. run_ts.dataset.channels_recorded_magnetic == ['hx', 'hy', 'hz']
                    if field['name'] in run_ts.dataset.attrs:
                        num_channels = len(getattr(run_ts.dataset, field['name']))
                        if num_channels == 0:
                            pyspedas.logger.warning(f"Run has no {field['print_name']} components")
                            continue
                        if num_channels < n_columns:
                            pyspedas.logger.warning(f"Run has {num_channels} of {n_columns} {field['print_name']} components; missing ones will be NaN-filled")
                        run_datatypes.append(datatype)
                    else:
                        pyspedas.logger.warning(f"Run dataset has no {field['name']} attribute")
                # Skip the run only if none of the requested datatypes has components.
                if not run_datatypes:
                    continue

                # Check if the filters are available to calibrate data
                if len(run_ts.filters) == 0:
                    pyspedas.logger.warning("Filters were not added to run_ts")
                    continue

                # Convert counts to physical units.
                # Calibrated once per run: one run_ts holds all datatypes (e.g. ex, ey, hx, hy, hz).
                run_ts = run_ts.calibrate()

                for datatype in run_datatypes:
                    field = _FIELDS[datatype]

                    # Check if at least one channel is present to build a run from.
                    any_attribute_present = any(
                        hasattr(run_ts.dataset, attr)
                        for attrs in field['components'] for attr in attrs
                    )
                    if not any_attribute_present:
                        pyspedas.logger.warning("None of the attributes are present in run_ts dataset")
                        continue

                    # Capture calibrated data and metadata without merging it yet.
                    # Copy numpy arrays to ensure that data is in memory after mth5 is closed
                    run_time = run_ts.dataset.time.to_numpy()
                    run_variables = {}
                    # Keep one unit and measurement type entry for each channel.
                    run_units = []
                    run_measurements_type = []
                    # e.g. attrs=('hx', 'bx'), var_name='x'
                    for attrs, var_name in zip(field['components'], field['labels']):
                        attrs_str = '/'.join(attrs)  # e.g. 'hx/bx', used in log messages
                        present = [attr for attr in attrs if hasattr(run_ts.dataset, attr)]
                        if present:
                            # attrs are in order of preference: take the first one found (hx before bx)
                            data = getattr(run_ts.dataset, present[0])
                        else:
                            # Missing channel: NaN-fill so the output keeps a fixed
                            # number of columns; matplotlib skips NaN points natively.
                            pyspedas.logger.warning(f"None of {attrs_str} found in run dataset; filling {var_name} with NaN")
                            run_variables[var_name] = np.full(len(run_time), np.nan)
                            run_units.append(None)
                            run_measurements_type.append(None)
                            continue

                        # e.g. run_variables == {'x': array([...]), 'y': ..., 'z': ...}
                        run_variables[var_name] = data.to_numpy()

                        # Keep run_units/run_measurements_type aligned with run_variables
                        # (one entry per channel) even when a channel is missing
                        # its units or type, so a partial run gets its own signature
                        # instead of silently matching a fully-populated one.
                        try:
                            run_units.append(str(data.units))
                        except AttributeError:
                            pyspedas.logger.warning(f"Problem with adding {attrs_str} dataset units")
                            run_units.append(None)

                        try:
                            run_measurements_type.append(str(data.type))
                        except AttributeError:
                            pyspedas.logger.warning(f"Problem with adding {attrs_str} dataset type")
                            run_measurements_type.append(None)

                    # Preserve the run's coordinate, per-channel units, and measurement types as one signature.
                    # Identical per-channel values collapse to one entry,
                    # e.g. ('geographic', ('nanoTesla',), ('magnetic',)) or
                    # ('geographic', ('nT', None, 'nT'), ('magnetic',)) for a channel without units.
                    run_signature = (
                        coord_sys,
                        tuple(run_units[:1]) if len(set(run_units)) <= 1 else tuple(run_units),
                        tuple(run_measurements_type[:1]) if len(set(run_measurements_type)) <= 1 else tuple(run_measurements_type)
                    )
                    # Store one complete run record for the post-processing merge.
                    run_records[datatype].append({
                        "time": run_time,
                        "variables": run_variables,
                        "metadata": station_data.metadata,
                        "coord_sys": coord_sys,
                        "units": run_units,
                        "measurements_type": run_measurements_type,
                        "signature": run_signature,
                    })

        created_variables = []
        for datatype in datatypes:  # e.g. 'mag', 'elec'
            field = _FIELDS[datatype]
            n_columns = len(field['labels'])
            # Processed runs of this datatype: [{'time', 'variables', 'signature', ...}, ...]
            runs = run_records[datatype]

            # Identify unique run signatures and rank exceptional signatures by their combined time points.
            unique_signatures = {run_record["signature"] for run_record in runs}
            if len(unique_signatures) > 1:
                signature_time_sizes = {
                    signature: sum(
                        len(run_record["time"])
                        for run_record in runs
                        if run_record["signature"] == signature
                    )
                    for signature in unique_signatures
                }
                ordered_signatures = sorted(
                    signature_time_sizes.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
                pyspedas.logger.warning(
                    "FDSN data has inconsistent run metadata (coordinate system, "
                    f"units, or measurement type); splitting into separate tplot "
                    f"variables: {ordered_signatures}"
                )
            else:
                ordered_signatures = [(signature, None) for signature in unique_signatures]

            # Create the primary and any suffixed tplot variables from signature-selected runs.
            # e.g. legacy: fdsn_4P_REU49; otherwise fdsn_mag_4P_REU49, fdsn_elec_8P_CAS04
            if legacy:
                tplot_variable_base = f"fdsn_{network}_{station}"
            else:
                tplot_variable_base = f"fdsn_{datatype}_{network}_{station}"

            # No processed runs: still go through the loop once so the empty case is logged.
            if not ordered_signatures:
                ordered_signatures = [(None, None)]

            # Merge runs one signature group at a time in ranked order.
            for tplot_index, (signature, _) in enumerate(ordered_signatures):
                # Runs sharing this signature, merged into one tplot variable.
                signature_runs = [
                    run_record
                    for run_record in runs
                    if run_record["signature"] == signature
                ]
                if signature_runs:
                    time = np.concatenate([record["time"] for record in signature_runs])
                    variables = {
                        var_name: np.concatenate([record["variables"][var_name] for record in signature_runs])
                        for var_name in field['labels']  # e.g. 'x', 'y', 'z'
                    }
                    # Sort timestamps and vector components together before saving.
                    # Runs may arrive out of order; "stable" keeps equal timestamps in arrival order.
                    sort_index = np.argsort(time, kind="stable")
                    time = time[sort_index]
                    for var_name in variables:
                        variables[var_name] = variables[var_name][sort_index]
                    metadata = signature_runs[0]["metadata"]
                    coord_sys, units, measurements_type = signature
                else:
                    time = np.array([])
                    variables = {var_name: np.array([]) for var_name in field['labels']}  # e.g. 'x', 'y', 'z'
                    metadata = last_station_metadata
                    coord_sys = None
                    units = ()
                    measurements_type = ()

                # data['y'] has shape (N, n_columns), e.g. (N, 3) for mag, (N, 2) for elec.
                data = {'x': time, 'y': np.vstack([variables[var_name] for var_name in field['labels']]).T}
                tplot_variable = tplot_variable_base if tplot_index == 0 else f"{tplot_variable_base}_{tplot_index}"

                # Handle legends
                legend_names = field['labels']
                if legacy:
                    try:
                        legend_names = metadata.channels_recorded
                        # A partial run can leave fewer names than the data columns.
                        if len(legend_names) != n_columns:
                            legend_names = field['labels']
                    except AttributeError:
                        pyspedas.logger.error("station_data was not defined correctly")
                        if not noexception:
                            raise
                else:
                    # Station channels_recorded mixes fields (e.g. ['ex', 'ey', 'hx', 'hy', 'hz']),
                    # so use this field's preferred component names, e.g. ['hx', 'hy', 'hz'].
                    legend_names = [attrs[0] for attrs in field['components']]

                # Store PySPEDAS coordinate and units metadata with this output group.
                # str() turns a missing per-channel unit/type (None) into the
                # text "None" instead of raising on str.join.
                data_att = {'coord_sys': coord_sys}
                if units:
                    data_att['units'] = ','.join(str(unit) for unit in units)

                if measurements_type:
                    data_att['measurements_type'] = ','.join(str(measurement_type) for measurement_type in measurements_type)

                # metadata with filename
                attr_dict = {
                    'filename': mth5_path,
                    'metadata': metadata,
                    'data_att': data_att,
                }

                # Store the merged group as a tplot variable.
                tplot_variable_created = False
                try:
                    store_data(tplot_variable, data=data, attr_dict=attr_dict)
                    tplot_variable_created = True
                except IndexError:
                    pyspedas.logger.error(f"Cannot create empty tplot variable {tplot_variable}")
                except Exception as E:
                    pyspedas.logger.error(f"Unexpected error {E} while creating tplot variable {tplot_variable}")
                    if not noexception:
                        raise

                if tplot_variable_created:
                    # Apply group-specific plot labels and legends.
                    tplot_options = {
                        "name": f"FDSN: {network}, station: {station}",
                        "ytitle": data_att['measurements_type'],
                        "ysubtitle": data_att['units'],
                        "legend_names": legend_names,
                    }
                    options(tplot_variable, opt_dict=tplot_options)
                    created_variables.append(tplot_variable)

        if created_variables:
            # legacy returns one name (str) as earlier versions did; otherwise all created names (list)
            return created_variables[0] if legacy else created_variables

from pyspedas.projects.mms.mms_load_data import mms_load_data
from pyspedas.projects.mms.feeps_tools.mms_feeps_correct_energies import mms_feeps_correct_energies
from pyspedas.projects.mms.feeps_tools.mms_feeps_flat_field_corrections import mms_feeps_flat_field_corrections
from pyspedas.projects.mms.feeps_tools.mms_feeps_active_eyes import mms_feeps_active_eyes
from pyspedas.projects.mms.feeps_tools.mms_feeps_split_integral_ch import mms_feeps_split_integral_ch
from pyspedas.projects.mms.feeps_tools.mms_feeps_remove_bad_data import mms_feeps_remove_bad_data
from pyspedas.projects.mms.feeps_tools.mms_feeps_remove_sun import mms_feeps_remove_sun
from pyspedas.projects.mms.feeps_tools.mms_feeps_omni import mms_feeps_omni
from pyspedas.projects.mms.feeps_tools.mms_feeps_spin_avg import mms_feeps_spin_avg
from pyspedas.projects.mms.mms_config import CONFIG
from pytplot import time_clip as tclip

def recvary_log_filter(log):
    if 'record-varying' in log.msg:
        return False
    else:
        return True

def mms_load_feeps(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='electron', varformat=None, varnames=[], get_support_data=True, suffix='', time_clip=False,
    no_update=False, available=False, notplot=False, no_flatfield_corrections=False, data_units=['count_rate', 'intensity'], 
    latest_version=False, major_version=False, min_version=None, cdf_version=None, spdf=False, always_prompt=False, filter_recvary_warnings=True):
    """
    Load data from the MMS Fly's Eye Energetic Particle Sensor (FEEPS)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2015-10-16','2015-10-17']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4'].
            Default: '1'

        data_rate : str or list of str
            instrument data rates for FEEPS include ['brst', 'srvy'].
            Default: 'srvy'

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'
            Default: 'l2'

        datatype : str or list of str
            Valid datatypes for FEEPS are::

                       L2, L1b: ['electron', 'ion']
                       L1a: ['electron-bottom', 'electron-top', 'ion-bottom', 'ion-top']

            Default: 'electron'

        data_units : str or list of str
            Unit types to be loaded, options are 'count_rate', 'intensity'
            Default: ['count_rate', 'intensity']

        no_flatfield_corrections: bool
            If True, no flatfield corrections are performed.
            Default: False

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: True

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            Default: False
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables are loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded.
            Default: []

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.
            Default: None

        notplot: bool
            If True, then data are returned in a hash table instead of 
            being stored in tplot variables (useful for debugging, and
            access to multidimensional data products)
            Default: False

        available: bool
            If True, simply return the available data files (without downloading)
            for the requested parameters
            Default: False

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten
            Default: False

        cdf_version: str
            Specify a specific CDF version # to load (e.g., cdf_version='4.3.0')
            Default: None

        min_version: str
            Specify a minimum CDF version # to load
            Default: None

        latest_version: bool
            Only grab the latest CDF version in the requested time interval

        major_version: bool
            Only open the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidentally save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC

        filter_recvary_warnings: bool
            If True, capture warnings from cdf_to_tplot and filter out the ones complaining about non-record-varying support data with timestamps

    Returns
    --------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> feeps_data = pyspedas.projects.mms.mms_load_feeps(trange=['2015-10-16', '2015-10-17'], probe='1', datatype='electron')
    >>> tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin', 'mms1_epd_feeps_srvy_l2_electron_intensity_omni'])



    """

    # For log filtering
    from pyspedas import logger
    # as of 3 July 2023, there's a mixture of v7.x.x and v6.x.x files at the SDC
    # these files aren't compatible, so we need to only load the latest major version
    # to avoid crashes (unless otherwise specified)
    if not latest_version and not major_version and min_version is None and cdf_version is None:
        major_version = True

    if filter_recvary_warnings:
        logger.addFilter(recvary_log_filter)

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='feeps',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix,
            no_update=no_update, available=available, latest_version=latest_version,
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if filter_recvary_warnings:
        logger.removeFilter(recvary_log_filter)

    if tvars == [] or available or notplot or CONFIG['download_only'] or tvars is None:
        return tvars

    probes = probe if isinstance(probe, list) else [probe]
    data_rates = data_rate if isinstance(data_rate, list) else [data_rate]
    levels = level if isinstance(level, list) else [level]
    datatypes = datatype if isinstance(datatype, list) else [datatype]
    data_units = data_units if isinstance(data_units, list) else [data_units]

    probes = [str(p) for p in probes]

    mms_feeps_correct_energies(probes, data_rate, level=level, suffix=suffix)

    if not no_flatfield_corrections:
        mms_feeps_flat_field_corrections(probes=probes, data_rate=data_rate, suffix=suffix)

    for probe in probes:
        for lvl in levels:
            for drate in data_rates:
                for datatype in datatypes:
                    mms_feeps_remove_bad_data(trange=trange, probe=probe, data_rate=drate, datatype =datatype, level=lvl, suffix=suffix)

                    for data_unit in data_units:
                        eyes = mms_feeps_active_eyes(trange, probe, drate, datatype, lvl)

                        split_vars = mms_feeps_split_integral_ch(data_unit, datatype, probe, suffix=suffix, data_rate=drate, level=lvl, sensor_eyes=eyes)

                        sun_removed_vars = mms_feeps_remove_sun(eyes, trange, probe=probe, datatype=datatype, data_units=data_unit, data_rate=drate, level=lvl, suffix=suffix)

                        omni_vars = mms_feeps_omni(eyes, probe=probe, datatype=datatype, data_units=data_unit, data_rate=drate, level=lvl, suffix=suffix)

                        if split_vars is not None:
                            tvars = tvars + split_vars

                        if sun_removed_vars is not None:
                            tvars = tvars + sun_removed_vars

                        if omni_vars is not None:
                            tvars = tvars + omni_vars

                        spin_avg_vars = mms_feeps_spin_avg(probe=probe, data_units=data_unit, datatype=datatype, data_rate=drate, level=lvl, suffix=suffix)

                        if spin_avg_vars is not None:
                            tvars.append(spin_avg_vars)

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

from pyspedas.projects.mms.mms_load_data import mms_load_data
from pyspedas.projects.mms.eis_tools.mms_eis_omni import mms_eis_omni
from pyspedas.projects.mms.eis_tools.mms_eis_spin_avg import mms_eis_spin_avg
from pyspedas.projects.mms.eis_tools.mms_eis_set_metadata import mms_eis_set_metadata
from pyspedas.projects.mms.mms_config import CONFIG
from pytplot import tnames



def mms_load_eis(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='extof',
        varformat=None, varnames=[], get_support_data=True, suffix='', time_clip=False, no_update=False,
        available=False, notplot=False, latest_version=False, major_version=False, min_version=None, cdf_version=None, 
        spdf=False, always_prompt=False):
    """
    Load data from the MMS Energetic Ion Spectrometer (EIS)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2015-10-16', '2015-10-17']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4'].
            Default: '1'

        data_rate : str or list of str
            instrument data rates for EIS include ['brst', 'srvy'].
            Default: 'srvy'

        level : str
            indicates level of data processing.
            Default: 'l2'

        datatype : str or list of str
            Valid datatypes for EIS are: ['extof', 'phxtof', and 'electronenergy']
            Default: 'extof'

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: 'True'

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            Default: 'False'
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables are loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded.
            Default: []

        suffix: str
            The tplot variable names will be given this suffix.
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
            Default: False

        major_version: bool
            Only open the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval
            Default: False

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidentally save an incorrect password, or if your SDC password has changed
            Default: False

        spdf: bool
            If True, download the data from the SPDF instead of the SDC
            Default: False

    Returns
    -------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> eis_vars = pyspedas.projects.mms.mms_load_eis(trange=['2015-10-16', '2015-10-17'], probe='1', datatype=['phxtof', 'extof'])
    >>> # plot the non-spin averaged flux
    >>> tplot(['mms1_epd_eis_srvy_l2_extof_proton_flux_omni', 'mms1_epd_eis_srvy_l2_phxtof_proton_flux_omni'])
    >>> # plot the spin averaged flux
    >>> tplot(['mms1_epd_eis_srvy_l2_extof_proton_flux_omni_spin', 'mms1_epd_eis_srvy_l2_phxtof_proton_flux_omni_spin'])


    """

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='epd-eis',
            datatype=datatype, varformat=varformat, varnames=varnames, get_support_data=get_support_data, prefix='', suffix=suffix,
            time_clip=time_clip, no_update=no_update, available=available, latest_version=latest_version, 
            major_version=major_version, min_version=min_version, cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)

    if tvars == [] or available or notplot or CONFIG['download_only'] or tvars is None:
        return tvars

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]
    if not isinstance(datatype, list): datatype = [datatype]

    # the probes will need to be strings beyond this point
    if isinstance(probe, list):
        probe = [str(p) for p in probe]

    for probe_id in probe:
        for datatype_id in datatype:
            for level_id in level:
                for data_rate_id in data_rate:
                    if datatype_id == 'electronenergy':
                        e_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='electron', datatype=datatype_id, data_rate=data_rate_id, level=level_id, suffix=suffix)
                        # create non-spin averaged omni-directional spectra
                        e_omni_spectra = mms_eis_omni(probe_id, species='electron', data_rate=data_rate_id, level=level_id, datatype=datatype_id)
                        # create spin averaged omni-directional spectra
                        e_omni_spectra_spin = mms_eis_omni(probe_id, species='electron', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix+'_spin')
                        # add the vars to the output
                        if e_spin_avg_var is not None:
                            for tvar in e_spin_avg_var:
                                tvars.append(tvar)
                        if e_omni_spectra is not None:
                            tvars.append(e_omni_spectra)
                        if e_omni_spectra_spin is not None:
                            tvars.append(e_omni_spectra_spin)
                    elif datatype_id == 'extof':
                        # 9Feb2021, egrimes added 'helium' species for updates coming soon to the CDFs
                        p_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='proton', datatype=datatype_id, data_rate=data_rate_id, level=level_id, suffix=suffix)
                        o_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='oxygen', datatype=datatype_id, data_rate=data_rate_id, level=level_id, suffix=suffix)
                        a_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='alpha', datatype=datatype_id, data_rate=data_rate_id, level=level_id, suffix=suffix)
                        h_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='helium', datatype=datatype_id, data_rate=data_rate_id, level=level_id, suffix=suffix)
                        # create non-spin averaged omni-directional spectra
                        p_omni_spectra = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix)
                        o_omni_spectra = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix)
                        a_omni_spectra = mms_eis_omni(probe_id, species='alpha', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix)
                        h_omni_spectra = mms_eis_omni(probe_id, species='helium', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix)
                        # create spin averaged omni-directional spectra
                        p_omni_spectra_spin = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix+'_spin')
                        o_omni_spectra_spin = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix+'_spin')
                        a_omni_spectra_spin = mms_eis_omni(probe_id, species='alpha', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix+'_spin')
                        h_omni_spectra_spin = mms_eis_omni(probe_id, species='helium', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix+'_spin')
                        # add the vars to the output
                        if p_spin_avg_var is not None:
                            for tvar in p_spin_avg_var:
                                tvars.append(tvar)
                        if o_spin_avg_var is not None:
                            for tvar in o_spin_avg_var:
                                tvars.append(tvar)
                        if a_spin_avg_var is not None:
                            for tvar in a_spin_avg_var:
                                tvars.append(tvar)
                        if h_spin_avg_var is not None:
                            for tvar in h_spin_avg_var:
                                tvars.append(tvar)
                        if p_omni_spectra is not None:
                            tvars.append(p_omni_spectra)
                        if o_omni_spectra is not None:
                            tvars.append(o_omni_spectra)
                        if a_omni_spectra is not None:
                            tvars.append(a_omni_spectra)
                        if h_omni_spectra is not None:
                            tvars.append(h_omni_spectra)
                        if p_omni_spectra_spin is not None:
                            tvars.append(p_omni_spectra_spin)
                        if o_omni_spectra_spin is not None:
                            tvars.append(o_omni_spectra_spin)
                        if a_omni_spectra_spin is not None:
                            tvars.append(a_omni_spectra_spin)
                        if h_omni_spectra_spin is not None:
                            tvars.append(h_omni_spectra_spin)
                    elif datatype_id == 'phxtof':
                        # 9Feb2021, egrimes commented out oxygen calculations to match IDL updates
                        p_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='proton', datatype=datatype_id, data_rate=data_rate_id, level=level_id, suffix=suffix)
                        # o_spin_avg_var = mms_eis_spin_avg(probe=probe_id, species='oxygen', datatype=datatype_id, level=level_id, data_rate=data_rate_id, suffix=suffix)
                        # create non-spin averaged omni-directional spectra
                        p_omni_spectra = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, datatype=datatype_id, level=level_id, suffix=suffix)
                        # o_omni_spectra = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix)
                        # create spin averaged omni-directional spectra
                        p_omni_spectra_spin = mms_eis_omni(probe_id, species='proton', data_rate=data_rate_id, datatype=datatype_id, level=level_id, suffix=suffix+'_spin')
                        # o_omni_spectra_spin = mms_eis_omni(probe_id, species='oxygen', data_rate=data_rate_id, level=level_id, datatype=datatype_id, suffix=suffix+'_spin')
                        # add the vars to the output
                        if p_spin_avg_var is not None:
                            for tvar in p_spin_avg_var:
                                tvars.append(tvar)
                        # if o_spin_avg_var is not None:
                        #     for tvar in o_spin_avg_var:
                        #         tvars.append(tvar)
                        if p_omni_spectra is not None:
                            tvars.append(p_omni_spectra)
                        # if o_omni_spectra is not None:
                        #     tvars.append(o_omni_spectra)
                        if p_omni_spectra_spin is not None:
                            tvars.append(p_omni_spectra_spin)
                        # if o_omni_spectra_spin is not None:
                        #     tvars.append(o_omni_spectra_spin)

                    mms_eis_set_metadata(tnames(tvars), data_rate=data_rate_id, datatype=datatype_id, suffix=suffix)

    return tnames(tvars)

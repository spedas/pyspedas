from .load import load
from pyspedas.rbsp.rbspice_lib.rbsp_load_rbspice_read import rbsp_load_rbspice_read
from pyspedas.rbsp.rbspice_lib.rbsp_rbspice_omni import rbsp_rbspice_omni
from pyspedas.rbsp.rbspice_lib.rbsp_rbspice_spin_avg import rbsp_rbspice_spin_avg
from pyspedas.utilities.datasets import find_datasets


def emfisis(trange=['2018-11-5', '2018-11-6'], 
        probe='a',
        datatype='magnetometer', 
        level='l3',
        cadence='4sec', # for EMFISIS mag data
        coord='sm', # for EMFISIS mag 
        wavetype='waveform', # for EMFISIS waveform data
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Electric and Magnetic Field Instrument Suite and Integrated Science (EMFISIS) instrument

    For information on the EMFISIS data products, see:
        https://emfisis.physics.uiowa.edu/data/level_descriptions
    
    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype : str, default='magnetometer'
            Data type with options varying by data level.
            Level 1:
                'magnetometer'
                'hfr'
                'housekeeping'
                'sc-hk'
                'spaceweather'
                'wfr'
                'wna'
            Level 2:
                'magnetometer'
                'wfr'
                'hfr'
                'housekeeping'
            Level 3:
                'magnetometer'
            Level 4:
                'density'
                'wna-survey'

        level : str, default='l3'
            Data level; options: 'l1', 'l2', 'l3', l4'

        cadence : str, default='4sec'
            Data cadence; options: '1sec', 'hires', '4sec'

        coord : str, default='sm'
            Data coordinate system

        wavetype : str, default='waveform'
            Type of level 2 waveform data with options:
                For WFR data:
                    'waveform' (default)
                    'waveform-continuous-burst'
                    'spectral-matrix'
                    'spectral-matrix-diagonal'
                    'spectral-matrix-diagonal-merged'
                For HFR data:
                    'waveform'
                    'spectra'
                    'spectra-burst'
                    'spectra-merged'
            For descriptions of these data, see:
                https://emfisis.physics.uiowa.edu/data/L2_products
                suffix: str
                    The tplot variable names will be given this suffix.  By default,
                    no suffix is added.

        suffix : str, optional
            Suffix for tplot variable names. By default, no suffix is added.

        get_support_data : bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat : str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5/10:00', '2018-11-5/15:00'], datatype='magnetometer', level='l3', time_clip=True)
    >>> tplot(['Mag', 'Magnitude'])
    """
    return load(instrument='emfisis', wavetype=wavetype, trange=trange, probe=probe, datatype=datatype, level=level, cadence=cadence, coord=coord, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def rbspice(trange=['2018-11-5', '2018-11-6'], 
        probe='a',
        datatype='TOFxEH',
        level='l3',
        suffix='',  
        get_support_data=True,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE) instrument
    
    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype: str, default='TOFxEH'
            Data type; Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool, default=True
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> rbspice_vars = pyspedas.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEH', level='l3')
    >>> tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_spin')

    # Calculate the pitch angle distributions
    >>> from pyspedas.rbsp.rbspice_lib.rbsp_rbspice_pad import rbsp_rbspice_pad
    >>> rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3')
    >>> tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad_spin')
    """

    # Valid names
    vprobe = ['a', 'b']
    vlevels = ['l1', 'l2', 'l3', 'l4']
    vdatatypesl1 = ['TOFxEH', 'TOFxEnonH', 'TOFxPHHHELT']
    vdatatypesl2 = ['TOFxEH', 'TOFxEnonH', 'TOFxPHHHELT']
    vdatatypesl3 = ['TOFxEH', 'TOFxEnonH', 'TOFxPHHHELT']
    vdatatypesl3pap = ['']  # L3PAP data is not yet supported
    vdatatypesl4 = ['']  # L4 data is not yet supported
    vdatatypes = vdatatypesl1 + vdatatypesl2 + vdatatypesl3 + vdatatypesl3pap + vdatatypesl4
    vdatatypes_lower = [vdatatype.lower() for vdatatype in vdatatypes]

    tvars = load(instrument='rbspice', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    if not isinstance(probe, list):
        probe = [probe]

    if datatype.lower() in vdatatypes_lower:
        for prb in probe:
            # Add energy channel energy values to primary data variable,
            # create variables for individual telescopes, and set appropriate tplot options
            rbsp_load_rbspice_read(level=level, probe=prb, datatype=datatype)

            # Calculate omni-directional variable
            omni_vars = rbsp_rbspice_omni(probe=prb, datatype=datatype, level=level)
            if omni_vars:
                tvars.extend(omni_vars)

            # Calculate spin-averaged variable
            sp_avg_vars = rbsp_rbspice_spin_avg(probe=prb, datatype=datatype, level=level)
            if omni_vars:
                tvars.extend(sp_avg_vars)

    return tvars


def efw(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='spec', 
        level='l3',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Electric Field and Waves Suite (EFW)
    
    Parameters
    ----------
        trange : list of str, default=['2015-11-5', '2015-11-6']
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype : str, default='spec'
            Data type. Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')
    >>> tplot(['efield_in_inertial_frame_spinfit_mgse', 'spacecraft_potential'])
    """
    return load(instrument='efw', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def mageis(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='', 
        level='l3',
        rel='rel04',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
    
    Parameters
    ----------
        trange : list of str, default=['2015-11-5', '2015-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype : str, default=''
            Data type. Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        rel : str, default='rel04'
            Release version of the data.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> mageis_vars = pyspedas.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')
    >>> tplot('I')
    """
    return load(instrument='mageis', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def hope(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='moments', 
        level='l3',
        rel='rel04',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
    
    Parameters
    ----------
        trange : list of str, default=['2015-11-5', '2015-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype : str, default='moments'
            Data type. Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        rel : str, default='rel04'
            Release version of the data.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')
    >>> tplot('Ion_density')
    """

    return load(instrument='hope', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def rept(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='', 
        level='l3',
        rel='rel03',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
    
    Parameters
    ----------
        trange : list of str, default=['2015-11-5', '2015-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype : str, default=''
            Data type. Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        rel : str, default='rel03'
            Release version of the data.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> rept_vars = pyspedas.rbsp.rept(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel03')
    >>> tplot('FEDU')
    """

    return load(instrument='rept', rel=rel, trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def rps(trange=['2015-11-5', '2015-11-6'], 
        probe='a',
        datatype='rps-1min', 
        level='l2',
        suffix='',  
        get_support_data=True, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Relativistic Proton Spectrometer (RPS)
    
    Parameters
    ----------
        trange : list of str, default=['2015-11-5', '2015-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name ('a' or 'b')

        datatype : str, default='rps-1min'
            Data type. Valid options are specific to different data levels.

        level : str, default='l2'
            Data level. Valid options: 'l1', 'l2', 'l3', 'l4'

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> rps_vars = pyspedas.rbsp.rps(trange=['2018-11-5', '2018-11-6'], datatype='rps', level='l2')
    >>> tplot('DOSE1')
    """
    return load(instrument='rps', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def datasets(instrument=None, label=True):
    """
    Retrieves available datasets for the specified instrument on the Van Allen Probes (RBSP) mission.

    Parameters
    ----------
    instrument : str, optional
        Name of the instrument for which to find datasets. If None, finds datasets for all instruments on the mission.

    label : bool, default=True
        If True, the function prints both the dataset ID and label. If False, only the dataset ID is printed.

    Returns
    -------
    list of str
        List of available datasets for the specified instrument or for all instruments if no instrument is specified.

    Examples
    --------
    >>> pyspedas.rbsp.find_datasets(instrument='REPT', label=True)
    ...
    RBSPA_REL03_ECT-REPT-SCI-L3: RBSP/ECT REPT Pitch Angle Resolved Electron and Proton Fluxes. Electron energies: 2 - 59.45 MeV. Proton energies: 21.25 - 0 MeV - D. Baker (University of Colorado at Boulder)
    ...
    """
    return find_datasets(mission='Van Allen Probes (RBSP)', instrument=instrument, label=label)

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        cadence: str
            Data cadence (default: 4sec); other options: '1sec', 'hires'

        coord: str
            Data coordinate system (default: sm)

        level: str
            Data level; options: 'l1', 'l2', 'l3', l4'

        datatype: str
            Data type; valid options:
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

        wavetype: str
            Type of level 2 waveform data; valid options:
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

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        datatype: str
            Data type (default: tofxeh); Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

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
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe name ('a' or 'b'); default: a

        datatype: str
            Data type; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='rps', trange=trange, probe=probe, datatype=datatype, level=level, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def datasets(instrument=None, label=True):
    return find_datasets(mission='Van Allen Probes (RBSP)', instrument=instrument, label=label)

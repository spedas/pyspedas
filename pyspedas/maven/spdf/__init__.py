from .load import load


def mag(trange=['2014-10-18', '2014-10-19'],
        datatype='sunstate-1sec', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Magnetometer (MAG)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                'sunstate-1sec' for L2 data

        level: str
            Data level; options: 'l1', 'l2' (default: l2)

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
    tvars = load(instrument='mag', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return mag_postprocessing(tvars)


def mag_postprocessing(variables):
    """
    Placeholder for MAG post-processing 
    """
    return variables


def swea(trange=['2014-10-18', '2014-10-19'],
        datatype='arc3d', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Solar Wind Electron Analyzer (SWEA)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                'arc3d' for L2 data
                'arcpad' for L2 data
                'svy3d' for L2 data
                'svypad' for L2 data
                'svyspec' for L2 data

        level: str
            Data level; options: 'l2' (default: l2)

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
    tvars = load(instrument='swea', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return swea_postprocessing(tvars)


def swea_postprocessing(variables):
    """
    Placeholder for SWEA post-processing 
    """
    return variables


def swia(trange=['2014-10-18', '2014-10-19'],
        datatype='onboardsvyspec', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Solar Wind Ion Analyzer (SWIA)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                'onboardsvyspec' for L2 data
                'onboardsvymom' for L2 data
                'finesvy3d' for L2 data
                'finearc3d' for L2 data
                'coarsesvy3d' for L2 data
                'coarsearc3d' for L2 data

        level: str
            Data level; options: 'l2' (default: l2)

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
    tvars = load(instrument='swia', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return swia_postprocessing(tvars)


def swia_postprocessing(variables):
    """
    Placeholder for SWIA post-processing 
    """
    return variables


def static(trange=['2014-10-18', '2014-10-19'],
        datatype='c0-64e2m', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the SupraThermal And Thermal Ion Composition (STATIC)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                'c0-64e2m' for L2 data
                'c2-32e32m' for L2 data
                'c4-4e64m' for L2 data
                'c6-32e64m' for L2 data
                'c8-32e16d' for L2 data
                'ca-16e4d16a' for L2 data
                'cc-32e8d32m' for L2 data
                'cd-32e8d32m' for L2 data
                'ce-16e4d16a16m' for L2 data
                'cf-16e4d16a16m' for L2 data
                'd0-32e4d16a8m' for L2 data
                'd1-32e4d16a8m' for L2 data
                'd4-4d16a2m' for L2 data
                'd6-events' for L2 data
                'd7-fsthkp' for L2 data
                'd8-12r1e' for L2 data
                'd9-12r64e' for L2 data
                'da-1r64e' for L2 data
                'db-1024tof' for L2 data
                'hkp' for L2 data

        level: str
            Data level; options: 'l2' (default: l2)

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
    tvars = load(instrument='static', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return static_postprocessing(tvars)


def static_postprocessing(variables):
    """
    Placeholder for STATIC post-processing 
    """
    return variables


def sep(trange=['2014-10-18', '2014-10-19'],
        datatype='s1-cal-svy-full', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Solar Energetic Particle (SEP) instrument
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                's1-cal-svy-full' for L2 data
                's2-cal-svy-full' for L2 data

        level: str
            Data level; options: 'l2' (default: l2)

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
    tvars = load(instrument='sep', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return sep_postprocessing(tvars)


def sep_postprocessing(variables):
    """
    Placeholder for SEP post-processing 
    """
    return variables


def kp(trange=['2014-10-18', '2014-10-19'],
        datatype='kp-4sec', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Key Parameters (KP)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
                'kp-4sec' for 4 second KP data

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
    tvars = load(instrument='kp', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return kp_postprocessing(tvars)


def kp_postprocessing(variables):
    """
    Placeholder for KP post-processing 
    """
    return variables

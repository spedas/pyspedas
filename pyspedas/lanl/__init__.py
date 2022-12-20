from .load import load
from pyspedas.utilities.datasets import find_datasets


def mpa(trange=['2004-10-31', '2004-11-01'],
        probe='l1', 
        level='k0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Magnetospheric Plasma Analyzer (MPA)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            LANL probe #; Valid options:
                'l0' for LANL 1990 data
                'l1' for LANL 1991 data
                'l4' for LANL 1994 data
                'l7' for LANL 1997 data
                'l9' for LANL 1989 data
                'a1' for LANL 2001 data
                'a2' for LANL 2002 data

        level: str
            Data level; options: 'k0' (default: k0)

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
    tvars = load(instrument='mpa', trange=trange, level=level, probe=probe, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return mpa_postprocessing(tvars)


def mpa_postprocessing(variables):
    """
    Placeholder for MPA post-processing 
    """
    return variables


def spa(trange=['2004-10-31', '2004-11-01'],
        probe='l1', 
        level='k0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Synchronous Orbit Particle Analyzer (SPA)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            LANL S/C probe #; Valid options:
                'l0' for LANL 1990 data
                'l1' for LANL 1991 data
                'l4' for LANL 1994 data
                'l7' for LANL 1997 data
                'l9' for LANL 1989 data
                'a1' for LANL 2001 data
                'a2' for LANL 2002 data

        level: str
            Data level; options: 'k0' (default: k0)

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
    tvars = load(instrument='spa', trange=trange, level=level, probe=probe, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return spa_postprocessing(tvars)


def spa_postprocessing(variables):
    """
    Placeholder for SPA post-processing 
    """
    return variables


def datasets(instrument=None, label=True):
    return find_datasets(mission='LANL', instrument=instrument, label=label)

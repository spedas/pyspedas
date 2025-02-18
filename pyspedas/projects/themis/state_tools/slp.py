import logging
from pyspedas.projects.themis.load import load
from pytplot import set_coords


def slp(trange=['2007-03-23', '2007-03-24'],
          level='l1',
          suffix='',
          get_support_data=False,
          varformat=None,
          varnames=[],
          downloadonly=False,
          notplot=False,
          no_update=False,
          time_clip=False):
    """
    This function loads THEMIS Solar and Lunar Ephemeris data (SLP).  

    Parameters
    ----------
        trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        level: str
            Data type; Valid options: 'l1'
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix
            Default: no suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  
            Default: False, only loads in data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, (if not specified, all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified
            in the trange keyword
            Default: False

    Returns
    -------
        List of str
        List of tplot variables created
        Empty list if no data loaded

    Example
    -------
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> slp_vars = pyspedas.projects.themis.slp(trange=['2023-11-06', '2023-11-07'])
        >>> tplot(['slp_sun_pos','slp_lun_pos'])

    """
    retval =  load(instrument='slp', trange=trange, level=level,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                time_clip=time_clip, no_update=no_update)

    if not downloadonly:
        # Coordinate system is not set in the data CDFs, so setting it here for now.
        # Everything except for the light travel time variables is in GEI true-of-date.
        for varname in retval:
            if not "ltime" in varname:
                logging.debug("Setting %s to GEI coordinates", varname)
                set_coords(varname,"GEI")

    return retval

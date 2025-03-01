from pyspedas.projects.themis.load import load


def ask(site=None,
         trange=['2007-03-23', '2007-03-24'],
         group=None,
         level='l1',
         datatype='asf',
         suffix='',
         get_support_data=False,
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads THEMIS All Sky Keograms

    Parameters
    ----------
        site: str
            Observatory name, IF set, loads ASF data, not ASK
            Default: None, all sites are loaded
            
        trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        level: str
            Data level; Valid options: 'l1'
            Default: 'l1'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  
            Default: False; only loads data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None; all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, so all data variables are loaded

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
        Empty list if no data
    
    Example
    -------
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> ask_vars = pyspedas.projects.themis.ask(trange=['2013-11-05', '2013-11-06'])
        >>> tplot(['thg_ask_atha', 'thg_ask_chbg'])
    """

    return load(instrument='ask', trange=trange, level=level, datatype=datatype,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames, stations=site,
                downloadonly=downloadonly, notplot=notplot, 
                time_clip=time_clip, no_update=no_update)


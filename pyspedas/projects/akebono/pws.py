from .load import load
from .pws_postprocessing import pws_postprocessing

# This routine was originally in akebono/__init__.py.  If you need to see the history of this routine before
# it was moved to its own file, please check the history for __init__.py.

def pws(trange=['2012-10-01', '2012-10-02'],
        datatype='ne', 
        level='h1',
        prefix='',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        force_download=False):
    """
    Load data from the Akebono Plasma Waves and Sounder experiment (PWS)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2012-10-01', '2012-10-02']

        datatype: str
            Data type; Valid options:

                'ne', 'npw-ds', 'npw-py', 'spw'

            Default: 'ne'

        level: str
            Data level; options: 'h1' (default: h1)
            Default: 'h1'

        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
            Default: None

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)
            Default: []

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
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False


    Returns
    ----------
    list of str
        List of tplot variables created.


    Example
    ---------- 
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> pws_vars = pyspedas.projects.akebono.pws(trange=['2012-10-01', '2012-10-02'])
        >>> tplot(['akb_pws_RX1', 'akb_pws_RX2'])

    """

    if prefix is None:
        prefix=''

    if suffix is None:
        suffix=''

    tvars = load(instrument='pws', trange=trange, level=level, datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)

    if tvars is None or notplot or downloadonly:
        return tvars

    # Note, prefixes and suffixes have already been applied at this point, but may need
    # them to get original variable names for postprocessing
    return pws_postprocessing(tvars, prefix=prefix, suffix=suffix)



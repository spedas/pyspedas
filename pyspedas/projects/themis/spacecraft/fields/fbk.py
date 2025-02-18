from pyspedas.projects.themis.load import load
import pytplot

def fbk(trange=['2007-03-23', '2007-03-24'],
        probe='c',
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
    This function loads THEMIS FBK data

    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Data level; Valid options: 'l1', 'l2'
            Default: 'l2'

        level: str
            Data level; Valid options: 'l1', 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix

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
        >>> fbk_vars = pyspedas.projects.themis.fbk(probe='d', trange=['2013-11-5', '2013-11-6'])
        >>> tplot(['thd_fb_edc12', 'thd_fb_scm1'])
    """
    outvars = load(instrument='fbk', trange=trange, level=level,
                   suffix=suffix, get_support_data=get_support_data,
                   varformat=varformat, varnames=varnames,
                   downloadonly=downloadonly, notplot=notplot,
                   probe=probe, time_clip=time_clip, no_update=no_update)

    #turn off auto Y resample
    scmv = pytplot.tnames('*_fb_s*')
    if len(scmv) > 0:
        for scv in scmv:
            pytplot.options(scv, 'y_no_resample',1)
    efiv = pytplot.tnames('*_fb_e*')
    if len(efiv) > 0:
        for efv in efiv:
            pytplot.options(efv, 'y_no_resample',1)

    return outvars

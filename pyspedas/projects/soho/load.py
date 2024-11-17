import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2006-06-01', '2006-06-02'], 
         instrument='celias',
         datatype='pm_5min',
         suffix='', 
         prefix='',
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False,
         force_download=False):
    """
    This function loads data from the SOHO mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.projects.soho.celias
        pyspedas.projects.soho.cosp
        pyspedas.projects.soho.erne
        pyspedas.projects.soho.orbit

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2006-06-01', '2006-06-02']

        instrument: str
            Spacecraft identifier ('celias', 'cosp', 'erne', 'orbit')
            Default: 'celias'

        datatype: str
            Valid options: 'pm_5min'
            Default: 'pm_5min'

        suffix: str
            The tplot variable names will be given this suffix.
            no prefix is added.
            Default: ''
        
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: 'False', only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded in.

        varnames: list of str
            List of variable names to load
            Default: [], all data variables are loaded

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
            If True, downloads the file even if a newer version exists locally. 
            Default: False.

    Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        celias_soho_vars = pyspedas.projects.soho.celias(trange=['2006-06-01', '2006-06-02'])

        cosp_soho_vars = pyspedas.projects.soho.cosp(trange=['2006-06-01', '2006-06-02'])

        erne_soho_vars = pyspedas.projects.soho.erne(trange=['2006-06-01', '2006-06-02'])

        orbit_soho_vars = pyspedas.projects.soho.orbit(trange=['2006-06-01', '2006-06-02'])

    """

    if prefix is None:
        prefix = ''
    
    if suffix is None:
        suffix = ''

    res = 24 * 3600.

    if instrument == 'celias':
        pathformat = instrument+'/'+datatype+'/%Y/soho_'+instrument+'-'+datatype+'_%Y%m%d_v??.cdf'
    elif instrument == 'costep':
        pathformat = instrument+'/'+datatype+'/%Y/soho_'+instrument+'-'+datatype+'_%Y0101_v??.??.cdf'
        res = 24 * 3600. * 366
    elif instrument == 'erne':
        pathformat = instrument+'/'+datatype+'/%Y/soho_'+instrument+'-'+datatype+'_%Y%m%d_v??.cdf'
    elif instrument == 'orbit':
        if datatype not in ['pre_or', 'def_or', 'def_at']:
            logging.error('Invalod datatype: ' + datatype)
            return
        datatype_fn = datatype.split('_')[1] + '_' +datatype.split('_')[0]
        pathformat = instrument+'/'+datatype+'/cdf/%Y/so_'+datatype_fn+'_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange, res=res)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update, force_download=force_download)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, prefix=prefix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

    
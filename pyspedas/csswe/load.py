from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='reptile',
         datatype='flux', 
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
    This function loads data from the CSSWE mission; this function is not meant
    to be called directly; instead, see the wrapper:
        pyspedas.csswe.reptile

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        instrument: str
            Volid option: 'reptile'
            Default: 'reptile'

        datatype: str
            Valid options: 'flux'
            Default: 'flux'

        level: str
            Valid option: 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added.

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

    Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        reptile_csswe_vars = pyspedas.csswe.reptile(trange=['2013-11-5', '2013-11-6'])

    """

    if instrument == 'reptile':
        pathformat = level+'/'+instrument+'/'+datatype+'/%Y/csswe_'+instrument+'_6sec-'+datatype+'-'+level+'_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

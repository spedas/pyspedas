from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='mgf',
         datatype='k0', 
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
    This function loads data from the Geotail mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.projects.geotail.mgf
        pyspedas.projects.geotail.efd
        pyspedas.projects.geotail.lep
        pyspedas.projects.geotail.cpi
        pyspedas.projects.geotail.epi
        pyspedas.projects.geotail.pwi

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2013-11-5', '2013-11-6']

        instrument: str
            Spacecraft identifier ('mgf', 'efd', 'lep', 'cpi', 'edi', 'pwi')
            Default: 'mgf'

        datatype: str
            Data type; Valid options: ('k0', ''eda3sec', 'edb3sec')
            Default: 'k0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added

        prefix: str
            The tplot variable names will be given this prefix.
            Default: no prefix is added

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: all variables are loaded in

        varnames: list of str
            List of variable names to load
            Default: all data variables are loaded

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
    >>> mgf_vars = pyspedas.projects.geotail.mgf(trange=['2018-11-5', '2018-11-6'])
    >>> tplot(['IB', 'IB_vector'])

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> efd_vars = pyspedas.projects.geotail.efd(trange=['2018-11-5', '2018-11-6'])
    >>> tplot(['Es', 'Ss', 'Bs', 'Vs', 'Ew', 'Sw', 'Bw', 'Vw'])

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> lep_vars = pyspedas.projects.geotail.lep(trange=['2018-11-5/05:00', '2018-11-5/06:00'], time_clip=True)
    >>> tplot(['N0', 'V0'])

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> cpi_vars = pyspedas.projects.geotail.cpi(trange=['2018-11-5/15:00', '2018-11-5/18:00'], time_clip=True)
    >>> tplot(['SW_P_Den', 'SW_P_AVGE', 'SW_V', 'HP_P_Den'])

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> epic_vars = pyspedas.projects.geotail.epic(trange=['2018-11-5', '2018-11-6'])
    >>> tplot('IDiffI_I')

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> pwi_vars = pyspedas.projects.geotail.pwi(trange=['2018-11-5/06:00', '2018-11-5/07:00'], time_clip=True)
    >>> tplot(['MCAE_AVE', 'MCAB_AVE'])

    """

    if instrument == 'mgf':
        if datatype == 'k0':
            pathformat = 'mgf/mgf_k0/%Y/ge_'+datatype+'_mgf_%Y%m%d_v??.cdf'
        elif datatype == 'eda3sec' or datatype == 'edb3sec':
            pathformat = 'mgf/'+datatype+'_mgf/%Y/ge_'+datatype+'_mgf_%Y%m%d_v??.cdf'
    elif instrument == 'efd':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'lep':
        if datatype == 'k0':
            pathformat = 'lep/lep_k0/%Y/ge_'+datatype+'_lep_%Y%m%d_v??.cdf'
    elif instrument == 'cpi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'epi':
        pathformat = 'epic/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pwi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

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

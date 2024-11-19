from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['1997-01-03', '1997-01-04'], 
         instrument='mfe',
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
    This function loads data from the Polar mission; this function is not meant 
    to be called directly; instead, see the wrappera:
        pyspedas.projects.polar.mfe
        pyspedas.projects.polar.efi
        pyspedas.projects.polar.pwi
        pyspedas.projects.polar.hydra
        pyspedas.projects.polar.tide
        pyspedas.projects.polar.timas
        pyspedas.projects.polar.cammice
        pyspedas.projects.polar.ceppad
        pyspedas.projects.polar.uvi
        pyspedas.projects.polar.vis
        pyspedas.projects.polar.pixie
        pyspedas.projects.polar.orbit

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1997-01-03', '1997-01-04']

        instrument: str
            Spacecraft identifier ('mfe', 'efi', 'pwi', 'hydra', 'tide', 'timas',
                'cammice', 'ceppad', 'uvi', 'vis', 'pixie', 'orbit')
            Default: 'mfe'

        datatype: str
            Valid options: 'k0'
            Default: 'k0'

        suffix: str
            The tplot variable names will be given this suffix. By default,
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
        mfe_polar_vars = pyspedas.projects.polar.mfe(trange=['1997-01-03', '1997-01-04'])

        efi_polar_vars = pyspedas.projects.polar.efi(trange=['1997-01-03', '1997-01-04'])

        pwi_polar_vars = pyspedas.projects.polar.pwi(trange=['1997-01-03', '1997-01-04'])

        tide_polar_vars = pyspedas.projects.polar.tide(trange=['1997-01-03', '1997-01-04'])

        orbit_polar_vars = pyspedas.projects.polar.orbit(trange=['1997-01-03', '1997-01-04'])

    """
    if prefix is None:
        prefix = ''
    
    if suffix is None:
        suffix = ''

    if instrument == 'mfe':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'efi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pwi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'hydra':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_hyd_%Y%m%d_v??.cdf'
    elif instrument == 'tide':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_tid_%Y%m%d_v??.cdf'
    elif instrument == 'timas':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_tim_%Y%m%d_v??.cdf'
    elif instrument == 'cammice':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_cam_%Y%m%d_v??.cdf'
    elif instrument == 'ceppad':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_cep_%Y%m%d_v??.cdf'
    elif instrument == 'uvi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'vis':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pixie':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_pix_%Y%m%d_v??.cdf'
    elif instrument == 'spha':
        pathformat = 'orbit/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'

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

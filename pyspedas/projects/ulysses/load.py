from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot
from typing import List, Union
from .config import CONFIG

def load(trange:List[str]=['2009-01-01', '2009-01-02'],
         instrument:str='vhm',
         datatype:str='1min',
         prefix:str='',
         suffix:str='',
         get_support_data:bool=False,
         varformat:str=None,
         varnames:List[str]=[],
         downloadonly:bool=False,
         force_download:bool=False,
         notplot:bool=False,
         no_update:bool=False,
         time_clip:bool=False) -> List[str]:
    """
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2009-01-01', '2009-01-02']

        instrument: str
            Instrument to load.
            Default: 'vhm'

        datatype: str
            Data type
            Default: '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: '' (all variables loaded)

        varnames: list of str
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        force_download: bool
            Set this flag to download the CDF files, even if the local file is newer
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
    -------
        list of str
            List of tplot variables created.

    Notes
    _____
    This function is not meant to be called directly; please see the instrument specific wrappers in __init__.py
    """

    if prefix is None:
        prefix=''
    if suffix is None:
        suffix=''

    if instrument == 'vhm':
        pathformat = 'mag_cdaweb/vhm_'+datatype+'/%Y/uy_'+datatype+'_vhm_%Y%m%d_v??.cdf'
    elif instrument == 'swoops':
        if datatype in ['bai_m0', 'bai_m1', 'bae_m0']:
            pathformat = 'plasma/swoops_cdaweb/'+datatype+'/%Y/uy_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
        else:
            pathformat = 'plasma/swoops_cdaweb/'+datatype+'/%Y/uy_'+datatype+'_%Y0101_v??.cdf'
    elif instrument == 'swics':
        pathformat = 'plasma/swics_cdaweb/'+datatype+'/%Y/uy_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
    elif instrument == 'urap':
        pathformat = 'radio/urap_cdaweb/'+datatype+'/%Y/uy_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
    elif instrument == 'epac':
        if datatype == 'epac_m1':
            pathformat = 'particle/epac_cdaweb/'+datatype+'/%Y/uy_m1_epa_%Y%m%d_v??.cdf'
    elif instrument == 'hiscale':
        pathformat = 'particle/hiscale_cdaweb/'+datatype+'/%Y/uy_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
    elif instrument == 'cospin':
        pathformat = 'particle/cospin_cdaweb/'+datatype+'/%Y/uy_m0_'+datatype+'_%Y%m%d_v??.cdf'
    elif instrument == 'grb':
        pathformat = 'gamma/grb_cdaweb/'+datatype+'/%Y/uy_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'


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

    tvars = cdf_to_tplot(out_files, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

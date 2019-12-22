import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2004-11-5', '2004-11-6'],
         instrument='lena', 
         datatype='k0', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         downloadonly=False):
    """
    This function loads IMAGE data; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.image.lena
        pyspedas.image.mena
        pyspedas.image.hena
        pyspedas.image.rpi
        pyspedas.image.euv
        pyspedas.image.fuv
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """

    tvars_created = []

    if instrument == 'lena':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/im_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'mena':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/im_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'hena':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/im_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'rpi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/im_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'euv':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/im_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'fuv':
        pathformat = instrument+'/wic_'+datatype+'/%Y/im_'+datatype+'_wic_%Y%m%d_v??.cdf'
    elif instrument == 'orbit':
        if datatype == 'def_or':
            pathformat = instrument+'/def_or/%Y/im_or_def_%Y%m%d_v??.cdf'
        elif datatype == 'pre_or':
            pathformat = instrument+'/pre_or/%Y/im_or_pre_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    for remote_file in remote_names:
        files = download(remote_file=remote_file, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'])
        if files is not None:
            for file in files:
                out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, merge=True, get_support_data=get_support_data, varformat=varformat)
    if tvars is not None:
        tvars_created.extend(tvars)

    return tvars_created

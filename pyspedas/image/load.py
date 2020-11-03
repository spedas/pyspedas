import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2004-11-5', '2004-11-6'],
         instrument='lena', 
         datatype='k0', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads IMAGE data; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.image.lena
        pyspedas.image.mena
        pyspedas.image.hena
        pyspedas.image.rpi
        pyspedas.image.euv
        pyspedas.image.fuv
    
    """

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

import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='dcb',
         datatype='', 
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
    This function loads data from the FAST mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.fast.dcb
        pyspedas.fast.acb
        pyspedas.fast.esa
        pyspedas.fast.teams

    """
    file_resolution = 24*3600.

    if instrument == 'dcb':
        if level == 'k0':
            pathformat = 'dcf/'+level+'/%Y/fa_k0_dcf_%Y%m%d_v??.cdf'
        else:
            pathformat = 'dcf/'+level+'/'+instrument+'/%Y/%m/fast_hr_'+instrument+'_%Y%m%d%H????_v??.cdf'
            file_resolution = 3600.
    if instrument == 'acb':
        pathformat = 'acf/'+level+'/%Y/fa_'+level+'_acf_%Y%m%d_v??.cdf'
    elif instrument == 'esa':
        pathformat = instrument+'/'+level+'/'+datatype+'/%Y/%m/fa_'+instrument+'_'+level+'_'+datatype+'_%Y%m%d??????_*_v??.cdf'
    if instrument == 'teams':
        pathformat = 'teams/'+level+'/%Y/fa_'+level+'_tms_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange, res=file_resolution)

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

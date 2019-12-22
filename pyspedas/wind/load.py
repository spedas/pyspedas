import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='fgm',
         datatype='h0', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the WIND mission; this function is not meant 
    to be called directly; instead, see the wrapper:
        pyspedas.wind.mfi
        pyspedas.wind.swe

    """

    if instrument == 'fgm':
        pathformat = 'mfi/mfi_'+datatype+'/%Y/wi_'+datatype+'_mfi_%Y%m%d_v??.cdf'
    if instrument == 'swe':
        pathformat = 'swe/swe_'+datatype+'/%Y/wi_'+datatype+'_swe_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    for remote_file in remote_names:
        files = download(remote_file=remote_file, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
        if files is not None:
            for file in files:
                out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, merge=True, get_support_data=get_support_data, varformat=varformat, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars



from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2019-02-01','2019-02-02'], 
         site=None,
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads Magnetic Induction Coil Array (MICA) data; this function is not meant 
    to be called directly; instead, see the wrapper:
        pyspedas.mica.induction

    """

    if site == None:
        print('A valid MICA site code name must be entered.')
        print('Current site codes include: ')
        print('NAL, LYR, LOR, ISR, SDY, IQA, SNK, MCM, SPA, JBS, NEV, HAL, PG2[3,4,5]')
        return
    
    pathformat = site.upper()+'/%Y/%m/mica_ulf_'+site.lower()+'_%Y%m%d_v??.cdf'

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

    tvars = cdf_to_tplot(out_files, suffix='_'+site.upper()+suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

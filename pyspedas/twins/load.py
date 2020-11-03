import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-11-5', '2018-11-6'], 
         probe='1',
         instrument='lad', 
         datatype='', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads TWINS data; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.twins.lad
        pyspedas.twins.ephemeris
        pyspedas.twins.imager

    """

    if not isinstance(probe, list):
        probe = [probe]

    probe = [str(prb) for prb in probe]

    out_files = []

    for prb in probe:
        if instrument == 'lad':
            pathformat = 'twins'+prb+'/'+instrument+'/%Y/twins'+prb+'_l1_lad_%Y%m%d_v??.cdf'
        elif instrument == 'imager':
            pathformat = 'twins'+prb+'/'+instrument+'/%Y/twins'+prb+'_l1_imager_%Y%m%d??_v??.cdf'
        elif instrument == 'ephemeris':
            pathformat = 'twins'+prb+'/'+instrument+'/'+datatype+'/%Y/twins'+prb+'_'+datatype+'_def_%Y%m%d_v??.cdf'

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

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
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['1998-04-06', '1998-04-07'], 
         instrument='mam',
         datatype='pp',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the Equator-S mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.equator_s.mam
        pyspedas.equator_s.edi
        pyspedas.equator_s.esa (3DA)
        pyspedas.equator_s.epi
        pyspedas.equator_s.ici
        pyspedas.equator_s.pcd
        pyspedas.equator_s.sfd

    """

    if instrument == 'mam':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'edi':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == '3da':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'epi':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'ici':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pcd':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'sfd':
        pathformat = datatype+'/'+instrument+'/%Y/eq_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'

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

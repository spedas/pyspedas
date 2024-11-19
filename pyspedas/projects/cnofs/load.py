from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='cindi',
         datatype='efield_1sec',
         prefix='',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False,
         force_download=False):
    """
    This function loads data from the CNOFS mission; this function is not meant
    to be called directly; instead, see the wrappers:
        pyspedas.projects.cnofs.cindi
        pyspedas.projects.cnofs.plp
        pyspedas.projects.cnofs.vefi
    """

    if prefix is None:
        prefix=''
    if suffix is None:
        suffix=''

    if instrument == 'cindi':
        pathformat = instrument+'/ivm_500ms_cdf/%Y/cnofs_'+instrument+'_ivm_500ms_%Y%m%d_v??.cdf'
    elif instrument == 'plp':
        pathformat = instrument+'/plasma_1sec/%Y/cnofs_'+instrument+'_plasma_1sec_%Y%m%d_v??.cdf'
    elif instrument == 'vefi':
        pathformat = instrument+'/'+datatype+'/%Y/cnofs_'+instrument+'_'+datatype+'_%Y%m%d_v??.cdf'

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

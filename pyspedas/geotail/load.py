from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='mgf',
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
    This function loads data from the Geotail mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.geotail.mgf
        pyspedas.geotail.efd
        pyspedas.geotail.lep
        pyspedas.geotail.cpi
        pyspedas.geotail.epi
        pyspedas.geotail.pwi

    """

    if instrument == 'mgf':
        if datatype == 'k0':
            pathformat = 'mgf/mgf_k0/%Y/ge_'+datatype+'_mgf_%Y%m%d_v??.cdf'
        elif datatype == 'eda3sec' or datatype == 'edb3sec':
            pathformat = 'mgf/'+datatype+'_mgf/%Y/ge_'+datatype+'_mgf_%Y%m%d_v??.cdf'
    elif instrument == 'efd':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'lep':
        if datatype == 'k0':
            pathformat = 'lep/lep_k0/%Y/ge_'+datatype+'_lep_%Y%m%d_v??.cdf'
    elif instrument == 'cpi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'epi':
        pathformat = 'epic/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pwi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/ge_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'

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

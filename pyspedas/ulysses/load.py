from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2009-01-01', '2009-01-02'], 
         instrument='vhm',
         datatype='1min', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function is not meant to be called directly; please see the instrument specific wrappers in __init__.py
    """

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

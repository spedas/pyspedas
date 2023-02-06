import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2006-06-01', '2006-06-02'], 
         instrument='celias',
         datatype='pm_5min',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the SOHO mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.soho.celias
        pyspedas.soho.cosp
        pyspedas.soho.erne
        pyspedas.soho.orbit

    """
    res = 24 * 3600.

    if instrument == 'celias':
        pathformat = instrument+'/'+datatype+'/%Y/soho_'+instrument+'-'+datatype+'_%Y%m%d_v??.cdf'
    elif instrument == 'costep':
        pathformat = instrument+'/'+datatype+'/%Y/soho_'+instrument+'-'+datatype+'_%Y0101_v??.??.cdf'
        res = 24 * 3600. * 366
    elif instrument == 'erne':
        pathformat = instrument+'/'+datatype+'/%Y/soho_'+instrument+'-'+datatype+'_%Y%m%d_v??.cdf'
    elif instrument == 'orbit':
        if datatype not in ['pre_or', 'def_or', 'def_at']:
            logging.error('Invalod datatype: ' + datatype)
            return
        datatype_fn = datatype.split('_')[1] + '_' +datatype.split('_')[0]
        pathformat = instrument+'/'+datatype+'/cdf/%Y/so_'+datatype_fn+'_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange, res=res)

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

    
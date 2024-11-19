import logging
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2012-10-01', '2012-10-02'], 
         instrument='pws',
         datatype='epd', 
         level='l2',
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
    This function loads data from the Akebono mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.projects.akebono.pws
        pyspedas.projects.akebono.rdm
        pyspedas.projects.akebono.orb

    """
    if prefix is not None:
        user_prefix = prefix
    else:
        user_prefix = ''

    if instrument == 'pws':
        #  only PWS data are available in CDF files
        prefix = user_prefix + 'akb_pws_'
        pathformat = instrument + '/NPW-DS/%Y/ak_h1_pws_%Y%m%d_v??.cdf'
    elif instrument == 'rdm':
        prefix = user_prefix + 'akb_rdm_'
        pathformat = instrument + '/%Y/sf%y%m%d'
    elif instrument == 'orb':
        prefix = user_prefix + 'akb_orb_'
        pathformat = 'orbit/daily/%Y%m/ED%y%m%d.txt'
    else:
        logging.error('Unknown instrument: ' + instrument)
        return

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update, force_download=force_download)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly or instrument != 'pws':
        return out_files

    tvars = cdf_to_tplot(out_files, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

    
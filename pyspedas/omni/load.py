import logging
import warnings
import astropy

from pyspedas.utilities.dailynames import dailynames, yearlynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'],
         datatype='1min',
         level='hro2',
         suffix='', 
         get_support_data=False,
         get_ignore_data=False,         
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=True):
    """
    This function loads OMNI (Combined 1AU IP Data; Magnetic and Solar Indices) data; this function is not meant 
    to be called directly; instead, see the wrapper:
        pyspedas.omni.data

    """
    file_res = 24*3600.0

    if 'min' in datatype:
        pathformat = level + '_' + datatype + '/%Y/omni_' + level + '_' + datatype + '_%Y%m01_v??.cdf'
        remote_names = dailynames(file_format=pathformat, trange=trange, res=file_res)
    elif 'hour' in datatype:
        pathformat = 'hourly/%Y/omni2_h0_mrg1hr_%Y%m01_v??.cdf'
        get_ignore_data = True  # required to load these files
        remote_names = yearlynames(file_format=pathformat, trange=trange, resolution='half-year')
    else:
        logging.error('Invalid datatype: '+ datatype)
        return

    # find the full remote path names using the trange

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    with warnings.catch_warnings():
        # for some reason, OMNI CDFs throw ERFA warnings (likely while converting
        # times inside astropy); we're ignoring these here
        # see: https://github.com/astropy/astropy/issues/9603
        warnings.simplefilter('ignore', astropy.utils.exceptions.ErfaWarning)
        tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, get_ignore_data=get_ignore_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

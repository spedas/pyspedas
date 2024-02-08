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
    Loads OMNI (Combined 1AU IP Data; Magnetic and Solar Indices) data; intended for internal use.

    This function is a core component for data loading but is not meant to be called directly by users.
    Instead, users should utilize the wrapper function `pyspedas.omni.data` to access this functionality.

    Parameters
    ----------
    trange : list of str, default=['2013-11-5', '2013-11-6']
        Time range of interest specified as ['starttime', 'endtime'] with the format
        'YYYY-MM-DD' or 'YYYY-MM-DD/hh:mm:ss' to specify more or less than a day.
    datatype : str, default='1min'
        Data type; valid options: '1min', '5min', 'hourly'.
    level : str, default='hro2'
        Data level; valid options: 'hro', 'hro2'.
    suffix : str, optional
        Suffix for the tplot variable names. By default, no suffix is added.
    get_support_data : bool, default=False
        If True, loads data with "VAR_TYPE" attribute value "support_data" into tplot.
        By default, only loads data with a "VAR_TYPE" attribute of "data".
    get_ignore_data : bool, default=False
        If True, specific data types will be ignored during loading. This is especially
        used for hourly data where ignoring certain data is required.
    varformat : str, optional
        The file variable formats to load into tplot. Wildcard character "*" is accepted.
        By default, all variables are loaded.
    varnames : list of str, optional
        List of variable names to load. If not specified, all data variables are loaded.
    downloadonly : bool, default=False
        If True, downloads the CDF files but does not load them into tplot variables.
    notplot : bool, default=False
        If True, returns the data in hash tables instead of creating tplot variables.
    no_update : bool, default=False
        If True, loads data only from the local cache.
    time_clip : bool, default=True
        If True, clips the variables to exactly the range specified in the trange parameter.

    Returns
    -------
    list or dict
        List of tplot variables created if notplot is False. Otherwise, returns a dictionary
        with data tables.

    Examples
    --------
    This function is not intended to be called directly.
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

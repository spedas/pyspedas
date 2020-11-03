import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-10-16', '2018-10-17'], 
         instrument='mag', 
         datatype='h0', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads DSCOVR data into tplot variables; this function is not 
    meant to be called directly; instead, see the wrappers: 
        dscovr.mag: Fluxgate Magnetometer data
        dscovr.fc: Faraday Cup data
        dscovr.orb: Ephemeris data
        dscovr.att: Attitude data
        dscovr.all: Load all data

    """

    remote_path = datatype + '/' + instrument + '/%Y/'

    if instrument == 'mag':
        if datatype == 'h0':
            pathformat = remote_path + 'dscovr_h0_mag_%Y%m%d_v??.cdf'
    elif instrument == 'faraday_cup':
        if datatype == 'h1':
            pathformat = remote_path + 'dscovr_h1_fc_%Y%m%d_v??.cdf'
    elif instrument == 'pre_or':
        if datatype == 'orbit':
            pathformat = remote_path + 'dscovr_orbit_pre_%Y%m%d_v??.cdf'
    elif instrument == 'def_at':
        if datatype == 'orbit':
            pathformat = remote_path + 'dscovr_at_def_%Y%m%d_v??.cdf'

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

import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import netcdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         probe='15',
         instrument='fgm',
         datatype='1min', 
         suffix='', 
         downloadonly=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the GOES mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.goes.fgm

    """

    if not isinstance(probe, list):
        probe = [probe]

    fullavgpath = ['full', 'avg']
    goes_path_dir = fullavgpath[datatype == '1min' or datatype == '5min']

    for prb in probe:
        remote_path = goes_path_dir + '/%Y/%m/goes' + str(prb) + '/netcdf/'

        if instrument == 'fgm':
            if datatype == '512ms': # full, unaveraged data
                pathformat = remote_path + 'g' + str(prb) + '_magneto_512ms_%Y%m%d_%Y%m%d.nc'
            elif datatype == '1min': # 1 min averages
                pathformat = remote_path + 'g' + str(prb) + '_magneto_1m_%Y%m01_%Y%m??.nc'
            elif datatype == '5min': # 5 min averages
                pathformat = remote_path + 'g' + str(prb) + '_magneto_5m_%Y%m01_%Y%m??.nc'

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

    tvars = netcdf_to_tplot(out_files, suffix=suffix, merge=True, time='time_tag')

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

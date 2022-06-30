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
        pyspedas.goes.eps
        pyspedas.goes.epead
        pyspedas.goes.maged
        pyspedas.goes.magpd
        pyspedas.goes.hepad
        pyspedas.goes.xrs

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
        elif instrument == 'eps':
            # energetic particle sensor -- only valid for GOES-08 through GOES-12, only averaged data available
            if datatype == '1min':
                pathformat = remote_path + 'g' + str(prb) + '_eps_1m_%Y%m01_%Y%m??.nc'
            else:
                pathformat = remote_path + 'g' + str(prb) + '_eps_5m_%Y%m01_%Y%m??.nc'
        elif instrument == 'epead':
            # electron, proton, alpha detector -- only valid on GOES-13, 14, 15
            if datatype == '1min':
                pathformat = [remote_path + 'g' + str(prb) + '_epead_e13ew_1m_%Y%m01_%Y%m??.nc',
                                                             '_epead_p17ew_1m_%Y%m01_%Y%m??.c',
                                                             '_epead_a16ew_1m_%Y%m01_%Y%m??.nc']
            elif datatype == '5min':
                pathformat = [remote_path + 'g' + str(prb) + '_epead_e13ew_5m_%Y%m01_%Y%m??.nc',
                                                             '_epead_p17ew_5m_%Y%m01_%Y%m??.c',
                                                             '_epead_a16ew_5m_%Y%m01_%Y%m??.nc']
            else:
                pathformat = [remote_path + 'g' + str(prb) + '_epead_e1ew_4s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_e2ew_16s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_e3ew_16s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_p1ew_8s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_p27e_32s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_p27w_32s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_a16e_32s_%Y%m%d_%Y%m%d.nc',
                                                             '_epead_a16w_32s_%Y%m%d_%Y%m%d.nc']
        elif instrument == 'maged':
            # magnetospheric electron detector -- only valid on GOES 13, 14, 15
            if datatype == '1min':
                pathformat = remote_path + 'g' + str(prb) + '_maged_19me15_1m_%Y%m01_%Y%m??.nc'
            elif datatype == '5min':
                pathformat = remote_path + 'g' + str(prb) + '_maged_19me15_5m_%Y%m01_%Y%m??.nc'
            else:
                channels = ['me1','me2','me3','me4','me5']
                resolution = ['2','2','4','16','32']
                pathformat = []
                for idx, channel in enumerate(channels):
                    pathformat.append(remote_path + 'g' + str(prb) + '_maged_19'+channel+'_'+resolution[idx]+'s_%Y%m%d_%Y%m%d.nc')
        elif instrument == 'magpd':
            # magnetospheric proton detector -- only valid on GOES 13, 14, 15
            if datatype == '1min':
                pathformat = remote_path + 'g' + str(prb) + '_magpd_19mp15_1m_%Y%m01_%Y%m??.nc'
            elif datatype == '5min':
                pathformat = remote_path + 'g' + str(prb) + '_magpd_19mp15_5m_%Y%m01_%Y%m??.nc'
            else:
                channels = ['mp1','mp2','mp3','mp4','mp5']
                resolution = ['16','16','16','32','32']
                pathformat = []
                for idx, channel in enumerate(channels):
                    pathformat.append(remote_path + 'g' + str(prb) + '_magpd_19'+channel+'_'+resolution[idx]+'s_%Y%m%d_%Y%m%d.nc')
        elif instrument == 'hepad':
            # high energy proton and alpha detector -- valid for GOES 08-15
            if datatype == '1min':
                pathformat = [remote_path + 'g' + str(prb) + '_hepad_ap_1m_%Y%m01_%Y%m??.nc',
                                                             '_hepad_s15_1m_%Y%m01_%Y%m??.nc']
            elif datatype == '5min':
                pathformat = [remote_path + 'g' + str(prb) + '_hepad_ap_5m_%Y%m01_%Y%m??.nc',
                                                             '_hepad_s15_5m_%Y%m01_%Y%m??.nc']
            else:
                pathformat = [remote_path + 'g' + str(prb) + '_hepad_ap_32s_%Y%m%d_%Y%m%d.nc',
                                                             '_hepad_s15_4s_%Y%m%d_%Y%m%d.nc']
        elif instrument == 'xrs':
            # x-ray sensor -- valid for GOES 08-15
            if datatype == '1min':
                pathformat = remote_path + 'g' + str(prb) + '_xrs_1m_%Y%m01_%Y%m??.nc'
            elif datatype == '5min':
                pathformat = remote_path + 'g' + str(prb) + '_xrs_5m_%Y%m01_%Y%m??.nc'
            else:
                pathformat = remote_path + 'g' + str(prb) + '_xrs_2s_%Y%m%d_%Y%m%d.nc'

        # find the full remote path names using the trange
        if isinstance(pathformat, list):
            remote_names = []
            for path in pathformat:
                remote_names.extend(dailynames(file_format=path, trange=trange))
        else:
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

    if tvars is None:
        return

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

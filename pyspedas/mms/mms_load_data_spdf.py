import os
from pyspedas import time_double
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from .mms_file_filter import mms_file_filter
from pytplot import cdf_to_tplot
from pyspedas.analysis.time_clip import time_clip as tclip

from .mms_config import CONFIG

CONFIG['remote_data_dir'] = 'https://spdf.gsfc.nasa.gov/pub/data/mms/'

def mms_load_data_spdf(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', 
    instrument='fgm', datatype='', varformat=None, suffix='', get_support_data=False, time_clip=False, 
    no_update=False, center_measurement=False, available=False, notplot=False, latest_version=False, 
    major_version=False, min_version=None, cdf_version=None, varnames=[]):
    """
    This function loads MMS data from NASA SPDF into pyTplot variables

    This function is not meant to be called directly. Please see the individual load routines for documentation and use. 

    """

    tvars_created = []

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]
    if not isinstance(datatype, list): datatype = [datatype]


    for prb in probe:
        for lvl in level:
            for drate in data_rate:
                if drate == 'brst':
                    time_format = '%Y%m%d%H%M??'
                    file_res = 60.
                else:
                    time_format = '%Y%m%d'
                    file_res = 24*3600.
                for dtype in datatype:
                    remote_path = 'mms' + prb + '/' + instrument + '/' + drate + '/' + lvl + '/'

                    if instrument == 'fgm':
                        pathformat = remote_path + '%Y/%m/mms' + prb + '_fgm_' + drate + '_' + lvl + '_' + time_format + '_v*.cdf'
                    elif instrument == 'aspoc':
                        pathformat = remote_path + '%Y/%m/mms' + prb + '_aspoc_' + drate + '_' + lvl + '_' + time_format + '_v*.cdf'
                    elif instrument == 'edi':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_edi_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'fpi':
                        if drate != 'brst':
                            time_format = '%Y%m%d??0000'
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_fpi_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'epd-eis':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_epd-eis_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'feeps':
                        if drate != 'brst':
                            time_format = '%Y%m%d000000'
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_feeps_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'hpca':
                        time_format = '%Y%m%d??????'
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_hpca_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'mec':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_mec_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'scm':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_scm_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'dsp':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_dsp_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'edp':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_edp_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'

                    if drate == 'brst':
                        if isinstance(trange[0], float):
                            trange = [trange[0]-300., trange[1]]
                        else:
                            trange = [time_double(trange[0])-300., trange[1]]
                    # find the full remote path names using the trange
                    remote_names = dailynames(file_format=pathformat, trange=trange, res=file_res)

                    out_files = []

                    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'])
                    if files is not None:
                        for file in files:
                            out_files.append(file)
                    
                    out_files = sorted(out_files)

                    filtered_out_files = mms_file_filter(out_files, latest_version=latest_version, major_version=major_version, min_version=min_version, version=cdf_version)
        
                    tvars = cdf_to_tplot(filtered_out_files, varformat=varformat, varnames=varnames, get_support_data=get_support_data, suffix=suffix, center_measurement=center_measurement, notplot=notplot)
                    if tvars is not None:
                        tvars_created.extend(tvars)

    if time_clip:
        for new_var in tvars_created:
            tclip(new_var, trange[0], trange[1], suffix='')
            
    return tvars_created

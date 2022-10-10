from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2020-06-01', '2020-06-02'], 
         instrument='mag',
         datatype='rtn-normal', 
         mode=None,
         level='l2', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the Solar Orbiter mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.solo.mag
        pyspedas.solo.epd
        pyspedas.solo.rpw
        pyspedas.solo.swa

    """

    # Defaults for L2, L3 data
    science_or_low_latency = 'science'
    date_format = '%Y%m%d'
    cdf_version = '??'

    res = 24*3600.

    if level == 'll02':
        science_or_low_latency = 'low_latency'
        date_format = '%Y%m%dt%H%M??-*'
        cdf_version = '???'
        res = 60.0

    if instrument == 'mag':
        if level == 'll02':
            pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/%Y/solo_'+level+'_'+instrument+'_'+date_format+'_v'+cdf_version+'.cdf'
        else:
            pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
    elif instrument == 'epd':
        pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/'+mode+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'-'+mode+'_'+date_format+'_v'+cdf_version+'.cdf'
    elif instrument == 'rpw':
        pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
    elif instrument == 'swa':
        if level == 'l2' or level == 'll02':
            if datatype == 'pas-eflux' or datatype == 'pas-grnd-mom' or datatype == 'pas-vdf':
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
            else:
                date_format = '%Y%m%dt%H%M??-*'
                res = 60.0
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
        elif level == 'l1':
            if datatype == 'his-pha' or datatype == 'his-sensorrates' or datatype == 'pas-3d' or datatype == 'pas-cal' or datatype == 'pas-mom':
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
            else:
                date_format = '%Y%m%dt%H%M??-*'
                res = 60.0
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'

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

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

    if level == 'll02':
        science_or_low_latency = 'low_latency'
        date_format = '%Y%m%dt%H%M??-*'
        cdf_version = '???'

    if instrument == 'mag':
        pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
    elif instrument == 'epd':
        pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/'+mode+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'-'+mode+'_'+date_format+'_v'+cdf_version+'.cdf'
    elif instrument == 'rpw':
        pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
    elif instrument == 'swa':
        if datatype == 'pas-eflux':
            pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'

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

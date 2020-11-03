import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-11-5', '2018-11-6'], 
         probe='a',
         instrument='emfisis', 
         level='l3',
         datatype='magnetometer', 
         suffix='', 
         cadence='4sec', # for EMFISIS mag data
         coord='sm', # for EMFISIS mag data
         rel='rel04', # for ECT data
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads Van Allen Probes (RBSP) data; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.rbsp.emfisis
        pyspedas.rbsp.rbspice
        pyspedas.rbsp.efw
        pyspedas.rbsp.mageis
        pyspedas.rbsp.hope
        pyspedas.rbsp.rept
        pyspedas.rbsp.rps
    
    """

    if not isinstance(probe, list):
        probe = [probe]

    out_files = []

    for prb in probe:
        if instrument == 'emfisis':
            pathformat = 'rbsp'+prb+'/'+level+'/'+instrument+'/'+datatype+'/'+cadence+'/'+coord+'/%Y/rbsp-'+prb+'_'+datatype+'_'+cadence+'-'+coord+'_'+instrument+'-'+level+'_%Y%m%d_v*.cdf'
        elif instrument == 'rbspice':
            pathformat = 'rbsp'+prb+'/'+level+'/'+instrument+'/'+datatype+'/%Y/rbsp-'+prb+'-'+instrument+'_lev-'+str(level[-1])+'_'+datatype+'_%Y%m%d_v*.cdf'
        elif instrument == 'efw':
            pathformat = 'rbsp'+prb+'/'+level+'/'+instrument+'/%Y/rbsp'+prb+'_'+instrument+'-'+level+'_%Y%m%d_v??.cdf'
        elif instrument == 'mageis':
            pathformat = 'rbsp'+prb+'/'+level+'/ect/'+instrument+'/sectors/'+rel+'/%Y/rbsp'+prb+'_'+rel+'_ect-mageis-'+level+'_%Y%m%d_v*.cdf'
        elif instrument == 'hope':
            if datatype == 'moments':
                pathformat = 'rbsp'+prb+'/'+level+'/ect/'+instrument+'/'+datatype+'/'+rel+'/%Y/rbsp'+prb+'_'+rel+'_ect-hope-mom-'+level+'_%Y%m%d_v*.cdf'
            elif datatype == 'pitchangle':
                pathformat = 'rbsp'+prb+'/'+level+'/ect/'+instrument+'/'+datatype+'/'+rel+'/%Y/rbsp'+prb+'_'+rel+'_ect-hope-pa-'+level+'_%Y%m%d_v*.cdf'
        elif instrument == 'rept':
            pathformat = 'rbsp'+prb+'/'+level+'/ect/'+instrument+'/sectors/'+rel+'/%Y/rbsp'+prb+'_'+rel+'_ect-rept-sci-'+level+'_%Y%m%d_v*.cdf'
        elif instrument == 'rps':
            if datatype == 'rps-1min':
                pathformat = 'rbsp'+prb+'/'+level+'/psbr/'+datatype+'/%Y/rbsp'+prb+'_'+level+'-1min_psbr-rps_%Y%m%d_v*.cdf'
            elif datatype == 'rps':
                pathformat = 'rbsp'+prb+'/'+level+'/psbr/'+datatype+'/%Y/rbsp'+prb+'_'+level+'_psbr-rps_%Y%m%d_v*.cdf'


        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

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


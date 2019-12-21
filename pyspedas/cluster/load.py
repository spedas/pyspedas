import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-11-5', '2018-11-6'], 
         probe='1',
         instrument='fgm',
         datatype='up', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         downloadonly=False):
    """
    This function loads data from the Cluster mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.cluster.fgm
        pyspedas.cluster.aspoc
        pyspedas.cluster.cis
        pyspedas.cluster.dwp
        pyspedas.cluster.edi
        pyspedas.cluster.efw
        pyspedas.cluster.peace
        pyspedas.cluster.rapid
        pyspedas.cluster.staff
        pyspedas.cluster.wbd
        pyspedas.cluster.whi
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

    Returns:
        List of tplot variables created.

    """

    if not isinstance(probe, list):
        probe = [probe]

    tvars_created = []

    for prb in probe:
        if instrument == 'fgm':
            if datatype == 'spin':
                pathformat = 'c'+prb+'/cp/%Y/c'+prb+'_cp_fgm_spin_%Y%m%d_v??.cdf'
            else:
                pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        if instrument == 'aspoc':
            pathformat = 'c'+prb+'/'+datatype+'/asp/%Y/c'+prb+'_'+datatype+'_asp_%Y%m%d_v??.cdf'
        if instrument == 'cis':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        if instrument == 'dwp':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        if instrument == 'edi':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        if instrument == 'efw':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        if instrument == 'peace':
            pathformat = 'c'+prb+'/'+datatype+'/pea/%Y/c'+prb+'_'+datatype+'_pea_%Y%m%d_v??.cdf'
        if instrument == 'rapid':
            pathformat = 'c'+prb+'/'+datatype+'/rap/%Y/c'+prb+'_'+datatype+'_rap_%Y%m%d_v??.cdf'
        if instrument == 'staff':
            pathformat = 'c'+prb+'/'+datatype+'/sta/%Y/c'+prb+'_'+datatype+'_sta_%Y%m%d_v??.cdf'
        if instrument == 'whi':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        if instrument == 'wbd':
            pathformat = 'c'+prb+'/'+instrument+'/%Y/%m/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d????_v??.cdf'

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

        out_files = []

        for remote_file in remote_names:
            files = download(remote_file=remote_file, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'])
            if files is not None:
                for file in files:
                    out_files.append(file)

        out_files = sorted(out_files)

        if downloadonly:
            return out_files

        tvars = cdf_to_tplot(out_files, suffix=suffix, merge=True, get_support_data=get_support_data, varformat=varformat)
        if tvars is not None:
            tvars_created.extend(tvars)

    return tvars_created

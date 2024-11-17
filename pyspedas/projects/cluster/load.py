from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot
from typing import List, Union
from .config import CONFIG

def load(trange:List[str]=['2018-11-5', '2018-11-6'],
         probe:Union[str,List[str]]='1',
         instrument:str='fgm',
         datatype:str='up',
         prefix:str = '',
         suffix:str='',
         get_support_data:bool=False,
         varformat:str=None,
         varnames:List[str]=[],
         downloadonly:bool=False,
         notplot:bool=False,
         no_update:bool=False,
         time_clip:bool=False,
         force_download=False) -> List[str]:
    """
    Load data from Cluster instruments

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        probe: list of str
            List of probes to load.  Valid options: '1','2','3','4'
            Default: '1'

        instrument: str
            Instrument to load.
            Default: 'fgm;

        datatype: str
            Data type; Valid options:
            Default: 'up'

        prefix: str
            The tplot variable names will be given this prefix.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            If True, Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted. If empty or None, all variables will be loaded.
            Default: None (all variables loaded)

        varnames: list of str
            List of CDF variable names to load (if empty or not specified,
            all data variables are loaded)
            Default: [] (all variables loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False


    Returns
    -------
        list of str
            List of tplot variables created.

    Notes
    -----
    This function loads data from the Cluster mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.projects.cluster.fgm
        pyspedas.projects.cluster.aspoc
        pyspedas.projects.cluster.cis
        pyspedas.projects.cluster.dwp
        pyspedas.projects.cluster.edi
        pyspedas.projects.cluster.efw
        pyspedas.projects.cluster.peace
        pyspedas.projects.cluster.rapid
        pyspedas.projects.cluster.staff
        pyspedas.projects.cluster.wbd
        pyspedas.projects.cluster.whi

    """
    if prefix is None:
        prefix = ''
    if suffix is None:
        suffix = ''

    if not isinstance(probe, list):
        probe = [probe]

    probe = [str(prb) for prb in probe] # these will need to be strings from now on

    out_files = []

    res=24*3600

    if instrument != 'wbd':
        # note: can't use last_version with WBD data due to using wild cards for the times (and not just in the version)
        last_version = True
    else:
        last_version = False

    for prb in probe:
        if instrument == 'fgm':
            if datatype == 'cp':
                pathformat = 'c'+prb+'/cp/%Y/c'+prb+'_cp_fgm_spin_%Y%m%d_v??.cdf'
            else:
                pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        elif instrument == 'aspoc':
            pathformat = 'c'+prb+'/'+datatype+'/asp/%Y/c'+prb+'_'+datatype+'_asp_%Y%m%d_v??.cdf'
        elif instrument == 'cis':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        elif instrument == 'dwp':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        elif instrument == 'edi':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        elif instrument == 'efw':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        elif instrument == 'peace':
            pathformat = 'c'+prb+'/'+datatype+'/pea/%Y/c'+prb+'_'+datatype+'_pea_%Y%m%d_v??.cdf'
        elif instrument == 'rapid':
            pathformat = 'c'+prb+'/'+datatype+'/rap/%Y/c'+prb+'_'+datatype+'_rap_%Y%m%d_v??.cdf'
        elif instrument == 'staff':
            pathformat = 'c'+prb+'/'+datatype+'/sta/%Y/c'+prb+'_'+datatype+'_sta_%Y%m%d_v??.cdf'
        elif instrument == 'whi':
            pathformat = 'c'+prb+'/'+datatype+'/'+instrument+'/%Y/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
        elif instrument == 'wbd':
            pathformat = 'c'+prb+'/'+instrument+'/%Y/%m/c'+prb+'_'+datatype+'_'+instrument+'_%Y%m%d%H%M_v??.cdf'
            res = 600.0

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange, res=res)

        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update, last_version=last_version, force_download=force_download)
        if files is not None:
            for file in files:
                out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

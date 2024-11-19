from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot
from typing import List, Union
from .config import CONFIG

def load(trange:List[str]=['2018-11-5', '2018-11-6'],
         probe:Union[str,List[str]]='1',
         instrument:str='lad',
         datatype:str='',
         prefix:str='',
         suffix:str='',
         get_support_data:bool=False,
         varformat:str=None,
         varnames:List[str]=[],
         downloadonly:bool=False,
         force_download:bool=False,
         notplot:bool=False,
         no_update:bool=False,
         time_clip:bool=False) -> List[str]:
    """Load data from the TWINS mission
        Parameters
        ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        probe: str or list of str
            Probe to load. Valid options: '1', '2'
            Default: '1'

        instrument : str
            The instrument to load. Valid options: 'lad', 'imager', 'ephemeris'
            Default: 'lad'

        datatype: str
            Data type; Valid options: ''
            Default: ''

        prefix: str
            The tplot variable names will be given this prefix.
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: '' (all variables loaded)

        varnames: list of str
            List of variable names to load
            Default: [] (all variables will be loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        force_download: bool
            If True, download the file even if the local version is newer
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

    Returns
    --------
        list of str
            List of tplot variables created.

    Notes
    -----
    This function loads TWINS data; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.projects.twins.lad
        pyspedas.projects.twins.ephemeris
        pyspedas.projects.twins.imager

    """

    if prefix is None:
        prefix = ''
    if suffix is None:
        suffix = ''

    if not isinstance(probe, list):
        probe = [probe]

    probe = [str(prb) for prb in probe]

    out_files = []

    for prb in probe:
        if instrument == 'lad':
            pathformat = 'twins'+prb+'/'+instrument+'/%Y/twins'+prb+'_l1_lad_%Y%m%d_v??.cdf'
        elif instrument == 'imager':
            pathformat = 'twins'+prb+'/'+instrument+'/%Y/twins'+prb+'_l1_imager_%Y%m%d??_v??.cdf'
        elif instrument == 'ephemeris':
            pathformat = 'twins'+prb+'/'+instrument+'/'+datatype+'/%Y/twins'+prb+'_'+datatype+'_def_%Y%m%d_v??.cdf'

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update, force_download=force_download)
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
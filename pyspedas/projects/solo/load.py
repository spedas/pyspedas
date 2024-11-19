from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2020-06-01', '2020-06-02'], 
         instrument='mag',
         datatype='rtn-normal', 
         mode=None,
         level='l2', 
         suffix='', 
         prefix='',
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False,
         force_download=False):
    """
    This function loads data from the Solar Orbiter mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.projects.solo.mag
        pyspedas.projects.solo.epd
        pyspedas.projects.solo.rpw
        pyspedas.projects.solo.swa

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2020-06-01', '2020-06-02']

        instrument: str
            Spacecraft identifier ('mag', 'epd', 'rpw', 'swa')
            Default: 'mag'

        datatype: str
            Valid options: 'rtn-normal'
            Default: 'rtn_normal'

        mode: str
            Valid options: None
            Default: None

        level: str
            Valid options: 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            no prefix is added.
            Default: ''
        
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: 'False', only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded in.

        varnames: list of str
            List of variable names to load
            Default: [], all data variables are loaded

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
            If True, downloads the file even if a newer version exists locally. 
            Default: False.

    Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        mag_solar_vars = pyspedas.solar.mag(trange=['2020-06-01', '2020-06-02'])

        epd_solar_vars = pyspedas.solar.epd(trange=['2020-06-01', '2020-06-02'])

        rpw_solar_vars = pyspedas.solar.rpw(trange=['2020-06-01', '2020-06-02'])

        swa_solar_vars = pyspedas.solar.swa(trange=['2020-06-01', '2020-06-02'])

    """

    if prefix is None:
        prefix = ''
    
    if suffix is None:
        suffix = ''

    # Defaults for L2, L3 data
    science_or_low_latency = 'science'
    date_format = '%Y%m%d'
    cdf_version = '??'

    res = 24*3600.

    if level == 'll02':
        science_or_low_latency = 'low_latency'
        date_format = '%Y%m%dt??????-*'
        cdf_version = '???'
        res = 86400.0

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
                date_format = '%Y%m%dt??????-*'
                res = 86400.0
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
        elif level == 'l1':
            if datatype == 'his-pha' or datatype == 'his-sensorrates' or datatype == 'pas-3d' or datatype == 'pas-cal' or datatype == 'pas-mom':
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
            else:
                date_format = '%Y%m%dt??????-*'
                res = 86400.0
                pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'
        elif level == 'l3':
            pathformat = instrument+'/'+science_or_low_latency+'/'+level+'/'+datatype+'/%Y/solo_'+level+'_'+instrument+'-'+datatype+'_'+date_format+'_v'+cdf_version+'.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange, res=res)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update, force_download=force_download)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, prefix=prefix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

from .load import load
from pyspedas.utilities.datasets import find_datasets
from .load_csa import load_csa
from typing import List, Union, Optional


def fgm(trange:List[str]=['2018-11-5', '2018-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str ='up',
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
    Load data from the Cluster Fluxgate Magnetometer
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        probe: str or list of str
            List of probes to load.  Valid options: '1','2','3','4'
            Default: '1'

        datatype: str
            Data type; Valid options:
            Default: 'up'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> fgm_vars = pyspedas.cluster.fgm(trange=['2018-11-5', '2018-11-6'],probe=['1','2'])

    """
    return load(instrument='fgm', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def aspoc(trange:List[str]=['2003-11-5', '2003-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Active Spacecraft Potential Control experiment
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-11-5', '2003-11-6']

        probe: list of str
            List of probes to load.  Valid options: '1','2','3','4'
            Default: '1'

        datatype: str
            Data type; Valid options:
            Default: 'pp'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> aspoc_vars=pyspedas.cluster.aspoc(trange=['2003-11-05','2003-11-06'],probe=['1','2'])
    >>> tplot(['I_ion__C1_PP_ASP','I_ion__C2_PP_ASP'])

    """
    return load(instrument='aspoc', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def cis(trange:List[str]=['2018-11-5', '2018-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Ion Spectroscopy experiment
    
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

        datatype: str
            Data type; Valid options:
            Default: 'pp'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> cis_vars = pyspedas.cluster.cis(trange=['2003-11-01','2003-11-02'],probe=['1'])
    >>> tplot(['N_p__C1_PP_CIS','N_O1__C1_PP_CIS','N_He1__C1_PP_CIS','N_He2__C1_PP_CIS','N_HIA__C1_PP_CIS'])

    """
    return load(instrument='cis', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def dwp(trange:List[str]=['2018-11-5', '2018-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Digital Wave Processing instrument
    

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

        datatype: str
            Data type; Valid options:
            Default: 'pp'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> dwp_vars = pyspedas.cluster.dwp(trange=['2003-11-01','2003-11-02'],probe=['1','2'])
    >>> tplot(['Correl_freq__C1_PP_DWP','Correl_P__C1_PP_DWP'])

    """
    return load(instrument='dwp', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def edi(trange:List[str]=['2018-11-5', '2018-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Electron Drift Instrument
    
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

        datatype: str
            Data type; Valid options:
            Default: 'pp'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> edi_vars = pyspedas.cluster.edi(trange=['2003-11-01','2003-11-02'],probe=['1','2'])
    >>> tplot(['V_ed_xyz_gse__C1_PP_EDI','V_ed_xyz_gse__C1_PP_EDI'])
    """
    return load(instrument='edi', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def efw(trange:List[str]=['2018-11-5', '2018-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Electric Field and Wave experiment
    
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

        datatype: str
            Data type; Valid options:
            Default: 'up'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> efw_vars = pyspedas.cluster.efw(trange=['2003-11-01','2003-11-02'],probe=['2'])
    >>> tplot('E_pow_f1__C2_PP_EFW')
    """
    return load(instrument='efw', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def peace(trange:List[str]=['2016-11-5', '2016-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Plasma Electron and Current Experiment
    
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

        datatype: str
            Data type; Valid options:
            Default: 'up'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> peace_vars = pyspedas.cluster.peace(trange=['2003-11-01','2003-11-02'],probe=['1','2'])
    >>> tplot([ 'N_e_den__C1_PP_PEA', 'V_e_xyz_gse__C1_PP_PEA', 'N_e_den__C2_PP_PEA', 'V_e_xyz_gse__C2_PP_PEA'])

    """
    return load(instrument='peace', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def rapid(trange:List[str]=['2016-11-5', '2016-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Research with Adaptive Particle Imaging Detectors
    
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

        datatype: str
            Data type; Valid options:
            Default: 'up'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> rapid_vars = pyspedas.cluster.rapid(trange=['2003-11-01','2003-11-02'],probe=['1','2'])
    >>> tplot([ 'J_e_lo__C1_PP_RAP', 'J_e_hi__C1_PP_RAP', 'J_e_lo__C2_PP_RAP', 'J_e_hi__C2_PP_RAP'])

    """
    return load(instrument='rapid', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def staff(trange:List[str]=['2012-11-5', '2012-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Spatio-Temporal Analysis of Field Fluctuation experiment
    
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

        datatype: str
            Data type; Valid options:
            Default: 'pp'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> staff_vars = pyspedas.cluster.staff(trange=['2003-11-01','2003-11-02'],probe=['1','2'])
    >>> tplot(['B_par_f1__C1_PP_STA', 'B_perp_f1__C1_PP_STA', 'B_par_f1__C2_PP_STA', 'B_perp_f1__C2_PP_STA'])

    """
    return load(instrument='staff', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def wbd(trange:List[str]=['2003-11-01/14:00:00','2003-11-01/14:05:00'],
        probe:Union[str,List[str]]='1',
        datatype:str='waveform',
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
    Load data from the Cluster Wide Band Data receiver
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-11-01/14:00:00','2003-11-01/14:05:00']

        probe: list of str
            List of probes to load.  Valid options: '1','2','3','4'
            Default: '1'

        datatype: str
            Data type; Valid options:
            Default: 'waveform'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> wbd_vars = pyspedas.cluster.wbd(trange=['2003-11-01/14:00:00','2003-11-01/14:05:00'],probe=['1'])
    >>> # Note lack of probe IDs in the variables loaded -- only load one probe at a time
    >>> tplot('WBD_Elec')
    """
    return load(instrument='wbd', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def whi(trange:List[str]=['2012-11-5', '2012-11-6'],
        probe:Union[str,List[str]]='1',
        datatype:str='pp',
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
    Load data from the Cluster Waves of High Frequency and Sounder for Probing of Density by Relaxation instrument
    
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

        datatype: str
            Data type; Valid options:
            Default: 'pp'

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

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> whi_vars = pyspedas.cluster.whi(trange=['2003-11-01','2003-11-02'],probe=['1','2'])
    >>> tplot(['N_e_res__C1_PP_WHI','E_pow_f4__C1_PP_WHI','N_e_res__C2_PP_WHI','E_pow_f4__C2_PP_WHI'])

    """
    return load(instrument='whi', trange=trange, probe=probe, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, no_update=no_update, time_clip=time_clip, force_download=force_download)


def datasets(instrument=None, label=True):
    """
    Query SPDF for datasets available for a given Cluster instrument

    Parameters
    ----------
        instrument : str
            Instrument to use in query. Valid options: 'ASP','CIS','DWP','EDI','EFW','FGM','PEA','RAP','STA','WBD','WHI'
            Default: None

        label: bool
            If True, print both the dataset name and label; otherwise print only the dataset name.


    Examples
    --------
    >>> import pyspedas
    >>> pyspedas.cluster.datasets('FGM')
    """
    return find_datasets(mission='Cluster', instrument=instrument, label=label)

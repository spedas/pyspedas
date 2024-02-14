from .load import load
from pyspedas.utilities.datasets import find_datasets


def vhm(trange=['2009-01-01', '2009-01-02'],
        datatype='1min', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=True):
    """
    Load data from the VHM/FGM experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2009-01-01', '2009-01-02']

        datatype: str
            Data type; Valid options:'1min', '1sec', 'm1'
            Default: '1min'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vhm_vars = pyspedas.ulysses.vhm(trange=['2009-01-01', '2009-01-02'])
    >>> tplot('B_MAG')
    """
    return load(instrument='vhm', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def swoops(trange=['2009-01-01', '2009-01-02'],
        datatype='bai_m0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the SWOOPS experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2009-01-01', '2009-01-02']

        datatype: str
            Data type; Valid options: 'bai_m0, 'bai_m1', 'bae_m0'
            Default: 'bai_m0'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> swoops_vars = pyspedas.ulysses.swoops(trange=['2009-01-01', '2009-01-02'])
    >>> tplot(['Density', 'Temperature', 'Velocity'])
    """
    return load(instrument='swoops', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def swics(trange=['2009-01-01', '2009-01-02'],
        datatype='scs_m1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the SWICS experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2009-01-01', '2009-01-02']

        datatype: str
            Data type; Valid options: 'scs_m1', 'swi_m1', 'glg_h0'
            Default: 'scs_m1'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> swics_vars = pyspedas.ulysses.swics(trange=['2009-01-01', '2009-01-02'])
    >>> tplot('Velocity')
    """
    return load(instrument='swics', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def urap(trange=['2003-01-01', '2003-01-02'],
        datatype='pfrp_m0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the URAP experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-01-01', '2003-01-02']

        datatype: str
            Data type; Valid options: 'pfra_m0', 'pfrp_m0', 'r144_m0', 'rara_m0', 'rarp_m0', 'wfba_m0',
            'wfbp_m0', 'wfea_m0', 'wfep_m0'
            Default: 'pfrp_m0'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> urap_vars = pyspedas.ulysses.urap(trange=['2003-01-01', '2003-01-02'])
    >>> print(urap_vars)
    """
    return load(instrument='urap', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def epac(trange=['1996-01-01', '1996-01-02'],
        datatype='epac_m1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the EPAC experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['1996-01-01', '1996-01-02']

        datatype: str
            Data type; Valid options: 'epac_br', 'epac_el', 'epac_er', 'epac_hr', 'epac_hs', epac_m1', 'epac_op',
            'epac_oz', epac_pr', 'epac_ps', 'epac_zr', epac_zs'
            Default: 'epac_m1'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> epac_vars = pyspedas.ulysses.epac(trange=['1996-01-01', '1996-01-02'])
    >>> tplot('Omni_Protons')

    """
    return load(instrument='epac', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def hiscale(trange=['2003-01-01', '2003-01-02'],
        datatype='lmde_m1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the HI-SCALE experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-01-01', '2003-01-02']

        datatype: str
            Data type; Valid options: 'lf15_m1', 'lf60_m1', 'lm12_m1', 'lm30_m1', 'lmde_m1', 'wart_m1', 'wrtd_m1'
            Default: 'lmde_m1'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vhm_vars = pyspedas.ulysses.vhm(trange=['2009-01-01', '2009-01-02'])
    >>> tplot('B_MAG')
    """
    return load(instrument='hiscale', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def cospin(trange=['2003-01-01', '2003-01-02'],
        datatype='het', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the COSPIN experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-01-01', '2003-01-02']

        datatype: str
            Data type; Valid options: 'at1', 'at2', 'het', 'hft', 'ket', 'let'
            Default: 'het'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> cospin_vars = pyspedas.ulysses.cospin(trange=['2003-01-01', '2003-01-02'])
    >>> print(cospin_vars)
    """
    return load(instrument='cospin', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def grb(trange=['2003-01-01', '2003-01-02'],
        datatype='grb_m0', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the GRB experiment from the Ulysses mission
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2003-01-01', '2003-01-02']

        datatype: str
            Data type; Valid options: 'grb_m0'
            Default: 'grb_m0'

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
            List of variable names to load (If empty list or not specified,
            all data variables are loaded)
            Default: []

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

    Returns
    -------
        list of str
            List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> grb_vars = pyspedas.ulysses.grb(trange=['2003-01-01', '2003-01-02'])
    >>> tplot('Count_Rate')

    """
    return load(instrument='grb', trange=trange, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)


def datasets(instrument=None, label=True):
    return find_datasets(mission='Ulysses', instrument=instrument, label=label)

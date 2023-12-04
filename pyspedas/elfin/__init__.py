from functools import wraps

from .load import load
from .epd.epd import elfin_load_epd

@wraps(elfin_load_epd)
def epd(*args, **kwargs):
    """
    This function loads data from the Energetic Particle Detector (EPD) and process L1 and L2 data.

    Parameters for Load Routine
    ----------
        trange : list of str
            Time range of interest [starttime, endtime]. Format can be
            ['YYYY-MM-DD','YYYY-MM-DD'] or ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str, optional
            Spacecraft identifier. Options are 'a' (default) and 'b'.

        level: str, optional.
            Data level. Options are 'l1' (default) and 'l2'.

        suffix: str, optional
            Suffix added to tplot variable names during loading. Defaults to no suffix.

        get_support_data: bool, optional
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted. By default, all variables are loaded in.

        varnames: list of str, optional
            List of variable names to load. By default, all data variables are loaded.

        downloadonly: bool, optional
            If True, only downloads the CDF files without loading them into tplot variables. 
            Default is False.

        notplot: bool, optional
            If True, returns data in hash tables instead of creating tplot variables. 
            Default is False.

        no_update: bool
            If True, loads data only from the local cache. Default is False. 

        time_clip: bool
            If True, clips the variables to the exact range specified in the trange. 
            Default is True.

    Parameters for L1 data
    ----------
        datatype: str, optional. 
            Data type of L1 data. Options are 'pef' (default), 'pif', 'pes', 'pis'. 

        type_ : str, optional
            Calibrated data type of L1 data. Options are 'raw', 'cps', 'nflux' (default), 'eflux'.

        nspinsinsum: int, optional
            Number of spins in sum which is needed by the L1 calibration function.
    
    Parameters for L2 data
    ----------
        fullspin: bool, optional.
            If True, generate L2 full spin spectrogram. By default, L2 half spin spectrogram is generated.

        PAspec_energybins: list of tuple of int, optional
            Specified the energy bins used for generating L2 pitch angle spectrogram. 
            Default is [(0,2),(3,5), (6,8), (9,15)]. If both 'PAspec_energybins' and 'PAspec_energies' 
            are set, 'energybins' takes precedence.
            
        PAspec_energies: list of tuple of float, optional
            Specifies the energy range for each bin in the L2 pitch angle spectrogram.
            Example: energies=[(50.,160.),(160.,345.),(345.,900.),(900.,7000.)]
            If both 'energybins' and 'energies' are set, 'energybins' takes precedence.
            Energy and energybin table:
            channel     energy_range    energy_midbin
            0           50-80           63.2
            1           80-120          97.9
            2           120-160         138.5
            3           160-210         183.3
            4           210-270         238.1
            5           270-345         305.2
            6           345-430         385.1
            7           430-630         520.4
            8           630-900         752.9
            9           900-1300        1081.6
            10          1300-1800       1529.7
            11          1800-2500       2121.3
            12          2500-3350       2893.9
            13          3350-4150       3728.6
            14          4150-5800       4906.1
            15          5800+           6500.0

        Espec_LCfatol: float, optional
            Tolerance angle for para and anti flux in generating L2 energy spectrogram. 
            A positive value makes the loss cone/antiloss cone smaller by this amount. 
            Default is 22.25 deg.

        Espec_LCfptol: float, optional
            Tolerance angle for perp flux in generating L2 energy spectrogram. 
            A negative value means a wider angle for perp flux.
            Default is -11 deg.

    Returns
    ----------
        List of tplot variables created.

    """
    return elfin_load_epd(*args, **kwargs)

def fgm(trange=['2020-10-01', '2020-10-02'],
        probe='a',
        datatype='survey',
        level='l1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Fluxgate Magnetometer (FGM)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Spacecraft identifier ('a' or 'b')

        datatype: str
            Data type; Valid options:
                'fast', 'survey' for L1 data

        level: str
            Data level; options: 'l1' (default: l1)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    tvars = load(instrument='fgm', probe=probe, trange=trange, level=level, 
                datatype=datatype, suffix=suffix, get_support_data=get_support_data, 
                varformat=varformat, varnames=varnames, downloadonly=downloadonly, 
                notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return fgm_postprocessing(tvars)


def fgm_postprocessing(variables):
    """
    Placeholder for FGM post-processing
    """
    return variables





def mrma(trange=['2020-11-5', '2020-11-6'],
        probe='a',
        datatype='mrma', 
        level='l1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Magneto Resistive Magnetometer (MRMa)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Spacecraft identifier ('a' or 'b')

        datatype: str
            Data type; Valid options:
                'mrma' for L1 data

        level: str
            Data level; options: 'l1' (default: l1)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    tvars = load(instrument='mrma', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return mrma_postprocessing(tvars)


def mrma_postprocessing(variables):
    """
    Placeholder for MRMa post-processing 
    """
    return variables


def mrmi(trange=['2020-11-5', '2020-11-6'],
        probe='a',
        datatype='mrmi', 
        level='l1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Magneto Resistive Magnetometer (MRMi)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Spacecraft identifier ('a' or 'b')

        datatype: str
            Data type; Valid options:
                'mrmi' for L1 data

        level: str
            Data level; options: 'l1' (default: l1)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    tvars = load(instrument='mrmi', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return mrmi_postprocessing(tvars)


def mrmi_postprocessing(variables):
    """
    Placeholder for MRMi post-processing 
    """
    return variables


def state(trange=['2020-11-5/10:00', '2020-11-5/12:00'],
        probe='a',
        datatype='defn',
        level='l1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=True):
    """
    This function loads data from the State data (state)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Spacecraft identifier ('a' or 'b')

        datatype: str
            Data type; Valid options:
                'defn' (default)
                'pred'

        level: str
            Data level; options: 'l1' (default: l1)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    tvars= load(instrument='state', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return state_postprocessing(tvars)


def state_postprocessing(variables):
    """
    Placeholder for State post-processing 
    """
    return variables


def eng(trange=['2020-11-5', '2020-11-6'],
        probe='a',
        datatype='eng_datatype', 
        level='l1', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Engineering (ENG)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            Spacecraft identifier ('a' or 'b')

        datatype: str
            Data type; Valid options:
                'eng_datatype' for L1 data

        level: str
            Data level; options: 'l1' (default: l1)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    tvars = load(instrument='eng', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    return eng_postprocessing(tvars)


def eng_postprocessing(variables):
    """
    Placeholder for ENG post-processing 
    """
    return variables

        


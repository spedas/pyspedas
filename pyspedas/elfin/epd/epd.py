import logging

from pyspedas.elfin.load import load
from pyspedas.elfin.epd.postprocessing import epd_l1_postprocessing, epd_l2_postprocessing


def elfin_load_epd(trange=['2020-11-01', '2020-11-02'],
        probe='a',
        datatype='pef',
        level='l1',
        type_='nflux',
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=True,
        nspinsinsum=None,
        fullspin=False,
        PAspec_energies=None,
        PAspec_energybins=None,
        Espec_LCfatol=None,
        Espec_LCfptol=None,
):
    """
    This function loads data from the Energetic Particle Detector (EPD)

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
                'pef' for L1 data
                'pif' for L1 data
                'pes' for L1 data
                'pis' for L1 data

        level: str
            Data level; options: 'l1' (default: l1)

        type_ : str
            Calibrated data type, one of ('raw', 'cps', 'nflux', 'eflux'). ('eflux' not fully tested)
            Default: 'nflux'.

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

        nspinsinsum : int, optional
            Number of spins in sum which is needed by the calibration function.

        fullspin: bool
            If true, generate full spin with l2 epd instead of half spin
            Default is False

        PAspec_energybins: list of tuple of int, optional
            Specified the energy bins used for generating l2 pitch angle spectra. 
            Default is [(0,2),(3,5), (6,8), (9,15)]. If both 'PAspec_energybins' and 'PAspec_energies' 
            are set, 'energybins' takes precedence
            
        PAspec_energies: list of tuple of float, optional
            Specifies the energy range for each bin in the l2 pitch angle spectra.
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
            Tolerance angle for para and anti flux. A positive value makes the loss 
            cone/antiloss cone smaller by this amount. 
            Default is 22.25 deg.

        Espec_LCfptol: float, optional
            Tolerance angle for perp flux. A negative value means a wider angle for 
            perp flux.
            Default is -11 deg.

    Returns
    ----------
        List of tplot variables created.

    """
    logging.info("ELFIN EPD: START LOADING.")
    tvars = load(instrument='epd', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix,
                 get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                 notplot=notplot, time_clip=time_clip, no_update=no_update)
    logging.info("ELFIN EPD: LOADING END.")
    if tvars is None or notplot or downloadonly:
        return tvars

    CALIBRATED_TYPE_UNITS = {
        "raw": "counts/sector",
        "cps": "counts/s",
        "nflux": "#/(s-cm$^2$-str-MeV)",
        "eflux": "keV/(s-cm$^2$-str-MeV)0",
    }

    if type_ in ("cal", "calibrated") or type_ not in CALIBRATED_TYPE_UNITS.keys():
        type_ = "nflux"

    if level == "l1":
        tvars = epd_l1_postprocessing(tvars, trange=trange, type_=type_, nspinsinsum=nspinsinsum,
                                     unit=CALIBRATED_TYPE_UNITS[type_])
        return tvars
    
    elif level == "l2":
        logging.info("ELFIN EPD L2: START PROCESSING.")
        # check whether input type is allowed
        if type_ not in ("nflux","eflux"):
            logging.warning(f"fluxtype {type_} is not allowed in l2 data, change to nflux!")
            type_ = "nflux"

        res = 'hs' if fullspin is False else 'fs'
        tvars = epd_l2_postprocessing(
            tvars,
            fluxtype=type_,
            res=res,
            PAspec_energies=PAspec_energies,
            PAspec_energybins=PAspec_energybins,
            Espec_LCfatol=Espec_LCfatol,
            Espec_LCfptol=Espec_LCfptol,)
        
        return tvars
    else:
        raise ValueError(f"Unknown level: {level}")

    return tvars

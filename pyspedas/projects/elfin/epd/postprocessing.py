import logging

from pytplot import get, store, del_data, tnames, tplot_rename, options, tplot
from pytplot import time_clip as tclip

from pyspedas.projects.elfin.epd.calibration_l2 import epd_l2_Espectra, epd_l2_PAspectra
from pyspedas.projects.elfin.epd.calibration_l1 import calibrate_epd

def epd_l1_postprocessing(
    tplotnames,
    trange=None,
    type_=None,
    nspinsinsum=None,
    unit=None,
):
    """
    Calibrates data from the Energetic Particle Detector (EPD) and sets dlimits.

    Parameters
    ----------
        tplotnames : list of str
            The tplot names of EPD data to be postprocessed.

        trange : list of str
            Time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        type_ : str, optional
            Desired data type. Options: 'raw', 'cps', 'nflux', 'eflux'.

        nspinsinsum : int, optional
            Number of spins in sum which is needed by the calibration function.

        unit : str, optional
            Units of the data.


    Returns
    ----------
        List of tplot variables created.

    """

    tplotnames = tplotnames.copy()

    # Calibrate spinper to turn it to seconds
    FGM_SAMPLE_RATE = 80.0

    for name in filter(lambda n: "spinper" in n, tplotnames):
        d = get(name)
        cal_spinper = d.y / FGM_SAMPLE_RATE
        store(name, {"x": d.times, "y": cal_spinper}, metadata=get(name, metadata=True))

    if nspinsinsum is None:
        tn = tnames("*nspinsinsum*")
        if tn:
            nspin = get(tn[0])
            nspinsinsum = nspin.y if nspin is not None else 1
        else:
            nspinsinsum = 1

    new_tvars = []

    for name in tplotnames:
        if "energies" in name:
            del_data(name)
            continue
        if "sectnum" in name:
            options(name, 'ytitle', name)
            new_tvars.append(name)
            continue
        if "spinper" in name:
            options(name, 'ytitle', name)
            options(name, 'ysubtitle','[sec]')
            new_tvars.append(name)
            continue
        if "nspinsinsum" in name:
            options(name, 'ytitle', name)
            new_tvars.append(name)
            continue
        if "nsectors" in name:
            options(name, 'ytitle', name)
            new_tvars.append(name)
            continue
        
        new_name = f"{name}_{type_}"
        tplot_rename(name, new_name)
        options(new_name, 'ytitle', new_name) # set units for elx_pef variable
        options(new_name, 'ysubtitle', unit)
        new_tvars.append(new_name)

        calibrate_epd(new_name, trange=trange, type_=type_, nspinsinsum=nspinsinsum)

    # TODO: Set units and tplot options (obey no_spec)

    return new_tvars


def epd_l2_postprocessing(
    tplotnames,
    fluxtype='nflux',
    res='hs',
    datatype='e',
    PAspec_energies = None,
    PAspec_energybins = None,
    Espec_LCfatol = None,
    Espec_LCfptol = None,
):
    """
    Process ELF EPD L2 data and generate omni, para, anti, perp flux spectra.

    Parameters
    ----------
        tplotnames : list of str
            The tplot names of EPD data to be postprocessed.

        fluxtype: str, optional
            Type of flux spectra. 
            Options: 'nflux' for number flux, 'eflux' for energy flux.
            Default is 'nflux'.

        res: str, optional
            Resolution of spectra. 
            Options: 'hs' for half spin, 'fs' for full spin. 
            Default is 'hs'.

        datatype: str, optional
            Type of data. 
            Options: 'e' for electron data, 'i' for ion data
            Default is 'e'.
        
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

    tplotnames = tplotnames.copy()

    flux_tname = [name for name in tplotnames if f"p{datatype}f_{res}_Epat_{fluxtype}" in name]
    LC_tname = [name for name in tplotnames if f"_{res}_LCdeg" in name]
    
    if len(flux_tname) != 1:
        logging.error(f'{len(flux_tname)} flux tplot variables is found!')
        return
    
    if len(LC_tname) != 1:
        logging.error(f'{len(LC_tname)} LC tplot variables is found!')
        return
    
    logging.info("ELFIN EPD L2: START ENERGY SPECTOGRAM.")
    # get energy spectra in four directions
    E_tvar = epd_l2_Espectra(flux_tname[0], LC_tname[0], LCfatol=Espec_LCfatol, LCfptol=Espec_LCfptol)

    logging.info("ELFIN EPD L2: START PITCH ANGLE SPECTOGRAM.")
    # get pitch angle spectra
    #PA_tvar = epd_l2_PAspectra(flux_tname[0], energies=[(60, 200),(300, 1000)])
    PA_tvar = epd_l2_PAspectra(flux_tname[0], energies=PAspec_energies, energybins=PAspec_energybins)

    return E_tvar + PA_tvar
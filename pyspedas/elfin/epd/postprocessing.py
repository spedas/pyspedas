import logging

from pytplot import get, store, del_data, tnames, tplot_rename, options, tplot
from pyspedas.analysis.time_clip import time_clip as tclip

from .calibration_l2 import epd_l2_flux4dir
from .calibration import calibrate_epd

def epd_l1_postprocessing(
    tplotnames,
    trange=None,
    type_=None,
    nspinsinsum=None,
    unit=None,
    no_spec=False,
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

        no_spec : bool
            Flag to set tplot options to linear rather than the default of spec.
            Default is False.

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

        

    Returns
    ----------
        List of tplot variables created.
    """

    tplotnames = tplotnames.copy()
    tvars=[]
    flux_tname = [name for name in tplotnames if f"p{datatype}f_{res}_Epat_{fluxtype}" in name]
    LC_tname = [name for name in tplotnames if f"_LCdeg_{res}" in name]  #TODO: change loss cone name later
    if len(flux_tname) != 1 | len(LC_tname) != 1:
        logging.error('two flux tplot variables are founded!')
        return
  
    tvars = epd_l2_flux4dir(flux_tname[0], LC_tname[0])

    return tvars
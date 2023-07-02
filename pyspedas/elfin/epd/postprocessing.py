import logging

from pytplot import get, store, del_data, tnames, tplot_rename, options

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
            options(name, 'ytitle', 'sectnum')
            new_tvars.append(name)
            continue
        if "spinper" in name:
            options(name, 'ytitle', 'spinper')
            options(name, 'ysubtitle','[sec]')
            new_tvars.append(name)
            continue
        if "nspinsinsum" in name:
            options(name, 'ytitle', 'nspinsinsum')
            new_tvars.append(name)
            continue
        if "nsectors" in name:
            options(name, 'ytitle', 'nsectors')
            new_tvars.append(name)
            continue

        new_name = f"{name}_{type_}"
        tplot_rename(name, new_name)
        new_tvars.append(new_name)

        calibrate_epd(new_name, trange=trange, type_=type_, nspinsinsum=nspinsinsum)

    # TODO: Set units and tplot options (obey no_spec)

    return new_tvars

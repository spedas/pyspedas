from ..load import load

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
        time_clip=False,
        nspinsinsum=None,
        no_spec=False,
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

    Returns
    ----------
        List of tplot variables created.

    """
    tvars = load(instrument='epd', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix,
                 get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                 notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    CALIBRATED_TYPE_UNITS = {
        "raw": "counts/sector",
        "cps": "counts/s",
        "nflux": "#/(scm!U2!NstrMeV)",
        "eflux": "keV/(scm!U2!NstrMeV)",
    }

    if type_ in ("cal", "calibrated") or type_ not in CALIBRATED_TYPE_UNITS.keys():
        type_ = "nflux"

    return epd_postprocessing(tvars, trange=trange, type_=type_, nspinsinsum=nspinsinsum,
                              unit=CALIBRATED_TYPE_UNITS[type_], no_spec=no_spec)


def epd_postprocessing(
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

    return tplotnames


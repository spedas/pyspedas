import logging
import pathlib
import importlib.resources
from typing import List, Dict

import numpy as np
from pytplot import time_double, time_string
from pytplot import get_timespan, store, get, store_data, get_data


def read_epde_calibration_data(path: pathlib.Path) -> List[Dict]:
    """
    Read ELFIN EPDE calibration data from file and return
    list of parsed calibration datasets.

    Parameters
    ----------
        path : pathlib.Path
            The path to the calibration data file.

    Returns
    ----------
        List of EPDE calibration data parsed from the file.

    """

    def parse_float_line(line: str):
        array_str = line.split(":")[1].strip()
        return [float(f.rstrip(".")) for f in array_str.split(",")]

    lines = []
    with open(path, "r") as f:
        lines = f.readlines()

    date_lines = (i for i, line in enumerate(lines) if line.startswith("Date"))
    calibrations = []
    for i in date_lines:

        date_str = lines[i].split(":")[1].strip()
        gf_str = lines[i+1].split(":")[1].strip()

        cal = {
            "date": time_double(date_str),
            "gf": float(gf_str),
            "overaccumulation_factors": parse_float_line(lines[i+2]),
            "thresh_factors": parse_float_line(lines[i+3]),
            "ch_efficiencies": parse_float_line(lines[i+4]),
            "ebins": parse_float_line(lines[i+5]),
        }

        calibrations.append(cal)

    return calibrations


def get_epde_calibration(calibration_data: Dict) -> Dict:
    """
    Performs basic transformations on calibration parameters loaded
    from a data file, e.g. calculate channel factors and create energy bin labels.

    Returned dictionary values are (mostly) numpy arrays for later usage.

    Parameters
    ----------
        calibration_data : dict
            A single set of calibration data read from a file. See `obj`:read_epde_calibration_data:

    Returns
    ----------
        Dictionary with EPD gain factor, overaccumulation factors, threshold factors,
        channel efficiencies, energy bins (and logmean), calibration channel factors,
        and the labels for the energy bins.

    """

    gf = calibration_data["gf"]

    overaccumulation_factors = np.array(calibration_data["overaccumulation_factors"])
    thresh_factors = np.array(calibration_data["thresh_factors"])
    ch_efficiencies = np.array(calibration_data["ch_efficiencies"])
    ebins = np.array(calibration_data["ebins"])

    cal_ch_factors = 1.0 / (gf * thresh_factors * ch_efficiencies)

    ebins_logmean = ebins.copy()
    for i in range(0, 15):
        i_mean_of_logs = (np.log10(ebins[i]) + np.log10(ebins[i+1])) / 2.0
        ebins_logmean[i] = np.power(10.0, i_mean_of_logs)
    ebins_logmean[15] = 6500.0

    ebin_labels = [
        "50-80", "80-120", "120-160", "160-210",
        "210-270", "270-345", "345-430", "430-630",
        "630-900", "900-1300", "1300-1800", "1800-2500",
        "2500-3350", "3350-4150", "4150-5800", "5800+",
    ]

    calibration = {
        "epd_gf": gf,
        "epd_overaccumulation_factors": overaccumulation_factors,
        "epd_thresh_factors": thresh_factors,
        "epd_ch_efficiencies": ch_efficiencies,
        "epd_ebins": ebins,
        "epd_cal_ch_factors": cal_ch_factors,
        "epd_ebins_logmean": ebins_logmean,
        "epd_ebin_labels": ebin_labels,
    }

    return calibration


def get_epdi_calibration() -> Dict:
    """
    Ported from IDL SPEDAS elf_get_epd_calibration procedure. There are
    no calibration data files for epdi. Current as of 2023-06-11.

    Vassilis Angelopoulos' most recent comments from IDL procedure reproduced.

    Returns
    ----------
        Dictionary with EPD gain factor, overaccumulation factors, threshold factors,
        channel efficiencies, energy bins (and logmean), calibration channel factors,
        and the labels for the energy bins.

    """

    # 9deg x 9deg (FWHM Solid Angle) by 1/4" dia. round aperture area
    gf = 0.031256

    overaccumulation_factors = np.ones(16)
    thresh_factors = np.ones(16)
    thresh_factors[0] = 0.2
    ch_efficiencies = np.ones(16)

    cal_ch_factors = 1.0 / (gf * thresh_factors * ch_efficiencies)

    # in keV based on Jiang Liu's Geant4 code 2019-3-5
    ebins = np.array([
        50.0, 80.0, 120.0, 160.0,
        210.0, 270.0, 345.0, 430.0,
        630.0, 900.0, 1300.0, 1800.0,
        2500.0, 3350.0, 4150.0, 5800.0,
    ])

    ebins_logmean = ebins.copy()
    for i in range(0, 15):
        i_mean_of_logs = (np.log10(ebins[i]) + np.log10(ebins[i+1])) / 2.0
        ebins_logmean[i] = np.power(10.0, i_mean_of_logs)
    ebins_logmean[15] = 6500.0

    # used same bins as electrons (dead layer well below 50keV)
    ebin_labels = [
        "50-80", "80-120", "120-160", "160-210",
        "210-270", "270-345", "345-430", "430-630",
        "630-900", "900-1300", "1300-1800", "1800-2500",
        "2500-3350", "3350-4150", "4150-5800", "5800+",
    ]

    calibration = {
        "epd_gf": gf,
        "epd_overaccumulation_factors": overaccumulation_factors,
        "epd_thresh_factors": thresh_factors,
        "epd_ch_efficiencies": ch_efficiencies,
        "epd_ebins": ebins,
        "epd_cal_ch_factors": cal_ch_factors,
        "epd_ebins_logmean": ebins_logmean,
        "epd_ebin_labels": ebin_labels,
    }

    return calibration


def get_epd_calibration(probe, instrument, trange):

    if instrument == "epde":
        filename = f"el{probe}_epde_cal_data.txt"

        cal_datasets = None
        with importlib.resources.path("pyspedas.projects.elfin.epd", filename) as cal_file_path:
            cal_datasets = read_epde_calibration_data(cal_file_path)

        if not cal_datasets:
            raise ValueError("Could not load calibration data")

        # Choose the latest calibration data preceeding the start of trange
        cal_datasets.sort(key=lambda cal: cal["date"])
        filtered = list(filter(lambda cal: cal["date"] < time_double(trange[0]), cal_datasets))
        epde_cal_file_data = filtered[-1]

        cal_date = time_string(epde_cal_file_data["date"])
        logging.info(f"Using EPDE calibration data from {cal_date}")

        return get_epde_calibration(epde_cal_file_data)

    elif instrument == "epdi":
        return get_epdi_calibration()
    else:
        raise ValueError(f"Unknown instrument: {instrument!r}")


def calibrate_epd(
    tplotname,
    trange=None,
    type_="eflux",
    probe=None,
    deadtime_corr=None,
    nspinsinsum=1,
):
    """
    Ported from IDL SPEDAS elf_cal_epd procedure. Originally authored
    by Colin Wilkins (colinwilkins@ucla.edu). Relevant comments on
    calibration details have been reproduced here.
    """

    probe = probe if probe is not None else tplotname[2]

    sc = f"el{probe}"
    if "pef" in tplotname:
        instrument = "epde"
        stype = "pef"
    elif "pif" in tplotname:
        instrument = "epdi"
        stype = "pif"

    d = get(tplotname)
    if not d:
        return # TODO: Or raise ValueError?

    trange = time_double(trange) if trange is not None else get_timespan(tplotname)

    dspinper = get_data(f"{sc}_{stype}_spinper")
    dsectnum = get_data(f"{sc}_{stype}_sectnum")
    dnsectors = get_data(f"{sc}_{stype}_nsectors")

    epd_cal = get_epd_calibration(probe=probe, instrument=instrument, trange=trange)

    num_samples = len(d.times)
    cal_ch_factors = epd_cal["epd_cal_ch_factors"]
    overint_factors = epd_cal["epd_overaccumulation_factors"]
    ebins = epd_cal["epd_ebins"]
    ebins_logmean = epd_cal["epd_ebins_logmean"]
    n_sectors = dnsectors.y

    dE = 1.0e-3 * (ebins[1:16] - ebins[0:15]) # in MeV
    dE = np.append(dE, 6.2)

    mytimesra = np.ones(num_samples)
    n_energies = len(ebins)
    mynrgyra = np.ones(n_energies)

    if deadtime_corr is None:
        logging.info("Deadtime correction applied with default deadtime; "
                     "to not apply set deadtime_corr= 0. or a tiny value, e.g. 1.e-9")
        # [default ~ 2% above ~max cps in data (after overaccum. corr.)
        # of 125Kcps corresponds to 8.e-6 us peak hold in front preamp]
        deadtime_corr = 1.0 / (1.02 * 1.25e5)

    dt = (nspinsinsum * dspinper.y / n_sectors * overint_factors[dsectnum.y])
    dt = dt[:,np.newaxis] @ mynrgyra[np.newaxis]

    if type_ == "raw":
        store_data(
            tplotname,
            data={"x": d.times, "y": d.y, "v": np.arange(16, dtype=np.float32)},
            attr_dict=get_data(tplotname, metadata=True)
        )
    elif type_ == "cps":
        cps = d.y / dt
        tot_cps = np.nansum(cps, axis=1)[:,np.newaxis] @ mynrgyra[np.newaxis,:]

        # Deadtime correction
        cps_deadtime_corrected = cps / (1.0 - tot_cps * deadtime_corr)

        # Only reason for negatives is deadtime correction
        ineg = np.where(np.nansum(cps_deadtime_corrected, axis=1) < 0.0)[0]
        if len(ineg) > 0:
            cps_deadtime_corrected[ineg,:] = 0.0
            d3interpol = cps_deadtime_corrected.copy()
            d3interpol[1:num_samples-1,:] = (cps_deadtime_corrected[0:num_samples-2,:] + 
                                             cps_deadtime_corrected[2:num_samples,:]) / 2.0
            cps_deadtime_corrected[ineg,:] = d3interpol[ineg,:]

        store_data(
            tplotname,
            data={"x": d.times, "y": cps_deadtime_corrected, "v": ebins_logmean},
            attr_dict=get_data(tplotname, metadata=True)
        )

    elif type_ == "nflux":
        cps = d.y / dt
        tot_cps = np.nansum(cps, axis=1)[:,np.newaxis] @ mynrgyra[np.newaxis,:]

        # Deadtime correction
        cps_deadtime_corrected = cps / (1.0 - tot_cps * deadtime_corr)

        rel_energy_cal = cal_ch_factors / dE
        nflux = cps_deadtime_corrected * (mytimesra[:,np.newaxis] @ rel_energy_cal[np.newaxis,:])

        # Only reason for negatives is deadtime correction
        ineg = np.where(np.nansum(nflux, axis=1) < 0.0)[0]
        if len(ineg) > 0:
            nflux[ineg,:] = 0.0
            d3interpol = nflux.copy()
            d3interpol[1:num_samples-1,:] = (nflux[0:num_samples-2,:] + 
                                             nflux[2:num_samples,:]) / 2.0
            nflux[ineg,:] = d3interpol[ineg,:]

        store_data(
            tplotname,
            data={"x": d.times, "y": nflux, "v": ebins_logmean},
            attr_dict=get_data(tplotname, metadata=True)
        )

    elif type_ == "eflux":
        cps = d.y / dt
        tot_cps = np.nansum(cps, axis=1)[:,np.newaxis] @ mynrgyra[np.newaxis,:]

        # Deadtime correction
        cps_deadtime_corrected = cps / (1.0 - tot_cps * deadtime_corr)

        eflux_cal = ebins_logmean * (cal_ch_factors / dE)
        eflux = cps_deadtime_corrected * (mytimesra[:,np.newaxis] @ eflux_cal[np.newaxis,:])

        # Only reason for negatives is deadtime correction
        ineg = np.where(np.nansum(eflux, axis=1) < 0.0)[0]
        if len(ineg) > 0:
            eflux[ineg,:] = 0.0
            d3interpol = eflux.copy()
            d3interpol[1:num_samples-1,:] = (eflux[0:num_samples-2,:] + 
                                             eflux[2:num_samples,:]) / 2.0
            eflux[ineg,:] = d3interpol[ineg,:]

        store_data(
            tplotname,
            data={"x": d.times, "y": eflux, "v": ebins_logmean},
            attr_dict=get_data(tplotname, metadata=True)
        )
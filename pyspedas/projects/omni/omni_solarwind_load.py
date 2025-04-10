import numpy as np
import logging
from pytplot import tnames, store_data, time_double, degap, tdeflag, time_clip
from pyspedas.projects.omni.load import load
from pyspedas.analysis.tinterpol import tinterpol
from pyspedas.utilities.tcopy import tcopy_one


def get_omni_default_solarwind(trange):
    # Convert time range to epoch seconds
    times = time_double(trange[0])
    timee = time_double(trange[1])

    # Create time grid with 1001 points
    nnom = 1000
    dt = (timee - times) / nnom
    tgrid = times + dt * np.arange(nnom)

    # Create default pressure and Bz arrays
    bzout = np.zeros(nnom)
    dpout = np.full(nnom, 2.088)  # nPa

    return [tgrid, dpout, bzout]


def omni_solarwind_load(
    trange, interpolto=None, prefix=None, suffix=None, level="hro2", min5=False
):
    """
    Loads solar wind data from OMNI.

    Parameters
    ----------
    trange : list of float
        Time range of data to be loaded.
    level : str, optional
        Data level for OMNI data; valid options: 'hro', 'hro2'.
        Default is 'hro2'.
    min5 : bool, optional
        Flag indicating whether to load 1-minute or 5-minute data. Default is False (1-minute data).

    Returns
    -------
    Numpy array of solar wind data with shape (N, 3), where N is the number of time points
    and the columns are time, pressure, and Bz GSM.

    """

    if min5:
        datatype = "5min"
    else:
        datatype = "1min"

    if prefix is None:
        prefix = "omni_solarwind_"
    if suffix is None:
        suffix = ""
    new_bz = prefix + "BZ" + suffix
    new_p = prefix + "P" + suffix

    omni_vars = load(trange=trange, level=level, datatype=datatype)

    bz_name = tnames("BZ_GSM")
    p_name = tnames("Pressure")
    if bz_name is None or p_name is None or len(bz_name) < 1 or len(p_name) < 1:
        logging.warning("OMNI Solar Wind data not found. Loading default values.")
        defd = get_omni_default_solarwind(trange)
        tout = defd[0]
        dpout = defd[1]
        bzout = defd[2]
        store_data(new_p, data={"x": tout, "y": dpout})
        store_data(new_bz, data={"x": tout, "y": bzout})
    else:
        tcopy_one(bz_name[0], new_bz)
        tcopy_one(p_name[0], new_p)

    degap(new_bz)
    degap(new_p)
    tdeflag([new_bz, new_p], method="remove_nan", overwrite=True)

    if interpolto is not None and len(tnames(interpolto)) > 0:
        tinterpol(new_bz, interpolto, newname=new_bz)
        tinterpol(new_p, interpolto, newname=new_p)

    time_clip([new_bz, new_p], trange[0], trange[1], overwrite=True)

    return [new_bz, new_p]

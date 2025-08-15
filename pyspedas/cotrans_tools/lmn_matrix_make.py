import logging
import numpy as np
from pyspedas.cotrans_tools.gsm2lmn import gsm2lmn
from .rotmat_set_coords import rotmat_set_coords
from pyspedas.tplot_tools import get_data, store_data, set_coords, tnames, options, time_clip
from pyspedas import tinterpol
from pyspedas.projects.omni.omni_solarwind_load import omni_solarwind_load


def lmn_matrix_make(
    pos_var_name,
    mag_var_name,
    trange=None,
    hro2=False,
    newname=None,
):
    """
    Generate an LMN (boundary-normal) coordinate transformation matrix from the given magnetic field B and position data,
    and store it in a tplot variable using the GSM to LMN transformation.

    Parameters
    ----------
    pos_var_name : str
        Name of tplot variable containing the spacecraft position data in GSM coordinates.
    mag_var_name : str
        Name of tplot variable containing the magnetic field data in GSM coordinates.
    trange : list, optional
        Time range to use for interpolation.
        If None, the time range will be set from the mag_var_name tplot variable.
    hro2 : bool, optional
        Flag indicating whether to use the HRO2 level of OMNI data.
        If False, the HRO level will be used.
        Default is False.
     newname : str, optional
        Name of the output tplot variable. Defaults to mag_var_name + "_lmn_mat".

    Returns
    -------
    str or None
        The name of the output tplot variable containing the LMN matrix,
        or None if an error occurs.
    """

    # Check if the variables exist in tplot
    if not tnames(pos_var_name):
        logging.error(f"lmn_matrix_make requires pos_var_name to be set")
        return None
    if not tnames(mag_var_name):
        logging.error(f"lmn_matrix_make requires mag_var_name to be set")
        return None
    
    # Set OMNI level (hro or hro2)
    if hro2:
        level = "hro2"
    else:
        level = "hro"

    # Set the name of the output variable
    if newname is None:
        newname = mag_var_name + "_lmn_mat"

    # Set trange if not provided
    if trange is None or len(trange) != 2:
        mag_var_name_data = get_data(mag_var_name)
        if mag_var_name_data is None:
            logging.error(f"Error reading tplot variable: {mag_var_name}")
            return None
        trange = [mag_var_name_data.times[0], mag_var_name_data.times[-1]]

    # Get solarwind data
    swind = omni_solarwind_load(trange=trange, level=level, min5=False)

    if swind is not None and len(swind) == 2:
        # Interpolate solar wind data to match themagnetic field data
        bz_name = swind[0] + "_interpol"
        p_name = swind[1] + "_interpol"
        tinterpol(swind[0], mag_var_name, newname=bz_name, extrapolate=True)
        tinterpol(swind[1], mag_var_name, newname=p_name, extrapolate=True)

        bz_data = get_data(bz_name)
        p_data = get_data(p_name)
        if bz_data is None or p_data is None:
            logging.error(f"Error reading tplot variables: {bz_name}, {p_name}")
            return None
        timesw = bz_data.times
        dpnon = p_data.y
        bnon = bz_data.y
        swdata = np.array([timesw, dpnon, bnon]).T
    else:
        logging.warning("OMNI Solar Wind data could not be loaded. Exiting.")
        return None

    # Get position and magnetic field data
    pos_var_name_interpol = pos_var_name + "_interpol"
    tinterpol(pos_var_name, mag_var_name, newname=pos_var_name_interpol, extrapolate=True)
    pos_data = get_data(pos_var_name_interpol)
    mag_data = get_data(mag_var_name)
    if pos_data is None or mag_data is None:
        logging.error(f"Error reading tplot variables: {pos_var_name_interpol}, {mag_var_name}")
        return None
    times = mag_data.times
    rxyz = pos_data.y
    bxyz = mag_data.y

    # Perform the GSM to LMN transformation
    try:
        blmn = gsm2lmn(times, rxyz, bxyz, swdata=swdata)
    except Exception as e:
        logging.error(f"Error during GSM to LMN transformation: {e}")
        return None

    # Store the LMN transformation matrix in a new tplot variable
    store_data(newname, data={"x": times, "y": blmn})
    rotmat_set_coords(newname, "GSM", "LMN")
    options(newname, "ysubtitle", "[LMN]")
    options(newname, "legend_names", ["BL", "BM", "BN"])

    time_clip(newname, trange[0], trange[1], overwrite=True)

    return newname

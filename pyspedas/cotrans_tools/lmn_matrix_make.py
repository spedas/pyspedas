import logging
import numpy as np
from .gsm2lmn import gsm2lmn
from pytplot import get_data, store_data, set_coords

def lmn_matrix_make(mag_var_name, pos_var_name, swdata=None, swdata_var_name=None, newname=None):
    """
    Generate an LMN (boundary-normal) coordinate transformation matrix from the given magnetic field B and position data, 
    and store it in a tplot variable using the GSM to LMN transformation.

    Parameters
    ----------
    mag_var_name : str
        Name of tplot variable containing the magnetic field data in GSM coordinates.
    pos_var_name : str
        Name of tplot variable containing the spacecraft position data in GSM coordinates.
    swdata : np.ndarray, optional
        Predefined solar wind data array (times, dynamic pressure, Bz). If provided, this will be used instead of swdata_var_name.
    swdata_var_name : str, optional
        Name of tplot variable containing solar wind data (times, dynamic pressure, Bz).
    newname : str, optional
        Name of the output tplot variable. Defaults to mag_var_name + "_lmn_mat".

    Returns
    -------
    str or None
        The name of the output tplot variable containing the LMN matrix,
        or None if an error occurs.
    """
    # Get magnetic field data
    mag_data = get_data(mag_var_name)
    if mag_data is None:
        logging.error(f"Error reading tplot variable: {mag_var_name}")
        return None

    # Get position data
    pos_data = get_data(pos_var_name)
    if pos_data is None:
        logging.error(f"Error reading tplot variable: {pos_var_name}")
        return None

    # Get name for the output variable
    if newname is None:
        newname = mag_var_name + "_lmn_mat"

    # Extract times, positions, and magnetic field vectors
    times = mag_data.times
    Bxyz = mag_data.y
    Rxyz = pos_data.y

    # Use provided swdata if available, otherwise retrieve from swdata_var_name
    if swdata is None and swdata_var_name is not None:
        swdata_data = get_data(swdata_var_name)
        if swdata_data is None:
            logging.warning(f"Solar wind data variable {swdata_var_name} not found. Using default values.")
        else:
            swdata = np.column_stack((swdata_data.times, swdata_data.y))

    # Perform the GSM to LMN transformation
    try:
        blmn = gsm2lmn(times, Rxyz, Bxyz, swdata=swdata)
    except Exception as e:
        logging.error(f"Error during GSM to LMN transformation: {e}")
        return None

    # Store the LMN transformation matrix in a new tplot variable
    store_data(newname, data={'x': times, 'y': blmn})
    set_coords(newname, 'LMN')

    return newname
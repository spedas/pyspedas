import logging
import numpy as np
from .gsm2lmn import gsm2lmn
from pytplot import get_data, store_data, set_coords, tnames, options
from pyspedas import tinterpol
from pyspedas.projects.omni.solarwind_load import solarwind_load

def lmn_matrix_make(pos_var_name, mag_var_name, swdata=None, swdata_var_name=None, loadsolarwind=True, swlevel='hro2', interpol_to_pos=False, newname=None):
    """
    Generate an LMN (boundary-normal) coordinate transformation matrix from the given magnetic field B and position data, 
    and store it in a tplot variable using the GSM to LMN transformation.

    Parameters
    ----------   
    pos_var_name : str
        Name of tplot variable containing the spacecraft position data in GSM coordinates.
    mag_var_name : str
        Name of tplot variable containing the magnetic field data in GSM coordinates.
    swdata : np.ndarray, optional
        Predefined solar wind data array (times, dynamic pressure, Bz). If provided, this will be used instead of swdata_var_name.
    swdata_var_name : str, optional
        Name of tplot variable containing solar wind data (times, dynamic pressure, Bz).
    loadsolarwind : bool, optional
        Flag indicating whether to load solar wind data from OMNI. 
        Default is True. If true then swdata and swdata_var_name are ignored.
    swlevel : str, optional
        Solar wind OMNI data level; valid options: 'hro', 'hro2'. 
        Default is 'hro2'.
    interpol_to_pos : bool, optional
        Flag indicating whether to interpolate the magnetic field data to the spacecraft position data.
        The default is False, which means the position data will be interpolated to the magnetic field data.
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
    
    # Get name for the output variable
    if newname is None:
        newname = mag_var_name + "_lmn_mat"

    interpol_var = mag_var_name
    if interpol_to_pos:
        # Interpolate to position
        interpol_name = pos_var_name
        mag_temp = mag_var_name + '_temp'
        tinterpol(mag_var_name, interpol_name, newname=mag_temp)

        mag_data = get_data(mag_temp)
        if mag_data is None:
            logging.error(f"Error reading tplot variable: {mag_temp}")
            return None
        pos_data = get_data(pos_var_name)        
        if pos_data is None:
            logging.error(f"Error reading tplot variable: {pos_var_name}")
            return None
        
        times = pos_data.times
        Rxyz = pos_data.y
        Bxyz = mag_data.y
    else:
        # Interpolate to magnetic field
        interpol_name = mag_var_name
        pos_temp = pos_var_name + '_temp'
        tinterpol(pos_var_name, interpol_name, newname=pos_temp)

        pos_data = get_data(pos_temp)
        if pos_data is None:
            logging.error(f"Error reading tplot variable: {pos_temp}")
            return None
        mag_data = get_data(mag_var_name)        
        if mag_data is None:
            logging.error(f"Error reading tplot variable: {mag_var_name}")
            return None
        
        times = mag_data.times
        Rxyz = pos_data.y
        Bxyz = mag_data.y

  
    if loadsolarwind:
        # If loadsolarwind is True, then load solar wind data
        swdata = solarwind_load([times[0], times[-1]], level=swlevel, min5=False)
    elif swdata is not None:
        # If swdata is provided, use it
        pass
    elif swdata_var_name is not None:
        # If swdata_var_name is provided, load it
        swdata_data = get_data(swdata_var_name)
        if swdata_data is None:
            logging.warning(f"Solar wind data variable {swdata_var_name} not found. Using default values.")
        else:
            swdata = np.column_stack((swdata_data.times, swdata_data.y))
    else:
        # If neither swdata nor swdata_var_name is provided, use default values  
        swdata = None
        logging.warning("No solar wind data provided. Using default values.")

    # Perform the GSM to LMN transformation
    try:
        blmn = gsm2lmn(times, Rxyz, Bxyz, swdata=swdata)
    except Exception as e:
        logging.error(f"Error during GSM to LMN transformation: {e}")
        return None

    # Store the LMN transformation matrix in a new tplot variable
    store_data(newname, data={'x': times, 'y': blmn})
    set_coords(newname, 'LMN')
    options(newname, 'ysubtitle', '[LMN]')
    options(newname, 'legend_names', ['BL', 'BM', 'BN'])

    return newname


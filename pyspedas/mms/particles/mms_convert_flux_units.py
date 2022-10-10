import logging
import numpy as np

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_convert_flux_units(data_in, units=None):
    """
    Perform unit conversions for MMS particle data structures
    
    Input
    ----------
        data_in: dict
            Single particle data structure

    Parameters
    ----------
        units: str
            String specifying output units
            supported units:
                flux   -   # / (cm^2 * s * sr * eV)
                eflux  -  eV / (cm^2 * s * sr * eV)
                df_cm  -  s^3 / cm^6
                df_km     -  s^3 / km^6

    Returns
    ----------
        3D particle data structure with the data in the units specified by
        the 'units' parameter
    """

    if units is None:
        logging.error('Error, no units specified')
        return None

    units_out = units.lower()
    species_lc = data_in['species'].lower()
    units_in = data_in['units_name'].lower()

    if units_in == units_out:
        return data_in

    data_out = data_in.copy()

    # handle synonymous notations
    if units_in == 'psd':
        units_in = 'df_km'
    if units_out == 'psd':
        units_out = 'df_km'

    # get mass of species
    if species_lc == 'i':
        A = 1.0  # H+
    elif species_lc == 'proton':
        A = 1.0  # H+
    elif species_lc == 'hplus':
        A = 1.0  # H+
    elif species_lc == 'heplus':
        A = 4.0  # He+
    elif species_lc == 'heplusplus':
        A = 4.0  # He++
    elif species_lc == 'oplus':
        A = 16.0  # O+
    elif species_lc == 'oplusplus':
        A = 16.0  # O++
    elif species_lc == 'e':
        A = 1.0/1836.0  # e-

    # scaling factor between df and flux units
    flux_to_df = A**2.0 * 0.5447 * 1e6

    # convert between km^6 and cm^6 for df_km
    cm_to_km = 1e30

    # calculation will be kept simple and stable as possible by 
    # pre-determining the final exponent of each scaling factor 
    # rather than multiplying by all applicable in/out factors
    # these exponents should always be integers!
    #    [energy, flux_to_df, cm_to_km]
    exp_in = [0, 0, 0]
    exp_out = [0, 0, 0]

    # get input/output scaling exponents
    if units_in == 'flux':
        exp_in = [1, 0, 0]
    elif units_in == 'df_km':
        exp_in = [2, -1, 0]
    elif units_in == 'df_cm':
        exp_in = [2, -1, 1]

    if units_out == 'flux':
        exp_out = [-1, 0, 0]
    elif units_out == 'df_km':
        exp_out = [-2, 1, 0]
    elif units_out == 'df_cm':
        exp_out = [-2, 1, 1]

    exp = np.array(exp_in) + np.array(exp_out)

    data_out['units_name'] = units_out
    data_out['data'] = data_in['data']*data_in['energy']**exp[0]*(flux_to_df**exp[1]*cm_to_km**exp[2])

    return data_out

import logging

import numpy as np

from copy import deepcopy

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def erg_convert_flux_units(input_dist, units='flux', relativistic=False):
    """
    ; The following unit names are acceptable for units:
    ;   'flux' 'eflux' 'df' 'df_cm'
    ;
    ;   'df_km' and 'psd' are referred to as 'df'.
    ;
    ; CAUTION!!!
    ; "relativistic" keyword is valid only for electron currently.
    ; Using it for ions just messes up the conversion.
    """

    output_dist = deepcopy(input_dist)

    units_out = units.lower()
    species_lc = input_dist['species'].lower()
    units_in = input_dist['units_name'].lower()

    if units_in == units_out:
        return input_dist

    # Unify some unit notations

    if (units_in == 'df_km') or (units_in == 'psd'):
        units_in = 'df'
    if (units_out == 'df_km') or (units_out == 'psd'):
        units_out = 'df'

    # Get the mass of species (unit: proton mass)
    if species_lc == 'e':
        A = 1.0/1836.0  # e-
    elif species_lc == 'hplus':
        A = 1.0  # H+
    elif species_lc == 'proton':
        A = 1.0  # H+
    elif species_lc == 'he2plus':
        A = 4.0  # He2+
    elif species_lc == 'alpha':
        A = 4.0  # He2+
    elif species_lc == 'heplus':
        A = 4.0  # He+
    elif species_lc == 'oplusplus':
        A = 16.0  # O++
    elif species_lc == 'oplus':
        A = 16.0  # O+
    elif species_lc == 'o2plus':
        A = 32.0  # (O2)+

    """
    ;; Scaling factor between df (s^3/km^6) and flux (#/eV/s/str/cm2).
    ;; Note that the notation is in such a way that the conversion is
    ;; done below as:
    ;; f [s3/km6] = j [#/eV/s/str/cm2] / K [eV] * flux_to_df
    ;;                                 for non-relativistic cases
    ;;
    ;; f [(c/MeV/cm)^3] = j [#/eV/s/str/cm2] * flux_to_df / K [eV]
    ;;                 for relativisitc electron cases with keyword relativistic on
    ;; 
    ;; !!CAUTION!! MEPs data should be converted to (#/eV/s/str/cm2) 
    ;; when one uses the mep_part_products libraries.
    ;;
    ;; !!CAUTION2!!
    ;; Keyword "relativistic" is valid for only electrons.
    ;; DO NOT USE it for ions. 
    """

    flux_to_df = A**2.0 * 0.5447 * 1e6

    if relativistic:
        # Conversion here is based on those adopted by Hilmer+JGR,2000.

        mc2 = 5.10999e-1  # Electron rest energy [MeV]
        ene = deepcopy(input_dist['energy'])  # [eV]
        MeV_ene = ene * 1e-6  # [MeV]
        p2c2 = MeV_ene * (MeV_ene + 2.0 * mc2)  # [MeV^2]

        """
        ;; f [(c/MeV/cm)^3]
        ;;     = j [#/eV/s/str/cm2] * 1d+3 / p2c2 * 1.66d-10 * 200.3 
        ;; 1d+3 is to convert input flux values to [#/keV/s/sr/cm2]. 
        ;; The multiplication of energy [eV] is to be consistent
        ;; with the conversion below. 
        """
        flux_to_df = 1.0e+3 / p2c2 * 1.66e-10 * 200.3 * ene

    # factor between km^6 and cm^6 for df
    cm_to_km = 1e+30

    """
    ;; Calculation will be kept simple and stable as possible by 
    ;; pre-determining the final exponent of each scaling factor 
    ;; rather than multiplying by all applicable in/out factors
    ;; these exponents should always be integers!
    ;;    [energy, flux_to_df, cm_to_km]
    """
    exp_in = [0, 0, 0]
    exp_out = [0, 0, 0]

    """
    ;; get input/output scaling exponents  
    ;; All conversions are done via energy flux (eflux).
    """

    if units_in == 'flux':
        exp_in = [1, 0, 0]
    elif units_in == 'df':
        exp_in = [2, -1, 0]
    elif units_in == 'df_cm':
        exp_in = [2, -1, 1]

    if units_out == 'flux':
        exp_out = [-1, 0, 0]
    elif units_out == 'df':
        exp_out = [-2, 1, 0]
    elif units_out == 'df_cm':
        exp_out = [-2, 1, -1]

    exp = np.array(exp_in) + np.array(exp_out)

    """
    ;; Ensure everything is double prec first for numerical stability
    ;;  -target field won't be mutated since it's part of a structure
    """

    output_dist['data'] = input_dist['data'] * input_dist['energy']**exp[0] * \
        (flux_to_df ** exp[1] * cm_to_km ** exp[2])

    output_dist['units_name'] = units_out

    return output_dist

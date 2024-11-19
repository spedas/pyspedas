import logging
from pytplot import get_data, store_data, tplot_copy
import numpy as np
from pytplot import data_exists


def apply_oneaxis_correction(rawvar: str,
                             deltavar: str,
                             corrvar: str):
    """
    This function applies spin axis corrections for a single spin axis quantity (RA or DEC).

    Parameters:
        rawvar: str
            Name of tplot variable holding the uncorrected quantity of interest.

        deltavar: str
            Name of tplot variable holding the corrections for the quantity of interest

        corrvar: str
            Name of tplot variable to receive the corrected quantity
    """

    if (data_exists(rawvar)) and (data_exists(deltavar)):
        logging.debug("Applying spin axis corrections")
        res1 = get_data(rawvar)
        raw_times = res1.times
        raw_data = res1.y
        metadata = get_data(rawvar, metadata=True)

        res2 = get_data(deltavar)
        corr_times = res2.times
        corr_data = res2.y

        # Interpolate corrections using input_times

        # In IDL, there was a special case, if the correction had only a single quantity, because the
        # interpol routine would crash with only a single value given. np.interp does the right thing
        # by default.

        interp_correction = np.interp(raw_times, corr_times, corr_data)

        # Apply corrections
        fix_raw = raw_data - interp_correction

        # Make output tplot variable
        store_data(corrvar, data={'x': raw_times, 'y': fix_raw}, attr_dict=metadata)
    elif not (data_exists(deltavar)):
        # If the corrections aren't present, just copy the original data
        logging.info('Spin axis corrections variable ' + deltavar + ' not found, copying ' + rawvar + ' to ' + corrvar)
        tplot_copy(rawvar,corrvar)
    else:
        # Raw variable doesn't exist, nothing to do here.
        logging.info('Spin axis variable ' + rawvar + ' not found, skipping ' + corrvar)


def apply_spinaxis_corrections(spinras: str,
                               spindec: str,
                               delta_spinras: str,
                               delta_spindec: str,
                               corrected_spinras: str,
                               corrected_spindec: str):
    """
    This function applies V03 state spin axis corrections (if present) to state spinras and spindec
    quantities, creating new tplot variables.

    Parameters:
        spinras: str
            Name of tplot variable holding the uncorrected spin axis right ascension.

        spindec: str
            Name of tplot variable holding the uncorrected spin axis declination.

        delta_spinras: str
            Name of tplot variable holding the correction to the spin axis right ascension.

        delta_spindec: str
            Name of tplot variable holding the corrections to the spin axis declination.

        corrected_spinras: str
            Name of tplot variable to receive the corrected spin axis right ascension.

        corrected_spindec: str
            Name of tplot variable to receive the corrected spin axis declination.
    """
    apply_oneaxis_correction(rawvar=spinras, deltavar=delta_spinras, corrvar=corrected_spinras)
    apply_oneaxis_correction(rawvar=spindec, deltavar=delta_spindec, corrvar=corrected_spindec)

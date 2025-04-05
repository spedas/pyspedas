import logging
import numpy as np
def xdegap(var):
    """
    Replace NaN values in an array.

    Parameters
    ----------
    var : numpy.ndarray
        Input array that may contain NaN values.

    Returns
    -------
    numpy.ndarray
        Array with NaN values replaced by the average of surrounding non-NaN values.

    """
    if np.all(np.isnan(var)):
        logging.info("All values are NaN. No replacement performed.")
        return var

    # Iterate through the array and replace NaN values
    for i in range(len(var)):
        if np.isnan(var[i]):
            # Find the first non-NaN value before the current index
            before = np.where(~np.isnan(var[:i]))[0]
            # Find the first non-NaN value after the current index
            after = np.where(~np.isnan(var[i+1:]))[0]

            if len(before) > 0 and len(after) > 0:
                # Both before and after values exist
                before_value = var[before[-1]]
                after_value = var[i + 1 + after[0]]
                var[i] = (before_value + after_value) / 2.0
            elif len(before) > 0:
                # Only before value exists
                var[i] = var[before[-1]]
            elif len(after) > 0:
                # Only after value exists
                var[i] = var[i + 1 + after[0]]

    return var

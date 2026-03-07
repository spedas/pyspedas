import numpy as np
import numbers
import logging
from pyspedas.tplot_tools import get_data, time_string, data_exists, tdeflag
from pyspedas.analysis.tinterpol import tinterpol

def clean_model_parameters(input_times, model_param, method="linear") -> np.ndarray:
    """
    Create a 1D array of model parameter values from a scalar, array, or tplot variable name.

    Parameters
    ----------
    input_times: ndarray of floats
       The timestamp array of the input tplot variable.  Model parameters will be interpolated to these
       times.
    model_param: Any
        A scalar floating point value, array of values, or tplot variable name.  Scalars are repeated
        to match the number of input timestamps.  Arrays are taken as-is, after checking that the array size
        matches the number of timestamps. tplot variables are interpolated to input_times after removing NaN values.
    method: str
        The interpolation method to use.  Kp and iopt values are not from a continuous scale, so they should be
        interpolated with method="nearest". Default: "linear"

    Returns
    -------
    ndarray of floats
        An array of cleaned parameter values, with the same number of elements as the input times.

    """

    ntimes = len(input_times)
    output_array = np.zeros(ntimes)

    if isinstance(model_param, np.ndarray):
        # Check that array is 1-d, matches input times, and contains non-nan numeric values
        if len(model_param.shape)  != 1:
            txt = f'Model parameter array must have 1 dimension, but received {model_param.shape}'
            logging.error(txt)
            raise ValueError(txt)
        if len(model_param) != ntimes:
            txt = f'Array size mismatch: {ntimes} input times, {len(model_param)} parameter values'
            logging.error(txt)
            raise ValueError(txt)
        if not isinstance(model_param[0], numbers.Number):
            txt='Parameter values must be numeric'
            logging.error(txt)
            raise ValueError(txt)
        if np.isnan(model_param).any():
            txt='Model parameter array cannot contain NaN values'
            logging.error(txt)
            raise ValueError(txt)
        output_array[:] = model_param

    elif isinstance(model_param, list):
        # Convert to numpy array, check for array size and non-nan
        inp = np.array(model_param)
        if len(inp.shape)  != 1:
            txt=f'Model parameter array must have 1 dimension, but received {inp.shape}'
            logging.error(txt)
            raise ValueError(txt)

        if len(inp) != ntimes:
            txt=f'Array size mismatch: {ntimes} input times, {len(inp)} parameter values'
            logging.error(txt)
            raise ValueError(txt)
        if not isinstance(inp[0], numbers.Number):
            txt='Parameter values must be numeric'
            logging.error(txt)
            raise ValueError(txt)
        if np.isnan(inp).any():
            txt='Model parameter array cannot contain NaN values'
            logging.error(txt)
            raise ValueError(txt)
        output_array[:] = inp

    elif isinstance(model_param, (float, int, np.int64, np.integer, np.float64, np.float16, np.float32)):
        if np.isfinite(model_param):
            output_array[:] = model_param
        else:
            txt='Scalar model values must be non-NaN'
            logging.error(txt)
            raise ValueError(txt)

    elif isinstance(model_param, str):
        if not data_exists(model_param):
            txt=f'tplot variable {model_param} does not exist'
            logging.error(txt)
            raise ValueError(txt)

        inp_data = get_data(model_param)
        # Check that variable times overlap input times
        if inp_data.times[0] > input_times[0]:
            txt=f'Parameter start time {time_string(inp_data.times[0])} is after input start time {time_string(input_times[0])} (no extrapolation allowed)'
            logging.error(txt)
            raise ValueError(txt)
        elif inp_data.times[-1] < input_times[-1]:
            txt=f'Parameter end time {time_string(inp_data.times[-1])} is before input end time {time_string(input_times[-1])} (no extrapolation allowed)'
            logging.error(txt)
            raise ValueError(txt)
        # remove nans
        clean_name = model_param + '_deflag'
        tdeflag(model_param, method='remove_nan', newname=clean_name)
        # interpolate to input times
        interp_name = model_param + '_itrp'
        tinterpol(clean_name, input_times, method=method, newname=interp_name)
        cleaned_interp_data = get_data(interp_name)
        output_array[:] = cleaned_interp_data.y
    else:
        txt='Invalid model parameter type: must be tplot variable name or numeric scalar or array'
        logging.error(txt)
        raise ValueError(txt)

    return output_array

def clean_parmod_data(input_times, parmod_var, method="linear") -> np.ndarray:
    """
    Create a 2D n-by-10 array of model parameter values from a parmod tplot variable.

    Parameters
    ----------
    input_times: ndarray of floats
       The timestamp array of the input tplot variable.  Model parameters will be interpolated to these
       times.
    parmod_var: str
        A tplot variable name containing 10-element arrays at each sample time
    method: str
        The interpolation method to use.  Kp and iopt values are not from a continuous scale, so they should be
        interpolated with method="nearest". Default: "linear"

    Returns
    -------
    ndarray of floats
        An n-by-10 array of cleaned parameter values, with n equal to the number of input times

    """

    ntimes = len(input_times)

    if not isinstance(parmod_var, str) or not data_exists(parmod_var):
        txt=f"Parmod tplot variable {parmod_var} does not exist."
        logging.error(txt)
        raise ValueError(txt)
    inp_data = get_data(parmod_var)
    if inp_data.y.shape[1] != 10:
        txt=f"Parmod variable {parmod_var} has {inp_data.y.shape[1]} samples per timestamp, but expected 10-element array"
        logging.error(txt)
        raise ValueError(txt)
    # Check that variable times overlap input times
    if inp_data.times[0] > input_times[0]:
        txt=f'Parmod start time {time_string(inp_data.times[0])} is after input start time {time_string(input_times[0])} (no extrapolation allowed)'
        logging.error(txt)
        raise ValueError(txt)
    elif inp_data.times[-1] < input_times[-1]:
        txt=f'Parmod end time {time_string(inp_data.times[-1])} is before input end time {time_string(input_times[-1])} (no extrapolation allowed)'
        logging.error(txt)
        raise ValueError(txt)
    # remove nans
    clean_name = parmod_var + '_cleaned'
    tdeflag(parmod_var, method='remove_nan', newname=clean_name)
    # interpolate to input times
    interp_name = parmod_var + '_itrp'
    tinterpol(clean_name, input_times, method=method, newname=interp_name)
    cleaned_interp_data = get_data(interp_name)
    return cleaned_interp_data.y
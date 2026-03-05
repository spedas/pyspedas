import numpy as np
import numbers
import logging
from pyspedas.tplot_tools import interp_nan, get_data, time_string, data_exists
from pyspedas.utilities.interpol import interpol

def clean_model_parameters(input_times, model_param) -> np.ndarray:
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
            raise ValueError(f'Model parameter array must have 1 dimension, but received {model_param.shape}')
        if len(model_param) != ntimes:
            raise ValueError(f'Array size mismatch: {ntimes} input times, {len(model_param)} parameter values')
        if not isinstance(model_param[0], numbers.Number):
            raise ValueError('Parameter values must be numeric')
        if np.isnan(model_param).any():
            raise ValueError('Model parameter array cannot contain NaN values')
        output_array[:] = model_param

    elif isinstance(model_param, list):
        # Convert to numpy array, check for array size and non-nan
        inp = np.array(model_param)
        if len(inp.shape)  != 1:
            raise ValueError(f'Model parameter array must have 1 dimension, but received {inp.shape}')
        if len(inp) != ntimes:
            raise ValueError(f'Array size mismatch: {ntimes} input times, {len(inp)} parameter values')
        if not isinstance(inp[0], numbers.Number):
            raise ValueError('Parameter values must be numeric')
        if np.isnan(inp).any():
            raise ValueError('Model parameter array cannot contain NaN values')
        output_array[:] = inp

    elif isinstance(model_param, (float, int, np.int64, np.integer, np.float64, np.float16, np.float32)):
        if np.isfinite(model_param):
            output_array[:] = model_param
        else:
            raise ValueError('Scalar model values must be non-NaN')

    elif isinstance(model_param, str):
        if not data_exists(model_param):
            raise ValueError(f'tplot variable {model_param} does not exist')

        inp_data = get_data(model_param)
        # Check that variable times overlap input times
        if inp_data.times[0] > input_times[0]:
            raise ValueError(f'Parameter start time {time_string(inp_data.times[0])} is after input start time {time_string(input_times[0])} (no extrapolation allowed)')
        elif inp_data.times[-1] < input_times[-1]:
            raise ValueError(f'Parameter end time {time_string(inp_data.times[-1])} is before input end time {time_string(input_times[-1])} (no extrapolation allowed)')
        # remove nans
        clean_name = model_param + '_cleaned'
        interp_nan(model_param,newname=clean_name)
        cleaned_data = get_data(clean_name)
        clean_interpolated = interpol(cleaned_data.y, cleaned_data.times, input_times)
        output_array[:] = clean_interpolated
    else:
        raise ValueError('Invalid model parameter type: must be tplot variable name or numeric scalar or array')

    return output_array

def clean_parmod_data(input_times, parmod_var) -> np.ndarray:
    """
    Create a 2D n-by-10 array of model parameter values from a parmod tplot variable.

    Parameters
    ----------
    input_times: ndarray of floats
       The timestamp array of the input tplot variable.  Model parameters will be interpolated to these
       times.
    parmod_var: str
        A tplot variable name containing 10-element arrays at each sample time

    Returns
    -------
    ndarray of floats
        An n-by-10 array of cleaned parameter values, with n equal to the number of input times

    """

    ntimes = len(input_times)

    if not isinstance(parmod_var, str) or not data_exists(parmod_var):
        logging.error(f"Parmod tplot variable {parmod_var} does not exist.")
        raise ValueError(f'tplot variable {parmod_var} does not exist')

    inp_data = get_data(parmod_var)
    if inp_data.y.shape[1] != 10:
        logging.error(f"Parmod variable {parmod_var} has {inp_data.y.shape[1]} samples per timestamp, but expected 10-element array")
        raise ValueError("bad parmod variable")
    # Check that variable times overlap input times
    if inp_data.times[0] > input_times[0]:
        logging.error(f'Parmod start time {time_string(inp_data.times[0])} is after input start time {time_string(input_times[0])} (no extrapolation allowed)')
        raise ValueError(f'Parmod start time {time_string(inp_data.times[0])} is after input start time {time_string(input_times[0])} (no extrapolation allowed)')
    elif inp_data.times[-1] < input_times[-1]:
        logging.error(f'Parmod end time {time_string(inp_data.times[-1])} is before input end time {time_string(input_times[-1])} (no extrapolation allowed)')
        raise ValueError(f'Parmod end time {time_string(inp_data.times[-1])} is before input end time {time_string(input_times[-1])} (no extrapolation allowed)')
    # remove nans
    clean_name = parmod_var + '_cleaned'
    interp_nan(parmod_var,newname=clean_name)
    cleaned_data = get_data(clean_name)
    clean_interpolated = interpol(cleaned_data.y, cleaned_data.times, input_times)

    return clean_interpolated
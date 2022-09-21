import logging
import warnings
from copy import deepcopy
import numpy as np


def slice2d_collate(data, weight, sphere, previous_out=None, sum_samples=False):
    """
    Collate data aggregated as slice2d_get_data loops over input
    Data aggregation continues until a change in energy or angle
    bins occurs (mode change or other) or aggregation completes.
    At those points this procedure is called to average the data,
    concatenate data to output variables, and clear the appropriate
    variables for the next loop.
    """
    if sum_samples:
        data_out = data
    else:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=RuntimeWarning)
            data_out = data/weight

    data_out = data_out.flatten(order='F')
    weight = weight.flatten(order='F')
    rad_in = sphere['rad'].flatten(order='F')
    phi_in = sphere['phi'].flatten(order='F')
    theta_in = sphere['theta'].flatten(order='F')
    dr_in = sphere['dr'].flatten(order='F')
    dp_in = sphere['dp'].flatten(order='F')
    dt_in = sphere['dt'].flatten(order='F')

    # remove bins with no valid data
    valid = np.argwhere(weight > 0).flatten()

    if len(valid) > 0:
        data_out = data_out[valid]
        rad_in = rad_in[valid]
        phi_in = phi_in[valid]
        theta_in = theta_in[valid]
        dr_in = dr_in[valid]
        dp_in = dp_in[valid]
        dt_in = dt_in[valid]
    else:
        logging.error('No valid data in distribution(s).')
        return

    if previous_out is None:
        rad_out = deepcopy(rad_in)
        phi_out = deepcopy(phi_in)
        theta_out = deepcopy(theta_in)
        dr_out = deepcopy(dr_in)
        dp_out = deepcopy(dp_in)
        dt_out = deepcopy(dt_in)
    else:
        data_out = np.concatenate((previous_out['data'], data_out))
        rad_out = np.concatenate((previous_out['rad'], rad_in))
        phi_out = np.concatenate((previous_out['phi'], phi_in))
        theta_out = np.concatenate((previous_out['theta'], theta_in))
        dr_out = np.concatenate((previous_out['dr'], dr_in))
        dp_out = np.concatenate((previous_out['dp'], dp_in))
        dt_out = np.concatenate((previous_out['dt'], dt_in))

    return {
            'data': data_out,
            'rad': rad_out,
            'phi': phi_out,
            'theta': theta_out,
            'dr': dr_out,
            'dp': dp_out,
            'dt': dt_out
        }

import logging
import re
import pyspedas as ps #! for testing
import numpy as np
from pyspedas import get_data, time_double #! is pytplot later

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def cluster_get_hia_dist(tname, probe=None):
    """
    Returns 3D particle data structures containing Cluster HIA
    data for use with SPEDAS particle routines. 
    
    Input
    ----------
        tname: str
            tplot variable name containing the HIA distribution data
            Example: 
            It should have the format [time, psd, theta, phi, energy]

    Parameters
    ----------
        probe: str
            Spacecraft probe #

    Returns
    ----------
    list of dict
        3D particle data structure(s) containing Cluster HIA distribution functions
    """
    data = get_data(tname)

    if data is None:
        logging.error('Problem extracting the HIA distribution data.')
        return
    
    if any(data[i].ndim == 2 for i in (2, 3, 4)):
        raise ValueError(
            "data[2], data[3], and data[4] must all be 1-D arrays"
        )
    species = 'Ions'
    mass = 1.04535e-2 
    charge = 1.0

    out = {'project_name': 'Cluster',
            'spacecraft': probe, 
            'species': species,
            'data_name': 'HIA ' + species,
            'charge': charge,
            'units_name': 'df_m', # because we are transforming data to s3/m6
            'mass': mass}

    # --- Now we need to reformat the data
    # we shuffle the output to be [time, energy, phi, theta] 
    # (data[1] is currently [time, theta, phi, energy])
    out_data = data[1].transpose([0, 3, 2, 1]) * 1.0E-18 # convert from s^3 km^-6 to s^3 m^-6
    out_bins = np.zeros(out_data.shape) + 1
    out_dphi = np.zeros(out_data.shape) + 22.5   # 16 pixels in 360 degree window
    out_dtheta = np.zeros(out_data.shape) + 22.5 # 8 pixels in 180 degree window
    out_denergy = np.zeros(out_data.shape) 

    # theta
    # elevations are constant across time
    # convert colat -> lat
    theta_reform = np.asarray(data[2])                 # shape: (theta,)
    theta_reform = theta_reform[None, None, :]         # shape: (1, 1, theta)
    theta_rebinned = np.broadcast_to(
        theta_reform,
        (len(data[4]), len(data[3]), theta_reform.shape[2])
    )                                                  # shape: (energy, phi, theta) 
    out_theta = np.broadcast_to(
        theta_rebinned,
        (len(data[0]),) + theta_rebinned.shape
    )                                                  # shape: (time, energy, phi, theta) 

    # energy
    energy_len = len(data[4])
    energy_reform = np.asarray(data[4])[:, None, None] # shape: (energy, 1, 1)
    energy_table = np.broadcast_to(
        energy_reform,
        (len(data[4]), len(data[3]), len(data[2]))
    )                                                  # shape: (energy, phi, theta)
    out_energy = np.broadcast_to(
        energy_table,
        (len(data[0]),) + energy_table.shape
    )                                                  # shape: (time, energy, phi, theta)

    # phi
    phi_reform = np.asarray(data[3])[None, :, None]   # shape: (1, phi, 1)
    phi_rebinned = np.broadcast_to(
        phi_reform,
        (len(data[4]), len(data[3]), len(data[2])) 
    )                                          # shape: (energy, phi, theta)
    out_phi = np.broadcast_to(
        phi_rebinned,
        (len(data[0]),) + phi_rebinned.shape
    )                                             # shape: (time, energy, phi, theta)

    out_list = []
    for time_idx, time in enumerate(data[0]):
        out_table = {**out}
        out_table['data'] = out_data[time_idx, :]
        out_table['bins'] = out_bins[time_idx, :]
        out_table['theta'] = out_theta[time_idx, :]
        out_table['phi'] = out_phi[time_idx, :]
        out_table['energy'] = out_energy[time_idx, :]
        out_table['dtheta'] = out_dtheta[time_idx, :]
        out_table['dphi'] = out_dphi[time_idx, :]
        out_table['denergy'] = out_denergy[time_idx, :]
        out_table['n_energy'] = energy_len
        out_table['n_theta'] = len(data[3])
        out_table['n_phi'] = len(data[2])
        out_table['start_time'] = time # note: assumes the data weren't centered
        out_table['end_time'] = time + 4 #! one spin = 4 seconds, verify!
        out_list.append(out_table)

    return out_list
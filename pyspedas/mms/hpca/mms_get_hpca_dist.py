import logging
import numpy as np
from pytplot import get_data

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_get_hpca_dist(tname, index=None, probe=None, data_rate=None, species=None, times=False):
    """
    Returns 3D particle data structures containing MMS HPCA
    data for use with SPEDAS particle routines. 
    
    Input
    ----------
        tname: str
            tplot variable name containing the HPCA distribution data

    Parameters
    ----------
        probe: str
            Spacecraft probe #

        data_rate: str
            Instrument data rates for HPCA include 'brst' and 'srvy'

        species: str
            Species of the data specified by the 'tname' input

        index: int
            Index of time sample to return

        times: bool
            Flag to return the distribution times instead of the particle data structure(s)

    Returns
    ------------
        3D particle data structure(s) containing MMS HPCA distribution functions
    """
    data_in = get_data(tname)

    # Match particle data to azimuth data
    # ------------------------

    # get azimuths and full dist sample times from ancillary variable
    azimuth = get_data('mms' + probe + '_hpca_azimuth_angles_per_ev_degrees')

    if azimuth is None:
        logging.error('No azimuth data found for the current time range')
        return

    # check if the time series is monotonic to avoid doing incorrect 
    # calculations when there's a problem with the CDF files
    time_data = azimuth.times

    wherenonmono = np.where(time_data[1:] <= time_data[:-1])
    if len(wherenonmono[0]) != 0:
        logging.error('Error, non-monotonic data found in the HPCA Epoch_Angles time series data')
        return

    # find azimuth times with complete 1/2 spins of particle data
    # this is used to determine the number of 3D distributions that will be created
    # and where their corresponding data is located in the particle data structure
    n_times = len(azimuth.y[0, 0, :])
    data_idx = np.searchsorted(data_in.times, time_data)-1
    full = np.argwhere((data_idx[1:]-data_idx[:-1]) == n_times)
    if len(full) == 0:
        logging.error('Azimuth data does not cover current data\'s time range')
        return

    # filter times when azimuth data is all zero
    #   -just check the first energy & elevation
    #   -assume azimuth values are positive
    n_valid_az = np.count_nonzero(azimuth.y[full, 0, 0, :])
    if n_valid_az != azimuth.y[full, 0, 0, :].size:
        logging.error('Error, zeroes found in the azimuth array')
        return
        # should check to see if all azimuths are 0 (and if not, use the valid ones)

    if index is not None:
        if index >= full.size:
            logging.error('Error, index greater than data size')
            return
        full = full[index]

    full = full.squeeze()

    data_idx = data_idx[full].flatten()

    if times:
        return time_data[full]

    # Initialize energies, angles, and support data
    # ------------------------
    
    # final dimensions for a single distribution (energy-azimuth-elevation)
    azimuth_dim = azimuth.y.shape
    dim = (azimuth_dim[3], azimuth_dim[2], azimuth_dim[1])

    if species == 'hplus':
        mass = 1.04535e-2
        charge = 1.0
    elif species == 'heplus':
        mass = 4.18138e-2
        charge = 1.0
    elif species == 'heplusplus':
        mass = 4.18138e-2
        charge = 2.0
    elif species == 'oplus':
        mass = 0.167255
        charge = 1.0
    elif species == 'oplusplus':
        mass = 0.167255
        charge = 2.0
    else:
        logging.error('Cannot determine species')
        return

    out = {'project_name': 'MMS',
           'spacecraft': probe, 
           'species': species,
           'data_name': 'HPCA ' + species,
           'charge': charge,
           'units_name': 'df_cm',
           'mass': mass}

    out_bins = np.zeros(dim) + 1
    out_denergy = np.zeros(dim)

    # energy bins are constant
    energy_reform = np.reshape(data_in.v2, [len(data_in.v2), 1, 1])
    energy_rebin1 = np.repeat(energy_reform, dim[1], axis=2) # repeated across theta
    out_energy = np.repeat(energy_rebin1, dim[2], axis=1)
    energy_len = len(data_in.v2)

    # elevations are constant across time
    # convert colat -> lat
    theta_reform = 90. - np.reshape(data_in.v1, [1, 1, len(data_in.v1)])

    # in the IDL code, we use reform to repeat the vector above
    # here, we'll do the same thing with np.repeat
    theta_rebin1 = np.repeat(theta_reform, azimuth_dim[1], axis=1) # repeated across phi
    out_theta = np.repeat(theta_rebin1, data_in[1].shape[2], axis=0) # repeated across energy
    theta_len = len(data_in.v1)
    out_dtheta = np.zeros([energy_len, theta_len, azimuth_dim[2]]) + 22.5

    # get start/end times
    # - this assumes that the times from the particle (and angle) data
    #   are at the center of the corresponding energy sweep
    # - also assumes that there are no gaps in the data
    dt = time_data[1:]-time_data[0:-1]
    dt_sweep = data_in.times[1:]-data_in.times[0:-1]
    start_times = time_data[full]-dt_sweep[data_idx]
    end_times = start_times + dt[full]

    # get azimuth 
    #  -shift from time-azimuth-elevation-energy to time-energy-azimuth-elevation
    out_phi = azimuth.y[full, :, :, :]

    if len(out_phi.shape) == 4:
        out_phi = out_phi.transpose([0, 3, 1, 2])
    elif len(out_phi.shape) == 3:
        out_phi = out_phi.transpose([2, 0, 1])
    
    phi_len = azimuth_dim[1]

    # get dphi
    #  -use median distance between subsequent phi measurements within each distribution
    #   (median is used to discard large differences across 0=360)
    #  -preserve dimensionality in case differences arise across energy or elevation
    
    if len(out_phi.shape) == 4:
        out_dphi = np.median(azimuth.y[full, 1:, :, :] - azimuth.y[full, :-1, :, :], axis=1)
        out_dphi = out_dphi.transpose([0, 2, 1])
    elif len(out_phi.shape) == 3:
        out_dphi = np.median(azimuth.y[full, 1:, :, :] - azimuth.y[full, :-1, :, :], axis=0)
        out_dphi = out_dphi.transpose([1, 0])

    if len(out_phi.shape) == 4:
        dphi_reform = np.reshape(out_dphi, [full.size, energy_len, theta_len, 1])
        out_dphi = np.repeat(dphi_reform, phi_len, axis=3)
    elif len(out_phi.shape) == 3:
        dphi_reform = np.reshape(out_dphi, [energy_len, theta_len, 1])
        out_dphi = np.repeat(dphi_reform, phi_len, axis=2)

    out_data = np.zeros((full.size, dim[0], dim[1], dim[2]))

    # copy particle data
    for i in range(full.size):
        # need to extract the data from the center of the half-spin
        if data_idx[i]-n_times/2.0 < 0:
            start_idx = 0
        else:
            start_idx = int(data_idx[i]-n_times/2.)

        if data_idx[i]+n_times/2.-1 >= len(data_in.times):
            end_idx = len(data_in.times)
        else:
            end_idx = int(data_idx[i]+n_times/2.)

        try:
            out_data[i, :, :, :] = data_in.y[start_idx:end_idx, :, :].transpose([2, 0, 1])
        except ValueError:
            out_data[i, :, :, :] = np.nan

    out_list = []

    for time_idx, time in enumerate(start_times):
        out_table = {**out}
        out_table['data'] = out_data[time_idx, :, :, :]
        out_table['bins'] = out_bins
        out_table['theta'] = out_theta
        if len(out_phi.shape) == 4:
            out_table['phi'] = out_phi[time_idx, :, :, :]
        else:
            out_table['phi'] = out_phi
        out_table['energy'] = out_energy
        out_table['dtheta'] = out_dtheta
        if len(out_phi.shape) == 4:
            out_table['dphi'] = out_dphi[time_idx, :, :, :]
        else:
            out_table['dphi'] = out_dphi
        out_table['denergy'] = out_denergy
        out_table['n_energy'] = energy_len
        out_table['n_theta'] = len(data_in[2])
        out_table['n_phi'] = phi_len
        out_table['start_time'] = time
        out_table['end_time'] = end_times[time_idx]
        out_list.append(out_table)

    return out_list

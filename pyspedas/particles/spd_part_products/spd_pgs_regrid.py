
import numpy as np
from scipy.interpolate import griddata

def spd_pgs_regrid(data, regrid_dimen):
    """

    """
    if len(regrid_dimen) != 2:
        print('Invalid regrid dimensions; the dimensions should be [n_phi, n_theta]')
        return

    n_energy = len(data['energy'][:, 0])

    n_phi_grid = int(regrid_dimen[0])
    n_theta_grid = int(regrid_dimen[1])
    n_bins_grid = n_phi_grid*n_theta_grid

    d_phi_grid = 360.0/n_phi_grid
    d_theta_grid = 180.0/n_theta_grid

    phi_angles = (np.arange(n_bins_grid) % n_phi_grid)*d_phi_grid+d_phi_grid/2.0
    phi_grid = np.repeat(np.reshape(phi_angles, [n_bins_grid, 1]), n_energy, axis=1).T

    theta_angles = np.fix(np.arange(n_bins_grid)/n_phi_grid)*d_theta_grid+d_theta_grid/2.0 - 90
    theta_grid = np.repeat(np.reshape(theta_angles, [n_bins_grid, 1]), n_energy, axis=1).T

    d_phi_grid = np.zeros([n_energy, n_bins_grid]) + d_phi_grid
    d_theta_grid = np.zeros([n_energy, n_bins_grid]) + d_phi_grid

    data_grid = np.zeros([n_energy, n_bins_grid])
    bins_grid = np.zeros([n_energy, n_bins_grid])

    output = {'data': data_grid,
              'scaling': data_grid,
              'phi': phi_grid,
              'dphi': d_phi_grid,
              'theta': theta_grid,
              'dtheta': d_theta_grid,
              'energy': data_grid,
              'denergy': data_grid,
              'bins': bins_grid}

    # assumes energies are constant across angle
    output['energy'] = np.repeat(np.reshape(data['energy'][:, 0], [n_energy, 1]), n_bins_grid, axis=1).T
    output['denergy'] = np.repeat(np.reshape(data['denergy'][:, 0], [n_energy, 1]), n_bins_grid, axis=1).T

    for i in range(0, n_energy):
        phi_temp = data['phi'][i, :]
        theta_temp = data['theta'][i, :]
        data_temp = data['data'][i, :]
        bins_temp = data['bins'][i, :]

        points = np.stack((phi_temp, theta_temp)).T
        xi = np.stack((phi_grid[i, :], theta_grid[i, :])).T

        output['data'][i, :] = griddata(points, data_temp, xi, method='nearest')
        output['bins'][i, :] = griddata(points, bins_temp, xi, method='nearest')

    return output
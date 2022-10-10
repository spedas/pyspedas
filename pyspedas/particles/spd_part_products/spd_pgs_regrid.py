import logging
import numpy as np
from scipy.interpolate import NearestNDInterpolator
from astropy.coordinates import spherical_to_cartesian


def spd_pgs_regrid(data, regrid_dimen):
    """

    """
    if len(regrid_dimen) != 2:
        logging.error('Invalid regrid dimensions; the dimensions should be [n_phi, n_theta]')
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

        r_grid = np.ones(len(phi_grid[i, :]))

        data_grid_interp = griddata(phi_temp, theta_temp, data_temp)
        bins_grid_interp = griddata(phi_temp, theta_temp, bins_temp)

        grid_x, grid_y, grid_z = spherical_to_cartesian(r_grid, theta_grid[i, :]*np.pi/180.0, phi_grid[i, :]*np.pi/180.0)

        for j in range(0, len(phi_grid[i, :])):
            output['data'][i, j] = data_grid_interp(grid_x[j], grid_y[j], grid_z[j])
            output['bins'][i, j] = bins_grid_interp(grid_x[j], grid_y[j], grid_z[j])

    return output


def griddata(phi, theta, data):
    r = np.ones(len(phi))
    phi_rad = phi*np.pi/180.0
    theta_rad = theta*np.pi/180.0
    cart_temp = spherical_to_cartesian(r, theta_rad, phi_rad)

    points = np.stack(cart_temp).T
    return NearestNDInterpolator(points, data)

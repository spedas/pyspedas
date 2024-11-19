
import numpy as np


def mvn_kp_sc_traj_xyz(
    dims_x, dims_y, dims_z, values, x_array, y_array, z_array, nn="linear"
):
    """
    Interpolates the values of a 3D array at given coordinates using trilinear interpolation.

    Parameters:
        dims_x (array-like): The x-coordinates of the grid points.
        dims_y (array-like): The y-coordinates of the grid points.
        dims_z (array-like): The z-coordinates of the grid points.
        values (ndarray): The 3D array of values to be interpolated.
        x_array (array-like): The x-coordinates of the points to interpolate.
        y_array (array-like): The y-coordinates of the points to interpolate.
        z_array (array-like): The z-coordinates of the points to interpolate.
        nn (str, optional): The type of nearest neighbor interpolation to use.
            Defaults to "linear".

    Returns:
        list: The interpolated values at the given coordinates.
    """

    data = []
    if nn == "nearest":
        for x, y, z in np.array([a for a in zip(x_array, y_array, z_array)]):
            ix = np.abs(dims_x - x).argmin()
            iy = np.abs(dims_y - y).argmin()
            iz = np.abs(dims_z - z).argmin()
            data.append(values[ix, iy, iz])
    else:
        max_x = np.max(x_array)
        min_x = np.min(x_array)
        max_y = np.max(y_array)
        min_y = np.min(y_array)
        max_z = np.max(z_array)
        min_z = np.min(z_array)

        for x, y, z in np.array([a for a in zip(x_array, y_array, z_array)]):
            if x > max_x:
                data.append(np.nan)
            elif x < min_x:
                data.append(np.nan)
            elif y > max_y:
                data.append(np.nan)
            elif y < min_y:
                data.append(np.nan)
            elif z > max_z:
                data.append(np.nan)
            elif z < min_z:
                data.append(np.nan)

            sorted_x_distance = np.argsort(np.abs(dims_x - x))
            ix1 = dims_x[sorted_x_distance[0]]
            ix2 = dims_x[sorted_x_distance[1]]
            if ix2 < ix1:
                temp = ix2
                ix2 = ix1
                ix1 = temp
            sorted_y_distance = np.argsort(np.abs(dims_y - y))
            iy1 = dims_y[sorted_y_distance[0]]
            iy2 = dims_y[sorted_y_distance[1]]
            if iy2 < iy1:
                temp = iy2
                iy2 = iy1
                iy1 = temp
            sorted_z_distance = np.argsort(np.abs(dims_z - z))
            iz1 = dims_z[sorted_z_distance[0]]
            iz2 = dims_z[sorted_z_distance[1]]
            if iz2 < iz1:
                temp = iz2
                iz2 = iz1
                iz1 = temp

            nx = (x - ix1) / (ix2 - ix1)
            ny = (y - iy1) / (iy2 - iy1)
            nz = (z - iz1) / (iz2 - iz1)

            data.append(
                values[sorted_x_distance[0], sorted_y_distance[0], sorted_z_distance[0]]
                * (1 - nx)
                * (1 - ny)
                * (1 - nz)
                + values[
                    sorted_x_distance[1], sorted_y_distance[0], sorted_z_distance[0]
                ]
                * nx
                * (1 - ny)
                * (1 - nz)
                + values[
                    sorted_x_distance[0], sorted_y_distance[1], sorted_z_distance[0]
                ]
                * (1 - nx)
                * ny
                * (1 - nz)
                + values[
                    sorted_x_distance[0], sorted_y_distance[0], sorted_z_distance[1]
                ]
                * (1 - nx)
                * (1 - ny)
                * nz
                + values[
                    sorted_x_distance[1], sorted_y_distance[0], sorted_z_distance[1]
                ]
                * nx
                * (1 - ny)
                * nz
                + values[
                    sorted_x_distance[0], sorted_y_distance[1], sorted_z_distance[1]
                ]
                * (1 - nx)
                * ny
                * nz
                + values[
                    sorted_x_distance[1], sorted_y_distance[1], sorted_z_distance[0]
                ]
                * nx
                * ny
                * (1 - nz)
                + values[
                    sorted_x_distance[1], sorted_y_distance[1], sorted_z_distance[1]
                ]
                * nx
                * ny
                * nz
            )
    return data

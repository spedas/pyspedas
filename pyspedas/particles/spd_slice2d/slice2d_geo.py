import logging
from copy import deepcopy
from time import time
import numpy as np
from pyspedas.particles.spd_slice2d.quaternions import qtom, qcompose


def slice2d_geo(data, resolution, r, phi, theta, dr, dp, dt, orient_matrix=None, rotation_matrix=None,
                custom_matrix=None, msg_prefix='', shift=None, average_angle=None, sum_angle=None):
    """
    Produces slices showing each bin's boundaries by assigning
    each bin's value to all points on the slice plane that
    fall within that bin's boundaries.
    """
    n = float(resolution)
    n_int = int(n)
    rd = 180/np.pi
    tolerance = 5e-7 # to account for rounding errors
    # for progress messages
    previous_time = time()

    vrange = [-np.max(np.abs(r)), np.max(np.abs(r))]
    dr_range = [-np.max(dr), np.max(np.abs(dr))]
    xgrid = np.linspace(vrange[0]+dr_range[0], vrange[1]+dr_range[1], n_int)
    ygrid = np.linspace(vrange[0]+dr_range[0], vrange[1]+dr_range[1], n_int)
    z = 0

    uvals = np.zeros((n_int**2, 3))
    xvals = np.outer(xgrid, np.ones(n_int)).flatten(order='F')
    yvals = np.outer(np.ones(n_int), ygrid).flatten(order='F')
    zvals = np.zeros(n_int**2)
    uvals[:, 0] = xvals
    uvals[:, 1] = yvals
    uvals[:, 2] = zvals

    m = deepcopy(orient_matrix)
    # rotate slice coordinates to desired location
    if custom_matrix is not None:
        if rotation_matrix is not None:
            m = (custom_matrix @ rotation_matrix) @ m
        else:
            m = custom_matrix @ m
    else:
        if rotation_matrix is not None:
            m = rotation_matrix @ m
    uvals = uvals @ m.T

    if average_angle is not None or sum_angle is not None:
        if sum_angle is not None:
            alpha = [np.min(sum_angle), np.max(sum_angle)]
        if average_angle is not None:
            alpha = [np.min(average_angle), np.max(average_angle)]

        # number of additional slices to average/sum over
        na = 2 * np.sqrt(n) * (alpha[1] - alpha[0]) / 90.0
        if na < 2:
            na = 2

        na = int(np.floor(na))

        # copy slice's x-vector
        xv = np.outer(m[:, 0], np.ones(na)).T

        # interpolate across the angle range
        a_range = (np.append(np.arange(0, na-1, dtype=np.float64)/(na-1), 1) * (alpha[1]-alpha[0])) + alpha[0]

        # construct quaternion array to get rotation matrices
        qs = qcompose(xv, a_range/rd, free=True)  # quaternions to rotate about x by a
        ms = qtom(qs)  # get matrices
    else:
        na = 0

    num_points = len(data)
    out = np.zeros(n_int**2)
    weight = np.zeros(n_int**2)

    # loop over slice plans (if averaging over angle)
    for j in range(-1, na):
        if j >= 0:
            ut = np.matmul(ms[j, :, :], deepcopy(uvals).T).T
        else:
            ut = deepcopy(uvals)

        # Convert transformed slice coordinates to spherical
        pcoords = rd*np.arctan2(ut[:, 1], ut[:, 0])  # phi
        tcoords = rd*np.arctan2(ut[:, 2], np.sqrt(ut[:, 0]**2 + ut[:, 1]**2))  # theta
        rcoords = np.sqrt(ut[:, 0]**2 + ut[:, 1]**2 + ut[:, 2]**2)  # r

        # Loop over bins to determine what region each bin covers on the slice plane
        for i in range(0, num_points):
            if data[i] == 0:
                continue

            # theta
            tlim = np.array([theta[i]-0.5*dt[i], theta[i]+0.5*dt[i]])

            # account for rounding errors
            # this is particularly important is slice plane is at zero elevation
            tr = np.argwhere(np.abs(tlim - np.round(tlim)) < tolerance).flatten()
            if len(tr) > 0:
               tlim[tr] = np.round(tlim[tr])

            thetas =(tcoords > tlim[0]) & (tcoords <= tlim[1])

            if len(thetas) == 0:
                continue

            if np.sum(thetas) < 1:
                continue
            
            # phi
            plim = np.array([phi[i]-0.5*dp[i], phi[i]+0.5*dp[i]])

            # keep limits within [-180, 180]
            over = np.argwhere(plim > 180).flatten()
            under = np.argwhere(plim < -180).flatten()
            if len(over) > 0:
                plim[over] += -360.0
            if len(under) > 0:
                plim[under] += 360.0
            
            # account for rounding errors
            pr = np.argwhere(np.abs(plim - np.round(plim)) < tolerance).flatten()
            if len(pr) > 0:
               plim[pr] = np.round(plim[pr])
            
            # determine which region ( p0->p1 or p1->p0) the bin spans
            if plim[0] > plim[1]:
                phis = (pcoords > plim[0]) | (pcoords <= plim[1])
            else:
                phis = (pcoords > plim[0]) & (pcoords <= plim[1])
            
            if len(phis) == 0:
                continue

            if np.sum(phis) < 1:
                continue

            # R (velocity/energy)
            rdata = (rcoords >= r[i]-0.5*dr[i]) & (rcoords < r[i]+0.5*dr[i])

            bidx = np.argwhere(phis & thetas & rdata).flatten()

            if len(bidx) > 1:
                weight[bidx] = weight[bidx] + 1
                out[bidx] = out[bidx] + data[i]

            # output progress messages every 6 seconds
            if (time() - previous_time) > 6:
                if na == 0:
                    num_angles = 1
                else:
                    num_angles = na
                msg = msg_prefix + str(int(100*((j+1)*num_points + i)/(num_angles*num_points))) + '% complete'
                logging.info(msg)
                previous_time = time()

    # average areas where bins overlapped
    adj = np.argwhere(weight == 0)
    if len(adj) > 0:
        weight[adj] = 1

    if sum_angle is None:
        out = out / weight

    out = out.reshape((n_int, n_int), order='F')

    if shift is not None:
        xgrid -= shift[0]
        ygrid -= shift[1]

    return {'data': out, 'xgrid': xgrid, 'ygrid': ygrid}

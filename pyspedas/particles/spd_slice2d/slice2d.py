import numpy as np

from .slice2d_intrange import slice2d_intrange
from .slice2d_get_data import slice2d_get_data
from .slice2d_geo import slice2d_geo
from .slice2d_get_support import slice2d_get_support
from .slice2d_orientslice import slice2d_orientslice
from .slice2d_rotate import slice2d_rotate
from .slice2d_nearest import slice2d_nearest

from pyspedas import time_double, time_string


def slice2d(dists,
            time=None,
            samples=None,
            window=None,
            center_time=False,
            trange=None,
            resolution=500,
            rotation='xy',
            subtract_bulk=False,
            energy=False,
            log=False,
            mag_data=None,
            vel_data=None,
            sun_data=None,
            slice_x=None,
            slice_z=None):
    """

    """

    if trange is None:
        if time is None:
            print('Please specify a time or time range over which to compute the slice.')
            return
        if window is None and samples is None:
            # use single closest distribution by default
            samples = 1

    valid_rotations = ['bv', 'be', 'xy', 'xz', 'yz', 'xvel', 'perp', 'perp2',
                       'perp_xy', 'perp_xz', 'perp_yz', 'b_exb', 'perp1-perp2']

    if rotation not in valid_rotations:
        print('Invalid rotation requested; valid options: ' + ', '.join(valid_rotations))
        return

    if time is not None:
        time = time_double(time)

    # always use log scale when energy is requested instead of velocity
    if energy and not log:
        log = True

    # get the time range if a time & window were specified instead
    if trange is None and window is not None:
        if center_time:
            trange = [time - window/2.0, time + window/2.0]
        else:
            trange = [time, time + window]

    # if no trange or window was specified, then get a time range
    # from the N closest samples to the specified time
    # (defaults to 1 if samples is not defined)
    if trange is None:
        trange = slice2d_nearest(dists, time, samples)

    tr = time_double(trange)

    msg_prefix = 'Processing slice at ' + time_string(tr[0], fmt='%Y-%m-%d %H:%M:%S.%f') + '... '

    # check that there is data in range before proceeding
    times_ind = slice2d_intrange(dists, tr)

    data = slice2d_get_data(dists, trange=tr)

    # get original data and radial ranges for plotting
    #   - ignore outliers that may be the result of sanitizations performed outside this routine
    #   - this also effectively removes low-significance outliers at large velocities, which
    #     can lead to overly large velocity scales for some instruments
    idx = np.argwhere(data['data'] > 0.0)
    if len(idx) > 0:
        dmean = np.mean(np.log10(data['data'][idx]))
        dvar = np.var(np.log10(data['data'][idx]))
        dmin = 10**(dmean - 2*np.sqrt(dvar))
        drange = [dmin, np.nanmax(data['data'][idx])]
    else:
        drange = [0.0, 0.0]

    rrange = [np.nanmin(data['rad'] - 0.5*data['dr']), np.nanmax(data['rad'] + 0.5*data['dr'])]

    # get support data for aligning slice
    bfield = slice2d_get_support(mag_data, trange)
    vbulk = slice2d_get_support(vel_data, trange)
    sunvec = slice2d_get_support(sun_data, trange)
    slice_x_vec = slice2d_get_support(slice_x, trange)
    slice_z_vec = slice2d_get_support(slice_z, trange)

    orientation = slice2d_orientslice(vectors=None, # for interpolation
                                      vbulk=vbulk,
                                      bfield=bfield,
                                      sunvec=sunvec,
                                      slice_x=slice_x_vec,
                                      slice_z=slice_z_vec)

    rot_matrix = slice2d_rotate(rotation=rotation,
                                vectors=None,
                                bfield=bfield,
                                vbulk=vbulk,
                                sunvec=sunvec)

    geo_shift = [0, 0, 0]
    if subtract_bulk:
        geo_shift = vbulk

    geo = slice2d_geo(data['data'], resolution, data['rad'], data['phi'], data['theta'], data['dr'], data['dp'],
                      data['dt'], orient_matrix=orientation['matrix'], rotation_matrix=rot_matrix['matrix'],
                      msg_prefix=msg_prefix, shift=geo_shift)

    if energy:
        xyunits = 'eV'
    else:
        xyunits = 'km/s'

    out = {'project_name': dists[0]['project_name'],
           'spacecraft': dists[0]['spacecraft'],
           'data_name': dists[0]['data_name'],
           'units_name': dists[0]['units_name'],
           'species': dists[0]['species'],
           'xyunits': xyunits,
           'rotation': rotation,
           'energy': energy,
           'trange': trange,
           'zrange': drange,
           'rrange': rrange,
           'n_samples': len(times_ind),
           **geo}

    return out

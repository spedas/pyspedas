import numpy as np

from .slice2d_intrange import slice2d_intrange
from .slice2d_get_data import slice2d_get_data
from .slice2d_geo import slice2d_geo
from .slice2d_get_support import slice2d_get_support
from .slice2d_orientslice import slice2d_orientslice
from .slice2d_rotate import slice2d_rotate
from .slice2d_custom_rotation import slice2d_custom_rotation
from .slice2d_nearest import slice2d_nearest
from .slice2d_rlog import slice2d_rlog
from .slice2d_s2c import slice2d_s2c
from .slice2d_2di import slice2d_2di
from .slice2d_smooth import slice2d_smooth

from pyspedas import time_double, time_string


def slice2d(dists,
            time=None,
            samples=None,
            window=None,
            center_time=False,
            interpolation='geometric',
            trange=None,
            resolution=None,
            rotation='xy',
            custom_rotation=None,
            subtract_bulk=False,
            energy=False,
            log=False,
            erange=None,
            smooth=None,
            thetarange=None,
            zdirrange=None,
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

    if interpolation == '2d':
        if smooth is None:
            smooth = 7
        if resolution is None:
            resolution = 150
        if thetarange is None and zdirrange is None:
            thetarange = [-20, 20]
    elif interpolation == 'geometric':
        if resolution is None:
            resolution = 500

    if time is not None:
        time = time_double(time)

    # always use log scale when energy is requested instead of velocity
    if energy and not log:
        log = True

    # Get the slice's time range
    # ------------------------------------------------------------------------
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

    # Extract particle data
    #   - apply energy limits
    #   - average data over the time window
    #   - output r, phi, theta and dr, dphi and dtheta arrays
    # ------------------------------------------------------------------------
    data = slice2d_get_data(dists, trange=tr, erange=erange)

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

    # apply radial log scaling
    if log:
        scaled_r = slice2d_rlog(data['rad'], data['dr'])
        # replace original vars
        data['rad'] = scaled_r['r']
        data['dr'] = scaled_r['dr']

    # convert spherical data to cartesian coordinates for interpolation
    xyz = None
    if interpolation != 'geometric':
        xyz = slice2d_s2c(data['rad'], data['theta'], data['phi'])

    # Get/apply coordinate transformations
    #  - for 2D/3D interpolation, the data is transformed here
    #  - for geometric interpolation, the data is transformed in slice2d_geo
    #  - support data is always rotated at each step
    # ------------------------------------------------------------------------
    # get support data for aligning slice
    bfield = slice2d_get_support(mag_data, trange)
    vbulk = slice2d_get_support(vel_data, trange)
    sunvec = slice2d_get_support(sun_data, trange)
    slice_x_vec = slice2d_get_support(slice_x, trange)
    slice_z_vec = slice2d_get_support(slice_z, trange)

    # custom rotation
    custom_rot = slice2d_custom_rotation(custom_rotation=custom_rotation,
                                         trange=trange,
                                         vectors=xyz,
                                         bfield=bfield,
                                         vbulk=vbulk,
                                         sunvec=sunvec)

    # for 2D/3D interpolation
    orientation = slice2d_orientslice(vectors=custom_rot['vectors'],
                                      vbulk=custom_rot['vbulk'],
                                      bfield=custom_rot['bfield'],
                                      sunvec=custom_rot['sunvec'],
                                      slice_x=slice_x_vec,
                                      slice_z=slice_z_vec)

    # built-in rotation option
    rot_matrix = slice2d_rotate(rotation=rotation,
                                vectors=orientation['vectors'],
                                bfield=orientation['bfield'],
                                vbulk=orientation['vbulk'],
                                sunvec=orientation['sunvec'])

    # problem rotating data
    if rot_matrix is None:
        return

    geo_shift = [0, 0, 0]
    if subtract_bulk:
        geo_shift = vbulk

    # sort transformed vector grid
    if xyz is not None:
        sorted_idxs = np.argsort(rot_matrix['vectors'][:, 0], kind='stable')
        rot_matrix['vectors'] = rot_matrix['vectors'][sorted_idxs, :]
        data['data'] = data['data'][sorted_idxs]

    # Create the slice
    # ------------------------------------------------------------------------
    if interpolation == 'geometric':
        the_slice = slice2d_geo(data['data'], resolution, data['rad'], data['phi'], data['theta'], data['dr'], data['dp'],
                          data['dt'], orient_matrix=orientation['matrix'], rotation_matrix=rot_matrix['matrix'],
                          custom_matrix=custom_rot['matrix'], msg_prefix=msg_prefix, shift=geo_shift)
    elif interpolation == '2d':
        the_slice = slice2d_2di(data['data'], rot_matrix['vectors'], resolution, thetarange=thetarange, zdirrange=zdirrange)

    if smooth is not None:
        the_slice = slice2d_smooth(the_slice, smooth)

    # Get metadata and return slice
    # ------------------------------------------------------------------------
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
           'rlog': log,
           'n_samples': len(times_ind),
           **the_slice}

    print('Finished slice at ' + time_string(tr[0], fmt='%Y-%m-%d %H:%M:%S.%f'))
    return out

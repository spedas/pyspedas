import logging
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
from .slice2d_subtract import slice2d_subtract

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
            average_angle=None,
            sum_angle=None,
            mag_data=None,
            vel_data=None,
            sun_data=None,
            slice_x=None,
            slice_z=None):
    """
    Returns an interpolated 2D slice of 3D particle data for plotting

    Interpolation methods:

    2D Interpolation:
        Data points within the specified theta or z-axis range are projected onto
        the slice plane and linearly interpolated onto a regular 2D grid.

    Geometric:
        Each point on the plot is given the value of the bin it intersects.
        This allows bin boundaries to be drawn at high resolutions.

    Input
    ---------------------
        dists: list of dicts
            List of 3D particle data structures

    Basic Keywords
    ---------------------
        trange: list of str or list of float
            Two-element time range over which data will be averaged (optional)

        time: str
            Time at which the slice will be computed (optional)

        samples: int
            Numer of samples nearest to TIME to average (default 1)

        window: int or float
            Length in seconds from TIME over which data will be averaged.

        center_time: bool
            Flag denoting that TIME should be midpoint for window instead of beginning.

        interpolation: str
            Interpolation method to use; options: 'geometric' for geometric interpolation
            and '2d' for 2D interpolation (described above)

    Orientation Keywords
    ---------------------
        custom_rotation: str or np.ndarray
            Applies a custom rotation matrix to the data.  Input may be a
            3x3 rotation matrix or a tplot variable containing matrices.
            If the time window covers multiple matrices they will be averaged.

        rotation: str
            Aligns the data relative to the magnetic field and/or bulk velocity.
            This is applied after the CUSTOM_ROTATION. (BV and BE are invariant
            between coordinate systems)

            Use MAG_DATA keyword to specify magnetic field vector.
            Use VEL_DATA keyword to specify bulk velocity (optional).

            'BV':  The x-axis is parallel to B field; the bulk velocity defines the x-y plane
            'BE':  The x-axis is parallel to B field; the B x V(bulk) vector defines the x-y plane
            'xy':  (default) The x-axis is along the data's x-axis and y is along the data's y axis
            'xz':  The x-axis is along the data's x-axis and y is along the data's z axis
            'yz':  The x-axis is along the data's y-axis and y is along the data's z axis
            'xvel':  The x-axis is along the data's x-axis; the x-y plane is defined by the bulk velocity
            'perp':  The x-axis is the bulk velocity projected onto the plane normal to the B field; y is B x V(bulk)
            'perp_xy':  The data's x & y axes are projected onto the plane normal to the B field
            'perp_xz':  The data's x & z axes are projected onto the plane normal to the B field
            'perp_yz':  The data's y & z axes are projected onto the plane normal to the B field

        mag_data: str
            Name of tplot variable containing magnetic field data or 3-vector.
            This will be used for slice plane alignment and must be in the
            same coordinates as the particle data.

        vel_data: str
            Name of tplot variable containing the bulk velocity data or 3-vector.
            This will be used for slice plane alignment and must be in the
            same coordinates as the particle data.
            If not set the bulk velocity will be automatically calculated
            from the distribution (when needed).

    Other Keywords
    ---------------------
        resolution: int
            Integer specifying the resolution along each dimension of the
            slice (defaults:  2D interpolation: 150, geometric: 500)

        smooth: int
            An odd integer >=3 specifying the width of a smoothing window in #
            of points.  Smoothing is applied to the final plot using a gaussian
            convolution. Even entries will be incremented, 0 and 1 are ignored.

        energy: bool
            Flag to plot data against energy (in eV) instead of velocity.

        log: bool
            Flag to apply logarithmic scaling to the radial measure (i.e. energy/velocity).
            (on by default if energy=True)

        erange: list of float
            Two element list specifying the energy range to be used in eV

        thetarange: list of float
            (2D interpolation only): angle range, in degrees (-90, +90), used to calculate the slice
            default = [-20, 20]; will override zdirrange

        zdirrange: list of float
            (2D interpolation only): Z-Axis range, in km/s, used to calculate slice.
            Ignored if called with THETARANGE.

        subtract_bulk: bool
            Flag to subtract the bulk velocity vector

    Returns
    ---------------------
        Dictionary containing 2D slice of 3D particle data
    """

    if trange is None:
        if time is None:
            logging.error('Please specify a time or time range over which to compute the slice.')
            return
        if window is None and samples is None:
            # use single closest distribution by default
            samples = 1

    valid_rotations = ['bv', 'be', 'xy', 'xz', 'yz', 'xvel', 'perp', 'perp2',
                       'perp_xy', 'perp_xz', 'perp_yz', 'b_exb', 'perp1-perp2']

    if rotation not in valid_rotations:
        logging.error('Invalid rotation requested; valid options: ' + ', '.join(valid_rotations))
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
    else:
        logging.error('Unknown interpolation method: ' + interpolation + '; valid options: "geometric", "2d"')
        return

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
        vectors = slice2d_subtract(rot_matrix['vectors'], vbulk)

        if vectors is not None:
            rot_matrix['vectors'] = vectors

        # the shift is applied later for geometric interpolation
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
                                custom_matrix=custom_rot['matrix'], msg_prefix=msg_prefix, shift=geo_shift,
                                average_angle=average_angle, sum_angle=sum_angle)
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
           'interpolation': interpolation,
           'n_samples': len(times_ind),
           **the_slice}

    logging.info('Finished slice at ' + time_string(tr[0], fmt='%Y-%m-%d %H:%M:%S.%f'))
    return out

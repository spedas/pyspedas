from .slice2d_intrange import slice2d_intrange
from .slice2d_get_data import slice2d_get_data
from .slice2d_geo import slice2d_geo
from .slice2d_get_support import slice2d_get_support
from .slice2d_orientslice import slice2d_orientslice
from .slice2d_rotate import slice2d_rotate

from pyspedas import time_double, time_string


def slice2d(dists,
            trange=None,
            resolution=500,
            rotation='xy',
            energy=False,
            mag_data=None,
            vel_data=None,
            sun_data=None,
            slice_x=None,
            slice_z=None):
    """

    """

    if trange is None:
        print('trange keyword required')
        return

    tr = time_double(trange)

    msg_prefix = 'Processing slice at ' + time_string(tr[0], fmt='%Y/%m/%d %H:%M:%S.%f') + '... '

    # check that there is data in range before proceeding
    times_ind = slice2d_intrange(dists, tr)

    data = slice2d_get_data(dists, trange=tr)

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

    geo = slice2d_geo(data['data'], resolution, data['rad'], data['phi'], data['theta'], data['dr'], data['dp'],
                      data['dt'], orient_matrix=orientation['matrix'], rotation_matrix=rot_matrix['matrix'],
                      msg_prefix=msg_prefix)

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
           'n_samples': len(times_ind),
           **geo}

    return out

import numpy as np
import matplotlib.pyplot as plt
from .slice2d_getinfo import slice2d_getinfo
from pyspedas.particles.spd_units_string import spd_units_string


def plot(the_slice, direction, value, xrange=None, yrange=None):
    """

    """

    direction = direction.lower()
    if direction not in ['x', 'y']:
        print('Invalid direction specified. Valid options are: x, y')
        return

    if xrange is None:
        if direction == 'x':
            xrange = [np.nanmin(the_slice['ygrid']), np.nanmax(the_slice['ygrid'])]
        elif direction == 'y':
            xrange = [np.nanmin(the_slice['xgrid']), np.nanmax(the_slice['xgrid'])]

    # get annotations
    annotations = slice2d_getinfo(the_slice)

    yunits = spd_units_string(the_slice['units_name'])
    xunits = the_slice['xyunits']

    if the_slice['energy']:
        xtitle = 'E (' + xunits + ')'
    else:
        xtitle = 'V (' + xunits + ')'

    if isinstance(value, list):
        # sum over a range specified by value
        if direction == 'x':
            values_to_incl = np.argwhere((the_slice['ygrid'] >= value[0]) & (the_slice['ygrid'] <= value[1])).flatten()
            if len(values_to_incl) != 0:
                plt.plot(the_slice['xgrid'], np.nansum(the_slice['data'][:, values_to_incl]))
        elif direction == 'y':
            values_to_incl = np.argwhere((the_slice['xgrid'] >= value[0]) & (the_slice['xgrid'] <= value[1])).flatten()
            if len(values_to_incl) != 0:
                plt.plot(the_slice['ygrid'], np.nansum(the_slice['data'][values_to_incl, :]))

        plt.show()
        return

    # single point
    if direction == 'x':
        closest_at_this_value = the_slice['ygrid'].flat[np.abs(the_slice['ygrid'] - value).argmin()]
        idx_at_this_value = np.argwhere(the_slice['ygrid'] == closest_at_this_value)
        plt.plot(the_slice['ygrid'], np.nansum(the_slice['data'][:, idx_at_this_value]))
    elif direction == 'y':
        closest_at_this_value = the_slice['xgrid'].flat[np.abs(the_slice['xgrid'] - value).argmin()]
        idx_at_this_value = np.argwhere(the_slice['xgrid'] == closest_at_this_value)
        plt.plot(the_slice['xgrid'], np.nansum(the_slice['data'][idx_at_this_value, :]))

    plt.show()
    return

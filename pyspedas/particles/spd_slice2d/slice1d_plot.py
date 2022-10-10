import logging
import numpy as np
import matplotlib.pyplot as plt
from .slice2d_getinfo import slice2d_getinfo
from pyspedas.particles.spd_units_string import spd_units_string


def plot(the_slice, direction, value, xrange=None, yrange=None):
    """
    Create 1D plot from a 2D particle slice.

    If the 'value' argument is a scalar, this plots a cut through
    the distribution at the nearest point in the specified direction

    If the 'value' argument is a two-element list, this sums over
    the values between the min and max of the list

    Input
    --------
        the_slice: dict
            2D slice returned by slice2d

        direction: str
            Axis to plot - 'x' or 'y'

        value: float or list of float
            If direction is 'x', this is the y-value to create a 1D plot at (and vice versa)
            can also be a range of values, e.g., [-1000, 1000] to sum over the y-values
            from -1000 to +1000
    """

    direction = direction.lower()
    if direction not in ['x', 'y']:
        logging.error('Invalid direction specified. Valid options are: x, y')
        return

    if xrange is None:
        if direction == 'x':
            xrange = [np.nanmin(the_slice['ygrid']), np.nanmax(the_slice['ygrid'])]
        elif direction == 'y':
            xrange = [np.nanmin(the_slice['xgrid']), np.nanmax(the_slice['xgrid'])]

    fig = plt.figure()
    axis = fig.add_subplot(111)

    fig.subplots_adjust(left=0.14, right=0.94, top=0.90, bottom=0.14)

    # get annotations
    annotations = slice2d_getinfo(the_slice)

    xunits = the_slice['xyunits']

    if the_slice['energy']:
        xtitle = 'E (' + xunits + ')'
    else:
        if direction == 'x':
            xtitle = annotations['xtitle']
        else:
            xtitle = annotations['ytitle']

    options = {'linewidth': 0.5,
               'color': 'black'}

    axis.set_xlabel(xtitle)
    axis.set_ylabel(annotations['ztitle'])
    axis.set_yscale('log')

    if isinstance(value, list):
        # sum over a range specified by value
        if direction == 'x':
            values_to_incl = np.argwhere((the_slice['ygrid'] >= value[0]) & (the_slice['ygrid'] <= value[1])).flatten()
            if len(values_to_incl) != 0:
                axis.plot(the_slice['xgrid'], np.nansum(the_slice['data'][:, values_to_incl], axis=1), **options)
        elif direction == 'y':
            values_to_incl = np.argwhere((the_slice['xgrid'] >= value[0]) & (the_slice['xgrid'] <= value[1])).flatten()
            if len(values_to_incl) != 0:
                axis.plot(the_slice['ygrid'], np.nansum(the_slice['data'][values_to_incl, :], axis=0), **options)

        plt.show()
        return

    # single point
    if direction == 'x':
        closest_at_this_value = the_slice['ygrid'].flat[np.abs(the_slice['ygrid'] - value).argmin()]
        idx_at_this_value = np.argwhere(the_slice['ygrid'] == closest_at_this_value).flatten()
        axis.plot(the_slice['ygrid'], the_slice['data'][:, idx_at_this_value].flatten(), **options)
    elif direction == 'y':
        closest_at_this_value = the_slice['xgrid'].flat[np.abs(the_slice['xgrid'] - value).argmin()]
        idx_at_this_value = np.argwhere(the_slice['xgrid'] == closest_at_this_value).flatten()
        axis.plot(the_slice['xgrid'], the_slice['data'][idx_at_this_value, :].flatten(), **options)

    fig.show()
    return

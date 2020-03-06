# -*- coding: utf-8 -*-
"""
File:
    ex_test_smooth.py

Description:
    Applies the tsmooth function.
    To be compared with similar IDL function.

"""

import pytplot
from pyspedas.analysis.tsmooth import tsmooth


def ex_test_smooth():

    t = [1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12.]
    y = [3., 5., 8., 15., 20., 1., 2., 3., 4., 5., 6., 4.]

    pytplot.store_data('original', data={'x': t, 'y': y})
    tsmooth('original', width=5, new_names='smooth', preserve_nans=1)

    pytplot.tplot(['original', 'smooth'])

    d0 = pytplot.get_data('original')
    print('Original data: ', d0[1])
    d = pytplot.get_data('smooth')
    print('Smooth data: ', d[1])

    """
    Results:
    Original data:[ 3., 5., 8.,   15., 20., 1.,  2., 3., 4., 5.,  6.,  4.]
    Smooth data:  [ 3., 5., 10.2, 9.8, 9.2, 8.2  6., 3., 4., 4.4, 6.,  4.]
    """
    # Return 1 as indication that the example finished without problems.
    return 1


# Run the example code
# ex_test_smooth()

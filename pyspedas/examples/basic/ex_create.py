# -*- coding: utf-8 -*-
"""
File:
    ex_create.py

Desrciption:
    Creates a new pytplot object and applies analysis functions.

"""

import pyspedas
import pytplot
import numpy


def ex_create():
    # Delete any existing pytplot variables
    pytplot.del_data()
    # Create a sin wave plot
    a = list(range(0, 101))
    b = [2.0 / 100.0 * numpy.pi * s for s in a]
    c = pyspedas.time_float('2017-01-01')
    x = list()
    y = list()
    for i in range(len(b)):
        x.append(c + 60.0 / (2 * numpy.pi) * 60.0 * b[i])
        y.append(1000.0 * numpy.sin(b[i]))

    # Store data
    pytplot.store_data('sinx', data={'x': x, 'y': y})
    # Apply tclip
    pyspedas.tclip('sinx', -800.0, 800.0)
    # Remove NaN values
    pyspedas.tdeflag('sinx-clip')
    # Interpolate
    pyspedas.tinterpol(['sinx-clip-deflag'], ['sinx'], 'quadratic')
    # Plot
    pytplot.ylim('sinx', -1100.0, 1100.0)
    pytplot.ylim('sinx-clip', -1100.0, 1100.0)
    pytplot.ylim('sinx-clip-deflag', -1100.0, 1100.0)
    pytplot.ylim('sinx-clip-deflag-itrp', -1100.0, 1100.0)
    pytplot.tplot_options('title', 'Interpolation example')
    pytplot.tplot(['sinx', 'sinx-clip', 'sinx-clip-deflag',
                   'sinx-clip-deflag-itrp'])

# Run the example code
# ex_create()


"""
Examples of deriv_data.

One example with GMAG variables, and one example with sinx variable.

"""
import numpy as np
import pytplot
import pyspedas
from pyspedas.analysis.deriv_data import deriv_data


def ex_deriv():
    """Find the derivative of a GMAG variable."""
    # Derivative of data
    pytplot.del_data()

    # Define a time rage as a list
    trange = ['2007-03-23', '2007-03-23']

    # Download gmag files and load data into pytplot variables
    sites = ['ccnv']
    var = 'thg_mag_ccnv'
    pyspedas.themis.gmag(sites=sites, trange=trange, varnames=[var])
    # pytplot.tplot_options('title', 'GMAG data, thg_mag_ccnv 2007-03-23')
    pyspedas.subtract_average(var, median=1)
    var += '-m'

    # Five minute average
    deriv_data(var)
    # pytplot.options(var, 'ytitle', var)
    # pytplot.options(var + '-der', 'ytitle', var + '-der')
    pytplot.tplot([var, var + '-der'])

    # Return 1 as indication that the example finished without problems.
    return 1


def ex_deriv2():
    """Find the derivative of sinx."""
    # Delete any existing pytplot variables
    pytplot.del_data()

    # Create a sin wave plot
    a = list(range(0, 101))
    b = [2.0 / 100.0 * np.pi * s for s in a]
    c = pyspedas.time_float('2017-01-01')
    x = list()
    y = list()
    for i in range(len(b)):
        x.append(c + 60.0 / (2 * np.pi) * 60.0 * b[i])
        y.append(1000.0 * np.sin(b[i]))

    # Store data
    pytplot.store_data('sinx', data={'x': x, 'y': y})

    var = 'sinx'
    deriv_data(var)
    pytplot.tplot([var, var + '-der'])

    return 1


# Run the example code
# ex_deriv()

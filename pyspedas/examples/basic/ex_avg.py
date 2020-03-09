# -*- coding: utf-8 -*-
"""
File:
    ex_avg.py

Description:
    Example of avg_data.

"""
import random
import pytplot
import pyspedas
from pyspedas.analysis.avg_data import avg_data


def ex_avg():
    # Data averaged, 5 min intervals.
    # Delete any existing pytplot variables
    pytplot.del_data()

    # Define a time rage as a list
    trange = ['2007-03-23', '2007-03-23']

    # Download gmag files and load data into pytplot variables
    sites = ['ccnv']
    var = 'thg_mag_ccnv'
    pyspedas.themis.gmag(sites=sites, trange=trange, varnames=[var])
    pytplot.tplot_options('title', 'GMAG data, thg_mag_ccnv 2007-03-23')
    pyspedas.subtract_average(var, median=1)
    var += '-m'

    # Five minute average
    avg_data(var, width=5*60)
    pytplot.tplot([var, var + '-avg'])

    # Return 1 as indication that the example finished without problems.
    return 1


def ex_avg2():
    cy = [1009.4735, 1003.3744, 1001.9741, 1007.9487, 1008.4765, 1009.7213,
          1001.8322, 1003.8020, 1001.1117, 1008.7127, 1004.5268, 1005.7181,
          1005.2646, 1009.9537, 1007.4683, 1005.1428, 1001.3784, 1002.4366,
          1007.3653, 1006.0064, 1006.9906]

    t = []
    y = []
    for i in range(100):
        t.append(float(i))
        y.append(1000.0 + 10.0 * random.random())
    for i, yi in enumerate(cy):
        y[i] = yi
        print(yi)

    print("y: ", str(y[0:4]))
    pytplot.store_data('test', data={'x': t, 'y': y})
    d0 = pytplot.get_data('test')
    print('time start: ', d0[0])
    print('data start: ', d0[1])

    avg_data('test', 5)
    d = pytplot.get_data('test-avg')
    print('time end: ', d[0])
    print('data end: ', d[1])

    # Return data for testing
    # 1006.299      1003.99708    1006.7095     1004.83546
    return d[1][0:4] 


# Run the example code
print( '{0:.3g}'.format(ex_avg2()) ==  '{.3g}'.format([1006.299, 1003.99708, 1006.7095, 1004.83546]))

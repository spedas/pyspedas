"""
Example of avg_data.

This module demonstrates how to use the function avg_data.

"""
import random
import pytplot
import pyspedas
from pyspedas.analysis.avg_data import avg_data


def ex_avg(plot=False):
    """Load GMAG data and average over 5 min intervals."""
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
    if plot:
        pytplot.tplot([var, var + '-avg'])

    # Return 1 as indication that the example finished without problems.
    return 1


def ex_avg2():
    """Load some data and find time average.

    The same example can be run on IDL to compare results.
    """
    cy = [1059.45, 1083.30, 1011.95, 1027.95, 1038.45, 1059.72, 1091.83,
          1053.80, 1021.11, 1088.71, 1044.52, 1015.71, 1005.26, 1029.95,
          1077.46, 1035.14, 1051.37, 1062.43, 1077.36, 1046.00, 1026.90]

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
    print('time before: ', d0[0])
    print('data before: ', d0[1])

    avg_data('test', 5)
    d = pytplot.get_data('test-avg')
    print('time after: ', d[0])
    print('data after: ', d[1])
    print('first 4 results:', d[1][0:4])

    # Return data for testing
    # 1044.22 1063.034 1034.58 1054.46

    return d[1][0:4]


# Run the example code
# ex_avg()

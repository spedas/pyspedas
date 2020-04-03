
"""
Example of clean_spikes.

This module demonstrates how to use the function clean_spikes.

"""
import random
import pytplot
import pyspedas
from pyspedas.analysis.clean_spikes import clean_spikes


def ex_spikes():
    """Load GMAG data and average over 5 min intervals."""
    # Delete any existing pytplot variables.
    pytplot.del_data()

    # Define a time rage as a list
    trange = ['2007-03-23', '2007-03-23']

    # Download gmag files and load data into pytplot variables.
    sites = ['ccnv']
    var = 'thg_mag_ccnv'
    pyspedas.themis.gmag(sites=sites, trange=trange, varnames=[var])
    pytplot.tplot_options('title', 'GMAG data, thg_mag_ccnv 2007-03-23')

    # Add spikes to data.
    data = pytplot.data_quants[var].values
    dlen = len(data)
    for i in range(1, 16):
        s = (1 if random.random() < 0.5 else -1)
        p1 = int(i*dlen/16)
        data[p1, 0] = s * i * 40000
        data[p1+2000, 1] = s * i * 30000
        data[p1+4000, 2] = s * i * 20000

    pytplot.data_quants[var].values = data

    # Clean spikes.
    clean_spikes(var, sub_avg=True)

    # Plot all variables.
    pytplot.tplot(pytplot.tplot_names())

    # Return 1 as indication that the example finished without problems.
    return 1


# Run the example code:
# ex_spikes()

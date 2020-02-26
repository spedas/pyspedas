# -*- coding: utf-8 -*-
"""
File:
    ex_analysis.py

Description:
    Basic example using analysis functions.
    Download THEMIS data, subtract average, and plot it.

"""

import pyspedas
import pytplot


def ex_analysis():

    # Delete any existing pytplot variables
    pytplot.del_data()

    # Download THEMIS state data for 2015-12-31
    time_range = ['2015-12-31 00:00:00', '2015-12-31 23:59:59']
    pyspedas.themis.state(probe='a', trange=time_range)

    # Use some analysis functions on tplot variables
    pyspedas.subtract_average('tha_pos')
    pyspedas.subtract_median('tha_pos')

    # Plot
    pytplot.tplot(["tha_pos", "tha_pos-d", "tha_pos-m"])

    # Return 1 as indication that the example finished without problems.
    return 1

# Run the example code
# ex_analysis()

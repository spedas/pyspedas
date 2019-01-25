# -*- coding: utf-8 -*-
"""
File:
    ex_analysis.py

Desrciption:
    Basic example using analysis functions.
    Downloads THEMIS data and plots it.

"""

import pyspedas
import pytplot


def ex_analysis():
    # Print the installed version of pyspedas
    pyspedas.version()
    # Delete any existing pytplot variables
    pytplot.del_data()
    # Download THEMIS state data for 2015-12-31
    pyspedas.load_data('themis', '2015-12-31', ['tha'], 'state', 'l1')
    # Use some analysis functions on tplot variables
    pyspedas.subtract_average('tha_pos')
    pyspedas.subtract_median('tha_pos')
    # Plot
    pytplot.tplot(["tha_pos", "tha_pos-d", "tha_pos-m"])

# Run the example code
# ex_analysis()

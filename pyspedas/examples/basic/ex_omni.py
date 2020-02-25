# -*- coding: utf-8 -*-
"""
File:
    ex_omni.py

Description:
    Basic example of plotting OMNI data.

"""

import pyspedas
import pytplot


def ex_omni():
    # Print the installed version of pyspedas
    pyspedas.version()
    # Delete any existing pytplot variables
    pytplot.del_data()

    # Download OMNI data for 2015-12-31
    trange = ['2015-12-31 00:00:00', '2015-12-31 23:59:59']
    pyspedas.omni.load(trange=trange, datatype='1min')

    # Plot
    pytplot.tplot_options('title', 'OMNI flow_speed 2015-12-31')
    pytplot.tplot(['flow_speed'])

    # Return 1 as indication that the example finished without problems.
    return 1

# Run the example code
# ex_omni()

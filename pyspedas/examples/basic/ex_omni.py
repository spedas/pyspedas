# -*- coding: utf-8 -*-
"""
File:
    ex_omni.py

Desrciption:
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
    pyspedas.load_data('omni', ['2015-12-31 00:00:00',
                                '2016-01-01 23:59:59'], '', '', '1min')

    # Plot
    pytplot.tplot_options('title', 'OMNI flow_speed 2015-12-31 to 2016-01-01')
    pytplot.tplot(['flow_speed'])

# Run the example code
# ex_omni()

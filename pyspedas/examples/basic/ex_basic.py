# -*- coding: utf-8 -*-
"""
File:
    ex_basic.py

Desrciption:
    Basic example to verify that the installation works correctly.
    Downloads THEMIS data and plots it.

"""

import pyspedas
import pytplot


def ex_basic():
    # Delete any existing pytplot variables
    pytplot.del_data()
    # Download THEMIS state data for 2015-12-31
    pyspedas.load_data('themis', ['2015-12-31 00:00:00',
                       '2016-01-01 12:00:00'], ['tha'], 'state', 'l1')
    # Get data into python variables
    alldata = pytplot.get_data("tha_pos")      
    time = alldata[0]
    data = alldata[1]
    # Store a new pytplot variable
    pytplot.store_data("tha_position", data={'x': time, 'y': data})
    # Define the y-axis limits
    pytplot.ylim('tha_pos', -23000.0, 81000.0)
    pytplot.ylim('tha_position', -23000.0, 81000.0)
    pytplot.ylim('tha_vel', -8.0, 12.0)
    # Plot position and velocity using the pyqtgraph library (default)
    pytplot.tplot(["tha_pos", "tha_position", "tha_vel"])
    # Plot position and velocity using the bokeh library
    # pytplot.tplot(["tha_pos", "tha_position", "tha_vel"], bokeh=True)

# Run the example code
# ex_basic()

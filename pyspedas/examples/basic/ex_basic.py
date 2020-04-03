
"""
File:
    ex_basic.py

Description:
    Basic example to verify that the installation works correctly.
    Download THEMIS data and plot it.

"""

import pyspedas
import pytplot


def ex_basic():

    # Delete any existing pytplot variables
    pytplot.del_data()

    # Download THEMIS state data for 2015-12-31
    time_range = ['2015-12-31 00:00:00', '2016-01-01 12:00:00']
    pyspedas.themis.state(probe='a', trange=time_range, time_clip=True)

    # Get data into python variables
    alldata = pytplot.get_data("tha_pos")
    time = alldata[0]
    data = alldata[1]
    # Here we could work on the data before saving a new tplot variable.

    # Store a new pytplot variable
    pytplot.store_data("tha_position", data={'x': time, 'y': data})

    # Define the y-axis limits
    pytplot.ylim('tha_pos', -23000.0, 81000.0)
    pytplot.ylim('tha_position', -23000.0, 81000.0)
    pytplot.ylim('tha_vel', -8.0, 12.0)

    # Give a title to the plot and labels for the y-axis panels.
    pytplot.tplot_options('title', 'tha position and velocity, 2015-12-31')
    pytplot.options('tha_pos', 'ytitle', 'Position')
    pytplot.options('tha_vel', 'ytitle', 'Velocity')

    # Plot position and velocity using the pyqtgraph library (default)
    pytplot.tplot(["tha_pos", "tha_position", "tha_vel"])

    # Plot position and velocity using the bokeh library
    # pytplot.tplot(["tha_pos", "tha_position", "tha_vel"], bokeh=True)

    # Return 1 as indication that the example finished without problems.
    return 1

# Run the example code
# ex_basic()

import pyqtgraph as pg
import numpy as np
import pytplot
from pyqtgraph.Qt import QtGui, QtCore


def get_data(names):
    # Just grab variables that are spectrograms.
    valid_vars = list()
    for n in names:
        if pytplot.data_quants[n].spec_bins is not None:
            valid_vars.append(n)
    return valid_vars


def get_plot_labels(names):
    # Get labels and axis types for plots.
    plot_labels = {}
    for n in names:
        if pytplot.data_quants[n].spec_bins is not None:

            zlabel = pytplot.data_quants[n].zaxis_opt['axis_label']
            try:
                ztype = pytplot.data_quants[n].zaxis_opt['z_axis_type']
            except:
                ztype = pytplot.default_values['z_axis_type']
            try:
                ytype = pytplot.data_quants[n].yaxis_opt['y_axis_type']
            except:
                ytype = pytplot.default_values['y_axis_type']
            plot_labels[n] = [zlabel, ytype, ztype]
    return plot_labels


def get_bins(var):
    # Get bins to be plotted.
    bins = list()
    for name, values in pytplot.data_quants[var].spec_bins.iteritems():
        # name = variable name
        # value = data in variable name
        bins.append(values.values[0])
    return bins


def get_z_t_values(var):
    # Get data to be plotted and time data for indexing.
    time_values = list()
    z_values = list()
    for r, rows in pytplot.data_quants[var].data.iterrows():
        # r = time
        # rows = the flux at each time, where each row signifies a different time
        time_values.append(r)
        z_values.append(rows.values)
    return time_values, z_values


def interactive2dplot():
    """ If the interactive option is set to True in tplot, this function will take in the stored tplot variables
    and create a 2D interactive window that will pop up when any one of the tplot variables is plotted (so long
    as at least one of the tplot variables is a spectrogram). If the mouse hovers over a spectrogram plot, data
    for that point in time on the spectrogram plot will be plotted in the 2D interactive window. If the mouse
    hovers over a non-spectrogram plot, the 2D interactive window returns an empty plot. """

    # Grab names of data loaded in as tplot variables.
    names = list(pytplot.data_quants.keys())
    # Get data we'll actually work with here.
    valid_variables = get_data(names)

    # Don't plot anything unless we have spectrograms with which to work.
    if valid_variables != []:
        # Get z label
        labels = get_plot_labels(names)

        # Put together data in easy-to-access format for plots.
        data = {}
        for name in valid_variables:
            bins = get_bins(name)
            time_values, z_values = get_z_t_values(name)
            data[name] = [bins, z_values, time_values]

        # Set up the 2D interactive plot
        pytplot.interactive_window = pg.GraphicsWindow()
        pytplot.interactive_window.resize(1000,600)
        pytplot.interactive_window.setWindowTitle('Interactive Window')
        plot = pytplot.interactive_window.addPlot(title='2D Interactive Plot', row=0, col=0)
        # Make it so that whenever this first starts up, you just have an empty plot
        plot_data = plot.plot([],[])

        # The following update function is passed to change_hover_time in the HoverTime class
        # defined in __init__.py. For reference, "t" essentially originates inside of
        # TVarFigure(1D/Spec/Alt/Map), inside the _mousemoved function. It calls
        # "self._mouseMovedFunction(int(mousePoint.x()))" and that is called every time the mouse is
        # moved by Qt. Therefore, it gives the location of the mouse on the x axis. In tplot,
        # mouse_moved_event is set to pytplot.hover_time.change_hover_time, so the mouseMovedFunction
        # is pytplot.hover_time.change_hover_time. Thus, whenever change_hover_time is called, it
        # calls every other function that is registered. Since the below function update() is
        # registered as a listener, it'll update whenever hover_time is updated.
        # to the HoverTime class with "t" as the input.

        # TL;DR, t comes from getting the mouse location in pyqtgraph every time the mouse is moved
        # and the below function will update the plot's position as the mouse is moved.
        def update(t, name):
            if name in valid_variables:
                # When hovering over a spectrogram plot...
                # First, get the time closest to the x position the mouse is over.
                time_array = np.array(data[name][2])
                array = np.asarray(time_array)
                idx = (np.abs(array - t)).argmin()
                # If the spectrogram plot's y and z axes (corresponding to 2D interactive window's
                # x and y axes) are logarithmic, make sure the 2D interactive plot's axes are
                # also logarithmic.
                x_axis = False
                y_axis = False
                if labels[name][1] == 'log':
                    x_axis = True
                if labels[name][2] == 'log':
                    y_axis = True
                # Set plot labels and plot data based on time we're hovering over.
                plot.setLabel('bottom', '{} bins'.format(labels[name][0]))
                plot.setLabel('left', '{}'.format(labels[name][0]))
                plot.setLogMode(x_axis, y_axis)
                plot_data.setData(data[name][0][:], list(data[name][1][idx]))
            else:
                # Cover the situation where you hover over a non-spectrogram plot.
                plot.setLogMode(False, False)
                plot.setLabel('bottom', '')
                plot.setLabel('left', '')
                plot_data.setData([],[])

        # Make the above function called whenever hover_time is updated.
        pytplot.hover_time.register_listener(update)

        # Start Qt event loop unless running in interactive mode.
        import sys
        if not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

import pyqtgraph as pg
import numpy as np
import pytplot
from pytplot import tplot_utilities
from pyqtgraph.Qt import QtGui, QtCore


def interactiveplot(t_average=None):
    """ If the interactive option is set to True in tplot, this function will take in the stored tplot variables
    and create a 2D interactive window that will pop up when any one of the tplot variables is plotted (so long
    as at least one of the tplot variables is a spectrogram). If the mouse hovers over a spectrogram plot, data
    for that point in time on the spectrogram plot will be plotted in the 2D interactive window. If the mouse
    hovers over a non-spectrogram plot, the 2D interactive window returns an empty plot. If the 't_average'
    option is selected, then the interactive window's y values will be time-averaged values, where the
    amount of time for which those values have been averaged is determined by the number of seconds the user
    indicates. """

    # Grab names of data loaded in as tplot variables.
    names = list(pytplot.data_quants.keys())
    # Get data we'll actually work with here.
    valid_variables = tplot_utilities.get_data(names)

    # Don't plot anything unless we have spectrograms with which to work.
    if valid_variables:
        # Get z label
        labels = tplot_utilities.get_labels_axis_types(names)

        # Put together data in easy-to-access format for plots.
        data = {}
        for name in valid_variables:
            bins = tplot_utilities.get_bins(name)
            time_values, z_values = tplot_utilities.get_z_t_values(name)
            data[name] = [bins, z_values, time_values]

        # Set up the 2D interactive plot
        pytplot.interactive_window = pg.GraphicsWindow()
        pytplot.interactive_window.resize(1000, 600)
        pytplot.interactive_window.setWindowTitle('Interactive Window')
        plot = pytplot.interactive_window.addPlot(title='2D Interactive Plot', row=0, col=0)
        # Make it so that whenever this first starts up, you just have an empty plot
        plot_data = plot.plot([], [])

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
                # Get the time closest to the x position the mouse is over.
                time_array = np.array(data[name][2])
                array = np.asarray(time_array)
                idx = (np.abs(array - t)).argmin()

                # If user indicated they wanted the interactive plot's axes to be logged, log 'em.
                # But first make sure that values in x and y are loggable!
                x_axis = False
                y_axis = False
                # Checking x axis
                if np.nanmin(data[name][0][:]) < 0:
                    print('Negative data is incompatible with log plotting.')
                elif np.nanmin(data[name][0][:]) >= 0 and labels[name][2] == 'log':
                    x_axis = True
                # Checking y axis
                if np.nanmin(list(data[name][1][idx])) < 0:
                    print('Negative data is incompatible with log plotting')
                elif np.nanmin(list(data[name][1][idx])) >= 0 and labels[name][3] == 'log':
                    y_axis = True

                # Set plot labels
                plot.setLabel('bottom', '{}'.format(labels[name][0]))
                plot.setLabel('left', '{}'.format(labels[name][1]))
                plot.setLogMode(x=x_axis, y=y_axis)
                # Update x and y range if user modified it
                tplot_utilities.set_x_range(name, x_axis, plot)
                tplot_utilities.set_y_range(name, y_axis, plot)

                if 't_average' in pytplot.data_quants[name].extras:
                    # If the user indicated that they wanted to average the interactive plot's y values based on a
                    # certain time range around the cursor location, we then want to get average of values around
                    # the cursor location.
                    t_min = data[name][2][0]
                    t_max = data[name][2][-1]

                    delta = pytplot.data_quants[name].extras['t_average']/int(2)

                    left_bound = data[name][2][idx] - delta
                    right_bound = data[name][2][idx] + delta

                    if (left_bound - t_min >= 0) and (t_max - right_bound >= 0):
                        # Find index of left and right bounds, no fancy foot work necessary.
                        idx_left = (np.abs(array - left_bound)).argmin()
                        idx_right = (np.abs(array - right_bound)).argmin()
                    elif left_bound - t_min < 0:
                        # Find the number of seconds difference between the cursor's
                        # left bound and the minimum time in the dataset, add that
                        # difference to the right bound time (since you want to push the bound
                        # forward in time, and set the left bound's index to be 0.
                        idx_left = 0
                        diff = right_bound + (t_min - left_bound)
                        idx_right = (np.abs(array - diff)).argmin()
                    elif t_max - right_bound < 0:
                        # Find the number of seconds difference between the cursor's
                        # right bound and the maximum time in the dataset, subtract that
                        # difference from the left bound time (since you want to push the bound
                        # back in time), and set the right bound's index to be -1.
                        idx_right = -1
                        diff = left_bound - (right_bound - t_max)
                        idx_left = (np.abs(array - diff)).argmin()
                    elif (left_bound - t_min < 0) and (t_max - right_bound < 0):
                        # The user is asking to average the entire time frame of the dataset...
                        # dunno why they want that, but if they do, use the time-averaged static plot,
                        # not this.
                        print(
                            'This plot isn\'t appropriate for what you want, use the time-averaged static plot.')

                    # Average values based on the calculated right and left bounds' indices.
                    time_diff = abs(idx_right - idx_left)
                    # Make sure to account for edge problem
                    if idx_right != -1:
                        y_values_slice = data[name][1][idx_left:idx_right + 1]
                    else:
                        y_values_slice = data[name][1][idx_left:]
                    y_values_avgd = np.sum(y_values_slice, axis=0)/np.float(time_diff)

                    # Update x and y range if user modified it
                    tplot_utilities.set_x_range(name, x_axis, plot)
                    tplot_utilities.set_y_range(name, y_axis, plot)

                    try:
                        # Plot data based on time we're hovering over
                        plot_data.setData(data[name][0][:], y_values_avgd)
                    except ZeroDivisionError:
                        pass
                else:
                    # Update x and y range if user modified it
                    tplot_utilities.set_x_range(name, x_axis, plot)
                    tplot_utilities.set_y_range(name, y_axis, plot)
                    # If the user just wants a plain jane interactive plot...
                    # Plot data based on time we're hovering over'
                    try:
                        plot_data.setData(data[name][0][:], list(data[name][1][idx]))
                    except ZeroDivisionError:
                        pass

            else:
                # Cover the situation where you hover over a non-spectrogram plot.
                plot.setLogMode(False, False)
                plot.setLabel('bottom', '')
                plot.setLabel('left', '')
                plot_data.setData([], [])

        # Make the above function called whenever hover_time is updated.
        pytplot.hover_time.register_listener(update)

        # Start Qt event loop unless running in interactive mode.
        #import sys
        #if not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION'):
        #    QtGui.QApplication.instance().exec_()

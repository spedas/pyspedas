import pyqtgraph as pg
import numpy as np
import pytplot
from pytplot import tplot_utilities


def spec_slicer(var=None, time=None, interactive=False):
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
    valid_variables = tplot_utilities.get_spec_data(names)

    # Don't plot anything unless we have spectrograms with which to work.
    if valid_variables:
        # Get z label
        labels = tplot_utilities.get_spec_slicer_axis_types(names)

        # Set up the 2D interactive plot
        window = pytplot.tplot_utilities.get_available_qt_window(name='Spec_Slice')
        window.newlayout(pg.GraphicsWindow())
        window.resize(1000, 600)
        window.setWindowTitle('Interactive Window')
        plot = window.centralWidget().addPlot(title='Spectrogram Slicing Plot', row=0, col=0)
        # Make it so that whenever this first starts up, you just have an empty plot
        if pytplot.tplot_opt_glob['black_background']:
            pen_color = 'w'
        else:
            pen_color = 'k'
        plot_data = plot.plot([], [], pen=pg.mkPen(width=6, color=pen_color))

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

        # TODO: At some point, the indexing stuff can all be simplified with xarray functionality
        def update(t, name):
            if name in valid_variables:
                # Get the time closest to the x position the mouse is over.
                time_array = pytplot.data_quants[name].coords['time'].values
                array = np.asarray(time_array)

                using_avg = False
                # Take the average time for bin purposes
                if hasattr(t, '__len__'):
                    if len(t) == 2:
                        tavg = (t[0]+t[1]) / 2.0
                        using_avg = True
                        idx = (np.abs(array - tavg)).argmin()
                        plot.setTitle(name + " " + pytplot.tplot_utilities.int_to_str(tavg))
                    else:
                        idx = (np.abs(array - t)).argmin()
                        plot.setTitle(name + " " + pytplot.tplot_utilities.int_to_str(t[0]))
                else:
                    idx = (np.abs(array - t)).argmin()
                    plot.setTitle(name + " " + pytplot.tplot_utilities.int_to_str(t))
                # Grabbing the bins to display on the x axis
                if len(pytplot.data_quants[name].coords['spec_bins'].shape) == 2:
                    bins = pytplot.data_quants[name].coords['spec_bins'][idx, :]
                else:
                    bins = pytplot.data_quants[name].coords['spec_bins'].values

                # If user indicated they wanted the interactive plot's axes to be logged, log 'em.
                # But first make sure that values in x and y are loggable!
                x_axis_log = False
                y_axis_log = False
                # Checking x axis
                if np.nanmin(bins) >= 0 and labels[name][2] == 'log':
                    x_axis_log = True
                # Checking y axis
                if np.nanmin(bins) >= 0 and labels[name][3] == 'log':
                    y_axis_log = True

                # Set plot labels
                plot.setLabel('bottom', '{}'.format(labels[name][0]))
                plot.setLabel('left', '{}'.format(labels[name][1]))
                plot.setLogMode(x=x_axis_log, y=y_axis_log)
                # Update x and y range if user modified it
                tplot_utilities.set_x_range(name, x_axis_log, plot)
                tplot_utilities.set_y_range(name, y_axis_log, plot)

                if ('t_average' in pytplot.data_quants[name].attrs['plot_options']['extras']) or using_avg:
                    # If the user indicated that they wanted to average the interactive plot's y values based on a
                    # certain time range around the cursor location, we then want to get average of values around
                    # the cursor location.
                    t_min = time_array[0]
                    t_max = time_array[-1]

                    if using_avg:
                        left_bound = t[0]
                        right_bound = t[1]
                    else:
                        delta = pytplot.data_quants[name].attrs['plot_options']['extras']['t_average']/int(2)
                        left_bound = time_array[idx] - delta
                        right_bound = time_array[idx] + delta

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
                        return

                    # Average values based on the calculated right and left bounds' indices.
                    time_diff = abs(idx_right - idx_left)
                    # Make sure to account for edge problem
                    if idx_right != -1:
                        y_values_slice = pytplot.data_quants[name].isel(time=slice(idx_left,idx_right + 1))
                    else:
                        y_values_slice = pytplot.data_quants[name].isel(time=slice(idx_left,None))
                    y_values_avgd = np.sum(y_values_slice, axis=0)/np.float(time_diff)
                    if len(y_values_avgd.shape) >= 2:
                        y_values_avgd = np.nansum(y_values_avgd, 0)
                    while len(y_values_avgd.shape) > 1:
                        y_values_avgd = np.nansum(y_values_avgd, 1)
                    try:
                        # Plot data based on time we're hovering over
                        plot_data.setData(bins, y_values_avgd)
                    except ZeroDivisionError:
                        pass
                else:
                    # If the user just wants a plain jane interactive plot...
                    # Plot data based on time we're hovering over'
                    try:
                        data = pytplot.data_quants[name].isel(time=idx)
                        if len(data.shape) >= 2:
                            data = np.nansum(data, 0)
                        while len(data.shape) > 1:
                            data = np.nansum(data, 1)
                        if y_axis_log:
                            data[data<=0] = np.NaN
                        #Create a Mask for Nan Values
                        locations_where_nan = np.argwhere(np.isnan(data.values))
                        if len(locations_where_nan) > 0:
                            nanmask = np.ones(data.values.shape,dtype=bool)
                            nanmask[locations_where_nan] = False
                            nanmask[~locations_where_nan] = True
                            plot_data.setData(bins[nanmask], list(data.values[nanmask]))
                        else:
                            plot_data.setData(bins, list(data.values))
                    except ZeroDivisionError:
                        pass

            else:
                # Cover the situation where you hover over a non-spectrogram plot.
                plot.setLogMode(False, False)
                plot.setLabel('bottom', '')
                plot.setLabel('left', '')
                plot_data.setData([], [])

        if time is not None:
            if not isinstance(time, list):
                time = [time]
            user_time = [tplot_utilities.str_to_int(i) for i in time]
            update(user_time, var)

        # Make the above function called whenever hover_time is updated.
        if interactive:
            pytplot.hover_time.register_listener(update)

        # Turn on the window!
        window.show()


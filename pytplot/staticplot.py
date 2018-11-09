import pyqtgraph as pg
import numpy as np
import pytplot
from pytplot import tplot_utilities


def static2dplot(var, time):
    """ If the static option is set in tplot, and is supplied with a time, then the spectrogram plot(s) for which
    it is set will have another window pop up, with y and z values plotted at the specified time. """

    # Grab names of data loaded in as tplot variables.
    names = list(pytplot.data_quants.keys())
    # Get data we'll actually work with here.
    valid_variables = tplot_utilities.get_data(names)

    # Don't plot anything unless we have spectrograms with which to work.
    if valid_variables:
        # Get z label
        labels = tplot_utilities.get_plot_labels(names)

        # Put together data in easy-to-access format for plots.
        data = {}
        for name in valid_variables:
            bins = tplot_utilities.get_bins(name)
            time_values, z_values = tplot_utilities.get_z_t_values(name)
            data[name] = [bins, z_values, time_values]

        # Set up the 2D static plot
        pytplot.static_window = pg.GraphicsWindow()
        pytplot.static_window.resize(1000, 600)
        pytplot.static_window.setWindowTitle('Static Window')
        plot = pytplot.static_window.addPlot(title='2D Static Plot', row=0, col=0)
        # Make it so that whenever this first starts up, you just have an empty plot
        plot_data = plot.plot([], [])

        if var in valid_variables:
            # Get min/max values of data's time range (in both datetime and seconds since epoch)
            t_min = np.nanmin(time_values)
            t_min_str = tplot_utilities.int_to_str(np.nanmin(time_values))
            t_max = np.nanmax(time_values)
            t_max_str = tplot_utilities.int_to_str(np.nanmax(time_values))
            # Convert user input to seconds since epoch
            user_time = tplot_utilities.str_to_int(time)

            # Covering situation where user entered a time not in the dataset!
            # As long as they used a time in the dataset, this will not trigger.
            if user_time not in range(int(t_min), int(t_max)):
                while True:
                    try:
                        user_time = tplot_utilities.str_to_int(input(
                            'Chosen time not in range of data [{} to {}]. Input new time (%Y-%m-%d %H:%M:%S). '.format(
                                t_min_str, t_max_str)))
                    except:
                        continue
                    else:
                        if user_time not in range(int(t_min), int(t_max)):
                            continue
                        else:
                            break

            # Get time closest to the user's time choice
            time_array = np.array(data[var][2])
            array = np.asarray(time_array)
            idx = (np.abs(array - user_time)).argmin()
            # If user indicated they wanted the interactive plot's axes to be logged, log 'em.
            # But first make sure that values in x and y are loggable!
            x_axis = False
            y_axis = False
            # Checking x axis
            if np.nanmin(data[name][0][:]) < 0:
                print('Negative data is incompatible with log plotting.')
            elif np.nanmin(data[name][0][:]) >= 0 and labels[name][3] == 'log':
                x_axis = True
            # Checking y axis
            if np.nanmin(list(data[name][1][idx])) < 0:
                print('Negative data is incompatible with log plotting')
            elif np.nanmin(list(data[name][1][idx])) >= 0 and labels[name][4] == 'log':
                y_axis = True

            # Set plot labels
            plot.setLabel('bottom', '{} bins'.format(labels[name][0]))
            plot.setLabel('left', '{}'.format(labels[name][0]))
            plot.setLogMode(x=x_axis, y=y_axis)
            # Update x and y range if user modified it
            tplot_utilities.set_x_range(name, x_axis, plot)
            tplot_utilities.set_y_range(name, y_axis, plot)
            # Plot data based on time we're hovering over
            plot_data.setData(data[name][0][:], list(data[name][1][idx]))

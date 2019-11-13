import pyqtgraph as pg
import pytplot


def position_2d(temp=None):


    # Set up the 2D interactive plot
    pytplot.pytplotWindows.append(pg.GraphicsWindow())
    pytplot.pytplotWindows[-1].resize(600, 200)
    pytplot.pytplotWindows[-1].setWindowTitle('Interactive Window')
    plot1 = pytplot.pytplotWindows[-1].addPlot(title='Position x-y', row=0, col=0)
    plot2 = pytplot.pytplotWindows[-1].addPlot(title='Position y-z', row=0, col=1)
    plot3 = pytplot.pytplotWindows[-1].addPlot(title='Position x-z', row=0, col=2)
    # Make it so that whenever this first starts up, you just have an empty plot
    plot_data1 = plot1.plot([], [], symbol='o', symbol_size=14)
    plot1.setXRange(-10000, 10000)
    plot1.setYRange(-10000, 10000)
    plot_data2 = plot2.plot([], [], symbol='o', symbol_size=14)
    plot2.setXRange(-10000, 10000)
    plot2.setYRange(-10000, 10000)
    plot_data3 = plot3.plot([], [], symbol='o', symbol_size=14)
    plot3.setXRange(-10000, 10000)
    plot3.setYRange(-10000, 10000)


    def update(t, name):
        x_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['x']]
        y_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['y']]
        z_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['z']]

        new_x = x_tvar.sel(time=t, method='nearest').values
        new_y = y_tvar.sel(time=t, method='nearest').values
        new_z = z_tvar.sel(time=t, method='nearest').values

        plot_data1.setData([new_x], [new_y])
        plot_data2.setData([new_y], [new_z])
        plot_data3.setData([new_x], [new_z])

    pytplot.hover_time.register_listener(update)


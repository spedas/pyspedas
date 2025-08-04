import pyqtgraph as pg
import pytplot


def position_mars_2d(temp=None):
    '''
    This is a simple plot that shows spacecraft position relative to Mars in MSO coordinates
    '''

    # Set Mars Diameter constant
    MARS_DIAMETER = 3389.5 * 2

    # Set up the 2D interactive plot
    window = pytplot.tplot_utilities.get_available_qt_window(name='2D_MARS')
    window.newlayout(pg.GraphicsWindow())
    window.resize(900, 300)
    window.setWindowTitle('Mars Position 2D Window')

    # Add the 3 plots for 3 different views
    plot1 = window.centralWidget().addPlot(title='Position MSO x-y', row=0, col=0)
    plot1.setLabel('left', text = 'MSO Y', units = 'km')
    plot1.setLabel('bottom', text='MSO X', units='km')
    plot2 = window.centralWidget().addPlot(title='Position MSO y-z', row=0, col=1)
    plot2.setLabel('left', text='MSO Z', units='km')
    plot2.setLabel('bottom', text='MSO Y', units='km')
    plot3 = window.centralWidget().addPlot(title='Position MSO x-z', row=0, col=2)
    plot3.setLabel('left', text='MSO Z', units='km')
    plot3.setLabel('bottom', text='MSO X', units='km')



    # Make it so that whenever this first starts up, you just have an empty plot
    plot_data1 = plot1.plot([], [], symbol='o', symbol_size=14)
    plot_data2 = plot2.plot([], [], symbol='o', symbol_size=14)
    plot_data3 = plot3.plot([], [], symbol='o', symbol_size=14)

    # Add the representation of mars on the first plot
    mars1 = pg.QtGui.QGraphicsEllipseItem(-1*MARS_DIAMETER/2,-1*MARS_DIAMETER/2,MARS_DIAMETER,MARS_DIAMETER)
    mars1.setPen(pg.mkPen(None))
    mars1.setBrush(pg.mkBrush('r'))
    mars1.setZValue(-1)
    mars1.setSpanAngle(180 * 16)
    mars1.setStartAngle(-90 * 16)
    mars1_dark = pg.QtGui.QGraphicsEllipseItem(-1 * MARS_DIAMETER / 2, -1 * MARS_DIAMETER / 2, MARS_DIAMETER, MARS_DIAMETER)
    mars1_dark.setPen(pg.mkPen(None))
    mars1_dark.setBrush(pg.mkBrush(.2))
    mars1_dark.setZValue(-1)
    mars1_dark.setSpanAngle(180 * 16)
    mars1_dark.setStartAngle(90 * 16)
    plot1.vb.addItem(mars1)
    plot1.vb.addItem(mars1_dark)
    plot1.setXRange(-10000, 10000)
    plot1.setYRange(-10000, 10000)

    # Add the representation of mars on the second plot
    mars2 = pg.QtGui.QGraphicsEllipseItem(-1 *MARS_DIAMETER / 2, -1 * MARS_DIAMETER / 2, MARS_DIAMETER, MARS_DIAMETER)
    mars2.setPen(pg.mkPen(None))
    mars2.setBrush(pg.mkBrush('r'))
    mars2.setZValue(-1)
    plot2.vb.addItem(mars2)
    plot2.setXRange(-10000, 10000)
    plot2.setYRange(-10000, 10000)

    # Add the representation of mars on the third plot
    mars3 = pg.QtGui.QGraphicsEllipseItem(-1 * MARS_DIAMETER / 2, -1 * MARS_DIAMETER / 2, MARS_DIAMETER, MARS_DIAMETER)
    mars3.setPen(pg.mkPen(None))
    mars3.setBrush(pg.mkBrush('r'))
    mars3.setZValue(-1)
    mars3.setSpanAngle(180 * 16)
    mars3.setStartAngle(-90 * 16)
    mars3_dark = pg.QtGui.QGraphicsEllipseItem(-1 * MARS_DIAMETER / 2, -1 * MARS_DIAMETER / 2, MARS_DIAMETER, MARS_DIAMETER)
    mars3_dark.setPen(pg.mkPen(None))
    mars3_dark.setBrush(pg.mkBrush(.2))
    mars3_dark.setZValue(-1)
    mars3_dark.setSpanAngle(180 * 16)
    mars3_dark.setStartAngle(90 * 16)
    plot3.vb.addItem(mars3)
    plot3.vb.addItem(mars3_dark)
    plot3.setXRange(-10000, 10000)
    plot3.setYRange(-10000, 10000)

    # Define the update function on mouse moved events
    def update(t, name):
        # Get the xarray for x/y/z positions of the spacecraft
        if 'x' in pytplot.data_quants[name].attrs['plot_options']['links']:
            x_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['x']]
            y_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['y']]
            z_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['z']]
        elif 'mso_x' in pytplot.data_quants[name].attrs['plot_options']['links']:
            x_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['mso_x']]
            y_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['mso_y']]
            z_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['mso_z']]
        else:
            return

        # Use nearest neighbor to find closest x/y/z values
        new_x = x_tvar.sel(time=t, method='nearest').values
        new_y = y_tvar.sel(time=t, method='nearest').values
        new_z = z_tvar.sel(time=t, method='nearest').values

        # This moves the Mars spheres either to the front or the back depending on the location of the spacecraft
        if new_z < 0:
            mars1.setZValue(1)
            mars1_dark.setZValue(1)
        else:
            mars1.setZValue(-1)
            mars1_dark.setZValue(-1)
        if new_x < 0:
            mars2.setZValue(1)
        else:
            mars2.setZValue(-1)
        if new_y < 0:
            mars3.setZValue(1)
            mars3_dark.setZValue(1)
        else:
            mars3.setZValue(-1)
            mars3_dark.setZValue(-1)

        # Sets the position of the spacecraft in each window
        plot_data1.setData([new_x], [new_y])
        plot_data2.setData([new_y], [new_z])
        plot_data3.setData([new_x], [new_z])

    # Register the update function to pytplot
    pytplot.hover_time.register_listener(update)

    # Turn on the window!
    window.show()


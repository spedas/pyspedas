import pytplot

def position_mars_3d(temp=None):
    '''
    This is a simple 3D window that shows a spacecraft in MSO coordinates.
    This tool will look for links to the tplot variable that are named either "x/y/z" or "mso_(x/y/z)"
    '''

    # Import 3D functionality from opengl
    try:
        import pyqtgraph.opengl as gl
        from pyqtgraph.Qt import QtGui
        from OpenGL.GL import glLightModelfv, glLightfv, GL_LIGHT0, GL_POSITION, \
            GL_LIGHT_MODEL_AMBIENT, GL_LIGHTING, glEnable, GL_COLOR_MATERIAL, \
            GL_AMBIENT, GL_SPECULAR, GL_DIFFUSE, glMaterial, GL_FRONT_AND_BACK, \
            GL_AMBIENT_AND_DIFFUSE, GL_FRONT, glColorMaterial, GL_PROJECTION, \
            glMatrixMode, glLoadIdentity, glTexParameterf
    except:
        raise("In order to use the 3D position viewing tool you must pip install PyOpenGL")

    # Tell Pytplot about new window
    window = pytplot.tplot_utilities.get_available_qt_window(name='3D_MARS')
    window.resize(1000, 600)
    window.setWindowTitle('3D Mars Window')

    # Defining a new class that keeps track of spacecraft position and moves the
    class PlanetView(gl.GLViewWidget):
        spacecraft_x = 0
        spacecraft_y = 0
        spacecraft_z = 0
        tvar_name = 'temp' # Store the name of the tplot variable stored, so we know if we need to redraw the orbit
        def paintGL(self, region=None, viewport=None, useItemNames=False):
            glLightfv(GL_LIGHT0, GL_POSITION, [-100000,0,0,0])
            super().paintGL(region=region, viewport=viewport, useItemNames=useItemNames)

    plot1 = PlanetView()

    # Set up the "sun"
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [.3,.3,.3,1.0])
    light_position = [-100000,0,0,0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [1,1,1,0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1,0,0,0])

    # Create Mars and spacecraft icons (assuming spherical spacecraft)
    md = gl.MeshData.sphere(rows=100, cols=220)
    mars = gl.GLMeshItem(meshdata=md, smooth=True, color=(.5, 0, 0, 1), glOptions='opaque')
    mars.translate(0, 0, 0)
    mars.scale(3390, 3390, 3390)
    spacecraft = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 1, 1, 1))
    spacecraft.translate(plot1.spacecraft_x, plot1.spacecraft_y, plot1.spacecraft_z)

    spacecraft.scale(200, 200, 200)
    orbit_path = gl.GLLinePlotItem()
    plot1.addItem(mars)
    plot1.addItem(spacecraft)
    plot1.addItem(orbit_path)
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [.5,.5,.5,1])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Put the planetview plot into the pytplot window
    window.setCentralWidget(plot1)

    # Move around the camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    plot1.setModelview()
    plot1.setCameraPosition(distance=30000, azimuth=0, elevation=0)

    # Turn on the window!
    window.show()

    # Define the function that is called on new hover_time updates
    def update(t,name):
        # Move spacecraft back to 0,0,0
        previous_x = plot1.spacecraft_x
        previous_y = plot1.spacecraft_y
        previous_z = plot1.spacecraft_z
        previous_tvar = plot1.tvar_name

        spacecraft.translate(-1*previous_x, -1*previous_y, -1*previous_z)

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

        if name != previous_tvar:
            import numpy as np
            pathasdf = np.array((x_tvar.data, y_tvar.data, z_tvar.data), dtype=float).T
            orbit_path.setData(pos = pathasdf)


        # Get the nearest x/y/z of the hover time
        new_x = x_tvar.sel(time=t, method='nearest').values
        new_y = y_tvar.sel(time=t, method='nearest').values
        new_z = z_tvar.sel(time=t, method='nearest').values

        # Move the spacecraft
        spacecraft.translate(new_x,new_y,new_z)
        plot1.spacecraft_x, plot1.spacecraft_y, plot1.spacecraft_z = new_x, new_y, new_z
        plot1.tvar_name = name
        plot1.paintGL()

    # Register the above update function to the called functions
    pytplot.hover_time.register_listener(update)

    return


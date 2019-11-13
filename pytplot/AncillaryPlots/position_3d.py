import pytplot

def position_3d(temp=None):
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

    pytplot.pytplotWindows.append(QtGui.QMainWindow())
    pytplot.pytplotWindows[-1].resize(1000, 600)
    pytplot.pytplotWindows[-1].setWindowTitle('Interactive Window')


    class PlanetView(gl.GLViewWidget):
        spacecraft_x = 0
        spacecraft_y = 0
        spacecraft_z = 0
        def paintGL(self, region=None, viewport=None, useItemNames=False):
            glLightfv(GL_LIGHT0, GL_POSITION, [-100000,0,0,0])
            super().paintGL(region=region, viewport=viewport, useItemNames=useItemNames)

    plot1 = PlanetView()
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [.3,.3,.3,1.0])
    light_position = [-100000,0,0,0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [1,1,1,0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1,0,0,0])
    md = gl.MeshData.sphere(rows=100, cols=220)
    mars = gl.GLMeshItem(meshdata=md, smooth=True, color=(.5, 0, 0, 1))
    mars.translate(0, 0, 0)
    mars.scale(3390, 3390, 3390)
    maven = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 1, 1, 1))
    maven.translate(plot1.spacecraft_x, plot1.spacecraft_y, plot1.spacecraft_z)
    maven.scale(100, 100, 100)

    plot1.addItem(mars)
    plot1.addItem(maven)
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [.5,.5,.5,1])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    pytplot.pytplotWindows[-1].setCentralWidget(plot1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    plot1.setModelview()
    plot1.setCameraPosition(distance=30000, azimuth=0, elevation=0)
    pytplot.pytplotWindows[-1].show()

    def update(t,name):
        previous_x = plot1.spacecraft_x
        previous_y = plot1.spacecraft_y
        previous_z = plot1.spacecraft_z
        maven.translate(-1*previous_x, -1*previous_y, -1*previous_z)

        x_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['x']]
        y_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['y']]
        z_tvar = pytplot.data_quants[pytplot.data_quants[name].attrs['plot_options']['links']['z']]

        new_x = x_tvar.sel(time=t, method='nearest').values
        new_y = y_tvar.sel(time=t, method='nearest').values
        new_z = z_tvar.sel(time=t, method='nearest').values

        maven.translate(new_x,new_y,new_z)
        plot1.spacecraft_x, plot1.spacecraft_y, plot1.spacecraft_z = new_x, new_y, new_z
        plot1.paintGL()

    pytplot.hover_time.register_listener(update)
    return


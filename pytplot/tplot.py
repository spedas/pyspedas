# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import sys
import os
import logging
import pytplot
from pytplot import tplot_utilities
import tempfile
from .MPLPlotter.tplot import tplot as mpl_tplot

def webengine_hack():
    """ This function is a hack to resolve an import error. 
    Without this, we sometimes get:
    ImportError: QtWebEngineWidgets must be imported before a QCoreApplication instance is created
    """
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication.instance()
    if app is not None:
        import sip
        app.quit()
        sip.delete(app)
    import sys
    from PyQt5 import QtCore, QtWebEngineWidgets
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.qApp = QtWidgets.QApplication(sys.argv)
    return app


if pytplot.using_graphics:
    from .QtPlotter import PyTPlot_Exporter
    from pyqtgraph.Qt import QtCore, QtGui, QtCore
    import pyqtgraph as pg
    from . import QtPlotter
    from pytplot.AncillaryPlots import spec_slicer
    from pytplot.AncillaryPlots import position_mars_2d
    from pytplot.AncillaryPlots import position_mars_3d

def tplot(name,
          var_label=None,
          slice=False,
          combine_axes=True,
          nb=False,
          save_file=None,
          gui=False,
          qt=False,
          bokeh=False,
          save_png=None,
          display=True,
          testing=False,
          extra_functions=[],
          extra_function_args=[],
          vert_spacing=None,
          pos_2d=False,
          pos_3d=False,
          exec_qt=True,
          window_name='Plot',
          interactive=False,
          # the following are for the matplotlib version
          xsize=None,
          ysize=None,
          save_eps='', 
          save_svg='', 
          save_pdf='',
          save_jpeg='',
          dpi=None,
          fig=None, 
          axis=None, 
          pseudo_plot_num=None, 
          second_axis_size=0.0,
          return_plot_objects=False):
    """
    This is the function used to display the tplot variables stored in memory.  It is a wrapper that
    calls a matplotlib-specific version of tplot.

    Parameters
    ----------
        name : str or list of str, required
            List of tplot variables that will be plotted.
            If this is empty, nothing will be plotted.
        var_label : str, optional
            The name of the tplot variable you would like as
            a second x axis.
        xsize: float, optional
            Plot size in the horizontal direction (in inches)
        ysize: float, optional
            Plot size in the vertical direction (in inches)
        dpi: float, optional
            The resolution of the plot in dots per inch
        save_png : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in a PNG format.
        save_eps : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in a EPS format.
        save_jpeg : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in a JPEG format.
        save_pdf : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in a PDF format.
        save_svg : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in a SVG format.
        display: bool, optional
            If True, then this function will display the plotted tplot variables. Necessary to make this optional
            so we can avoid it in a headless server environment.
        return_plot_objects: bool, optional
            If true, returns the matplotlib fig and axes objects for further manipulation.

    Returns
    -------
        Any
            Returns matplotlib fig and axes objects, if return_plot_objects==True

    Examples
    --------
        >>> #Plot a single line in bokeh
        >>> import pytplot
        >>> x_data = [2,3,4,5,6]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.tplot("Variable1",bokeh=True)

        >>> #Display two plots
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> pytplot.store_data("Variable2", data={'x':x_data, 'y':y_data})
        >>> pytplot.tplot(["Variable1", "Variable2"])

        >>> #Display 2 plots, using Variable1 as another x axis
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pytplot.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        >>> pytplot.options("Variable3", 'spec', 1)
        >>> pytplot.tplot(["Variable2", "Variable3"], var_label='Variable1')

    """
    # If no tplot names were provided, exit
    if name is None or len(name) < 1:
        logging.error("No tplot variables were provided.")
        return
    elif not isinstance(name, list):
        name = [name] # If only one name was provided, put it in a list
    num_plots = len(name)

    if qt == False and bokeh == False:
        return mpl_tplot(name, var_label=var_label,
                         xsize=xsize,
                         ysize=ysize,
                         save_png=save_png,
                         save_eps=save_eps,
                         save_svg=save_svg,
                         save_pdf=save_pdf,
                         save_jpeg=save_jpeg,
                         dpi=dpi,
                         display=display,
                         fig=fig,
                         axis=axis,
                         slice=slice,
                         running_trace_count=pseudo_plot_num,
                         second_axis_size=second_axis_size,
                         return_plot_objects=return_plot_objects)

    # Code below this point should be unreachable, left in for reference purposes
    if interactive:
        slice=True

    if not pytplot.using_graphics and save_file is None:
        print("Qt was not successfully imported.  Specify save_file to save the file as a .html file.")
        return

    # Check a bunch of things
    for i in range(num_plots):
        if isinstance(name[i], int):
            name[i] = list(pytplot.data_quants.keys())[name[i]]
        if name[i] not in pytplot.data_quants.keys():
            logging.info(str(name[i]) + " is currently not in pytplot")
            return

    if isinstance(var_label, int):
        var_label = list(pytplot.data_quants.keys())[var_label]

    if vert_spacing is None:
        if 'vertical_spacing' in pytplot.tplot_opt_glob:
            vert_spacing = pytplot.tplot_opt_glob['vertical_spacing']
        else:
            vert_spacing = 25 # Just a default that looks ok

    if bokeh:
        logging.error("This version of pytplot no longer supports Bokeh plotting.")
    else:
        if save_png is not None:
            layout = QtPlotter.generate_stack(name, var_label=var_label, combine_axes=combine_axes, vert_spacing=vert_spacing)
            layout.resize(pytplot.tplot_opt_glob['window_size'][0], pytplot.tplot_opt_glob['window_size'][1])
            for i, item in enumerate(layout.items()):
                if type(item) == pg.graphicsItems.GraphicsLayout.GraphicsLayout:
                    layout.items()[i].resize(pytplot.tplot_opt_glob['window_size'][0],
                                             pytplot.tplot_opt_glob['window_size'][1])
            exporter = PyTPlot_Exporter.PytplotExporter(layout)
            exporter.parameters()['width'] = pytplot.tplot_opt_glob['window_size'][0]
            exporter.parameters()['height'] = pytplot.tplot_opt_glob['window_size'][1]
            exporter.export(save_png)

        if display:
            # This layout is used when the user wants a png image saved.
            layout_orig = QtPlotter.generate_stack(name, var_label=var_label, combine_axes=combine_axes, vert_spacing=vert_spacing)
            layout_orig.resize(pytplot.tplot_opt_glob['window_size'][0], pytplot.tplot_opt_glob['window_size'][1])
            for i, item in enumerate(layout_orig.items()):
                if type(item) == pg.graphicsItems.GraphicsLayout.GraphicsLayout:
                    layout_orig.items()[i].resize(pytplot.tplot_opt_glob['window_size'][0],
                                                  pytplot.tplot_opt_glob['window_size'][1])

            try: #TODO: This exporter requires h5py to be installed because that is what pyqtgraph requires.
                exporter = QtPlotter.PytplotExporter(layout_orig)
            except:
                exporter = None

            # Set up displayed plot window and grab plots to plot on it
            available_qt_window = tplot_utilities.get_available_qt_window(name=window_name)
            layout = QtPlotter.generate_stack(name, var_label=var_label, combine_axes=combine_axes, vert_spacing=vert_spacing)

            available_qt_window.newlayout(layout)
            available_qt_window.resize(pytplot.tplot_opt_glob['window_size'][0],
                                       pytplot.tplot_opt_glob['window_size'][1])

            # Implement button that lets you save the PNG
            available_qt_window.init_savepng(exporter)

            # Show the plot window and plot
            available_qt_window.show()
            available_qt_window.activateWindow()

            # This function is responsible for calling all of the extra plotting routines that a user might like with
            # their data plots
            extra_function_handler(extra_functions, extra_function_args, name, slice, pos_2d, pos_3d)

            if testing:
                return

            # (hasattr(sys, 'ps1')) checks to see if we're in ipython
            if (not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION')) and exec_qt:
                QtGui.QApplication.instance().exec_()
                pass
            else:
                try:
                    magic = get_ipython().magic
                    magic(u'%gui qt5')
                except:
                    pass
        return


def extra_function_handler(extra_functions, extra_functions_args, names, slice, pos_2d, pos_3d):
    functions_to_call = extra_functions
    function_args_to_call = extra_functions_args
    # Handles the old way of calling the spec slicing plots, (if anyone still uses that way)
    if slice:
        # Call 2D spice slicing window; This will only plot something when spectrograms are involved.
        functions_to_call.append(spec_slicer.spec_slicer)
        function_args_to_call.append([None, None, True])

    if pos_2d:
        functions_to_call.append(position_mars_2d.position_mars_2d)
        function_args_to_call.append([None])
    if pos_3d:
        functions_to_call.append(position_mars_3d.position_mars_3d)
        function_args_to_call.append([None])

    static_list = [i for i in names if 'static' in pytplot.data_quants[i].attrs['plot_options']['extras']]
    for tplot_var in static_list:
        # Call 2D static window; This will only plot something when spectrograms are involved.
        functions_to_call.append(spec_slicer.spec_slicer)
        function_args_to_call.append(
            [tplot_var, pytplot.data_quants[tplot_var].attrs['plot_options']['extras']['static'],
             False])

    static_tavg_list = [i for i in names if 'static_tavg' in pytplot.data_quants[i].attrs['plot_options']['extras']]
    for tplot_var in static_tavg_list:
        # Call 2D static window for time-averaged values; This will only plot something when spectrograms
        # are involved
        functions_to_call.append(spec_slicer.spec_slicer)
        function_args_to_call.append([tplot_var,pytplot.data_quants[tplot_var].attrs['plot_options']['extras']['static_tavg'],
                             False])

    for f, args in zip(functions_to_call, function_args_to_call):
        f(*args)
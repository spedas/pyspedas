# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import sys
import os
import pytplot
from bokeh.io import output_file, show, output_notebook, save
from . import HTMLPlotter
from bokeh.embed import components
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
    This is the function used to display the tplot variables stored in memory.
    The default output is to show the plots stacked on top of one another inside of a qt window

    Parameters:
        name : str / list
            List of tplot variables that will be plotted
        var_label : str, optional
            The name of the tplot variable you would like as
            a second x axis.
        slice : bool, optional
            If True, a secondary interactive plot will be generated next to spectrogram plots.
            Mousing over the spectrogram will display a slice of data from that time on the
            interactive chart.
        combine_axes : bool, optional
            If True, the axes are combined so that they all display the same x range.  This also enables
            scrolling/zooming/panning on one plot to affect all of the other plots simultaneously.
        nb : bool, optional
            If True, the plot will be displayed inside of a current Jupyter notebook session.
        save_file : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in an HTML format.
            The plots can then be opened and viewed on any browser without any requirements.
        bokeh : bool, optional
            If True, plots data using bokeh
            Else (bokeh=False or omitted), plots data using PyQtGraph
        extra_functions: func, optional
            This is an extra function that gets called just prior to the data being plotted.  This is useful if you'd
            like to build your own Qt display that reacts to the mouse movement.  Built in displays can be found in the
            AncillaryPlots folder.
        extra_function_args: list of tuples, optional
            These are the arguments to give your extra_functions
        vert_spacing: int
            Thes distance in pixels you'd like the plots to be
        gui : bool, optional
            If True, then this function will output the 2 HTML components of the generated plots as string variables.
            This is useful if you are embedded the plots in your own GUI.  For more information, see
            http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html
        qt : bool, optional
            If True, then this function will display the plot inside of the Qt window.  From this window, you
            can choose to export the plots as either an HTML file, or as a PNG.
        save_png : str, optional
            A full file name and path.
            If this option is set, the plot will be automatically saved to the file name provided in a PNG format.
        display: bool, optional
            If True, then this function will display the plotted tplot variables. Necessary to make this optional
            so we can avoid it in a headless server environment.
        testing: bool, optional
            If True, doesn't run the '(hasattr(sys, 'ps1'))' line that makes plots interactive - i.e., avoiding issues

    Returns:
        None

    Examples:
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

        >>> #Plot all 3 tplot variables, sending the output to an HTML file
        >>> pytplot.tplot(["Variable1", "Variable2", "Variable3"], save_file='C:/temp/pytplot_example.html')

        >>> #Plot all 3 tplot variables, sending the HTML output to a pair of strings
        >>> div, component = pytplot.tplot(["Variable1", "Variable2", "Variable3"], gui=True)
    """

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
                               pseudo_plot_num=pseudo_plot_num, 
                               second_axis_size=second_axis_size,
                               return_plot_objects=return_plot_objects)

    if interactive:
        slice=True

    if not pytplot.using_graphics and save_file is None:
        print("Qt was not successfully imported.  Specify save_file to save the file as a .html file.")
        return
    # Check a bunch of things
    if not isinstance(name, list):
        name = [name]
        num_plots = 1
    else:
        num_plots = len(name)

    for i in range(num_plots):
        if isinstance(name[i], int):
            name[i] = list(pytplot.data_quants.keys())[name[i]]
        if name[i] not in pytplot.data_quants.keys():
            print(str(name[i]) + " is currently not in pytplot")
            return

    if isinstance(var_label, int):
        var_label = list(pytplot.data_quants.keys())[var_label]

    if vert_spacing is None:
        if 'vertical_spacing' in pytplot.tplot_opt_glob:
            vert_spacing = pytplot.tplot_opt_glob['vertical_spacing']
        else:
            vert_spacing = 25 # Just a default that looks ok

    if bokeh:
        layout = HTMLPlotter.generate_stack(name, var_label=var_label, combine_axes=combine_axes,
                                            slice=slice)
        # Output types
        if gui:
            script, div = components(layout)
            return script, div
        elif nb:
            output_notebook()
            show(layout)
            return
        elif save_file is not None:
            output_file(save_file, mode='inline')
            save(layout)
            return
        elif qt:
            try:
                from PyQt5.QtWebKitWidgets import QWebView as WebView
            except:
                try:
                    from PyQt5.QtWebEngineWidgets import QWebEngineView as WebView
                except:
                    app = webengine_hack()
                    from PyQt5.QtWebEngineWidgets import QWebEngineView as WebView
            available_qt_window = tplot_utilities.get_available_qt_window()
            dir_path = tempfile.gettempdir()  # send to user's temp directory
            output_file(os.path.join(dir_path, "temp.html"), mode='inline')
            save(layout)
            new_layout = WebView()
            available_qt_window.resize(pytplot.tplot_opt_glob['window_size'][0] + 100,
                                       pytplot.tplot_opt_glob['window_size'][1] + 100)
            new_layout.resize(pytplot.tplot_opt_glob['window_size'][0], pytplot.tplot_opt_glob['window_size'][1])
            dir_path = tempfile.gettempdir()  # send to user's temp directory
            new_layout.setUrl(QtCore.QUrl.fromLocalFile(os.path.join(dir_path, "temp.html")))
            available_qt_window.newlayout(new_layout)
            available_qt_window.show()
            available_qt_window.activateWindow()
            if testing:
                return
            if not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()
            else:
                try:
                    magic = get_ipython().magic
                    magic(u'%gui qt5')
                except:
                    pass
            return
        else:
            dir_path = tempfile.gettempdir()  # send to user's temp directory
            output_file(os.path.join(dir_path, "temp.html"), mode='inline')
            if not testing:
                show(layout)
            return
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
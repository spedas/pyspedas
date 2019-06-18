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

if pytplot.using_graphics:
    from .QtPlotter import PyTPlot_Exporter
    from pyqtgraph.Qt import QtCore, QtGui, QtCore
    import pyqtgraph as pg
    from . import QtPlotter
    from pytplot.AncillaryPlots import spec_slicer

    try:
        from PyQt5.QtWebKitWidgets import QWebView as WebView
    except:
        from PyQt5.QtWebEngineWidgets import QWebEngineView as WebView


def tplot(name,
          var_label=None,
          auto_color=True,
          interactive=False,
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
          vert_spacing=None):
    """
    This is the function used to display the tplot variables stored in memory.
    The default output is to show the plots stacked on top of one another inside a GUI window.
    The GUI window has the option to export the plots in either PNG or HTML formats.

    .. note::
        This plotting routine uses the python Bokeh library, which creates plots using HTML and Javascript.
        Bokeh is technically still in beta, so future patches to Bokeh may require updates to this function.

    Parameters:
        name : str / list
            List of tplot variables that will be plotted
        var_label : str, optional
            The name of the tplot variable you would like as
            a second x axis.
        auto_color : bool, optional
            Automatically color the plot lines.
        interactive : bool, optional
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
            print(str(i) + " is currently not in pytplot")
            return

    if isinstance(var_label, int):
        var_label = list(pytplot.data_quants.keys())[var_label]

    if vert_spacing is None:
        if 'vertical_spacing' in pytplot.tplot_opt_glob:
            vert_spacing = pytplot.tplot_opt_glob['vertical_spacing']
        else:
            vert_spacing = 25 # Just a default that looks ok

    if bokeh:
        layout = HTMLPlotter.generate_stack(name, var_label=var_label, auto_color=auto_color, combine_axes=combine_axes,
                                            interactive=interactive)
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
            available_qt_window = tplot_utilities.get_available_qt_window()
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
            extra_function_handler(extra_functions, extra_function_args, name, interactive)

            # plots the plots!
            if testing:
                return

            # (hasattr(sys, 'ps1')) checks to see if we're in ipython
            if not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()

        return


def extra_function_handler(extra_functions, extra_functions_args, names, interactive):

    # Handles the old way of calling the spec slicing plots, (if anyone still uses that way)
    if interactive:
        # Call 2D interactive window; This will only plot something when spectrograms are involved.
        extra_functions.append(spec_slicer.spec_slicer)
        extra_functions_args.append([None, None, True])

    static_list = [i for i in names if 'static' in pytplot.data_quants[i].attrs['plot_options']['extras']]
    for tplot_var in static_list:
        # Call 2D static window; This will only plot something when spectrograms are involved.
        extra_functions.append(spec_slicer.spec_slicer)
        extra_functions_args.append(
            [tplot_var, pytplot.data_quants[tplot_var].attrs['plot_options']['extras']['static'],
             False])

    static_tavg_list = [i for i in names if 'static_tavg' in pytplot.data_quants[i].attrs['plot_options']['extras']]
    for tplot_var in static_tavg_list:
        # Call 2D static window for time-averaged values; This will only plot something when spectrograms
        # are involved
        extra_functions.append(spec_slicer.spec_slicer)
        extra_functions_args.append([tplot_var,pytplot.data_quants[tplot_var].attrs['plot_options']['extras']['static_tavg'],
                             False])

    for f, args in zip(extra_functions, extra_functions_args):
        f(*args)
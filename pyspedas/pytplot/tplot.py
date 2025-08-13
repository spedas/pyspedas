# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import sys
import os
import logging
import pyspedas
import tempfile
from .MPLPlotter.tplot import tplot as mpl_tplot


using_graphics = False  # there doesn't seem to be an execution path that make this true

def tplot(name,
          trange=None,
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
        trange: list of string or float, optional
            If set, this time range will be used, temporarily overriding any previous xlim or timespan calls
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
        >>> import pyspedas
        >>> x_data = [2,3,4,5,6]
        >>> y_data = [1,2,3,4,5]
        >>> pyspedas.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pyspedas.tplot("Variable1",bokeh=True)

        >>> #Display two plots
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> pyspedas.store_data("Variable2", data={'x':x_data, 'y':y_data})
        >>> pyspedas.tplot(["Variable1", "Variable2"])

        >>> #Display 2 plots, using Variable1 as another x axis
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pyspedas.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        >>> pyspedas.options("Variable3", 'spec', 1)
        >>> pyspedas.tplot(["Variable2", "Variable3"], var_label='Variable1')

    """
    # If no tplot names were provided, exit
    if name is None or len(name) < 1:
        logging.error("no valid tplot variables were provided.")
        return
    elif not isinstance(name, list):
        name = [name] # If only one name was provided, put it in a list
    num_plots = len(name)

    if qt == False and bokeh == False:
        return mpl_tplot(name,
                         trange=trange,
                         var_label=var_label,
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

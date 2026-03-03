from pyspedas.tplot_tools import tplot_wildcard_expand, get_data, get_coords, get_units
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from .save_plot import save_plot

def tplotxy(tvars,
            plane='xy',
            center_origin=True,
            reverse_x = False,
            reverse_y = False,
            plot_units='re',
            title=None,
            colors=('k', 'b', 'g', 'r', 'c', 'm', 'y'),
            linestyles=('solid'),
            linewidths=(None),
            markers=(None),
            startmarkers=(None),
            endmarkers=(None),
            markevery=10,
            markersize=5,
            legend_names=None,
            legend_location='upper right',
            show_centerbody=True,
            centerbody_size_re=1.0,
            save_png='',
            save_eps='',
            save_jpeg='',
            save_pdf='',
            save_svg='',
            dpi=300,
            display=True,
            fig=None,
            axis=None,
            ):
    """
    Plot one or more 3d tplot variables, by projecting them onto one of the coordinate planes XY, XY, or YZ.

    Parameters
    ----------
    tvars: string or list of strings
        Tplot variables to be plotted (wildcards accepted).  The data array should be ntimesx3,
        or in the case of field line plots, ntimesxnpointsx3
    plane: string or list of strings
        Plane to project the 3d vectors onto. Valid options: 'xy', 'xz', 'yz'. Default: 'xy'
    center_origin: bool
        If True, center the plot on the origin.
    reverse_x: bool
        If True, reverse the x-axis of the plot (more positive values to the left).  This is handy
        for GSE-like orbit plots if you want the sun depicted toward the left
    reverse_y: bool
        If True, reverse the y-axis of the plot (more positive values to the bottom)
        If reverse_x is set, and you're projecting onto the xy plane, this keeps the coordinate system right-handed.
    colors: list or tuple of strings
        Colors to use if multiple variables are plotted. Default: ('k', 'b', 'g', 'r', 'c', 'm', 'y').
        If number of variables exceeds number of colors, they will cycle.
    linestyles: list or tuple of strings
        Line styles to use for each variable. Default: ('solid').
        If number of variables exceeds number of linestyles, they will cycle.
    linewidths: list or tuple of strings
        Line widths to use for each variable. If number of variables exceeds number of linewidths, they will cycle.
        Default: (None) (use matplotlib default)
    markers: list or tuple of str
        marker style for the data points (default: (None))
    startmarkers: list or tuple of str
        marker style for the start of each trace (default: (None))
    endmarkers: list or tuple of str
        marker style for the end of each trace (default: (None))
    markevery: int or sequence of int
        plot a marker at every n-th data point (default: 10)
    markersize: float
        size of the marker in points (default: 5)
    legend_names: list of str
        If set, labels to use in the plot legend.
    legend_location: str
        Placement of legend relative to the plot window.
    show_centerbody: bool
        If True, draw the central body at the origin
    centerbody_size_re: float
        The size in Re of the center body. Default: 1.0
    save_png : str, optional
        A full file name and path.
        If this option is set, the plot will be automatically saved to the file name provided in PNG format.
    save_eps : str, optional
        A full file name and path.
        If this option is set, the plot will be automatically saved to the file name provided in EPS format.
    save_jpeg : str, optional
        A full file name and path.
        If this option is set, the plot will be automatically saved to the file name provided in JPEG format.
    save_pdf : str, optional
        A full file name and path.
        If this option is set, the plot will be automatically saved to the file name provided in PDF format.
    save_svg : str, optional
        A full file name and path.
        If this option is set, the plot will be automatically saved to the file name provided in SVG format.
    dpi: float, optional
        The resolution of the plot in dots per inch
    display: bool, optional
        If True, then this function will display the plotted tplot variables. Use False to suppress display (for example, if
        saving to a file, or returning plot objects to be displayed later). Default: True
    fig: Matplotlib figure object
        Use an existing figure to plot in (mainly for recursive calls to render composite variables)
    axis: Matplotlib axes object
        Use an existing set of axes to plot on (mainly for recursive calls to render composite variables)


    Returns
    -------
    None
    """

    tvars = tplot_wildcard_expand(tvars)
    if len(tvars) < 1:
        logging.error("No matching variables found to plot")
        return

    plane = plane.lower()
    if plane not in ['xy', 'xz', 'yz']:
        logging.error(f'Invalid plane {plane}: must be one of "xy", "xz", "yz"')
        return
    # Get maximum range of each variable to set plot x/y range
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0

    xsize=4.0
    ysize=4.0

    if not isinstance(colors, (list, np.ndarray,tuple)):
        colors = [colors]
    if not isinstance(markers, (list, np.ndarray,tuple)):
        markers = [markers]
    if not isinstance(startmarkers, (list, np.ndarray,tuple)):
        startmarkers = [startmarkers]
    if not isinstance(endmarkers, (list, np.ndarray,tuple)):
        endmarkers = [endmarkers]
    if not isinstance(linestyles, (list, np.ndarray,tuple)):
        linestyles = [linestyles]
    if not isinstance(linewidths, (list, np.ndarray,tuple)):
        linewidths = [linewidths]

    if legend_names is not None:
        if not isinstance(legend_names, (list, np.ndarray,tuple)):
            legend_names = [legend_names]
        if len(legend_names) != len(tvars):
            logging.warning(f"Length of legend_names ({len(legend_names)}) does not match length of tvars ({len(tvars)}), disabling legends")
            legend_names= None

    if fig is None and axis is None:
        fig, axis = plt.subplots(sharey=True, sharex=True, figsize=(xsize, ysize), layout='constrained')

    if title is not None and title != '':
        fig.suptitle(title)

    km_in_re = 6371.2
    if plot_units is None:
        plot_units = get_units(tvars[0])
    if isinstance(plot_units, (list, np.ndarray)):
        plot_units = plot_units[0]
    if plot_units is None:
        plot_units = 'None'
        unit_annotation=""
    else:
        unit_annotation=f' ({plot_units})'

    plot_coords = get_coords(tvars[0])
    if plot_coords is None:
        plot_coords = 'Unknown'
        coord_annotation=""
    else:
        coord_annotation=f"-{plot_coords}"

    full_annotation=coord_annotation+unit_annotation

    if plane=='xy':
        axis.set_xlabel('X' + full_annotation)
        axis.set_ylabel('Y' + full_annotation)

    elif plane=='xz':
        axis.set_xlabel('X' + full_annotation)
        axis.set_ylabel('Z' + full_annotation)

    elif plane=='yz':
        axis.set_xlabel('Y' + full_annotation)
        axis.set_ylabel('Z' + full_annotation)

    for index,tvar in enumerate(tvars):
        units=get_units(tvar)
        if isinstance(plot_units, (list, np.ndarray)):
            units=units[0]
        if units is None:
            units="None"
        unit_conv = 1.0
        if plot_units.lower() == 'km':
            if units.lower() == 'km':
                unit_conv = 1.0
            elif units.lower() == 're':
                unit_conv = km_in_re
            else:
                logging.warning(f"Input variable {tvar} has units {units}, unable to convert to plot_units {plot_units}")
        elif plot_units.lower() == 're':
            if units.lower() == 'km':
                unit_conv = 1.0/km_in_re
            elif units.lower() == 're':
                unit_conv = 1.0
            else:
                logging.warning(f"Input variable {tvar} has units {units.lower()}, unable to convert to plot_units {plot_units.lower()}")
        elif plot_units.lower() != units.lower():
                logging.warning(f"Input variable {tvar} has units {units.lower()}, unable to convert to plot_units {plot_units.lower}")
        d=get_data(tvar)
        ndim = len(d.y.shape)
        if ndim == 2: # orbits, foot points, hodograms, etc
            if plane=='xy':
                proj_x = d.y[:,0] * unit_conv
                proj_y = d.y[:,1] * unit_conv

            elif plane=='xz':
                proj_x = d.y[:,0] * unit_conv
                proj_y = d.y[:,2] * unit_conv

            elif plane=='yz':
                proj_x = d.y[:,1] * unit_conv
                proj_y = d.y[:,2] * unit_conv
        elif ndim == 3: # multiple field line traces
            if plane == 'xy':
                proj_x = d.y[:,:, 0] * unit_conv
                proj_y = d.y[:,:, 1] * unit_conv

            elif plane == 'xz':
                proj_x = d.y[:,:, 0] * unit_conv
                proj_y = d.y[:,:, 2] * unit_conv

            elif plane == 'yz':
                proj_x = d.y[:,:, 1] * unit_conv
                proj_y = d.y[:,:, 2] * unit_conv
        else:
            logging.error(f"Input variable {tvar} with {ndim} dimensions is not supported")
            return None

        local_xmax = np.nanmax(proj_x)
        local_ymax = np.nanmax(proj_y)
        local_xmin = np.nanmin(proj_x)
        local_ymin = np.nanmin(proj_y)

        max_x = np.nanmax([local_xmax, max_x])
        max_y = np.nanmax([local_ymax, max_y])
        min_x = np.nanmin([local_xmin, min_x])
        min_y = np.nanmin([local_ymin, min_y])

        n_colors = len(colors)
        thiscolor = colors[index % n_colors]
        n_styles = len(linestyles)
        thisstyle = linestyles[index % n_styles]
        n_widths = len(linewidths)
        thiswidth = linewidths[index % n_widths]
        n_markers = len(markers)
        thismarker = markers[index % n_markers]
        n_startmarkers = len(startmarkers)
        thisstartmarker = startmarkers[index % n_startmarkers]
        n_endmarkers = len(endmarkers)
        thisendmarker = endmarkers[index % n_endmarkers]

        this_line = axis.plot(proj_x, proj_y, color=thiscolor, linestyle=thisstyle, linewidth=thiswidth, marker=thismarker, markersize=markersize, markevery=markevery)
        if thisstartmarker is not None:
            axis.plot(proj_x[0], proj_y[0], color=thiscolor, linestyle=thisstyle, marker=thisstartmarker, markersize=markersize)
        if thisendmarker is not None:
            axis.plot(proj_x[-1], proj_y[-1], color=thiscolor, linestyle=thisstyle, marker=thisendmarker, markersize=markersize)

        if legend_names is not None:
            try:
                if isinstance(this_line, list):
                    this_line[0].set_label(legend_names[index])
                else:
                    this_line.set_label(legend_names[index])
            except IndexError:
                continue

    if center_origin:
        x_halfwidth = np.nanmax(np.abs([max_x, min_x]))
        y_halfwidth = np.nanmax(np.abs([max_y, min_y]))
        # Add 5% to each boundary to give a little margin
        all_halfwidth = 1.05 * np.nanmax([x_halfwidth, y_halfwidth])
        axis.set_xlim((-all_halfwidth, all_halfwidth))
        axis.set_ylim((-all_halfwidth, all_halfwidth))
    else:
        # Adjust the X and Y ranges by equal increments to give a little margin
        x_adjust = .05*(max_x - min_x)
        y_adjust = .05*(max_y - min_y)
        all_adjust = np.nanmax([x_adjust, y_adjust])
        xr = (min_x-all_adjust, max_x+all_adjust)
        yr = (min_y-all_adjust, max_y+all_adjust)
        axis.set_xlim(xr)
        axis.set_ylim(yr)

    if show_centerbody:
        if plot_units == 're':
            cb_radius = centerbody_size_re
        else:
            cb_radius = centerbody_size_re * km_in_re

        theta1, theta2 = -90, 90
        if plane=='xy' or plane=='xz':
            w1 = Wedge((0, 0), cb_radius, theta1, theta2, fc='white', edgecolor='black')
            w2 = Wedge((0, 0), cb_radius, theta2, theta1, fc='black', edgecolor='black')
            axis.add_artist(w1)
            axis.add_artist(w2)
        else:
            theta1,theta2 = 0,360
            w1 = Wedge((0, 0), cb_radius, theta1, theta2, fc='white', edgecolor='black')
            axis.add_artist(w1)

    axis.set_aspect('equal')
    if reverse_x:
        axis.invert_xaxis()
    if reverse_y:
        axis.invert_yaxis()

    if legend_names is not None:
        legend = axis.legend(loc=legend_location, markerfirst=True)

    fig.canvas.draw()

    save_plot(save_png=save_png, save_eps=save_eps, save_jpeg=save_jpeg, save_pdf=save_pdf, save_svg=save_svg, dpi=dpi)

    if display:
        plt.show()



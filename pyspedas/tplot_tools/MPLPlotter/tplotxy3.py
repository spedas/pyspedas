from pyspedas.tplot_tools import tplot_wildcard_expand, get_data, get_coords, get_units, set_coords, set_units, store_data
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from .save_plot import save_plot

km_in_re = 6371.2

def tplotxy3_add_mpause(x,
                        y,
                        fig=None,
                        legend_name=None,
                        color='k',
                        linestyle='solid',
                        linewidth=1,
                        units='re',
                        display=False,
                        save_png='',
                        save_eps='',
                        save_jpeg='',
                        save_pdf='',
                        save_svg='',
                        dpi=300,
                        ):
    """
    Add a magnetopause boundary or similar structure to a tplotxy3 figure

    This utility adds a magnetopause, bow shock, or similar structure to the XZ and XY planes of a tplotxy3 figure.
    The assumptions are that the structure is rotationally symmetric about the X axis, and the boundary
    is given by arrays of X and Y coordinates.

    The plot is assumed to be in units of either km or re.

    The plot X/Y/Z ranges will not be affected when the data is plotted.

    Parameters
    ----------
    x: array of floats
        The X coordinates of the boundary, presumably in GSE or GSM coordinates.
    y: array of floats
        The Y coordinates of the boundary, presumably in GSE or GSM coordinates.
    fig:
        The matplotlib figure object containing the panels to be updated.
    legend_name: str
        The string to add to the legend.
    color: str
        The color of the line to be plotted
    linestyle: str
        The style of the line to be plotted (e.g. 'solid', 'dotted', etc)
    linewidth: int
        The width of the line to be plotted
    units: str
        The units of the boundary position (default: Re)
    display: bool
        If True, display the figure after updating. Default: False
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

    Note
    ====

    If you intend to add other elements like neutral sheet or magnetopause boundaries, be sure to
    use display=False until the final element is added.  Otherwise, closing the plot window will
    destroy the matplotlib plot objects and cause blank plots.

    Returns
    -------
    None
    """

    if fig is None:
        logging.error("No figure provided")
        return

    # Get axes and properties stored in the fig object

    xy_plane = fig.xy_plane
    xz_plane = fig.xz_plane
    yz_plane = fig.yz_plane
    plot_units = fig.plot_units

    unit_conv = 1.0

    if units.lower() != plot_units.lower():
        if units.lower() == 're':
            unit_conv = km_in_re
        else:
            unit_conv = 1.0/km_in_re

    # Ensure that the axes don't autoscale when adding the new trace
    xy_plane.autoscale(False, axis='both')
    xz_plane.autoscale(False, axis='both')

    # Plot the trace on each plane

    xy_plane.plot(x*unit_conv, y*unit_conv, color=color, linestyle=linestyle, linewidth=linewidth)
    this_line = xz_plane.plot(x*unit_conv, y*unit_conv, color=color, linestyle=linestyle, linewidth=linewidth)

    if legend_name is not None and legend_name != '':
        fig.legend().remove()
        try:
            if isinstance(this_line, list):
                this_line[0].set_label(legend_name)
            else:
                this_line.set_label(legend_name)
        except IndexError:
            pass

        # Align the top of the legend box with the top of the XY subplot, and the right of the legend box with the right of
        # the YZ subplot

        bbox1 = xy_plane.get_position()
        bbox2 = yz_plane.get_position()

        legend_bbox_top = bbox1.y1
        legend_bbox_right = bbox2.x1

        handles, labels = xz_plane.get_legend_handles_labels()
        legend = fig.legend(handles, labels, loc="upper right", markerfirst=True, bbox_to_anchor=(legend_bbox_right, legend_bbox_top), framealpha=1.0)

    fig.canvas.draw()

    save_plot(save_png=save_png, save_eps=save_eps, save_jpeg=save_jpeg, save_pdf=save_pdf, save_svg=save_svg, dpi=dpi)

    if display:
        plt.show()

def tplotxy3_add_neutral_sheet( x,
                                y,
                                fig=None,
                                legend_name=None,
                                color='k',
                                linestyle='solid',
                                linewidth=1,
                                units='re',
                                display=False,
                                save_png='',
                                save_eps='',
                                save_jpeg='',
                                save_pdf='',
                                save_svg='',
                                dpi=300,
                                ):
    """
    Add a neutral or similar structure to a tplotxy3 figure

    This utility adds a neutral sheet or similar structure to the XZ plane of a tplotxy3 figure.
    The boundary is given by arrays of X and Z coordinates.

    The plot is assumed to be in units of either km or re.

    The plot X/Y/Z ranges will not be affected when the data is plotted.

    Parameters
    ----------
    x: array of floats
        The X coordinates of the boundary, presumably in GSE or GSM coordinates.
    y: array of floats
        The Y coordinates of the boundary, presumably in GSE or GSM coordinates.
    fig:
        The matplotlib figure object containing the panels to be updated.
    legend_name: str
        The string to add to the legend.
    color: str
        The color of the line to be plotted
    linestyle: str
        The style of the line to be plotted (e.g. 'solid', 'dotted', etc)
    linewidth: int
        The width of the line to be plotted
    units: str
        The units of the boundary position (default: Re)
    display: bool
        If True, display the figure after updating. Default: False
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

    Note
    ====

    If you intend to add other elements like neutral sheet or magnetopause boundaries, be sure to
    use display=False until the final element is added.  Otherwise, closing the plot window will
    destroy the matplotlib plot objects and cause blank plots.

    Returns
    -------
    None
    """

    if fig is None:
        logging.error("No figure provided")
        return

    # Get axes and properties stored in the fig object

    xz_plane = fig.xz_plane
    xy_plane = fig.xy_plane # We will need this to properly position the legend box
    yz_plane = fig.yz_plane

    plot_units = fig.plot_units

    unit_conv = 1.0

    if units.lower() != plot_units.lower():
        if units.lower() == 're':
            unit_conv = km_in_re
        else:
            unit_conv = 1.0/km_in_re

    # Ensure that the axes don't autoscale when adding the new trace
    xz_plane.autoscale(False, axis='both')

    # Plot the trace on each plane

    this_line = xz_plane.plot(x*unit_conv, y*unit_conv, color=color, linestyle=linestyle, linewidth=linewidth)

    if legend_name is not None and legend_name != '':
        fig.legend().remove()
        try:
            if isinstance(this_line, list):
                this_line[0].set_label(legend_name)
            else:
                this_line.set_label(legend_name)
        except IndexError:
            pass

        # Align the top of the legend box with the top of the XY subplot, and the right of the legend box with the right of
        # the YZ subplot

        bbox1 = xy_plane.get_position()
        bbox2 = yz_plane.get_position()

        legend_bbox_top = bbox1.y1
        legend_bbox_right = bbox2.x1

        handles, labels = xz_plane.get_legend_handles_labels()
        legend = fig.legend(handles, labels, loc="upper right", markerfirst=True,bbox_to_anchor=(legend_bbox_right,legend_bbox_top),framealpha=1.0)

    fig.canvas.draw()

    save_plot(save_png=save_png, save_eps=save_eps, save_jpeg=save_jpeg, save_pdf=save_pdf, save_svg=save_svg, dpi=dpi)
    if display:
        plt.show()


def tplotxy3(tvars,
            center_origin=True,
            reverse_x = False,
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
    Plot one or more 3d tplot variables, by projecting them onto the three coordinate axes planes in a single figure.

    Parameters
    ----------
    tvars: string or list of strings
        Tplot variables to be plotted (wildcards accepted).  The data array should be ntimesx3,
        or in the case of field line plots, ntimesxnpointsx3
    center_origin: bool
        If True, center the plot on the origin.
    reverse_x: bool
        If True, reverse the x-axis of the plot (more positive values to the left).
        For plots in GSE-like coordinates, this puts the sun to the left instead of the right.
        It will also reverse the Y axis of the upper left (XY) plot.
    plot_units: str
        The units to use for the plot (default: 're').
    title: str
        The title to use for the plot.
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


    Note
    ====

    If you intend to add other elements like neutral sheet or magnetopause boundaries, be sure to
    use display=False until the final element is added.  Otherwise, closing the plot window will
    destroy the matplotlib plot objects and cause blank plots.

    Returns
    -------
    Matplotlib fig object
    """

    tvars = tplot_wildcard_expand(tvars)
    if len(tvars) < 1:
        logging.error("No matching variables found to plot")
        return None

    # Get maximum range of each variable to set plot x/y range
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    max_z = 0
    min_z = 0

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
        fig, axis = plt.subplots(nrows=2, ncols=2, sharey='row', sharex='col', figsize=(2.5*xsize, 2.5*ysize), constrained_layout=True)

    xy_plane = axis[0,0]
    xz_plane = axis[1,0]
    yz_plane = axis[1,1]
    blank_plane = axis[0,1]

    # Save the plottable axes in the fig object in case we need to modify the plot later
    fig.xy_plane = xy_plane
    fig.xz_plane = xz_plane
    fig.yz_plane = yz_plane

    if title is not None and title != '':
        fig.suptitle(title)

    if plot_units is None:
        plot_units = get_units(tvars[0])
    if isinstance(plot_units, (list, np.ndarray)):
        plot_units = plot_units[0]
    if plot_units is None:
        plot_units = 'None'
        unit_annotation=""
    else:
        unit_annotation=f' ({plot_units}) '

    fig.plot_units = plot_units

    plot_coords = get_coords(tvars[0])
    if plot_coords is None:
        plot_coords = 'Unknown'
        coord_annotation=""
    else:
        coord_annotation=f"-{plot_coords}"
    fig.plot_coords = plot_coords

    full_annotation=coord_annotation+unit_annotation

    xy_plane.set_xlabel('X' + full_annotation)
    xy_plane.set_ylabel('Y' + full_annotation)

    xz_plane.set_xlabel('X' + full_annotation)
    xz_plane.set_ylabel('Z' + full_annotation)

    yz_plane.set_xlabel('Y' + full_annotation)
    yz_plane.set_ylabel('Z' + full_annotation)

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

        ndims = len(d.y.shape)
        if ndims == 2: # orbits, hodograms, etc
            proj_x = d.y[:,0] * unit_conv
            proj_y = d.y[:,1] * unit_conv
            proj_z = d.y[:,2] * unit_conv
        elif ndims == 3: # multiple field line traces
            proj_x = d.y[:,:,0] * unit_conv
            proj_y = d.y[:,:,1] * unit_conv
            proj_z = d.y[:,:,2] * unit_conv
        else:
            logging.error(f"Input variable {tvar} with {ndims} dimensions is not supported")
            return None


        local_xmax = np.nanmax(proj_x)
        local_ymax = np.nanmax(proj_y)
        local_zmax = np.nanmax(proj_z)
        local_xmin = np.nanmin(proj_x)
        local_ymin = np.nanmin(proj_y)
        local_zmin = np.nanmin(proj_z)

        max_x = np.nanmax([local_xmax, max_x])
        max_y = np.nanmax([local_ymax, max_y])
        max_z = np.nanmax([local_zmax, max_z])
        min_x = np.nanmin([local_xmin, min_x])
        min_y = np.nanmin([local_ymin, min_y])
        min_z = np.nanmin([local_zmin, min_z])

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

        # XY plane
        this_axis = xy_plane
        this_axis.plot(proj_x, proj_y, color=thiscolor, linestyle=thisstyle, linewidth=thiswidth, marker=thismarker, markersize=markersize, markevery=markevery)
        if thisstartmarker is not None:
            this_axis.plot(proj_x[0], proj_y[0], color=thiscolor, linestyle=thisstyle, marker=thisstartmarker, markersize=markersize)
        if thisendmarker is not None:
            this_axis.plot(proj_x[-1], proj_y[-1], color=thiscolor, linestyle=thisstyle, marker=thisendmarker, markersize=markersize)

        # XZ plane
        # If present, the neutral sheet will only be plotted on this axis. So it's the
        # one we'll use to track the legends.
        this_axis = xz_plane
        this_line = this_axis.plot(proj_x, proj_z, color=thiscolor, linestyle=thisstyle, linewidth=thiswidth, marker=thismarker, markersize=markersize, markevery=markevery)
        if thisstartmarker is not None:
            this_axis.plot(proj_x[0], proj_y[0], color=thiscolor, linestyle=thisstyle, marker=thisstartmarker, markersize=markersize)
        if thisendmarker is not None:
            this_axis.plot(proj_x[-1], proj_y[-1], color=thiscolor, linestyle=thisstyle, marker=thisendmarker, markersize=markersize)

        # YZ plane
        this_axis = yz_plane
        this_axis.plot(proj_y, proj_z, color=thiscolor, linestyle=thisstyle, linewidth=thiswidth, marker=thismarker, markersize=markersize, markevery=markevery)
        if thisstartmarker is not None:
            this_axis.plot(proj_x[0], proj_y[0], color=thiscolor, linestyle=thisstyle, marker=thisstartmarker, markersize=markersize)
        if thisendmarker is not None:
            this_axis.plot(proj_x[-1], proj_y[-1], color=thiscolor, linestyle=thisstyle, marker=thisendmarker, markersize=markersize)

        if legend_names is not None:
            try:
                if isinstance(this_line, list):
                    this_line[0].set_label(legend_names[index])
                else:
                    this_line.set_label(legend_names[index])
            except IndexError:
                continue

    # Adjust X, Y, Z ranges
    if center_origin:
        x_halfwidth = np.nanmax(np.abs([max_x, min_x]))
        y_halfwidth = np.nanmax(np.abs([max_y, min_y]))
        z_halfwidth = np.nanmax(np.abs([max_z, min_z]))
        # Add 5% to each boundary to give a little margin
        all_halfwidth = 1.05 * np.nanmax([x_halfwidth, y_halfwidth, z_halfwidth])
        axis[0,0].set_xlim(-all_halfwidth, all_halfwidth)
        axis[0,0].set_ylim(-all_halfwidth, all_halfwidth)
        axis[1,0].set_xlim(-all_halfwidth, all_halfwidth)
        axis[1,0].set_ylim(-all_halfwidth, all_halfwidth)
        axis[1,1].set_xlim(-all_halfwidth, all_halfwidth)
        axis[1,1].set_ylim(-all_halfwidth, all_halfwidth)
    else:
        # Adjust the X and Y ranges by equal increments to give a little margin
        x_adjust = .05*(max_x - min_x)
        y_adjust = .05*(max_y - min_y)
        z_adjust = .05*(max_z - min_z)
        all_adjust = np.nanmax([x_adjust, y_adjust, z_adjust])
        xr = (min_x-all_adjust, max_x+all_adjust)
        yr = (min_y-all_adjust, max_y+all_adjust)
        zr = (min_z-all_adjust, max_z+all_adjust)
        xy_plane.set_xlim(xr)
        xy_plane.set_ylim(yr)
        xz_plane.set_xlim(xr)
        xz_plane.set_ylim(zr)
        yz_plane.set_xlim(yr)
        yz_plane.set_ylim(zr)

    if show_centerbody:
        if plot_units == 're':
            cb_radius = centerbody_size_re
        else:
            cb_radius = centerbody_size_re * km_in_re

        theta1, theta2 = -90, 90

        # Artists can't be shared between axes, so we need two copies of each wedge (XY and XZ)
        w1 = Wedge((0, 0), cb_radius, theta1, theta2, fc='white', edgecolor='black')
        w2 = Wedge((0, 0), cb_radius, theta2, theta1, fc='black', edgecolor='black')
        w3 = Wedge((0, 0), cb_radius, theta1, theta2, fc='white', edgecolor='black')
        w4 = Wedge((0, 0), cb_radius, theta2, theta1, fc='black', edgecolor='black')

        # XY
        xy_plane.add_artist(w1)
        xy_plane.add_artist(w2)

        # XZ
        xz_plane.add_artist(w3)
        xz_plane.add_artist(w4)

        # YZ  (this is just a circle)
        theta1,theta2 = 0,360
        w5 = Wedge((0, 0), cb_radius, theta1, theta2, fc='white', edgecolor='black')
        yz_plane.add_artist(w5)

    xy_plane.set_aspect('equal')
    xz_plane.set_aspect('equal')
    yz_plane.set_aspect('equal')

    if reverse_x:
        xy_plane.invert_xaxis()  # This should also reverse X axis on XZ plot, since they're shared
        xy_plane.invert_yaxis()  # This keeps the coordinate system right-handed
        #xz_plane.invert_xaxis() # XY and XZ plots share an X axis, so we don't need another flip

    # Grab the legend handles created for the XZ plot, and graft them onto the figure
    # instead of showing them on the XZ panel.

    # We need to do a draw() to lay out all the elements, so we know where to put the legend
    blank_plane.axis('off')
    fig.canvas.draw()

    # Align the top of the legend box with the top of the XY subplot, and the right of the legend box with the right of
    # the YZ subplot

    bbox1 = xy_plane.get_position()
    bbox2 = yz_plane.get_position()

    legend_bbox_top = bbox1.y1
    legend_bbox_right = bbox2.x1

    handles, labels = xz_plane.get_legend_handles_labels()
    if legend_names is not None:
        legend = fig.legend(handles, labels, loc="upper right", markerfirst=True, bbox_to_anchor=(legend_bbox_right,legend_bbox_top))

    fig.canvas.draw()

    save_plot(save_png=save_png, save_eps=save_eps, save_jpeg=save_jpeg, save_pdf=save_pdf, save_svg=save_svg, dpi=dpi)
    if display:
        plt.show()

    return fig



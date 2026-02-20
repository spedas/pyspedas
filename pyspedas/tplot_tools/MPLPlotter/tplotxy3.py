from pyspedas.tplot_tools import tplot_wildcard_expand, get_data, get_coords, get_units, set_coords, set_units, store_data
from pyspedas.utilities.bshock_2 import bshock_2
from pyspedas.utilities.mpause_2 import mpause_2
from pyspedas.analysis.neutral_sheet import neutral_sheet
from pyspedas.cotrans_tools.cotrans import cotrans
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

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
            legend_location='upper right',
            show_centerbody=True,
            centerbody_size_re=1.0,
            plot_bow_shock=False,
            plot_magnetopause=False,
            plot_neutral_sheet=False,
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
    plot_bow_shock: bool
        If True, plot the bow shock location on each panel. Default: False
    plot_magnetopause: bool
        If True, plot the magnetopause boundary on each panel. Default: False
    plot_neutral_sheet: bool
        If True, plot the AEN neutral sheet boundary on the XZ panel. Default: False
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
        fig, axis = plt.subplots(nrows=2, ncols=2, sharey='row', sharex='col', figsize=(2.5*xsize, 2.5*ysize), layout='constrained')

    xy_plane = axis[0,0]
    xz_plane = axis[1,0]
    yz_plane = axis[1,1]
    blank_plane = axis[0,1]

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
        unit_annotation=f' ({plot_units}) '

    plot_coords = get_coords(tvars[0])
    if plot_coords is None:
        plot_coords = 'Unknown'
        coord_annotation=""
    else:
        coord_annotation=f"-{plot_coords}"

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

        proj_x = d.y[:,0] * unit_conv
        proj_y = d.y[:,1] * unit_conv
        proj_z = d.y[:,2] * unit_conv

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

    if plot_units.lower() == 'km':
        extras_conv = km_in_re
    else:
        extras_conv = 1.0

    # bow shock
    bs_color = 'black'
    bs_linestyle = 'dotted'
    bs_linewidth = 1
    bs = bshock_2()
    # XY plane, just plot
    bs_x = bs[0]*extras_conv
    bs_y = bs[1]*extras_conv
    xy_plane.plot(bs_x, bs_y, color=bs_color, linestyle=bs_linestyle, linewidth=bs_linewidth)
    # XZ plane, plot and add legend
    this_line = xz_plane.plot(bs_x,bs_y, color=bs_color, linestyle=bs_linestyle, linewidth=bs_linewidth)
    # YZ plane, TBD (what to show for head-on view?
    # update legends as we did for the s/c traces
    if legend_names is not None:
        try:
            if isinstance(this_line, list):
                this_line[0].set_label("Bow Shock")
            else:
                this_line.set_label("Bow Shock")
        except IndexError:
            pass

    # magnetopause
    mp_color = 'black'
    mp_linestyle ='dashed'
    mp_linewidth = 1
    mp = mpause_2()
    # XY plane, just plot
    mp_x = mp[0]*extras_conv
    mp_y = mp[1]*extras_conv
    xy_plane.plot(mp_x, mp_y, color=mp_color, linestyle=mp_linestyle, linewidth=mp_linewidth)
    # XZ plane, plot and add legend
    this_line = xz_plane.plot(mp_x,mp_y, color=mp_color, linestyle=mp_linestyle, linewidth=mp_linewidth)
    # YZ plane, TBD (what to show for head-on view?
    # update legends as we did for the s/c traces
    if legend_names is not None:
        try:
            if isinstance(this_line, list):
                this_line[0].set_label("Magnetopause")
            else:
                this_line.set_label("Magnetopause")
        except IndexError:
            pass

    # neutral sheet

    # This is time-dependent, so we'll just pick the midpoint of the first tplot variable
    d=get_data(tvars[0])
    mid_time = (d.times[-1] - d.times[0])/2.0
    ns_x_re = -1.0*np.arange(0.0,375.0, 5.0)
    times=np.zeros(len(ns_x_re))
    times[:] = mid_time
    ns_gsm_pos=np.zeros((len(ns_x_re),3))
    ns_gsm_pos[:,0] = ns_x_re
    ns = neutral_sheet(times, ns_gsm_pos, model="aen", sc2NS=False)
    ns_gsm_pos[:,2] = ns
    store_data('ns_gsm_pos', data={'x':times, 'y':ns_gsm_pos})
    set_coords('ns_gsm_pos','GSM')
    set_units('ns_gsm_pos', 're')
    cotrans('ns_gsm_pos', 'ns_gse_pos',coord_in='gsm', coord_out='gse')
    gse_dat = get_data('ns_gse_pos')
    ns_z = gse_dat.y[:,2]*extras_conv
    ns_x = ns_x_re * extras_conv
    ns_color = 'black'
    ns_linestyle ='dashdot'
    ns_linewidth = 1

    this_line = xz_plane.plot(ns_x,ns_z, color=ns_color, linestyle=ns_linestyle, linewidth=ns_linewidth)
    # YZ plane, TBD (what to show for head-on view?
    # update legends as we did for the s/c traces
    if legend_names is not None:
        try:
            if isinstance(this_line, list):
                this_line[0].set_label("Neutral Sheet, AEN model (XZ panel only)")
            else:
                this_line.set_label("Neutral Sheet, AEN model (XZ panel only)")
        except IndexError:
            pass

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

    handles, labels = xz_plane.get_legend_handles_labels()
    if legend_names is not None:
        bbox_to_anchor = (1.04, 0.5)
        legend = fig.legend(handles, labels, loc="upper right", markerfirst=True)

    blank_plane.axis('off')
    fig.canvas.draw()

    if save_png is not None and save_png != '':
        if not save_png.endswith('.png'):
            save_png += '.png'
        plt.savefig(save_png, dpi=dpi)

    if save_eps is not None and save_eps != '':
        if not save_eps.endswith('.eps'):
            save_eps += '.eps'
        plt.savefig(save_eps, dpi=dpi)

    if save_svg is not None and save_svg != '':
        if not save_svg.endswith('.svg'):
            save_svg += '.svg'
        plt.savefig(save_svg, dpi=dpi)

    if save_pdf is not None and save_pdf != '':
        if not save_pdf.endswith('.pdf'):
            save_pdf += '.pdf'
        plt.savefig(save_pdf, dpi=dpi)

    if save_jpeg is not None and save_jpeg != '':
        if not save_jpeg.endswith('.jpeg'):
            save_jpeg += '.jpeg'
        plt.savefig(save_jpeg, dpi=dpi)

    if display:
        plt.show()



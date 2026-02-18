from pyspedas.tplot_tools import tplot_wildcard_expand, get_data, get_coords, get_units
import logging
import numpy as np
import matplotlib.pyplot as plt

def tplotxy(tvars,
            plane='xy',
            colors=('k','b','g','r','c','m','y'),
            center_origin=True,
            reverse_x = False,
            reverse_y = False,
            plot_units='re',
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
    Parameters
    ----------
    tvars: string or list of strings
        Tplot variables to be plotted (wildcards accepted).  The data array should be ntimesx3,
        or in the case of field line plots, ntimesxnpointsx3
    plane: string or list of strings
        Plane to project the 3d vectors onto. Valid options: 'xy', 'xz', 'yz'. Default: 'xy'
    colors: list or tuple of strings
        Colors to use if multiple variables are plotted.
    center_origin: bool
        If True, center the plot on the origin.
    reverse_x: bool
        If True, reverse the x-axis of the plot (more positive values to the left)
    reverse_y: bool
        If True, reverse the y-axis of the plot (more positive values to the bottom)
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

    if fig is None and axis is None:
        fig, axis = plt.subplots(sharey=True, sharex=True, figsize=(xsize, ysize), layout='constrained')

    km_in_re = 6371.2
    if plot_units is None:
        plot_units = get_units(tvars[0])
    if isinstance(plot_units, (list, np.ndarray)):
        plot_units = plot_units[0]
    if plot_units is None:
        plot_units = 'None'
        unit_annotation=""
    else:
        unit_annotation=f' Units: {plot_units} '

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
        if plane=='xy':
            proj_x = d.y[:,0] * unit_conv
            proj_y = d.y[:,1] * unit_conv
            axis.set_xlabel('X' + unit_annotation)
            axis.set_ylabel('Y' + unit_annotation)

        elif plane=='xz':
            proj_x = d.y[:,0] * unit_conv
            proj_y = d.y[:,2] * unit_conv
            axis.set_xlabel('X' + unit_annotation)
            axis.set_ylabel('Z' + unit_annotation)

        elif plane=='yz':
            proj_x = d.y[:,1] * unit_conv
            proj_y = d.y[:,2] * unit_conv
            axis.set_xlabel('X' + unit_annotation)
            axis.set_ylabel('Z' + unit_annotation)



        local_xmax = np.max(proj_x)
        local_ymax = np.max(proj_y)
        local_xmin = np.max(proj_x)
        local_ymin = np.max(proj_y)

        max_x = np.max([local_xmax, max_x])
        max_y = np.max([local_ymax, max_y])
        min_x = np.min([local_xmin, min_x])
        min_y = np.min([local_ymin, min_y])
        axis.plot(proj_x, proj_y, color=colors[index])

    if center_origin:
        x_halfwidth = np.max(np.abs([max_x, min_x]))
        y_halfwidth = np.max(np.abs([max_y, min_y]))
        all_halfwidth = np.max([x_halfwidth, y_halfwidth])
        axis.set_xlim((-all_halfwidth, all_halfwidth))
        axis.set_ylim((-all_halfwidth, all_halfwidth))
    else:
        pass

    axis.set_aspect('equal')
    if reverse_x:
        axis.invert_xaxis()
    if reverse_y:
        axis.invert_yaxis()
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



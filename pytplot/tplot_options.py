import pytplot
from . import tplot_utilities


def tplot_options(option, value):
    """
    This function allows the user to set GLOBAL options for the generated plots.
    
    Parameters
    ----------
        option : str
            The name of the option.  See section below  
        value : str/int/float/list
            The value of the option.  See section below.  
            
    Options
    -------
        ==================  ==========   =====
        Option              Value type   Notes
        ==================  ==========   =====
        title               str          Title of the the entire plot (above any panel titles)
        title_size          int          Font size of the title
        var_label           str          Name of the tplot variable to be used as another x axis
        data_gap            int          Number of seconds with consecutive nan values allowed before no interp should occur
        x_range             [flt, flt]   The min and max x_range (time) to be plotted on all plots
        vertical_spacing    flt          The space (in inches) vertically between two plots
        axis_font_size      int          The font size of the axis ticks.  Default is 10.
        charsize            int          The font size for the legend strings
        style               str          The matplotlib plot style to use
        xsize               flt          The size of the plot window in the X dimension (units of inches)
        ysize               flt          The size of the plot window in the Y dimension (units of inches)
        title_text          str          Plot title
        xmargin             [flt, flt]   The width of the left and right margins of the plot (in inches)
        ymargin             [flt, flt]   The height of the top and bottom margins of the plot (in inches)
        annotations         dict         A dictionary of text, positions, xycoords, and other options to be placed on the plot
        ==================  ==========   =====


    Options
    -------
        ============================  ==========   =====
        Obsolete/Not Yet Implemented  Value type   Notes
        ============================  ==========   =====
        wsize                         [flt, flt]   [height, width], size of the plot window in inches (not yet implemented)
        title_align                   flt          Offset position (in inches) of the title (not yet implemented)
        alt_range                     [flt, flt]   The min and max altitude to be plotted on all alt plots (not yet implemented)
        map_x_range                   [int, int]   The min and max longitude to be plotted on all map plots (not yet implemented)
        map_y_range                   [int, int]   The min and max latitude to be plotted on all map plots (not yet implemented)
        roi                           [str, str]   Times between which there's a region of interest for a user (not yet implemented)
        crosshair                     bool         Option allowing crosshairs and crosshair legend (not yet implemented)
        show_all_axes                 bool         Whether or not to just use one axis at the bottom of the plot (not yet implemented)
        black_background              bool         Whether or not to make plot backgrounds black w/ white text (not yet implemented)
        axis_tick_num                 [tuples]     A list of tuples that determines how many ticks appear. (not yet implemented)
        yaxis_width                   int          The number of pixels wide of the y axis (not yet implemented)
        y_axis_zoom                   bool         Set True if the mouse wheel should zoom in on the y axis as well as the x on plots (not yet implemented)
        var_label                     [str]        List of variables to have their values printed at the boottom of the plot Not yet implemented
        ============================  ==========   =====

    Returns
    -------
        None
    
    Examples
    --------
        >>> # Set the plot title
        >>> import pyspedas
        >>> pyspedas.tplot_options('title', 'SWEA Data for Orbit 1563')
    
    """
    
    option = option.lower()
    
    temp = tplot_utilities.set_tplot_options(option, value, pytplot.tplot_opt_glob)
    pytplot.tplot_opt_glob = temp
    
    return

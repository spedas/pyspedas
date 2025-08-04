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
        Option (Synonyms)   Value type   Notes
        ==================  ==========   =====
        title_text (title)  str          Title of the entire plot (mpl 'suptitle', above any panel titles)
        title_size          int          Font size of the title
        data_gap            int          Number of seconds with consecutive nan values allowed before no interp should occur
        x_range             [flt, flt]   The min and max x_range (time) to be plotted on all plots
        axis_font_size      int          The font size of the axis ticks.  Default is 10.
        charsize            int          The font size for the legend strings
        style               str          The matplotlib plot style to use
        xsize               flt          The size of the plot window in the X dimension (units of inches)
        ysize               flt          The size of the plot window in the Y dimension (units of inches)
        xmargin             [flt, flt]   The width of the left and right margins of the plot (in inches)
        ymargin             [flt, flt]   The height of the top and bottom margins of the plot (in inches)
        annotations         dict         A dictionary of text, positions, xycoords, and other options to be placed on the plot
        ==================  ==========   =====

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

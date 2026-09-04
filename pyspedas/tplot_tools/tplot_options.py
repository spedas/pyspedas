import copy
import logging
import pyspedas


def set_tplot_options(option, value, old_tplot_opt_glob):
    new_tplot_opt_glob = old_tplot_opt_glob

    if option in ['title_text', 'title']:
        new_tplot_opt_glob['title_text'] = value

    elif option == 'title_size':
        new_tplot_opt_glob['title_size'] = value

    elif option == 'var_label':
        new_tplot_opt_glob['var_label'] = value

    elif option == 'x_range':
        new_tplot_opt_glob['x_range'] = value

    elif option == 'data_gap':
        new_tplot_opt_glob['data_gap'] = value

    elif option == 'axis_font_size':
        new_tplot_opt_glob['axis_font_size'] = value

    elif option == 'xmargin':
        new_tplot_opt_glob['xmargin'] = value

    elif option == 'ymargin':
        new_tplot_opt_glob['ymargin'] = value

    elif option == 'style':
        new_tplot_opt_glob['style'] = value

    elif option == 'charsize':
        new_tplot_opt_glob['charsize'] = value

    elif option == 'xsize':
        new_tplot_opt_glob['xsize'] = value

    elif option == 'ysize':
        new_tplot_opt_glob['ysize'] = value

    elif option == 'varlabel_style':
        new_tplot_opt_glob['varlabel_style'] = value

    elif option == 'background':
        new_tplot_opt_glob['background'] = value

    elif option == 'foreground':
        new_tplot_opt_glob['foreground'] = value

    elif option == 'grid':
        new_tplot_opt_glob['grid'] = value

    elif option == 'grid_properties':
        if not isinstance(value, dict):
            logging.warning("grid_properties must be a dictionary")
        elif 'visible' in value:
            logging.warning("Set grid visibility with the grid option, not grid_properties['visible']")
        else:
            new_tplot_opt_glob['grid_properties'] = copy.deepcopy(value)

    else:
        logging.warning("Unknown option supplied: " + str(option))

    return new_tplot_opt_glob


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
        axis_font_size      int          The font size of the axis tick labels and var_labels.  Default is 10.
        charsize            int          The font size for the legend strings
        style               str          The matplotlib plot style to use
        xsize               flt          The size of the plot window in the X dimension (units of inches)
        ysize               flt          The size of the plot window in the Y dimension (units of inches)
        xmargin             [flt, flt]   The width of the left and right margins of the plot (in inches)
        ymargin             [flt, flt]   The height of the top and bottom margins of the plot (in inches)
        annotations         dict         A dictionary of text, positions, xycoords, and other options to be placed on the plot
        varlabel_style      str          Set to 'extra_axes' for each variable on its own axis, or 'extra_panel' for a more compact display in a single panel
        background          color        Background color for the figure and all panels. Accepts any matplotlib color.
        foreground          color        Default color for titles, labels, ticks, spines, legends, annotations, and colorbars.
        grid                bool         Turns grid lines on or off for all panels. Per-variable settings take precedence.
        grid_properties     dict         Keyword arguments passed to matplotlib ``Axes.grid`` for all panels.
        ==================  ==========   =====

    Returns
    -------
        None
    
    Examples
    --------
        >>> # Set the plot title
        >>> import pyspedas
        >>> pyspedas.tplot_options('title', 'SWEA Data for Orbit 1563')

        >>> # Set colors suitable for a dark plot
        >>> pyspedas.tplot_options('background', '#001b33')
        >>> pyspedas.tplot_options('foreground', 'white')
    
    """


    option = option.lower()
    
    temp = set_tplot_options(option, value, pyspedas.tplot_tools.tplot_opt_glob)
    pyspedas.tplot_tools.tplot_opt_glob = temp
    
    return

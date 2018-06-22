# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants
import numpy as np

def options(name, option, value):
    """
    This function allows the user to set a large variety of options for individual plots.  
    
    Parameters:
        name : str 
            Name of the tplot variable
        option : str
            The name of the option.  See section below  
        value : str/int/float/list
            The value of the option.  See section below.  
            
    Options:
        ============  ==========   =====
        Options       Value type   Notes
        ============  ==========   =====
        Color         str/list     Red, Orange, Yellow, Green, Blue, etc
        Colormap      str/list     https://matplotlib.org/examples/color/colormaps_reference.html
        Spec          int          1 sets the Tplot Variable to spectrogram mode, 0 reverts
        Alt           int          1 sets the Tplot Variable to altitude plot mode, 0 reverts   
        Map           int          1 sets the Tplot Variable to latitude/longitude mode, 0 reverts
        ylog          int          1 sets the y axis to log scale, 0 reverts
        zlog          int          1 sets the z axis to log scale, 0 reverts (spectrograms only)
        legend_names  list         A list of strings that will be used to identify the lines
        line_style    str          solid_line, dot, dash, dash_dot, dash_dot_dot_dot, long_dash
        name          str          The title of the plot
        panel_size    flt          Number between (0,1], representing the percent size of the plot
        basemap       str          Full path and name of a background image for "Map" plots
        alpha         flt          Number between [0,1], gives the transparancy of the plot lines
        yrange        flt list     Two numbers that give the y axis range of the plot
        zrange        flt list     Two numbers that give the z axis range of the plot
        ytitle        str          Title shown on the y axis
        ztitle        str          Title shown on the z axis.  Spec plots only.  
        ============  ==========   =====
    
    Returns:
        None
    
    Examples:
        >>> # Change the y range of Variable1 
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.options('Variable1', 'yrange', [2,4])
        
        >>> # Change Variable1 to use a log scale
        >>> pytplot.options('Variable1', 'ylog', 1)
        
        >>> # Change the line color of Variable1
        >>> pytplot.options('Variable1', 'ylog', 1)
    
    """
    #if isinstance(name,int):
    #    name = tplot_common.data_quants.keys()[name]
    if not isinstance(name, list):
        name = [name]
    
    option = option.lower()
    
    for i in name:
        if i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
    
        if option == 'color':
            if isinstance(value, list):
                data_quants[i].extras['line_color'] = value
            else:
                data_quants[i].extras['line_color'] = [value]
        
        if option == 'link':
            if isinstance(value, list):
                data_quants[i].link_to_tvar(value[0], value[1])
                
        if option == 'colormap':
            if isinstance(value, list):
                data_quants[i].extras['colormap'] = value
            else:
                data_quants[i].extras['colormap'] = [value]
        
        if option == 'spec':
            data_quants[i].extras['spec'] = value
        
        if option == 'alt':
            data_quants[i].extras['alt'] = value
    
        if option == 'map':
            data_quants[i].extras['map'] = value
        
        if option == 'ylog':
            negflag = 0
            namedata =  data_quants[i]
            ##check variable data
            #if negative numbers, don't allow log setting
            datasets = []
            if isinstance(namedata.data, list):
                for oplot_name in namedata.data:
                    datasets.append(data_quants[oplot_name])
            else:
                datasets.append(namedata)
                
            for dataset in datasets:
                if 'spec' not in dataset.extras:
                    for column in dataset.data:
                        if np.nanmin(dataset.data[column]) < 0:
                            print('Negative data is incompatible with log plotting.')
                            negflag = 1
                            break
                else:
                    if dataset.extras['spec'] == 1:
                        for column in dataset.spec_bins:
                            if np.nanmin(dataset.spec_bins[column]) < 0:
                                print('Negative data is incompatible with log plotting.')
                                negflag = 1
                                break
                        
            if value == 1 and negflag == 0:
                data_quants[i].yaxis_opt['y_axis_type'] = 'log'
            else:
                data_quants[i].yaxis_opt['y_axis_type'] = 'linear'
            
        
        if option == 'legend_names':
            data_quants[i].yaxis_opt['legend_names'] = value
        
        if option == 'zlog':
            negflag = 0
            namedata =  data_quants[i]
            ##check variable data
            #if negative numbers, don't allow log setting
            datasets = []
            if isinstance(namedata.data, list):
                for oplot_name in namedata.data:
                    datasets.append(data_quants[oplot_name])
            else:
                datasets.append(namedata)
                
            for dataset in datasets:
                if 'spec' in dataset.extras:                       
                    if dataset.extras['spec'] == 1:
                        negflag = 0
                        for column in dataset.data:
                            if np.nanmin(dataset.data[column])  < 0:
                                print('Negative data is incompatible with log plotting.')
                                negflag = 1
                                break
                        #verify there are no negative values
                        if negflag == 0 and value == 1:
                            data_quants[i].zaxis_opt['z_axis_type'] = 'log'
                        else:
                            data_quants[i].zaxis_opt['z_axis_type'] = 'linear'
                    else:
                        if value == 1:
                            data_quants[i].zaxis_opt['z_axis_type'] = 'log'
                        else:
                            data_quants[i].zaxis_opt['z_axis_type'] = 'linear'
            else:
                if value == 1:
                    data_quants[i].zaxis_opt['z_axis_type'] = 'log'
                else:
                    data_quants[i].zaxis_opt['z_axis_type'] = 'linear'
        
        if option == 'nodata':
            data_quants[i].line_opt['visible'] = value
        
        if option == 'line_style':
            to_be = []
            if value == 0 or value == 'solid_line':
                to_be = []
            elif value == 1 or value == 'dot':
                to_be = [2, 4]
            elif value == 2 or value == 'dash':
                to_be = [6]
            elif value == 3 or value == 'dash_dot':
                to_be = [6, 4, 2, 4]
            elif value == 4 or value == 'dash_dot_dot_dot':
                to_be = [6, 4, 2, 4, 2, 4, 2, 4]
            elif value == 5 or value == 'long_dash':
                to_be = [10]
                
            data_quants[i].line_opt['line_dash'] = to_be
            
            if(value == 6 or value == 'none'):
                data_quants[i].line_opt['visible'] = False
                
        if option == 'name':
            data_quants[i].line_opt['name'] = value
        
        if option == "panel_size":
            if value > 1 or value <= 0:
                print("Invalid value. Should be (0, 1]")
                return
            data_quants[i].extras['panel_size'] = value
        
        if option =='basemap':
            data_quants[i].extras['basemap'] = value
        
        if option =='alpha':
            if value > 1 or value < 0:
                print("Invalid value. Should be [0, 1]")
                return
            data_quants[i].extras['alpha'] = value
            
        if option == 'thick':
            data_quants[i].line_opt['line_width'] = value
        
        if option == 'transparency':
            alpha_val = value/100
            data_quants[i].line_opt['line_alpha'] = alpha_val
        
        if option == ('yrange' or 'y_range'):
            data_quants[i].yaxis_opt['y_range'] = [value[0], value[1]]
            
        if option == ('zrange' or 'z_range'):
            data_quants[i].zaxis_opt['z_range'] = [value[0], value[1]]
        
        if option == 'ytitle':
            data_quants[i].yaxis_opt['axis_label'] = value
        
        if option == 'ztitle':
            data_quants[i].zaxis_opt['axis_label'] = value
        
        if option == 'plotter': 
            data_quants[i].extras['plotter'] = value
    
    return
        
    
from __future__ import division
import pytplot
from .TVarFigureAxisOnly import TVarFigureAxisOnly
from pyqtgraph import LabelItem
import pyqtgraph as pg


def generate_stack(name, 
                   var_label = None, 
                   auto_color=True, 
                   combine_axes=True, mouse_moved_event=None):
    
    new_stack = pg.GraphicsLayoutWidget()
    #Variables needed for pyqtgraph plots
    xaxis_thickness = 35
    varlabel_xaxis_thickness = 20
    title_thickness = 50
    #Setting up the pyqtgraph window
    new_stack.setWindowTitle(pytplot.tplot_opt_glob['title_text'])
    new_stack.resize(pytplot.tplot_opt_glob['window_size'][0], pytplot.tplot_opt_glob['window_size'][1])
    
    # Vertical Box layout to store plots
    all_plots = []
    axis_types=[]
    i = 0
    num_plots = len(name)
    
    # Configure plot sizes
    total_psize = 0
    j = 0
    while(j < num_plots):
        total_psize += pytplot.data_quants[name[j]].extras['panel_size']
        j += 1
    
    if var_label is not None:
        varlabel_correction = len(var_label) * varlabel_xaxis_thickness
    else:
        varlabel_correction = 0
        xaxis_thickness = 0
        title_thickness = 0
    p_to_use = (pytplot.tplot_opt_glob['window_size'][1]-xaxis_thickness-title_thickness-varlabel_correction)/total_psize
    
    #Whether or not there is a title row in pyqtgraph
    titlerow=0
    
    # Create all plots  
    while(i < num_plots):
        last_plot = (i == num_plots-1)
        temp_data_quant = pytplot.data_quants[name[i]]
        
        p_height = int(temp_data_quant.extras['panel_size'] * p_to_use)
        
        if last_plot:
            p_height += xaxis_thickness
        if i == 0:
            if _set_pyqtgraph_title(new_stack):
                titlerow=1
        new_stack.ci.layout.setRowPreferredHeight(i+titlerow, p_height) 
        new_fig = _get_figure_class(temp_data_quant, show_xaxis=last_plot, mouse_moved=mouse_moved_event)
        new_stack.addItem(new_fig, row=i+titlerow, col=0)
            
        axis_types.append(new_fig.getaxistype())
        new_fig.buildfigure()
        
        # Add plot to GridPlot layout
        all_plots.append(new_fig.getfig())
        i = i+1
    
    #Add extra x axes if applicable 
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]
        x_axes_index=0
        for new_x_axis in var_label:
            axis_data_quant = pytplot.data_quants[new_x_axis]
            new_axis = TVarFigureAxisOnly(axis_data_quant)
            new_stack.addItem(new_axis, row=num_plots+titlerow+x_axes_index, col=0)
            x_axes_index += 1
            axis_types.append(('time', False))
            all_plots.append(new_axis)
    
    # Set all plots' x_range and plot_width to that of the bottom plot
    #     so all plots will pan and be resized together.
    first_type = {}
    if combine_axes:
        k=0
        while(k < len(axis_types)):
            if axis_types[k][0] not in first_type:
                first_type[axis_types[k][0]] = k
            else:
                all_plots[k].plotwindow.setXLink(all_plots[first_type[axis_types[k][0]]].plotwindow)
            k+=1

    return new_stack

def _set_pyqtgraph_title(layout):
    '''
    Private function to add a title to the first row of the window.  
    Returns True if a Title is set.  Else, returns False.  
    '''
    if 'title_size' in pytplot.tplot_opt_glob:
        size = pytplot.tplot_opt_glob['title_size']
    if 'title_text' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['title_text'] != '':
                layout.addItem(LabelItem(pytplot.tplot_opt_glob['title_text'], size=size, color='k'), row=0, col=0)
                return True
    return False

def _get_figure_class(temp_data_quant, show_xaxis=True, mouse_moved=None):
    if 'plotter' in temp_data_quant.extras and temp_data_quant.extras['plotter'] in pytplot.qt_plotters:
        cls = pytplot.qt_plotters[temp_data_quant.extras['plotter']]
    else:
        spec_keyword = temp_data_quant.extras.get('spec', False)
        alt_keyword = temp_data_quant.extras.get('alt', False)
        if spec_keyword:
            cls = pytplot.qt_plotters['qtTVarFigureSpec']
        elif alt_keyword:
            cls = pytplot.qt_plotters['qtTVarFigureAlt']
        else:
            cls = pytplot.qt_plotters['qtTVarFigure1D']
    return cls(temp_data_quant, show_xaxis=show_xaxis, mouse_function = mouse_moved)
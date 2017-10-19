from __future__ import division
import sys
import os
from bokeh.io import output_file, show, output_notebook, save
from bokeh.models import LinearAxis, Range1d
from . import tplot_common
from .timestamp import TimeStamp
from bokeh.layouts import gridplot
from .TVarFigure1D import TVarFigure1D
from .TVarFigure2D import TVarFigure2D
from .TVarFigureSpec import TVarFigureSpec
from .TVarFigureAlt import TVarFigureAlt
from bokeh.embed import components, file_html
from bokeh.resources import JSResources, CSSResources

from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QFileDialog, QAction, QMainWindow


def tplot(name, 
          var_label = None, 
          auto_color=True, 
          interactive=False, 
          combine_axes=True, 
          nb=False, 
          save_file=None,
          gui=False, 
          qt=True):
    
    """
    This is the function used to display the tplot variables stored in memory.
    The default output is to show the plots stacked on top of one another inside a GUI window.  
    The GUI window has the option to export the plots in either PNG or HTML formats.
    
    .. note::
        This plotting routine uses the python Bokeh library, which creates plots using HTML and Javascript.  
        Bokeh is technically still in beta, so future patches to Bokeh may require updates to this function.  
    
    Parameters:
        name : str / list
            List of tplot variables that will be plotted
        var_label : str, optional
            The name of the tplot variable you would like as
            a second x axis. 
        auto_color : bool, optional
            Automatically color the plot lines.
        interactive : bool, optional
            If True, a secondary interactive plot will be generated next to spectrogram plots.  
            Mousing over the spectrogram will display a slice of data from that time on the 
            interactive chart.
        combine_axis : bool, optional
            If True, the axes are combined so that they all display the same x range.  This also enables
            scrolling/zooming/panning on one plot to affect all of the other plots simultaneously.  
        nb : bool, optional
            If True, the plot will be displayed inside of a current Jupyter notebook session.  
        save_file : str, optional
            A full file name and path.  
            If this option is set, the plot will be automatically saved to the file name provided in an HTML format.
            The plots can then be opened and viewed on any browser without any requirements. 
        gui : bool, optional
            If True, then this function will output the 2 HTML components of the generated plots as string variables.
            This is useful if you are embedded the plots in your own GUI.  For more information, see 
            http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html  
        qt : bool, optional
            If True, then this function will display the plot inside of the Qt window.  From this window, you
            can choose to export the plots as either an HTML file, or as a PNG.   
        
    Returns:
        None
        
    Examples:
        >>> #Plot a single line
        >>> import pytplot
        >>> x_data = [2,3,4,5,6]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.tplot("Variable1")
        
        >>> #Display two plots
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> pytplot.store_data("Variable2", data={'x':x_data, 'y':y_data})
        >>> pytplot.tplot(["Variable1", "Variable2"])
        
        >>> #Display 2 plots, using Variable1 as another x axis
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pytplot.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        >>> pytplot.options("Variable3", 'spec', 1)
        >>> pytplot.tplot(["Variable2", "Variable3"], var_label='Variable1')
        
        >>> #Plot all 3 tplot variables, sending the output to an HTML file
        >>> pytplot.tplot(["Variable1", "Variable2", "Variable3"], save_file='C:/temp/pytplot_example.html')
        
        >>> #Plot all 3 tplot variables, sending the HTML output to a pair of strings
        >>> div, component = pytplot.tplot(["Variable1", "Variable2", "Variable3"], gui=True)
    """

    # Name for .html file containing plots
    out_name = ""
    
    #Check a bunch of things
    if(not isinstance(name, list)):
        name=[name]
        num_plots = 1
    else:
        num_plots = len(name)
    
    for i in range(num_plots):
        if isinstance(name[i], int):
            name[i] = list(tplot_common.data_quants.keys())[name[i]]
        if name[i] not in tplot_common.data_quants.keys():
            print(str(i) + " is currently not in pytplot")
            return
    
    if isinstance(var_label, int):
        var_label = list(tplot_common.data_quants.keys())[var_label]
    
    # Vertical Box layout to store plots
    all_plots = []
    axis_types=[]
    i = 0
    
    # Configure plot sizes
    total_psize = 0
    j = 0
    while(j < num_plots):
        total_psize += tplot_common.data_quants[name[j]].extras['panel_size']
        j += 1
    p_to_use = tplot_common.tplot_opt_glob['window_size'][1]/total_psize
    
    # Create all plots  
    while(i < num_plots):
        last_plot = (i == num_plots-1)
        temp_data_quant = tplot_common.data_quants[name[i]]
        
        p_height = int(temp_data_quant.extras['panel_size'] * p_to_use)
        p_width = tplot_common.tplot_opt_glob['window_size'][0]
        
        #Check plot type       
        spec_keyword = temp_data_quant.extras.get('spec', False)
        alt_keyword = temp_data_quant.extras.get('alt', False)
        map_keyword = temp_data_quant.extras.get('map', False)
        
        if spec_keyword:     
            new_fig = TVarFigureSpec(temp_data_quant, interactive=interactive, last_plot=last_plot)
        elif alt_keyword:
            new_fig = TVarFigureAlt(temp_data_quant, auto_color=auto_color, interactive=interactive, last_plot=last_plot)
        elif map_keyword:    
            new_fig = TVarFigure2D(temp_data_quant, interactive=interactive, last_plot=last_plot)
        else:
            new_fig = TVarFigure1D(temp_data_quant, auto_color=auto_color, interactive=interactive, last_plot=last_plot)
            
        axis_types.append(new_fig.getaxistype())
        
        new_fig.setsize(height=p_height, width=p_width) 
        if i == 0:
            new_fig.add_title()
        
        new_fig.buildfigure()
        
            
        # Add name of variable to output file name
        if last_plot:    
            out_name += temp_data_quant.name
        else:
            out_name += temp_data_quant.name + '+'
        # Add plot to GridPlot layout
        all_plots.append(new_fig.getfig())
        i = i+1
    # Add date of data to the bottom left corner and timestamp to lower right
    # if py_timestamp('on') was previously called
    total_string = ""
    if 'time_stamp' in tplot_common.extra_layouts:
        total_string = tplot_common.extra_layouts['time_stamp']
    
    ts = TimeStamp(text = total_string)
    tplot_common.extra_layouts['data_time'] = ts
    all_plots.append([tplot_common.extra_layouts['data_time']])
        
    # Set all plots' x_range and plot_width to that of the bottom plot
    #     so all plots will pan and be resized together.
    first_type = {}
    if combine_axes:
        k=0
        while(k < num_plots):
            if axis_types[k][0] not in first_type:
                first_type[axis_types[k][0]] = k
            else:
                all_plots[k][0].x_range = all_plots[first_type[axis_types[k][0]]][0].x_range
                if axis_types[k][1]:
                    all_plots[k][0].y_range = all_plots[first_type[axis_types[k][0]]][0].y_range
            k+=1
    
    #Add extra x axes if applicable 
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]
        x_axes = []
        x_axes_index = 0
        for new_x_axis in var_label:
            
            axis_data_quant = tplot_common.data_quants[new_x_axis]
            axis_start = min(axis_data_quant.data.min(skipna=True).tolist())
            axis_end = max(axis_data_quant.data.max(skipna=True).tolist())
            x_axes.append(Range1d(start = axis_start, end = axis_end))
            k = 0
            while(k < num_plots ):
                all_plots[k][0].extra_x_ranges['extra_'+str(new_x_axis)] = x_axes[x_axes_index]
                k += 1
            all_plots[k-1][0].add_layout(LinearAxis(x_range_name = 'extra_'+str(new_x_axis)), 'below')
            all_plots[k-1][0].plot_height += 22
            x_axes_index += 1
    
    # Add toolbar and title (if applicable) to top plot.        
    final = gridplot(all_plots)


    #Output types
    if gui:
        script, div = components(final)
        return script, div
    elif nb:
        output_notebook()
        show(final)
        return
    elif save_file != None:
        output_file(save_file, mode='inline')
        save(final)    
        return
    else:        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        output_file(os.path.join(dir_path, "temp.html"), mode='inline')
        save(final)
        js = JSResources(mode='inline')
        css = CSSResources(mode='inline')
        total_html = file_html(final, (js, css))
        _generate_gui(total_html)
        return

def _generate_gui(total_html):  
    
    class PlotWindow(QMainWindow):
        
        def __init__(self):
            super().__init__()
            self.initUI()
            self.setcleanup()
            
        def initUI(self):
            self.setWindowTitle('PyTplot')
            self.plot_window = QWebEngineView()
            self.setCentralWidget(self.plot_window)
            
            self.resize(tplot_common.tplot_opt_glob['window_size'][0]+100,tplot_common.tplot_opt_glob['window_size'][1]+100)
            self.plot_window.resize(tplot_common.tplot_opt_glob['window_size'][0],tplot_common.tplot_opt_glob['window_size'][1])
            
            #self.plot_window.setHtml(total_html)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self.plot_window.setUrl(QtCore.QUrl.fromLocalFile(os.path.join(dir_path, "temp.html")))
            menubar = self.menuBar()
            exportMenu = menubar.addMenu('Export')
            exportDatahtmlAction = QAction("HTML", self)
            exportDatahtmlAction.triggered.connect(self.exporthtml)
            exportMenu.addAction(exportDatahtmlAction)        
            exportDatapngAction = QAction("PNG", self)
            exportDatapngAction.triggered.connect(self.exportpng)
            exportMenu.addAction(exportDatapngAction)
            
            self.show()
        
        def setcleanup(self):
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.plot_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            for child in self.findChildren(QWebEngineView):
                if child is not self.plot_window:
                    child.deleteLater()
        
        def exporthtml(self):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            fname = QFileDialog.getSaveFileName(self, 'Open file', 'pytplot.html', filter ="html (*.html *.)")
            with open(fname[0], 'w+') as html_file:
                with open(os.path.join(dir_path, "temp.html")) as read_file:
                    html_file.write(read_file.read())
            
        def exportpng(self):
            fname = QFileDialog.getSaveFileName(self, 'Open file', 'pytplot.png', filter ="png (*.png *.)")
            sshot = self.plot_window.grab()
            sshot.save(fname[0])            
    
    app = QApplication(sys.argv)
    web = PlotWindow()    
    web.show()
    web.activateWindow()
    app.exec_()
    return
    
    
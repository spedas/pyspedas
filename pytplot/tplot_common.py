from _collections import OrderedDict

#Global variable is data_quants
data_quants = OrderedDict()
tplot_num = 1

#Global variable for tplot options
tplot_opt_glob = dict(tools = "xpan,xwheel_zoom,crosshair,reset", 
                 min_border_top = 15, min_border_bottom = 0, 
                 title_align = 'center', window_size = [800, 200])
lim_info = {}
extra_renderers = []
extra_layouts = {}
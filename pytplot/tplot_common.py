from _collections import OrderedDict

#Global variable is data_quants
data_quants = OrderedDict()

#Global variable for tplot options
tplot_opt_glob = dict(tools = "xpan,xwheel_zoom,crosshair,reset", 
                 min_border_top = 15, min_border_bottom = 0, 
                 title_align = 'center', window_size = [800, 200],
                 title_size='12pt')
lim_info = {}
extra_renderers = []
extra_layouts = {}

class TVar(object):
    """ A PyTplot variable.
    
    Attributes:
        name: String representing the PyTplot variable
        data: 
    """
    
    def __init__(self, name, number, data, spec_bins, yaxis_opt, zaxis_opt, line_opt,
                 trange, dtype, create_time, time_bar, extras):
        self.name = name
        self.number = number
        self.data = data
        self.spec_bins = spec_bins
        self.yaxis_opt = yaxis_opt
        self.zaxis_opt = zaxis_opt
        self.line_opt = line_opt
        self.trange = trange
        self.dtype = dtype
        self.create_time = create_time
        self.time_bar = time_bar
        self.extras = extras
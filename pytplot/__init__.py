import pyqtgraph as pg
import numpy as np
from _collections import OrderedDict

pg.setConfigOptions(imageAxisOrder='row-major')
pg.setConfigOptions(background='w')
pg.mkQApp()
win = pg.GraphicsLayoutWidget()
win.ci.layout.setHorizontalSpacing(50)

#This variable will be constantly changed depending on what x value the user is hovering over
hover_time = 0


#Global variable is data_quants
data_quants = OrderedDict()

#Global variable for tplot options
tplot_opt_glob = dict(tools = "xpan,crosshair,reset", 
                 min_border_top = 15, min_border_bottom = 0, 
                 title_align = 'center', window_size = [800, 800],
                 title_size='12pt', title_text='PyTplot')
lim_info = {}
extra_renderers = []
extra_layouts = {}

class TVar(object):
    """ A PyTplot variable.
    
    TODO: Fill in
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
        
        #Other variables to calculate
        self.spec_bins_time_varying = False
        self.spec_bins_ascending = self._check_spec_bins_ordering()
        
    def _check_spec_bins_ordering(self):
        if self.spec_bins is None:
            return
        if len(self.spec_bins) == len(self.data.index):
            self.spec_bins_time_varying = True
            break_top_loop = False
            for index,row in self.spec_bins.iterrows():
                if row.isnull().values.all():
                    continue
                else:
                    for i in row.index:
                        if np.isfinite(row[i]) and np.isfinite(row[i+1]):
                            ascending = row[i] < row[i+1]
                            break_top_loop = True
                            break
                        else:
                            continue
                    if break_top_loop:
                        break
        else:
            ascending = self.spec_bins[0].iloc[0] < self.spec_bins[1].iloc[0]
        return ascending


from .store_data import store_data
from .tplot import tplot
from .get_data import get_data
from .xlim import xlim
from .ylim import ylim
from .zlim import zlim
from .tlimit import tlimit
from .tplot_save import tplot_save
from .tplot_names import tplot_names
from .tplot_restore import tplot_restore
from .get_timespan import get_timespan
from .tplot_options import tplot_options
from .tplot_rename import tplot_rename
from .get_ylimits import get_ylimits
from .timebar import timebar
from .del_data import del_data
from .timespan import timespan
from .options import options
from .timestamp import timestamp
from .cdf_to_tplot import cdf_to_tplot
from .tplot_utilities import compare_versions

compare_versions()
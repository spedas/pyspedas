from bokeh.models.formatters import DatetimeTickFormatter
from _collections import OrderedDict

#Global variable is data_quants
data_quants = OrderedDict()
tplot_num = 1

#Global variable for tplot options
tplot_opt_glob = dict(tools = "xpan,xwheel_zoom,crosshair,reset", 
                 min_border_top = 15, min_border_bottom = 0)
dttf = DatetimeTickFormatter(formats=dict(
            microseconds=["%H:%M:%S"],                        
            milliseconds=["%H:%M:%S"],
            seconds=["%H:%M:%S"],
            minsec=["%H:%M:%S"],
            minutes=["%H:%M:%S"],
            hourmin=["%H:%M:%S"],
            hours=["%H:%M"],
            days=["%F"],
            months=["%F"],
            years=["%F"]))
xaxis_opt_glob = dict(formatter = dttf)
title_opt = dict(align = 'center')
window_size = [800, 200]
lim_info = {}
extra_renderers = []
extra_layouts = {}
time_range_adjusted = False
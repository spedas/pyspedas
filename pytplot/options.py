from . import tplot_common
from .tplot_utilities import set_options

def options(name, option, value):
    
    if not isinstance(name, list):
        name = [name]
    
    option = option.lower()
    
    for i in name:
        if i not in tplot_common.data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        (new_yaxis_opt, new_zaxis_opt, new_line_opt, new_extras) = set_options(option, value, tplot_common.data_quants[i]['yaxis_opt'], tplot_common.data_quants[i]['zaxis_opt'], tplot_common.data_quants[i]['line_opt'], tplot_common.data_quants[i]['extras'])

        tplot_common.data_quants[i]['yaxis_opt'] = new_yaxis_opt
        tplot_common.data_quants[i]['zaxis_opt'] = new_zaxis_opt
        tplot_common.data_quants[i]['line_opt'] = new_line_opt
        tplot_common.data_quants[i]['extras'] = new_extras
    
    return
        
    
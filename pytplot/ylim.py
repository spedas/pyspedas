from . import tplot_common

def ylim(name, min, max, log_opt=False):
    
    if name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot.")
        return
    
    temp_data_quant = tplot_common.data_quants[name]
    temp_data_quant.yaxis_opt['y_range'] = [min, max]
    
    return
from . import tplot_common

def zlim(name, min, max, log_opt=False):
   
    if name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot.")
        return
    
    temp_data_quant = tplot_common.data_quants[name]
    temp_data_quant['zaxis_opt']['z_range'] = [min, max]
    
    return
from . import tplot_common

def get_data(name):
    global data_quants
    if name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot")
        return
    
    temp_data_quant = tplot_common.data_quants[name]
    data_val = temp_data_quant['data'].values
    time_val = temp_data_quant['data'].index
    
    return(time_val, data_val)
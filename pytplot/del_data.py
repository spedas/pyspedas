from . import tplot_common


def del_data(name):
    
    if not isinstance(name, list):
        name = [name]
    for i in name:
        if i not in tplot_common.data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        
    temp_data_quants = tplot_common.data_quants[i]
    str_name = temp_data_quants.name
    
        
    del tplot_common.data_quants[str_name]
        
    return

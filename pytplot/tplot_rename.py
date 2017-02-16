from . import tplot_common

def tplot_rename(old_name, new_name):
    if old_name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot")
        return
    if isinstance(old_name, int):
        old_name = tplot_common.data_quants[old_name].name
    
    tplot_common.data_quants[new_name] = tplot_common.data_quants.pop(old_name)
    tplot_common.data_quants[new_name].name = new_name
    
    return
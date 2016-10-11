from . import tplot_common

def tplot_names():
    print(iter(tplot_common.data_quants))
    for key, value in tplot_common.data_quants.items():
        if isinstance(key, int):
            print(key, ":", tplot_common.data_quants[key]['name'])
        
    return
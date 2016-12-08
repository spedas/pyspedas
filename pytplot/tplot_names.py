from . import tplot_common

def tplot_names():
    num=0
    for key, _ in tplot_common.data_quants.items():
        print(num, ":", tplot_common.data_quants[key]['name'])
        num=num+1    
    return
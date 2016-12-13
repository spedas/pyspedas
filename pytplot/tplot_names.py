from . import tplot_common

def tplot_names():
    num=0
    for key, _ in tplot_common.data_quants.items():
        if isinstance(tplot_common.data_quants[key]['data'], list):
            names_to_print = tplot_common.data_quants[key]['name'] + "  data from: "
            for name in tplot_common.data_quants[key]['data']:
                names_to_print = names_to_print + " " + name
        else:
            names_to_print = tplot_common.data_quants[key]['name']
        print(num, ":", names_to_print)
        num=num+1    
    return
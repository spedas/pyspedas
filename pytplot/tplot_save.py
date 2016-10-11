import pickle
from . import tplot_common

def tplot_save(name, filename=None):
    if name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot") 
        return
    
    temp_data_quant = tplot_common.data_quants[name]
    if filename==None:
        filename="var_"+name+".pytplot"
    pickle.dump(temp_data_quant, open(filename, "wb"))
    
    return
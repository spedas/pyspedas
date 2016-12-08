import pickle
from . import tplot_common

def tplot_save(names, filename=None):
    
    if not isinstance(names, list):
        names = [names]
    
    to_pickle =[]
    for name in names:    
        if name not in tplot_common.data_quants.keys():
            print("That name is currently not in pytplot") 
            return
        to_pickle.append(tplot_common.data_quants[name])
        
    num_quants = len(to_pickle)
    to_pickle = [num_quants] + to_pickle
    temp_tplot_opt_glob = tplot_common.tplot_opt_glob
    to_pickle.append(temp_tplot_opt_glob)
    
    if filename==None:
        filename='var_'+'-'.join(names)+'.pytplot'
    
    pickle.dump(to_pickle, open(filename, "wb"))
    
    return
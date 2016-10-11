import os
import pickle
import numpy as np
from . import tplot_common
from .options import options 
from .store_data import store_data
from scipy.io import readsav


def tplot_restore(file_name):
    #Error check
    if not (os.path.isfile(file_name)):
        print("Not a valid file name")
        return
    
    #Check if the restored file was an IDL file
    
    if file_name.endswith('.tplot'):
        temp_tplot = readsav(file_name)
        for i in range(len(temp_tplot['dq'])):
            data_name = temp_tplot['dq'][i][0].decode("utf-8")
            temp_x_data = temp_tplot['dq'][i][1][0][0]
            #Pandas reads in data the other way I guess
            if len(temp_tplot['dq'][i][1][0][2].shape) == 2:
                temp_y_data = np.transpose(temp_tplot['dq'][i][1][0][2])
            else:
                temp_y_data = temp_tplot['dq'][i][1][0][2]
            
            
            #If there are more than 4 fields, that means it is a spectrogram 
            if len(temp_tplot['dq'][i][1][0]) > 4:
                temp_v_data = temp_tplot['dq'][i][1][0][4]
                
                #Change from little endian to big endian, since pandas apparently hates little endian
                #We might want to move this into the py_store_data procedure eventually
                if (temp_x_data.dtype.byteorder == '>'):
                    temp_x_data = temp_x_data.byteswap().newbyteorder()
                if (temp_y_data.dtype.byteorder == '>'):
                    temp_y_data = temp_y_data.byteswap().newbyteorder()
                if (temp_v_data.dtype.byteorder == '>'):
                    temp_v_data = temp_v_data.byteswap().newbyteorder()
                
                store_data(data_name, data={'x':temp_x_data, 'y':temp_y_data, 'v':temp_v_data})
            else:
                #Change from little endian to big endian, since pandas apparently hates little endian
                #We might want to move this into the py_store_data procedure eventually
                if (temp_x_data.dtype.byteorder == '>'):
                    temp_x_data = temp_x_data.byteswap().newbyteorder()
                if (temp_y_data.dtype.byteorder == '>'):
                    temp_y_data = temp_y_data.byteswap().newbyteorder()
                store_data(data_name, data={'x':temp_x_data, 'y':temp_y_data})
            
            #Still have no idea what "lh" is
            #data_quants[data_name]['lh'] = temp_tplot['dq'][i][2]
            
            #Need to loop through the options and determine what goes where
            if temp_tplot['dq'][i][3].dtype.names is not None:
                for option_name in temp_tplot['dq'][i][3].dtype.names:
                    options(data_name, option_name, temp_tplot['dq'][i][3][option_name][0])
            
            tplot_common.data_quants[data_name]['trange'] =  temp_tplot['dq'][i][4].tolist()
            tplot_common.data_quants[data_name]['dtype'] =  temp_tplot['dq'][i][5]
            tplot_common.data_quants[data_name]['create_time'] =  temp_tplot['dq'][i][6]
        
        ###################################################################    
        #TODO: temp_tplot['tv']
        
        #if temp_tplot['tv'][0][0].dtype.names is not None:
        #    for option_name in temp_tplot['tv'][0][0].dtype.names:
        #        py_tplot_options(option_name, temp_tplot['tv'][0][0][option_name][0])
        #'tv' stands for "tplot variables"
        #temp_tplot['tv'][0][0] is all of the "options" variables
            #For example, TRANGE_FULL, TRANGE, REFDATE, DATA_NAMES
        #temp_tplot['tv'][0][1] is all of the "settings" variables
            #temp_tplot['tv'][0][1]['D'][0] is "device" options
            #temp_tplot['tv'][0][1]['P'][0] is "plot" options
            #temp_tplot['tv'][0][1]['X'][0] is x axis options
            #temp_tplot['tv'][0][1]['Y'][0] is y axis options
        ####################################################################
    else:
        temp_data_quant = pickle.load(open(file_name,"rb"))
        tplot_common.data_quants[temp_data_quant['name']] = temp_data_quant
        tplot_common.data_quants[temp_data_quant['number']] = temp_data_quant
        tplot_common.tplot_num += 1
    
    return
from . import tplot_common
from .get_data import get_data
from .store_data import store_data

def overplot(new_name, names, auto_format = False):
    for i in names:
        if i not in tplot_common.data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
    new_time = None
    new_data = []
    if auto_format:
        linestyle_guide = ['solid', 'dashed', 'dotted', 'dashdot']
        linestyle_list = []
        linestyle_added = 0
    
    # obtain time
    (new_time, _) = get_data(names[0])
    time_len = len(new_time)
    # create internal lists in new_data based off new_time
    for time in new_time:
        new_data.append([])
    for temp_name in names:
        (_, temp_data) = get_data(temp_name)
        data_len = None
        i = 0
        data_len = len(temp_data[0])
        while(i < time_len):
            j = 0
            while(j < data_len):
                new_data[i].append(temp_data[i][j])
                j += 1
            i += 1

        # add linestyle to linestyle_list based on how many
        # lines there were and which # plot this is
        if auto_format:
            temp_linestyle = linestyle_guide[linestyle_added]
            i = 0
            while(i < data_len):
                linestyle_list.append(temp_linestyle)
                i += 1
            linestyle_added += 1

    store_data(new_name, data={'x':new_time, 'y':new_data})
    if auto_format:
        tplot_common.data_quants[new_name].extras['linestyle'] = linestyle_list

    return


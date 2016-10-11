from . import tplot_common


def get_ylimits(name, trg = None):
    if not isinstance(name, list):
        name = [name]
    name_num = len(name)
    ymin = None
    ymax = None
    for i in range(name_num):
        if name[i] not in tplot_common.data_quants.keys():
            print(str(name[i]) + " is currently not in pytplot.")
            return
        temp_data_quant = tplot_common.data_quants[name[i]]
        yother = temp_data_quant['data']
        if trg is not None:
            for column_name in yother.columns:
                y = yother[column_name]
                trunc_tempt_data_quant = y.truncate(before = trg[0], after = trg[1])
                loc_min = trunc_tempt_data_quant.min(skipna=True)
                loc_max = trunc_tempt_data_quant.max(skipna=True)
                if (ymin is None) or (loc_min < ymin):
                    ymin = loc_min
                if (ymax is None) or (loc_max > ymax):
                    ymax = loc_max
        else:
            for column_name in yother.columns:
                y = yother[column_name]
                loc_min = y.min(skipna=True)
                loc_max = y.max(skipna=False)
                if (ymin is None) or (loc_min < ymin):
                    ymin = loc_min
                if (ymax is None) or (loc_max > ymax):
                    ymax = loc_max
    print("Y Minimum: " + str(ymin))
    print("Y Maximum: " + str(ymax))
    
    return(ymin, ymax)
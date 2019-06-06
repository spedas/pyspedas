import pytplot

#SPLIT TVAR
#store columns of TVar into new TVars


def split_vec(tvar,newtvars=None,columns='all'):
    if not 'spec_bins' in pytplot.data_quants[tvar].coords:
        dataframe = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
        spec_bins = None
    else:
        dataframe, spec_bins = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)

    #separate and add data
    time = dataframe.index
    data = dataframe
    defaultlist = []
    #grab column data
    if columns == 'all':
        columns = dataframe.columns.values
    for i,val in enumerate(columns):
        #if not a list
        if isinstance(val,list):
            range_start = val[0]
            range_end = val[1]
        else:
            range_start = val
            range_end = val
        split_col = list(range(range_start,range_end+1))
        #store split data
        defaultname = tvar+ '_' + str(i)
        defaultlist = defaultlist + [defaultname]
        data_for_tplot = {'x':time, 'y':data[split_col].squeeze()}
        if spec_bins is not None:
            data_for_tplot['v'] = spec_bins.values
        if newtvars is None:
            pytplot.store_data(defaultname,data=data_for_tplot)
        else:
            pytplot.store_data(newtvars[i],data=data_for_tplot)

    if newtvars is None:
        return defaultlist
    else:
        return newtvars

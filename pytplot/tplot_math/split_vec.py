import pytplot

def split_vec(tvar,newtvars=None,columns='all'):
    """
    Splits up 2D data into many 1D tplot variables.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tplot variable to split up
        newtvars : int/list, optional
            The names of the new tplot variables. This must be the same length as the number of variables created.
        columns : list of ints, optional
            The specific column numbers to grab from the data.  The default is to split all columns.

    Returns:
        None

    Examples:
        >>> pytplot.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
        >>> pytplot.tplot_math.split_vec('b',['b1','b2','b3'],[0,[1,3],4])
        >>> print(pytplot.data_quants['b2'].values)
    """

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

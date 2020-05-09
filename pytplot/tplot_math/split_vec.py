import pytplot
import numpy as np

def split_vec(tvar, new_name=None, columns='all', suffix=None):
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

    # Make sure the tvar is found
    if tvar not in pytplot.data_quants:
        print(f"Error: {tvar} not found in memory.")
        return

    # Give a default to the new name
    if new_name is None:
        new_name = tvar

    # Gather data from the tvar
    alldata = pytplot.get_data(tvar)
    time = alldata[0]
    data = alldata[1]
    dim = data.shape

    # If already size one, simply return
    if len(dim) == 1:
        return [tvar]

    vec_length = dim[1]

    # Determine what the suffix list will be
    if suffix is not None:
        if vec_length > len(suffix):
            print(f"split_vec error: number of columns ({vec_length}) is greater than the number of suffix entered")
    else:
        if vec_length == 3:
            suffix = ["_x", "_y", "_z"]
        else:
            suffix = []
            for i in range(vec_length):
                suffix.append("_"+str(i))


    created_variables = []

    #grab column data
    if columns == 'all':
        columns = range(vec_length)

    for i in columns:

        #if not a list
        if isinstance(i,list):
            range_start = i[0]
            range_end = i[1]
        else:
            range_start = i
            range_end = i
        split_col = list(range(range_start,range_end+1))
        split_name = new_name + suffix[i]
        created_variables = created_variables + [split_name]

        data_for_tplot = {'x':time, 'y':data[:,split_col].squeeze()}

        if not pytplot.store_data(split_name,data=data_for_tplot):
            raise Exception(f"Failed to store {split_name} in pytplot.")


    return created_variables

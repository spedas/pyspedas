"""
Take a stored vector like 'Vp' and create stored vectors 'Vp_x','Vp_y','Vp_z'.

Notes
-----
    Similar to SPEDAS split_vec function.
    Pytplot contains a similar function but currently it fails for THEMIS gmag
    data.

"""
import pyspedas
import pytplot


def split_vec(names, new_names=None, suffix=None):
    """
    Split a vector tplot variable.

    Parameters
    ----------
        names: str/list of str
            List of pytplot names.
        new_names: str/list of str
            List of new_names for pytplot variables.
            If not given, then a suffix is applied.
        suffix: str
            A suffix to apply. Default is ['_x', '_y', '_z'].

    Returns
    -------
        A list of pytplot variables.
    """
    old_names = pyspedas.tnames(names)
    allnewnames = []

    if len(old_names) < 1:
        print('split_vec error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = ['_x', '_y', '_z']

    if new_names is None:
        n_names = old_names
    else:
        n_names = new_names

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        print('split_vec error: new_names not the same length as old names.')
        return

    for i, old in enumerate(old_names):
        new = n_names[i]
        alldata = pytplot.get_data(old)
        time = alldata[0]
        data = alldata[1]

        dim = data.shape
        if len(dim) == 1:
            allnewnames.append(old)
        else:
            vec_len = dim[1]
            if vec_len > (len(suffix)):
                print('split_vec error: vector components larger than len of\
                      suffix')
                return
            for k in range(vec_len):
                ndata = list(data[:, k])
                newname = new + suffix[k]
                if len(alldata) < 3:
                    pytplot.store_data(newname, data={'x': time, 'y': ndata})
                else:
                    v = alldata[2]
                    if len(v) == len(time):
                        pytplot.store_data(newname, data={'x': time,
                                                          'y': ndata,
                                                          'v': v})
                    else:
                        pytplot.store_data(newname, data={'x': time,
                                                          'y': ndata})

                pytplot.data_quants[newname].attrs = pytplot\
                    .data_quants[old].attrs.copy()
                allnewnames.append(newname)

            print('split_vec was applied to: ' + old)
    return(allnewnames)

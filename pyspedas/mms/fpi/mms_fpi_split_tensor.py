from pytplot import get_data, store_data

def mms_fpi_split_tensor(tensor_variable):
    """
    Splits FPI tensor variables (pressure, temperature) into their components

    Input
    -----------
        tensor_variable: str
            Tplot variable containing the tensor data

    Returns
    ---------
        List of variables created.
    """

    data = get_data(tensor_variable)

    if data is None:
        print('Problem returning data from the variable: ' + tensor_variable)
        return

    saved = store_data(tensor_variable + '_xx', data={'x': data.times, 'y': data.y[:, 0, 0]})
    saved = store_data(tensor_variable + '_xy', data={'x': data.times, 'y': data.y[:, 0, 1]})
    saved = store_data(tensor_variable + '_xz', data={'x': data.times, 'y': data.y[:, 0, 2]})
    saved = store_data(tensor_variable + '_yx', data={'x': data.times, 'y': data.y[:, 1, 0]})
    saved = store_data(tensor_variable + '_yy', data={'x': data.times, 'y': data.y[:, 1, 1]})
    saved = store_data(tensor_variable + '_yz', data={'x': data.times, 'y': data.y[:, 1, 2]})
    saved = store_data(tensor_variable + '_zx', data={'x': data.times, 'y': data.y[:, 2, 0]})
    saved = store_data(tensor_variable + '_zy', data={'x': data.times, 'y': data.y[:, 2, 1]})
    saved = store_data(tensor_variable + '_zz', data={'x': data.times, 'y': data.y[:, 2, 2]})

    components = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz']
    return [tensor_variable + '_' + component for component in components]

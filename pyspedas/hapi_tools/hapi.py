import logging
import warnings
from pytplot import get_data, store_data, options, time_double
import numpy as np
from hapiclient import hapi as load_hapi


def hapi(trange=None, server=None, dataset=None, parameters='', suffix='',
         prefix='', catalog=False, quiet=False):
    """
    Loads data from a HAPI server into tplot variables

    Parameters
    -----------
        trange: list of str or list of float
            Time range to load the data for

        server: str
            HAPI server to load the data from

        dataset: str
            HAPI dataset to load

        parameters: str or list of str
            Parameters in the dataset to load; default
            is to load them all
            Default: '' (load all parameters)

        prefix: str
            Prefix to append to the tplot variables
            Default: ''

        suffix: str
            Suffix to append to the tplot variables
            Default: ''

        catalog: bool
            If True, returns the server's catalog of datasets
            Default: False

        quiet: bool
            If True, suppress printing the catalog ids retrieved
            Default: False

    Returns
    -------
        list of str
            List of catalog ids retrieved or tplot variables created.

    Examples
    --------

    >>> # Print catalog from CDAWeb HAPI server
    >>> import pyspedas
    >>> cat_entries = pyspedas.hapi(server='https://cdaweb.gsfc.nasa.gov/hapi', catalog=True)

    >>> # Load OMNI data from CDAWeb HAPI server
    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> h_vars = pyspedas.hapi(trange=['2003-10-20', '2003-11-30'],server='https://cdaweb.gsfc.nasa.gov/hapi',dataset='OMNI_HRO2_1MIN')
    >>> tplot(['BX_GSE','BY_GSE','BZ_GSE'])
    """

    if server is None:
        logging.error('No server specified; example servers include:')
        logging.error('- https://cdaweb.gsfc.nasa.gov/hapi')
        logging.error('- https://pds-ppi.igpp.ucla.edu/hapi')
        logging.error('- http://planet.physics.uiowa.edu/das/das2Server/hapi')
        logging.error('- https://iswa.gsfc.nasa.gov/IswaSystemWebApp/hapi')
        logging.error('- http://lasp.colorado.edu/lisird/hapi')
        return

    if catalog:
        catalog = load_hapi(server)
        items = []
        id_list = []
        if 'catalog' in catalog.keys():
            items = catalog['catalog']
        if not quiet:
            print('Available datasets: ')
        for item in items:
            if 'title' in item.keys():
                if not quiet:
                    print(item['id'] + ': ' + item['title'])
            else:
                if not quiet:
                    print(item['id'])
            id_list.append(item['id'])
        return id_list

    if dataset is None:
        logging.error('Error, no dataset specified; please see the catalog for a list of available data sets.')
        return

    if trange is None:
        logging.error('Error, no trange specified')
        return

    if isinstance(parameters, list):
        parameters = ','.join(parameters)

    opts = {'logging': False}

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=ResourceWarning)
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        data, hapi_metadata = load_hapi(server, dataset, parameters, trange[0], trange[1], **opts)

    out_vars = []

    # loop through the parameters in this dataset
    params = hapi_metadata['parameters']

    timestamps = [datapoint[0] for datapoint in data]
    unixtimes = [time_double(timestamp.decode('utf-8')) for timestamp in timestamps]

    for param_idx, param in enumerate(params[1:]):
        spec = False
        param_name = param.get('name')
        param_type = param.get('type')
        data_size = param.get('size')

        if param_type is None:
            param_type = 'double'

        if data_size is None:
            single_line = True

        try:
            if param_type == 'double':
                single_line = isinstance(data[0][param_idx+1], np.float64)
            elif param_type == 'integer':
                single_line = isinstance(data[0][param_idx+1], np.int32)
        except IndexError:
            continue

        if single_line:
            data_out = np.zeros((len(data)))
        else:
            try:
                data_out = np.zeros((len(data), len(data[0][param_idx+1])))
            except TypeError:
                continue

        for idx, datapoint in enumerate(data):
            if single_line:
                data_out[idx] = datapoint[param_idx+1]
            else:
                data_out[idx, :] = datapoint[param_idx+1]

        data_out = data_out.squeeze()

        # check for fill values
        fill_value = param.get('fill')
        if fill_value is not None:
            if param_type == 'double':
                fill_value = float(fill_value)
                data_out[data_out == fill_value] = np.nan
            elif param_type == 'integer':
                # NaN is only floating point, so we replace integer fill
                # values with 0 instead of NaN
                fill_value = int(fill_value)
                data_out[data_out == fill_value] = 0

        bins = param.get('bins')

        if bins is not None:
            centers = bins[0].get('centers')

            if centers is not None:
                spec = True

        data_table = {'x': unixtimes, 'y': data_out}

        if spec:
            data_table['v'] = centers

        saved = store_data(prefix + param_name + suffix, data=data_table)
        metadata = get_data(prefix + param_name + suffix, metadata=True)
        metadata['HAPI'] = param

        if spec:
            options(prefix + param_name + suffix, 'spec', True)

        param_units = param.get('units')
        if param_units is not None:
            options(prefix + param_name + suffix, 'ysubtitle', '[' + str(param_units) + ']')

        param_desc = param.get('description')
        if param_desc is not None:
            options(prefix + param_name + suffix, 'ytitle', param_desc)

        if saved:
            out_vars.append(prefix + param_name + suffix)

    return out_vars

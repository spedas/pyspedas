import warnings
from time import sleep
from pyspedas import time_double
from pytplot import get_data, store_data, options
import numpy as np

try:
    from hapiclient import hapi as load_hapi
except ImportError:
    print('hapiclient not found; install with: "pip install hapiclient"')

def hapi(trange=None, server=None, dataset=None, parameters='', suffix='',
         prefix='', catalog=False):
    """
    Loads data from a HAPI server into pytplot variables

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

        prefix: str
            Prefix to append to the tplot variables

        suffix: str
            Suffix to append to the tplot variables

        catalog: bool
            If True, returns the server's catalog of datasets

    Returns
    -------
        List of tplot variables created.
    """

    if server is None:
        print('Error, no server specified; example servers include:')
        print('- https://cdaweb.gsfc.nasa.gov/hapi')
        print('- https://pds-ppi.igpp.ucla.edu/hapi')
        print('- http://planet.physics.uiowa.edu/das/das2Server/hapi')
        print('- https://iswa.gsfc.nasa.gov/IswaSystemWebApp/hapi')
        print('- http://lasp.colorado.edu/lisird/hapi')
        return

    if catalog:
        catalog = load_hapi(server)
        items = []
        if 'catalog' in catalog.keys():
            items = catalog['catalog']
        print('Available datasets: ')
        for item in items:
            if 'title' in item.keys():
                print(item['id'] + ': ' + item['title'])
            else:
                print(item['id'])
        return

    if dataset is None:
        print('Error, no dataset specified; please see the catalog for a list of available data sets.')
        return

    if trange is None:
        print('Error, no trange specified')
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

    for param in params[1:]:
        spec = False
        param_name = param.get('name')
        print('Loading ' + prefix + param_name + suffix)

        # load the data only for this parameter
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=ResourceWarning)
                warnings.filterwarnings('ignore', message='Unverified HTTPS request')
                data, hapi_metadata = load_hapi(server, dataset, param_name, trange[0], trange[1], **opts)
        except:
            continue

        timestamps = [datapoint[0] for datapoint in data]
        unixtimes = [time_double(timestamp.decode('utf-8')) for timestamp in timestamps]

        param_type = hapi_metadata['parameters'][1].get('type')

        if param_type is None:
            param_type = 'double'

        data_size = hapi_metadata['parameters'][1].get('size')

        if data_size is None:
            single_line = True

        try:
            if param_type == 'double':
                single_line = isinstance(data[0][1], np.float64)
            elif param_type == 'integer':
                single_line = isinstance(data[0][1], np.int32)
        except IndexError:
            continue

        if single_line:
            data_out = np.zeros((len(data)))
        else:
            try:
                data_out = np.zeros((len(data), len(data[0][1])))
            except TypeError:
                continue

        for idx, datapoint in enumerate(data):
            if single_line:
                data_out[idx] = datapoint[1]
            else:
                data_out[idx, :] = datapoint[1]

        data_out = data_out.squeeze()

        # check for fill values
        fill_value = hapi_metadata['parameters'][1].get('fill')
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
        metadata['HAPI'] = hapi_metadata

        if spec:
            options(prefix + param_name + suffix, 'spec', True)

        if saved:
            out_vars.append(prefix + param_name + suffix)

        # wait for a second before going to the next variable
        # to avoid hitting the server too quickly
        sleep(1)
    
    return out_vars
import logging
import warnings
from pyspedas.tplot_tools import get_data, store_data, options, time_double
import numpy as np
from hapiclient import hapi as load_hapi
from .replace_fillvals import replace_fillvals


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

    if len(data) == 0:
        return []

    out_vars = []

    # loop through the parameters in this dataset
    params = hapi_metadata['parameters']

    timestamps = [datapoint[0] for datapoint in data]
    unixtimes = [time_double(timestamp.decode('utf-8')) for timestamp in timestamps]

    values_by_name = {}
    loaded_params = []

    # Keep the time dimension and all parameter dimensions from hapiclient.
    # In particular, squeeze() would lose time for a one-record response.
    for param_idx, param in enumerate(params[1:]):
        param_name = param.get('name')
        param_type = param.get('type') or 'double'
        data_out = np.array(data[data.dtype.names[param_idx + 1]], copy=True)

        if param_type in ('string', 'isotime'):
            # Preserve textual parameters instead of silently replacing them
            # with NaNs. Decode bytes so stored Unicode values remain readable.
            if data_out.dtype.kind == 'S':
                data_out = np.char.decode(data_out, 'utf-8')
            else:
                data_out = data_out.astype(str)
        elif param_type == 'double':
            data_out = data_out.astype(float)

        fill_value = param.get('fill')
        if fill_value is not None and param_type in ('double', 'integer'):
            replace_fillvals(data_out, fill_value, param_name, param_type)

        values_by_name[param_name] = data_out
        loaded_params.append(param)

    # Pass 2: Process any needed indirection (e.g. bin centers in separate variable) and make tplot variables
    # All parameter values are now available, regardless of parameter order.
    for param in loaded_params:
        param_name = param["name"]
        tname = prefix + param_name + suffix
        data_out = values_by_name[param_name]

        centers = None
        bins = param.get("bins")

        # Handle a single spectral axis, as in the IDL implementation.
        if bins and len(bins) == 1:
            centers = bins[0].get("centers")

            if isinstance(centers, str):
                reference = centers
                centers = values_by_name.get(reference)

                if centers is None:
                    logging.warning(
                        f"{param_name!r}: bin centers reference "
                        f"{reference!r}, but that parameter was not loaded; "
                        "storing without a spectral axis.",
                    )

        spec = centers is not None
        data_table = {"x": unixtimes, "y": data_out}

        if spec:
            data_table["v"] = centers

        saved = store_data(tname, data=data_table)
        if not saved:
            continue

        metadata = get_data(tname, metadata=True)
        metadata["HAPI"] = param

        if spec:
            options(tname, "spec", True)
            options(tname, "sort_spec_bins", True)

        param_units = param.get("units")
        if param_units is not None:
            options(tname, "ysubtitle", "[" + str(param_units) + "]")

        param_desc = param.get("description")
        if param_desc is not None:
            options(tname, "ytitle", param_desc)

        out_vars.append(tname)

    return out_vars

import logging

from pyspedas.tplot_tools import time_datetime
from pyspedas.tplot_tools import store_data, options


def load(trange=None,
         collection=None,
         measurements=None,
         models=None,
         sampling_step=None,
         auxiliaries=None,
         residuals=False):
    """

    """

    try:
        from viresclient import SwarmRequest
    except ImportError:
        logging.info('The viresclient package is needed for this operation, but does not appear to be installed.')
        logging.info('To use this feature, install viresclient with "pip install viresclient".')
        logging.info('If pip install fails, try "conda install viresclient".')

    from .config import CONFIG

    if CONFIG['access_token'] == '':
        logging.error('Invalid access token')
        return
    else:
        access_token = CONFIG['access_token']

    if trange is None:
        logging.error('No time range specified')
        return

    tr = time_datetime(trange)

    if not isinstance(measurements, list):
        measurements = [measurements]

    if auxiliaries is not None and not isinstance(auxiliaries, list):
        auxiliaries = [auxiliaries]

    if models is not None:
        if not isinstance(models, list):
            models = [models]

    request = SwarmRequest(url="https://vires.services/ows", token=access_token)
    if isinstance(collection, list):
        request.set_collection(*collection)
    else:
        request.set_collection(collection)

    if auxiliaries is None:
        request.set_products(measurements=measurements, models=models, sampling_step=sampling_step, residuals=residuals)
    else:
        request.set_products(measurements=measurements, auxiliaries=auxiliaries, models=models, sampling_step=sampling_step, residuals=residuals)

    data = request.get_between(start_time=tr[0], end_time=tr[1])
    return xarray_to_tplot(data.as_xarray())


def xarray_to_tplot(xr):
    out = []
    for key in xr.keys():
        times = xr[key].coords['Timestamp'].to_numpy()
        saved = store_data(key, data={'x': times, 'y': xr[key].data})
        options(key, 'ytitle', xr[key].description)
        options(key, 'ysubtitle', '[' + xr[key].units + ']')

        # find the legend if this is a vector
        for item in xr[key].coords:
            if item != 'Timestamp':
                options(key, 'legend_names', xr[key].coords[item].values.tolist())

        if saved:
            out.append(key)
        else:
            logging.warning('Problem saving: ' + key)
    return out

from pyspedas.vires.load import load


def data(trange=None,
         collection=None,
         measurements=None,
         models=None,
         sampling_step=None,
         auxiliaries=None,
         residuals=False):
    """
    Parameters
    ----------
    trange: list of str
        The time range for data to be loaded
    collection: str
        The data set to be loaded
    measurements: list of str
        The variables to be loaded from the specified collection
    models: list of str
        See viresclient documentation for more information
    sampling_step: str
        See viresclient documentation for more information
    auxiliaries: list of str
        See viresclient documentation for more information
    residuals: Optional
        See viresclient documentation for more information

    Returns
    -------
    list of str
        List of tplot variables loaded

    Examples
    --------

    >>> # Browse available collections
    >>> from viresclient import SwarmRequest
    >>> from pyspedas.vires.config import CONFIG
    >>> self.assertNotEqual(CONFIG['access_token'],'')
    >>> collections = SwarmRequest(url="https://vires.services/ows",token=CONFIG['access_token']).available_collections()
    >>> print(collections)

    >>> # Load SWARM-A magnetometer data
    >>> import pyspedas
    >>> from pytplot import tplot
    >>> vires_vars = pyspedas.vires.load(trange=['2014-01-01T00:00', '2014-01-01T01:00'],
    >>>                                  collection="SW_OPER_MAGA_LR_1B",
    >>>                                  measurements=["F", "B_NEC"],
    >>>                                  models=["CHAOS-Core"],
    >>>                                  sampling_step="PT10S",
    >>>                                  auxiliaries=["QDLat", "QDLon"])
    >>> tplot(['Longitude', 'Latitude', 'B_NEC'])

    """
    return load(trange=trange,
                collection=collection,
                measurements=measurements,
                models=models,
                sampling_step=sampling_step,
                auxiliaries=auxiliaries,
                residuals=residuals)

from .load import load
from pyspedas.utilities.datasets import find_datasets


def data(trange=['2013-11-5', '2013-11-6'],
        datatype='1min',
        level='hro2',
        prefix='',
        suffix='',  
        get_support_data=False, 
        get_ignore_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=True):
    """
    Loads OMNI (Combined 1AU IP Data; Magnetic and Solar Indices) data.

    Parameters
    ----------
    trange : list of str
        Time range of interest specified as ['starttime', 'endtime'] with the format
        'YYYY-MM-DD' or 'YYYY-MM-DD/hh:mm:ss' to specify more or less than a day.
        Default: ['2013-11-5', '2013-11-6']
    datatype : str
        Data type; valid options: '1min', '5min', 'hourly' (1 hour).
        Default: '1min'
    level : str
        Data level; valid options: 'hro', 'hro2'.
        default='hro2'
    prefix : str, optional
        Prefix for the tplot variable names. By default, no prefix is added.
    suffix : str, optional
        Suffix for the tplot variable names.
    get_support_data : bool
        If True, loads data with "VAR_TYPE" attribute value "support_data" into tplot.
        Default: False
    get_ignore_data : bool
        If True, ignores loading certain data. This parameter is not documented in the original function signature.
        Default: False
    varformat : str, optional
        If specified, variables matching this wildcard pattern will be loaded from the CDFs
        Default: all variables are loaded.
    varnames : list of str, optional
        List of variable names to load. If not specified, all data variables are loaded.
    downloadonly : bool
        If True, downloads the CDF files but does not load them into tplot variables. Default: False
    notplot : bool
        If True, returns the data in hash tables instead of creating tplot variables. Default: False
    no_update : bool
        If True, loads data only from the local cache. Default: False.
    time_clip : bool
        If True, clips the variables to exactly the range specified in the trange parameter. Default: True

    Returns
    -------
    list
        List of tplot variables created.

    Examples
    --------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> # This example will load 5-minute resolution data for the specified time range.
    >>> pyspedas.omni.data(trange=['2020-01-01', '2020-01-02'], datatype='5min', level='hro2')
    >>> tplot(['BX_GSE', 'BY_GSE', 'BZ_GSE', 'flow_speed', 'Vx', 'Vy', 'Vz', 'SYM_H'])
    """
    return load(trange=trange, level=level, datatype=datatype, prefix=prefix, suffix=suffix, 
                get_support_data=get_support_data, get_ignore_data=get_ignore_data,varformat=varformat, 
                varnames=varnames, downloadonly=downloadonly, notplot=notplot, 
                time_clip=time_clip, no_update=no_update)


def datasets(instrument=None, label=True):
    """
    Retrieves available datasets.

    Parameters
    ----------
    instrument : str, optional
        This variable is unused. The instrument is hardcoded for 'OMNI'
    label : bool, default=True
        Determines whether the returned datasets include descriptive labels. If True, datasets are
        returned with labels; otherwise, only dataset identifiers are returned.

    Returns
    -------
    list
        A list of available datasets. The format of the list items depends on the `label` parameter.

    Notes
    -----
    - This function is a utility for finding datasets associated with a specific mission,
      optionally filtered by instrument. It primarily serves as a wrapper for a more
      generalized dataset finding function, allowing users to specify the mission and
      instrument of interest.
    - The mission is hardcoded to 'ACE' and the instrument parameter defaults to 'OMNI',
      indicating that this function is tailored for retrieving datasets from the ACE mission
      with a focus on OMNI instrument data.
    """

    return find_datasets(mission='ACE', instrument='OMNI', label=label)

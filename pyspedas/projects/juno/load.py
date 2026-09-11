"""Load Juno data using the shared DAS2 download and parsing utilities."""

from pyspedas import time_float_one
from pyspedas.projects.juno.config import CONFIG
from pyspedas.utilities.das2.das2ascii import das2ascii
from pyspedas.utilities.das2.das2info import das2info
from pyspedas.utilities.das2.das2tplot import das2tplot


def get_info(datatype=""):
    """Get information about a Juno dataset from the University of Iowa DAS2 server.

    Parameters
    ----------
    datatype : str, optional
        Dataset abbreviation or full DAS2 dataset path from CONFIG["datasets"].
        Abbreviations are case-insensitive; full paths are case-sensitive.
        For example, "magnitude" and "Juno/FGM/Magnitude" select the same
        dataset. If omitted or empty, returns a list of all available datasets.

    Returns
    -------
    str
        Response text from the DAS2 server when the request succeeds, otherwise
        an empty string.

    Raises
    ------
    ValueError
        If datatype is unsupported.

    Examples
    --------
    >>> from pyspedas.projects.juno.load import get_info
    >>> info = get_info(datatype="magnitude")
    >>> isinstance(info, str)
    True
    """
    datasets = CONFIG["datasets"]

    if not isinstance(datatype, str):
        raise TypeError("datatype must be a string")
    # Keep the matching entry so its full path can identify the remote dataset.
    dataset = next(
        (item for item in datasets if datatype.lower() == item["abrev"] or datatype == item["full_set"]),
        None,
    )
    if dataset is None:
        names = [item["abrev"] for item in datasets]
        raise ValueError(f"datatype must be one of {names} or its full dataset path, got {datatype}")

    res = das2info(
        url=CONFIG["remote_data_dir"],
        server="dsdf",
        dataset=dataset["full_set"],
    )

    return res


def load(
    trange=None,
    datatype="",
    prefix="",
    suffix="",
    interval=300,
    varnames=None,
    params=None,
    extra=None,
):
    """Load Juno data from the University of Iowa DAS2 server.

    Parameters
    ----------
    trange : list of str, required
        Start and end times, for example
        ["2020-02-02T12:00:00", "2020-02-02T14:00:00"].
        The range must not exceed two days.
        A valid range must be supplied; the default None is not accepted.
    datatype : str, required
        Dataset abbreviation or full DAS2 dataset path from CONFIG["datasets"].
        Abbreviations are case-insensitive; full paths are case-sensitive.
        For example, "magnitude" and "Juno/FGM/Magnitude" select the same
        dataset. A supported selector must be supplied; the default empty
        string is not accepted.
    prefix : str, optional
        Prefix added to each output variable name. If empty or omitted,
        defaults to the configured dataset abbreviation followed by "_".
        A supplied prefix replaces this default. Defaults to "".
    suffix : str, optional
        Suffix appended to each output variable name. Defaults to "".
    interval : int or float, optional
        Sampling interval in seconds passed to the DAS2 server. Defaults
        to 300. Its effect depends on the selected dataset.
    varnames : list of str, optional
        List of variable names to load from the dataset. If omitted or None,
        all variables are loaded. If supplied, the names must match those
        in the DAS2 dataset. The names are case-sensitive and must not include
        the prefix or suffix.
    params : str, optional
        Additional variables to include in the request. Defaults to None.
        Multiple variables should be separated by a single space, for example params="JLAT CLAT JULT".
    extra : str, optional
        Extra query parameters to include in the request. Defaults to None.
    Returns
    -------
    list of str
        Names of the tplot variables created from the DAS2 ASCII response.

    Raises
    ------
    TypeError
        If trange is not a list or datatype is not a string.
    ValueError
        If trange does not contain two entries, the end is not later than
        the start, the range exceeds two days, or datatype is unsupported.

    Examples
    --------
    >>> from pyspedas.projects.juno.load import load
    >>> variables = load(
    ...     trange=["2020-02-02T12:00:00", "2020-02-02T14:00:00"],
    ...     datatype="magnitude",
    ...     interval=300,
    ... )
    """
    url = CONFIG["remote_data_dir"]

    # Validate the start/end pair before sending a request to the DAS2 server.
    if type(trange) != list:
        raise TypeError("trange must be a list")
    elif len(trange) != 2:
        raise ValueError("trange must be a list of two strings")
    elif time_float_one(trange[0]) >= time_float_one(trange[1]):
        raise ValueError("trange start time must be before end time")
    elif time_float_one(trange[1]) - time_float_one(trange[0]) > 172800.0:
        raise ValueError("trange must not exceed 2 days")

    datasets = CONFIG["datasets"]

    if not isinstance(datatype, str):
        raise TypeError("datatype must be a string")
    # Keep the matching entry so its full path can identify the remote dataset
    # and its abbreviation can identify the resulting tplot variables.
    dataset = next(
        (item for item in datasets if datatype.lower() == item["abrev"] or datatype == item["full_set"]),
        None,
    )
    if dataset is None:
        names = [item["abrev"] for item in datasets]
        raise ValueError(f"datatype must be one of {names} or its full dataset path, got {datatype}")

    if not extra:
        extra = "ascii=true"

    # Get ascii data from the DAS2 server. The interval is passed to the server.
    data = das2ascii(
        url=url,
        server="dataset",
        dataset=dataset["full_set"],
        start_time=trange[0],
        end_time=trange[1],
        interval=interval,
        params=params,
        extra=extra,
    )

    # Parse the ASCII data and create tplot variables. The prefix is either the
    # supplied prefix or the dataset abbreviation followed by "_".
    abbr = prefix or dataset["abrev"] + "_"
    result = das2tplot(
        data,
        prefix=abbr,
        suffix=suffix,
        varnames=varnames,
    )

    return result


if __name__ == "__main__":
    # Test and plot some information about the Juno magnetic field magnitude dataset.
    from pyspedas import tplot

    trange = ["2020-01-01 02:00:00", "2020-01-01 03:00:00"]
    datatype = "jovicentric"
    params = "JLAT CLAT JULT"

    print("=============================== Info ===============================")
    info = get_info(datatype=datatype)
    print(info)

    print("=============================== varnames ===============================")
    vars = load(trange=trange, datatype=datatype, params=params)
    print(vars)
    tplot(vars)

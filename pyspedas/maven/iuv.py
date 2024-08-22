from .maven_load import load_data

# This routine was originally in maven/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

maven_load = load_data

def iuv(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype=None,
    suffix="",
    prefix="",
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
):
    """
    Load MAVEN IUV data.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level. Defaults to "l2".
    datatype : str, optional
        Data type. Defaults to None.
    suffix: str
        The tplot variable names will be given this suffix.
        Default: '', no suffix is added.
    prefix: str
        The tplot variable names will be given this prefix.
        Default: '', no prefix is added.
    varformat : str, optional
        Variable format. Defaults to None.
    get_support_data : bool, optional
        Whether to retrieve support data. Defaults to False.
    auto_yes : bool, optional
        Whether to automatically answer "yes" to prompts. Defaults to True.
    downloadonly : bool, optional
        Whether to only download the data without loading it. Defaults to False.
    varnames : list, optional
        List of variable names to load. Defaults to [].

    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """

    return maven_load(
        instruments="iuv",
        start_date=trange[0],
        end_date=trange[1],
        type=datatype,
        level=level,
        suffix=suffix,
        prefix=prefix,
        varformat=varformat,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )

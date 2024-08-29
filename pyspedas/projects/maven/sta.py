from .maven_load import load_data
import pyspedas.projects.maven.spdf as spdf_load

# This routine was originally in maven/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

maven_load = load_data

def sta(
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
    spdf=False,
):
    """
    Function to load MAVEN STA data.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level. Defaults to "l2".
    datatype : str, optional
        Data type. Defaults to "c0-64e2m" (spdf) or None (all data loaded) (MAVEN SDC)
        Valid options (for MAVEN SDC)::

            2a, c0, c2, c4, c6, c8, ca, cc, cd, ce, cf, d0, d1, d4, d6, d7, d8, d9, da, db

    varformat : str, optional
        Variable format. Defaults to None.
    suffix: str
        The tplot variable names will be given this suffix.
        Default: '', no suffix is added.
    prefix: str
        The tplot variable names will be given this prefix.
        Default: '', no prefix is added.
    get_support_data : bool, optional
        Whether to retrieve support data. Defaults to False.
    auto_yes : bool, optional
        Whether to automatically answer "yes" to prompts. Defaults to True.
    downloadonly : bool, optional
        Whether to only download the data without loading it. Defaults to False.
    varnames : list, optional
        List of variable names to load. Defaults to [].
    spdf : bool, optional
        Whether to use the SPDF library for loading data. Defaults to False.

    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """

    if spdf:
        if datatype is None:
            datatype = "c0-64e2m"
        return spdf_load.static(
            trange=trange,
            level=level,
            datatype=datatype,
            varformat=varformat,
            get_support_data=get_support_data,
            downloadonly=downloadonly,
            varnames=varnames,
        )
    if datatype is None:
        datatype = None
    return maven_load(
        instruments="sta",
        start_date=trange[0],
        end_date=trange[1],
        type=datatype,
        level=level,
        varformat=varformat,
        suffix=suffix,
        prefix=prefix,
        get_metadata=True,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )

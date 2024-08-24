from .maven_load import load_data
import pyspedas.projects.maven.spdf as spdf_load

# This routine was originally in maven/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

maven_load = load_data

def kp(
    trange=["2016-01-01", "2016-01-02"],
    datatype=None,
    varformat=None,
    suffix="",
    prefix="",
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
    insitu=True,
    iuvs=False,
    spdf=False,
):
    """
    Load MAVEN KP (Key Parameters) data.

    Parameters:
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    datatype : str, optional
        Type of data to load. Default is None.
    varformat : str, optional
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
    insitu : bool, optional
        Flag indicating whether to load insitu data. Default is True.
    iuvs : bool, optional
        Flag indicating whether to load IUVS data. Default is False.
    spdf : bool, optional
        Flag indicating whether to use the SPDF library for loading data. Default is False.

    Returns:
    -------
    dict
        Dictionary of loaded data variables.

    """

    if spdf:
        if datatype is None:
            datatype = "kp-4sec"
        return spdf_load.kp(
            trange=trange,
            datatype=datatype,
            varformat=varformat,
            get_support_data=get_support_data,
        )
    return maven_load(
        start_date=trange[0],
        end_date=trange[1],
        type=datatype,
        level="kp",
        varformat=varformat,
        suffix=suffix,
        prefix=prefix,
        varnames=varnames,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        insitu=insitu,
        iuvs=iuvs,
    )

from .maven_load import load_data
import pyspedas.projects.maven.spdf as spdf_load

# This routine was originally in maven/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

maven_load = load_data

def swia(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype="onboardsvyspec",
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
    Load MAVEN Solar Wind Ion Analyzer (SWIA) data.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level to load. Default is "l2".
    datatype : str, optional
        Data type to load. Default is "onboardsvyspec".
    suffix: str
        The tplot variable names will be given this suffix.
        Default: '', no suffix is added.
    prefix: str
        The tplot variable names will be given this prefix.
        Default: '', no prefix is added.
    varformat : str, optional
        Variable format. Default is None.
    get_support_data : bool, optional
        Whether to retrieve support data. Defaults to False.
    auto_yes : bool, optional
        Whether to automatically answer "yes" to prompts. Default is True.
    downloadonly : bool, optional
        Whether to only download the data without loading it. Defaults to False.
    varnames : list, optional
        List of variable names to load. Defaults to [].
    spdf : bool, optional
        Whether to use the SPDF library for loading the data. Default is False.

    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """
    if spdf:
        return spdf_load.swia(
            trange=trange,
            level=level,
            datatype=datatype,
            varformat=varformat,
            get_support_data=get_support_data,
            downloadonly=downloadonly,
            varnames=varnames,
        )
    return maven_load(
        instruments="swi",
        start_date=trange[0],
        end_date=trange[1],
        type=datatype,
        level=level,
        varformat=varformat,
        suffix=suffix,
        prefix=prefix,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )

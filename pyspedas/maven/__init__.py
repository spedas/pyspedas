from .maven_load import load_data
import pyspedas.maven.spdf as spdf_load

maven_load = load_data



def euv(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype="bands",
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
):
    """
    Load EUV data from the MAVEN mission.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level. Defaults to "l2".
    datatype : str, optional
        Data type. Defaults to "bands".
    varformat : str, optional
        Variable format. Defaults to None.
    get_support_data : bool, optional
        Whether to retrieve support data. Defaults to False.
    auto_yes : bool, optional
        Whether to automatically answer yes to prompts. Defaults to True.
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
        instruments="euv",
        start_date=trange[0],
        end_date=trange[1],
        type=datatype,
        level=level,
        varformat=varformat,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )


def iuv(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype=None,
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
        varformat=varformat,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )


def ngi(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype=None,
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
):
    """
    Load NGI data from the MAVEN mission.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level. Defaults to "l2".
    datatype : str, optional
        Data type. Defaults to None.
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
        instruments="ngi",
        start_date=trange[0],
        end_date=trange[1],
        type=datatype,
        level=level,
        varformat=varformat,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )

from .maven_load import load_data
import pyspedas.maven.spdf as spdf_load


maven_load = load_data


def kp(
    trange=["2016-01-01", "2016-01-02"],
    datatype=None,
    varformat=None,
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
        Format of the variable names. Default is None.
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
        varnames=varnames,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        insitu=insitu,
        iuvs=iuvs,
    )


def mag(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype=None,
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
    spdf=False,
):
    """
    Function to retrieve Magnetometer (MAG) data from the MAVEN mission.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level to retrieve. Defaults to "l2".
    datatype : str, optional
        Data type to retrieve. Defaults to None.
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
    spdf : bool, optional
        Flag indicating whether to use the SPDF library for loading data. Default is False.

    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """

    if spdf:
        if datatype is None:
            datatype = "sunstate-1sec"
        return spdf_load.mag(
            trange=trange,
            level=level,
            datatype=datatype,
            varformat=varformat,
            get_support_data=get_support_data,
            downloadonly=downloadonly,
            varnames=varnames,
        )
    if datatype is None:
        datatype = "ss"
    return maven_load(
        instruments="mag",
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


def sta(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype=None,
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
        get_metadata=True,
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )


def swea(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype="svyspec",
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
    spdf=False,
):
    """
    Load MAVEN Solar Wind Electron Analyzer (SWEA) data.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level. Defaults to "l2".
    datatype : str, optional
        Data type. Defaults to "svyspec".
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
    spdf : bool, optional
        Whether to use the SPDF library for data loading. Defaults to False.

    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """

    if spdf:
        return spdf_load.swea(
            trange=trange,
            level=level,
            datatype=datatype,
            varformat=varformat,
            get_support_data=get_support_data,
            downloadonly=downloadonly,
            varnames=varnames,
        )
    return maven_load(
        instruments="swe",
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


def swia(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype="onboardsvyspec",
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
        get_support_data=get_support_data,
        auto_yes=auto_yes,
        download_only=downloadonly,
        varnames=varnames,
    )


def sep(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype="s2-cal-svy-full",
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
    spdf=False,
):
    """
    Loads MAVEN Solar Energetic Particle (SEP) data.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str, optional
        Data level. Defaults to "l2".
    datatype : str, optional
        Data type. Defaults to "s2-cal-svy-full".
    varformat : str, optional
        Variable format. Defaults to None.
    get_support_data : bool, optional
        Whether to download support data. Defaults to False.
    auto_yes : bool, optional
        Whether to automatically answer 'yes' to all prompts. Defaults to True.
    downloadonly : bool, optional
        Whether to only download the data without loading it. Defaults to False.
    varnames : list, optional
        List of variable names to load. Defaults to [].
    spdf : bool, optional
        Whether to use the SPDF library for loading the data. Defaults to False.

    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """

    if spdf:
        return spdf_load.sep(
            trange=trange,
            level=level,
            datatype=datatype,
            varformat=varformat,
            get_support_data=get_support_data,
            downloadonly=downloadonly,
            varnames=varnames,
        )
    return maven_load(
        instruments="sep",
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


def rse(
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
    Load MAVEN RSE data for the specified time range and parameters.

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
        instruments="rse",
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


def lpw(
    trange=["2016-01-01", "2016-01-02"],
    level="l2",
    datatype="lpiv",
    varformat=None,
    get_support_data=False,
    auto_yes=True,
    downloadonly=False,
    varnames=[],
):
    """
    Load LPW (Langmuir Probe and Waves) data from the MAVEN mission.

    Parameters
    ----------
    trange : list, optional
        Time range of the data in the format ["start_date", "end_date"].
        Defaults to ["2016-01-01", "2016-01-02"].
    level : str
        Data level to retrieve (e.g., "l1", "l2", "l3").
    datatype : str
        Type of data to retrieve (e.g., "lpiv", "lpwt").
    varformat : str
        Format of the variable names.
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
        instruments="lpw",
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

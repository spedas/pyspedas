import logging
import requests
from pyspedas.projects.themis.load import load


class Themis_gmag:
    """This object holds the dictionary of gmag stations and their metadata"""

    def __init__(self):
        self.gmag_dict = {}

    def query_gmags(self):
        """Fills a dictionary of gmag stations and all their metadata"""

        url = "http://themis.ssl.berkeley.edu/gmag/gmag_json.php"

        params = dict(station="", group="")
        resp = requests.get(url=url, params=params)
        data = resp.json()
        self.gmag_dict = data

    def get_gmag_list(self):
        """returns the gmag dictionary, querying if necessary"""
        if self.gmag_dict == {}:
            self.query_gmags()
        return self.gmag_dict


themis_gmag_dict = Themis_gmag()


def gmag(
    trange=["2007-03-23", "2007-03-24"],
    sites=None,
    group=None,
    level="l2",
    prefix="",
    suffix="",
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=False,
    force_download=False,
):
    """
    Load ground magnetometer data from the THEMIS mission.

    Parameters
    ----------
    trange : list, optional
        Time range of interest in the format ["start_date", "end_date"].
        Default is ["2007-03-23", "2007-03-24"].
    sites : list or str, optional
        List of ground magnetometer sites to load data for. If None, data
        for all available sites will be loaded. Default is None.
    group : str, optional
        Name of a pre-defined group of sites to load data for. If specified,
        the 'sites' parameter will be ignored. Default is None.
    level : str, optional
        Data level to load. Default is "l2".
    prefix : str, optional
        Prefix to append to the variable names. Default is "".
    suffix : str, optional
        Suffix to append to the variable names. Default is "".
    get_support_data : bool, optional
        Flag indicating whether to download support data. Default is False.
    varformat : str, optional
        Format of the variable names. Default is None.
    varnames : list, optional
        List of specific variable names to load. Default is [].
    downloadonly : bool, optional
        Flag indicating whether to only download the data without loading it.
        Default is False.
    notplot : bool, optional
        Flag indicating whether to plot the loaded data. Default is False.
    no_update : bool, optional
        Flag indicating whether to update the data files. Default is False.
    time_clip : bool, optional
        Flag indicating whether to clip the data to the specified time range.
        Default is False.
    force_download: bool, optional
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    dict
        A dictionary containing the loaded data.

    Examples
    --------
    >>> from pyspedas.projects.themis import gmag
    >>> from pyspedas import tplot
    >>>
    >>> # Load ground magnetometer data for specific sites and time range
    >>> gmag_vars = gmag(sites=['ccnv','bmls'], trange=['2013-11-05', '2013-11-06'])
    >>> tplot(['thg_mag_bmls', 'thg_mag_ccnv'])
    """

    if sites is None:
        thm_sites = (
            "idx atha chbg ekat fsim fsmi fykn gbay glyn gill inuv kapu "
            "kian kuuj mcgr nrsq pgeo pina rank snap snkq tpas whit "
            "yknf".split(" ")
        )
        tgo_sites = [
            "nal",
            "lyr",
            "hop",
            "bjn",
            "nor",
            "sor",
            "tro",
            "and",
            "don",
            "rvk",
            "sol",
            "kar",
            "jan",
            "jck",
            "dob",
        ]
        dtu_sites = [
            "atu",
            "dmh",
            "svs",
            "tdc",
            "bfe",
            "roe",
            "thl",
            "kuv",
            "upn",
            "umq",
            "gdh",
            "stf",
            "skt",
            "ghb",
            "fhb",
            "naq",
            "amk",
            "sco",
            "tab",
            "sum",
            "hov",
        ]
        ua_sites = [
            "arct",
            "bett",
            "cigo",
            "eagl",
            "fykn",
            "gako",
            "hlms",
            "homr",
            "kako",
            "pokr",
            "trap",
        ]
        maccs_sites = ["cdrt", "chbr", "crvr", "gjoa", "iglo", "nain", "pang", "rbay"]
        usgs_sites = [
            "bou",
            "brw",
            "bsl",
            "cmo",
            "ded",
            "frd",
            "frn",
            "gua",
            "hon",
            "new",
            "shu",
            "sit",
            "sjg",
            "tuc",
        ]
        atha_sites = [
            "roth",
            "leth",
            "redr",
            "larg",
            "vldr",
            "salu",
            "akul",
            "puvr",
            "inuk",
            "kjpk",
            "radi",
            "stfl",
            "sept",
            "schf",
        ]
        epo_sites = [
            "bmls",
            "ccnv",
            "drby",
            "fyts",
            "hots",
            "loys",
            "pgeo",
            "pine",
            "ptrs",
            "rmus",
            "swno",
            "ukia",
        ]
        falcon_sites = ["hris", "kodk", "lrel", "pblo", "stfd", "wlps"]
        mcmac_sites = ["amer", "benn", "glyn", "lyfd", "pcel", "rich", "satx", "wrth"]
        nrcan_sites = ["blc", "cbb", "iqa", "mea", "ott", "stj", "vic"]
        step_sites = ["fsj", "ftn", "hrp", "lcl", "lrg", "pks", "whs"]
        fmi_sites = [
            "han",
            "iva",
            "kev",
            "kil",
            "mas",
            "mek",
            "muo",
            "nur",
            "ouj",
            "pel",
            "ran",
            "tar",
        ]
        aair_sites = ["amd", "bbg", "brn", "dik", "loz", "pbk", "tik", "viz"]
        carisma_sites = [
            "anna",
            "back",
            "cont",
            "daws",
            "eski",
            "fchp",
            "fchu",
            "gull",
            "isll",
            "lgrr",
            "mcmu",
            "mstk",
            "norm",
            "osak",
            "oxfo",
            "pols",
            "rabb",
            "sach",
            "talo",
            "thrf",
            "vulc",
            "weyb",
            "wgry",
        ]
        sites = (
            thm_sites
            + tgo_sites
            + dtu_sites
            + ua_sites
            + maccs_sites
            + usgs_sites
            + atha_sites
            + epo_sites
            + falcon_sites
            + mcmac_sites
            + nrcan_sites
            + step_sites
            + fmi_sites
            + aair_sites
            + carisma_sites
        )

    if group is not None:
        sites = eval(group + "_sites")

    if not isinstance(sites, list):
        sites = [sites]

    # check for sites in Greenland
    greenland = []
    for site in sites:
        if check_greenland(site):
            greenland.append(True)
        else:
            greenland.append(False)

    return load(
        instrument="gmag",
        trange=trange,
        level=level,
        prefix=prefix,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        stations=sites,
        greenland=greenland,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
    )


def get_group(station_name):
    """
    Returns a list of groups a particular station belongs to.

    Parameters
    ----------
    station_name : str, required
        The station name.

    Returns
    -------
    list
        A list of station groups.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import get_group
    >>> atha_groups = get_group("atha")
    >>> print(atha_groups)
    ['ae', 'asi', 'carisma']
    """

    group_list = []
    gmag_dict = themis_gmag_dict.get_gmag_list()
    station_name = station_name.lower()

    for station in gmag_dict:
        if station["ccode"].lower() == station_name:
            for key, value in station.items():
                if value == "Y":
                    if station["ccode"].lower() not in group_list:
                        group_list.append(key)

    return group_list


def gmag_list(group="all"):
    """
    Returns a list of ground magnetometer station names based on the specified group.

    Parameters
    ----------
    group : str, optional
        The group of stations to filter by. Default is "all".

    Returns
    -------
    list
        A list of station names.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import gmag_list
    >>> epo_list = gmag_list("EPO")
    >>> print(epo_list)
    ['bmls', 'ccnv', 'drby', 'hots', 'loys', 'ptrs', 'ukia']
    """

    station_list = []
    gmag_dict = themis_gmag_dict.get_gmag_list()
    group = group.lower()

    for station in gmag_dict:
        station_name = station["ccode"].lower()
        station_group = get_group(station_name)
        if group in ["all", "*", ""] or group in station_group:
            station_list.append(station_name)
            logging.info(
                station_name
                + ": from "
                + station["day_first"]
                + " to "
                + station["day_last"]
            )

    return station_list


def gmag_groups():
    """
    Returns a dictionary containing groups of stations and their station codes.

    Returns
    -------
    dict
        A dictionary where the keys represent the gmag values and the values are lists of station codes.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import gmag_groups
    >>> groups = gmag_groups()
    >>> groups.keys()  # all groups
    dict_keys(['kyoto', 'sgu', 'autx', 'ae', 'aari', 'dtu', 'greenland', 'tgo', 'asi', 'carisma', 'mcmac',
    'nrcan', 'epo', 'usgs', 'maccs', 'gima', 'cgsm', 'gbo', 'autu', 'leirv', 'pen', 'falcon', 'fmi', 'secs', 'bas'])
    >>> groups['epo']  # stations in the EPO group
    ['bmls', 'ccnv', 'drby', 'hots', 'loys', 'ptrs', 'ukia']
    """
    group_dict = {}
    gmag_dict = themis_gmag_dict.get_gmag_list()

    for station in gmag_dict:
        for key, value in station.items():
            if value == "Y" or value == "N":
                if key in group_dict:
                    if station["ccode"].lower() not in group_dict[key]:
                        group_dict[key].append(station["ccode"].lower())
                else:
                    group_dict[key] = []
                    group_dict[key].append(station["ccode"].lower())

    # print the groups
    for g, s in group_dict.items():
        logging.info(g + ":" + ",'".join(s) + "'")

    return group_dict


def check_gmag(station_name):
    """
    Check if a station name exists in the gmag dictionary.

    Parameters
    ----------
    station_name : str
        The name of the station to check.

    Returns
    -------
    int
        Returns 1 if the station name exists in the gmag dictionary, otherwise returns 0.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import check_gmag
    >>> check_gmag("atha")
    1
    """

    gmag_dict = themis_gmag_dict.get_gmag_list()

    for station in gmag_dict:
        if station["ccode"].lower() == station_name.lower():
            return 1

    return 0


def check_greenland(station_name):
    """
    Check if a given station belongs to the Greenland group.

    Parameters
    ----------
    station_name : str
        The name of the station to check.

    Returns
    -------
    int
        Returns 1 if the station is in Greenland, otherwise returns 0.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import check_greenland
    >>> check_greenland("bfe")
    1
    """

    gmag_dict = themis_gmag_dict.get_gmag_list()

    for station in gmag_dict:
        if station["ccode"].lower() == station_name.lower():
            if (
                station["country"] is not None
                and station["country"].lower() == "greenland"
            ) or (
                station["greenland"] is not None and station["greenland"].lower() == "y"
            ):
                return 1

    return 0

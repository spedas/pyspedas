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
    sampling_rate=1,
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
    sampling_rate: int, optional
        Specify a sampling rate for loading variometer data. Accepts 1 (Hz) or 10 (Hz).
        Default: 1
    Returns
    -------
    dict
        A dictionary containing the loaded data.

    Examples
    --------
    >>> from pyspedas.projects.themis import gmag
    >>> from pyspedas import tplot
    >>> from pyspedas import subtract_median
    >>>
    >>> # Load ground magnetometer data for specific sites and time range
    >>> gmag_vars = gmag(sites=['ccnv','bmls'], trange=['2013-11-05', '2013-11-06'])
    >>> tplot(['thg_mag_bmls', 'thg_mag_ccnv'])
    >>>
    >>> # Load variometer data for specific sites and time range:
    >>> gmag_vars = gmag(sites=['s61a','anmo'], trange=['2026-02-24', '2026-02-25'])
    >>> subtract_median(['thg_mag_s61a', 'thg_mag_anmo'])    
    >>> tplot(['thg_mag_s61a-m', 'thg_mag_anmo-m'])
    >>>
    >>> # Load 10 Hz variometer data for specific sites and time range:
    >>> gmag_vars = gmag(sites=['s61a','anmo'], sampling_rate=10, trange=['2026-02-24', '2026-02-25'])
    >>> subtract_median(['thg_mag_s61a_100ms', 'thg_mag_anmo_100ms']) 
    >>> tplot(['thg_mag_s61a_100ms-m', 'thg_mag_anmo_100ms-m'])
    >>>
    >>> # Load 10 Hz variometer data for specific sites and time range using the 10 Hz file name format:
    >>> gmag_vars = gmag(sites=['s61a_100ms','anmo_100ms'], trange=['2026-02-24', '2026-02-25'])
    >>> subtract_median(['thg_mag_s61a_100ms', 'thg_mag_anmo_100ms'])
    >>> tplot(['thg_mag_s61a_100ms-m', 'thg_mag_anmo_100ms-m'])
    >>>
    
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
        variometer_sites=[
            "anmo",
            "casy",
            "ccm",
            "cola",
            "cor",
            "dgmt",
            "dwpf",
            "ecsd",
            "eymn",
            "e46a",
            "e62a",
            "goga",
            "hrv",
            "j47a",
            "kbs",
            "kevo",
            "kono",
            "ksu1",
            "k30b",
            "k50a",
            "mbwa",
            "mstx",
            "m63a",
            "o20a",
            "pab",
            "p57a",
            "qspa",
            "rssd",
            "r49a",
            "sba",
            "sfjd",
            "spmn",
            "sspa",
            "s61a",
            "t47a",
            "u38b",
            "wci",
            "whtx",
            "wvt",
            "352a"
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
            + variometer_sites
        )

    if group is not None:
        sites = eval(group + "_sites")

    if not isinstance(sites, list):
        sites = [sites]

    # check for sites in Variometer group
    variometer = []
    for site in sites:
        s_rate=check_variometer(site)
        # if check_variometer determines site
        # to be 1 Hz sampling rate, check if 
        # sampling_rate argument has been set
        if (s_rate == 1) and (sampling_rate is not None):
            # if so, pass sampling_rate value
            # (case where variometer base names
            # are passed, but 10 Hz sampling rate
            # data is to be loaded)
            
            # check if sampling_rate is valid:
            if sampling_rate not in [1,10]:
                # throw error
                logging.error('sampling_rate must be either 1 or 10. Setting to default value of 1')
                sampling_rate=1
            
            variometer.append(sampling_rate) 
        else:
            variometer.append(s_rate)

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
        variometer=variometer,
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

def check_variometer(station_name):
    """
    Check if a given station belongs to the Variometers group. 
    If so, check if the given stationname is formatted to request 
    data in the 10 Hz sampling rate.

    Parameters
    ----------
    station_name : str
        The name of the station to check.

    Returns
    -------
    int
        Returns sampling rate (1 or 10) if the station is in the variometers group, otherwise returns 0.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import check_variometer
    >>> check_variometer("s61a")
    1
    >>> check_variometer("s61a_100ms")
    10
    """

    # check if station_name contains "_100ms". If it does,
    # create copy of station name with the "_100ms" 
    # substring removed
    if "_100ms" in station_name.lower():
        station_name_base=station_name.lower()
        station_name_base=station_name_base.replace("_100ms","")
    else:
        station_name_base=station_name.lower()
    
    gmag_dict = themis_gmag_dict.get_gmag_list()
    for station in gmag_dict:
        # compare a copy of station name with any "_100ms" 
        # substring removed with the station ccode
        if station["ccode"].lower() == station_name_base:
            if (
                station["variom"] is not None and station["variom"].lower() == "y"
            ):
                if "_100ms" in station_name.lower():
                    return 10
                else:
                    return 1
    return 0
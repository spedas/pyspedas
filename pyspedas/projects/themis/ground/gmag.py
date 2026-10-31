import logging
import requests
import pandas as pd
from io import BytesIO
from pyspedas.projects.themis.load import load
from pyspedas.utilities.download import download

from pyspedas.projects.themis.config import CONFIG


remote_data_dir = CONFIG['remote_data_dir']

# TODO: needs to save somewhere locally once query_gmags is called. Should also attempt to load locally when initialized.
class GMAG_Info():
    """This object holds the table of gmag stations and their metadata"""
    def __init__(self,no_download:bool=False):
        # Initialize empty table:
        self.table = pd.DataFrame()
        self.no_download = no_download
        # Load GMAG info:
        self.table = self.get_gmag_info()
        # Note: the final info column should always be "notes"
        self._infocols = list(self.table.loc[:,:'notes'].columns)
        # Prepare group list:
        self.group_codes = self.get_group_opts()
        # Prepare sources list:
        self.network_codes = self.get_network_opts()
        # Prepare station codes list:
        self.station_codes = self.get_station_opts()
        # Prepare alt time resolutions:
        self.alt_time_resolution = self.get_alt_time_resolution_opts()

    def query_gmags(self):
        """Fills a Pandas DataFrame of gmag stations and all their metadata"""
        # url = "https://themis.ssl.berkeley.edu/gmag/gmags_meta.csv"
        # resp = requests.get(url=url)
        # resp.raise_for_status()
        # # convert response into Pandas dataframe:
        # self.table = pd.read_csv(BytesIO(resp.content))
        file = None
        if not self.no_download:
            file = download(remote_file="thg/gmags_meta.csv",
                            remote_path=remote_data_dir,
                            local_path=CONFIG['local_data_dir'],
                            no_download=CONFIG["no_download"])
        if file is not None:
            # load from newly downloaded file:
            self.table = pd.read_csv(file)
        else:
            # attempt to load local file:
            self.table = pd.read_csv(CONFIG['local_data_dir'] + "thg/gmags_meta.csv")

    def get_gmag_info(self) -> pd.DataFrame:
        """returns the gmag table, querying if necessary"""
        self.query_gmags()
        return self.table
    
    def get_group_opts(self) -> list:
        """returns possible groups which stations can be associated with"""
        if self.table.empty: 
            self.query_gmags()
        group_opts = list(set(self.table.columns) - set(self._infocols))
        group_opts.sort()
        return list(map(str.lower, group_opts))
    
    def get_network_opts(self) -> list:
        if self.table.empty: 
            self.query_gmags()
        network_opts = list(set(self.table[self.table["network_code"].notnull()]["network_code"]))
        network_opts.sort()
        return list(map(str.lower, network_opts))

    def get_station_opts(self) -> list:
        if self.table.empty: 
            self.query_gmags()
        station_opts = list(set(self.table[self.table["network_code"].notnull()]["ccode"]))
        station_opts.sort()
        return list(map(str.lower, station_opts))

    def get_alt_time_resolution_opts(self) -> list:
        if self.table.empty: 
            self.query_gmags()
        t_res_opts = list(set(self.table[self.table["alt_period"].notnull()]["alt_period"]))
        t_res_opts.sort()
        return t_res_opts

gmag_info = GMAG_Info()

# TODO: update description
def gmag(
    trange=["2007-03-23", "2007-03-24"],
    stations:str | list[str] | None = None,
    group:str | list[str] | None = None,
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
    time_resolution:str="",
    version=None,
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
    version: str, optional
        CDF version to use in place of a version wildcard, e.g. "v01".
        Default: None, which preserves the default file selection.

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
    if stations is None:
        if group is not None:
            stations = get_gmag_stations_from_group(group)
        else:
            raise ValueError("Insufficient argument: stations or group must be specified.")

    if not isinstance(stations, list):
        stations = [stations]

    gmag_groups=[]
    for i in range(len(stations)):
        ccode_split = _split_station_code_time_res(stations[i])
        ccode = clean_gmag_station_codes(ccode_split[0])

        if in_gmag_group(ccode,"variom"):
            g_group = "variom"
        elif in_gmag_group(ccode,"greenland"):
            g_group = "greenland"
        else:
            g_group = ""
        gmag_groups.append(g_group)

        if time_resolution != "":
            stations[i] = ccode + "_" + time_resolution
        elif ccode_split[1] != "":
            stations[i] = ccode + "_" + ccode_split[1]
        else:
            stations[i] = ccode
    
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
        stations=stations,
        time_clip=time_clip,
        no_update=no_update,
        force_download=force_download,
        gmag_group=gmag_groups,
        version=version,
    )

def _split_station_code_time_res(station_code: str) -> list:
    code_split = station_code.split("_")
    if len(code_split) == 1:
        code_split.append("")
    return code_split
def _get_clean_station_code(station_code: str) -> str:
    return _split_station_code_time_res(station_code)[0]
def _get_time_res(station_code: str) -> str:
    return _split_station_code_time_res(station_code)[1]
def _check_time_res(station_code: str) -> None:
    """Check if a station code contains a valid time resolution"""
    code_split = _split_station_code_time_res(station_code)
    if code_split[1] != "" and is_gmag(code_split[0]):
        station_entry = get_station_entries(code_split[0])
        alt_period = station_entry["alt_period"].value
        if alt_period != code_split[1]:
            raise ValueError(f"Time resolution {code_split[1]} does not match alternate time resolution options: {alt_period}")
    return


def clean_gmag_station_codes(station_code: str | list[str]) -> list:
    """
    Takes station code or list of station codes, removes time resolution 
    string (if present), and returns sorted list of cleaned station codes. 
    """
    if isinstance(station_code,str):
        station_code = [station_code]
    for scode in station_code:
        _check_time_res(scode)
    codes = list(map(_get_clean_station_code,station_code))
    codes.sort()
    return codes


def get_station_entries(station_code: str | list[str]) -> pd.DataFrame:
    station_codes = clean_gmag_station_codes(station_code)
    station_idx = gmag_info.table["ccode"].isin(list(map(str.upper, station_codes)))
    if not any(station_idx):
        raise ValueError(f"Station code(s) '{station_code}' not found!")
    return gmag_info.table[station_idx]


def get_groups(station_code: str | list[str]) -> list:
    """
    Return a list of groups corresponding to provided station code(s).

    Parameters
    ----------
    station_code : str, required
        The station code.

    Returns
    -------
    list
        A list of station groups associated with the provided station code.

    Examples
    --------
    >>> from pyspedas.projects.themis.ground.gmag import get_group
    >>> atha_groups = get_group("atha")
    >>> print(atha_groups)
    ['ae', 'asi', 'carisma']
    """
    station_codes = clean_gmag_station_codes(station_code)
    station_entries = get_station_entries(station_codes)
    # Only select entries which are group labels:
    station_group_table = station_entries[gmag_info.group_codes]
    station_group_list_matches = list(station_group_table.columns[station_group_table.isin(["Y"]).any()])
    station_group_list_matches.sort()
    return station_group_list_matches


def get_networks(station_code: str | list[str]) -> list:
    """Return a list of source networks corresponding to provided station code(s)"""
    station_codes = clean_gmag_station_codes(station_code)
    station_entries = get_station_entries(station_codes)
    station_network_list = list(set(station_entries["network_code"]))
    station_network_list.sort()
    return station_network_list


def get_gmag_stations_from_group(group_code:str | list[str] = "all") -> list:
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
    if isinstance(group_code,str):
        group_code = [group_code]
    
    # make sure each group code is lowercase:
    group_list = list(map(str.lower, group_code))

    for wildcardstr in ["all","*",""]:
        if wildcardstr in group_list:
            group_list = gmag_info.group_codes
    
    outlier_groups = set(group_list) - set(gmag_info.group_codes)
    if len(outlier_groups) > 0:
        raise ValueError(f"Groups not found in GMAG table: {outlier_groups}")

    station_codes = list(gmag_info.table["ccode"][list(gmag_info.table[group_list].isin(["Y"]).any(axis=1))])
    station_codes = list(map(str.lower, station_codes))
    station_codes.sort()
    return station_codes


def get_gmag_groups() -> dict:
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
    for group in gmag_info.group_codes:
        group_dict[group] = get_gmag_stations_from_group(group)
    # print the groups
    for g, s in group_dict.items():
        logging.info(g + ":" + ",'".join(s) + "'")
    return group_dict


def in_gmag_group(station_code: str | list[str], group_code: str | list[str]) -> bool:
    station_codes = clean_gmag_station_codes(station_code)
    return len(set(station_codes)) - set(get_gmag_stations_from_group(group_code)) == 0


def is_gmag(station_code: str | list[str]) -> bool:
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
    station_codes = clean_gmag_station_codes(station_code)
    return in_gmag_group(station_codes, group_code = "all")


# TODO: remove
if __name__ == "__main__":
    #print(get_groups(["atha","anmo"]))
    #print(get_gmag_stations_from_group(["EPO","usgs"]))
    
    # networks: ['carisma', 'cgsm', 'dtu', 'gbo', 'gima', 'mcmac']
    thm_sites = ("idx atha chbg ekat fsim fsmi fykn gbay glyn gill inuv kapu kian kuuj mcgr nrsq pgeo pina rank snap snkq tpas whit yknf".split(" "))

    # networks: ['dtu', 'tgo']
    tgo_sites = ["nal","lyr","hop","bjn","nor","sor","tro","and","don","rvk","sol","kar","jan","jck","dob"]

    # networks: ['dtu']
    dtu_sites = ["atu","dmh","svs","tdc","bfe","roe","thl","kuv","upn","umq","gdh","stf","skt","ghb","fhb","naq","amk","sco","tab","sum","hov"]
    
    # networks: ['gima']
    ua_sites = ["arct","bett","cigo","eagl","fykn","gako","hlms","homr","kako","pokr","trap"]

    # networks: ['maccs']
    maccs_sites = ["cdrt","chbr","crvr","gjoa","iglo","nain","pang","rbay"]
    
    # networks: ['usgs']
    usgs_sites = ["bou","brw","bsl","cmo","ded","frd","frn","gua","hon","new","shu","sit","sjg","tuc"]
    
    # networks: ['autu', 'autx']
    atha_sites = ["roth","leth","redr","larg","vldr","salu","akul","puvr","inuk","kjpk","radi","stfl","sept","schf"]    

    # networks: ['epo', 'gbo']
    epo_sites = ["bmls","ccnv","drby","fyts","hots","loys","pgeo","pine","ptrs","rmus","swno","ukia"]    
    
    # networks: ['falcon']
    falcon_sites = ["hris", "kodk", "lrel", "pblo", "stfd", "wlps"]
    
    # networks: ['mcmac']
    mcmac_sites = ["amer", "benn", "glyn", "lyfd", "pcel", "rich", "satx", "wrth"]
    
    # networks: ['nrcan']
    nrcan_sites = ["blc", "cbb", "iqa", "mea", "ott", "stj", "vic"]
    
    # networks: ['step']
    step_sites = ["fsj", "ftn", "hrp", "lcl", "lrg", "pks", "whs"]
    
    # networks: ['fmi']
    fmi_sites = ["han","iva","kev","kil","mas","mek","muo","nur","ouj","pel","ran","tar"]    
    
    # networks: ['aari']
    aari_sites = ["amd", "bbg", "brn", "dik", "loz", "pbk", "tik", "viz"]
    
    # networks: [nan]
    carisma_sites = ["anna","back","cont","daws","eski","fchp","fchu","gull","isll","lgrr","mcmu","mstk","norm","osak","oxfo","pols","rabb","sach","talo","thrf","vulc","weyb","wgry"]    
    
    # networks: ['variom']
    variometer_sites=["154a","352a","456a","anmo","bouv","casy","ccm","cola","cor","dgmt","dwpf","e46a","e62a","ecsd","eymn","goga","hrv","j47a","k30b","k50a","k62a","kbs","kevo","kono","ksu1","m63a","mbwa","midw","mstx","n51a","n53a","o20a","p57a","pab","qspa","r49a","rssd","s39b","s61a","sba","sfjd","spmn","sspa","t47a","t57a","u38b","wci","whtx","wvt","x48a","y49a"]

    print(get_networks(atha_sites))
    
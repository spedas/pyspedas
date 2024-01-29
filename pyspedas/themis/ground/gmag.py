import logging
import requests

from pyspedas.themis.load import load


def gmag(trange=['2007-03-23', '2007-03-24'],
         sites=None,
         group=None,
         level='l2',
         suffix='',
         get_support_data=False,
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads ground magnetometer data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        level: str
            Data level; Valid options: 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  
            Default: False; only loads data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None; all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, so all data variables are loaded

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified
            in the trange keyword
            Default: False

        sites: str/list of str
            GMAG station names to load (e.g. 'bmls').
            Default: None, all available sites are loaded

        group: str
            GMAG group of sites (eg. 'epo').
            If specified, sites input is ignored.
            Default: None

    Returns
    -------
        List of str
        List of tplot variables created
        Empty list if no data
    
    Example
    -------
        import pyspedas
        from pytplot import tplot
        >>> gmag_vars = pyspedas.themis.gmag(sites=['ccnv','bmls'], trange=['2013-11-05', '2013-11-06'])
        >>> tplot(['thg_mag_bmls', 'thg_mag_ccnv'])

    """

    if sites is None:
        thm_sites = 'idx atha chbg ekat fsim fsmi fykn gbay glyn gill inuv kapu '\
                     'kian kuuj mcgr nrsq pgeo pina rank snap snkq tpas whit '\
                     'yknf'.split(' ')
        tgo_sites = ['nal', 'lyr', 'hop', 'bjn', 'nor', 'sor', 'tro', 'and',
                     'don', 'rvk', 'sol', 'kar', 'jan', 'jck', 'dob']
        dtu_sites = ['atu', 'dmh', 'svs', 'tdc', 'bfe', 'roe', 'thl', 'kuv',
                     'upn', 'umq', 'gdh', 'stf', 'skt', 'ghb', 'fhb', 'naq',
                     'amk', 'sco', 'tab', 'sum', 'hov']
        ua_sites = ['arct', 'bett', 'cigo', 'eagl', 'fykn', 'gako', 'hlms',
                    'homr', 'kako', 'pokr', 'trap']
        maccs_sites = ['cdrt', 'chbr', 'crvr', 'gjoa', 'iglo', 'nain',
                       'pang', 'rbay']
        usgs_sites = ['bou', 'brw', 'bsl', 'cmo', 'ded', 'frd', 'frn',
                      'gua', 'hon', 'new', 'shu', 'sit', 'sjg', 'tuc']
        atha_sites = ['roth', 'leth', 'redr', 'larg', 'vldr', 'salu', 'akul',
                      'puvr', 'inuk', 'kjpk', 'radi', 'stfl', 'sept', 'schf']
        epo_sites = ['bmls', 'ccnv', 'drby', 'fyts', 'hots', 'loys',
                     'pgeo', 'pine', 'ptrs', 'rmus', 'swno', 'ukia']
        falcon_sites = ['hris', 'kodk', 'lrel', 'pblo', 'stfd', 'wlps']
        mcmac_sites = ['amer', 'benn', 'glyn', 'lyfd', 'pcel', 'rich',
                       'satx', 'wrth']
        nrcan_sites = ['blc', 'cbb', 'iqa', 'mea', 'ott', 'stj', 'vic']
        step_sites = ['fsj', 'ftn', 'hrp', 'lcl', 'lrg', 'pks', 'whs']
        fmi_sites = ['han', 'iva', 'kev', 'kil', 'mas', 'mek', 'muo', 'nur',
                     'ouj', 'pel', 'ran', 'tar']
        aair_sites = ['amd', 'bbg', 'brn', 'dik', 'loz', 'pbk', 'tik', 'viz']
        carisma_sites = ['anna', 'back', 'cont', 'daws', 'eski', 'fchp',
                         'fchu', 'gull', 'isll', 'lgrr', 'mcmu', 'mstk',
                         'norm', 'osak', 'oxfo', 'pols', 'rabb', 'sach',
                         'talo', 'thrf', 'vulc', 'weyb', 'wgry']
        sites = (thm_sites + tgo_sites + dtu_sites + ua_sites + maccs_sites
                 + usgs_sites + atha_sites + epo_sites + falcon_sites
                 + mcmac_sites + nrcan_sites + step_sites + fmi_sites
                 + aair_sites + carisma_sites)

    if group is not None:
        sites = eval(group+'_sites')

    if not isinstance(sites, list):
        sites = [sites]

    # check for sites in Greenland
    greenland = []
    for site in sites:
        if check_greenland(site):
            greenland.append(True)
        else:
            greenland.append(False)

    return load(instrument='gmag', trange=trange, level=level,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot, stations=sites,
                greenland=greenland, time_clip=time_clip, no_update=no_update)


gmag_dict = {}


def query_gmags():
    """ returns a dictionary of gmag stations and all their metadata
    """

    url = 'http://themis.ssl.berkeley.edu/gmag/gmag_json.php'
    global gmag_dict

    params = dict(
        station='',
        group=''
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()
    gmag_dict = data

    return data


def get_group(station_name):
    """ returns a list with the groups that station belongs to
    """

    global gmag_dict
    group_list = []
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        if station['ccode'].lower() == station_name:
            for key, value in station.items():
                if value == 'Y':
                    if station['ccode'].lower() not in group_list:
                        group_list.append(key)

    return group_list


def gmag_list(group='all'):
    """ returns a list of stations
        prints a list of "stations: start date - end date"
    """

    global gmag_dict
    station_list = []
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        station_name = station['ccode'].lower()
        station_group = get_group(station_name)
        if group in ['all', '*', ''] or group in station_group:
            station_list.append(station_name)
            logging.info(station_name + ": from " + station['day_first'] + " to "
                  + station['day_last'])

    return station_list


def gmag_groups():
    """ returns a dictionary of station groups with a list of stations
        prints a list of "group:'stations'"
    """

    global gmag_dict
    group_dict = {}
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        for key, value in station.items():
            if value == 'Y':
                if key in group_dict:
                    if station['ccode'].lower() not in group_dict[key]:
                        group_dict[key].append(station['ccode'].lower())
                else:
                    group_dict[key] = []
                    group_dict[key].append(station['ccode'].lower())

    # print them
    for g, s in group_dict.items():
        logging.info(g + ":" + ",'".join(s) + "'")

    return group_dict


def check_gmag(station_name):
    """ returns 1 if station_name is in the gmag list, 0 otherwise"
    """

    global gmag_dict
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        if station['ccode'].lower() == station_name.lower():
            return 1

    return 0


def check_greenland(station_name):
    """ returns 1 if station_name is in the greenland gmag list, 0 otherwise"
    """

    global gmag_dict
    if gmag_dict == {}:
        gmag_dict = query_gmags()

    for station in gmag_dict:
        if station['ccode'].lower() == station_name.lower():
            if ((station['country'] is not None
                 and station['country'].lower() == 'greenland')
                or (station['greenland'] is not None
                    and station['greenland'].lower() == 'y')):
                return 1

    return 0

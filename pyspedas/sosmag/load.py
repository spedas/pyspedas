'''
Load data from SOSMAG Space Weather instrument
    flying on the Korean GEO-KOMPSAT-2A satellite.

This function downloads data directly from the ESA HAPI server.
The ESA HAPI server requires authentication.
Users have to register with the ESA server
    and replace their username and password in the code below.

Notes
-----
https://swe.ssa.esa.int/sosmag
https://swe.ssa.esa.int/hapi
Data types available:
    1. (datatype='1m', esa_gk2a_sosmag_1m)
        Near-realtime Magnetic Field Data with 1-16Hz from SOSMAG
        on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.
        'spase://SSA/NumericalData/GEO-KOMPSAT-2A/esa_gk2a_sosmag_1m'

    2. (default, datatype='', esa_gk2a_sosmag_recalib)
        Recalibrated L2 Magnetic Field Data with 1-16Hz from SOSMAG
        on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.
        'spase://SSA/NumericalData/GEO-KOMPSAT-2A/esa_gk2a_sosmag_recalib'

Example
-------
from pytplot import tplot
from pyspedas import sosmag_load
t_ok, var_names = sosmag_load(trange=['2021-01-01 02:00','2021-01-01 03:00'])
tplot(var_names)

'''
import requests
import json
import numpy as np
from pytplot import store_data, options
from pyspedas import time_double, time_string


# Global parameters for the functions in this file.
# Users must replace username and password with their ESA credentials.
sosmag_parameters = {
    'username': 'spedas',  # Users must replace with their ESA username.
    'password': 'acQ4pG6u9Bh26v2',  # User ESA password.
    'portal_url': 'https://swe.ssa.esa.int/',
    'authenticate_url': 'https://sso.ssa.esa.int/am/json/authenticate',
    'sso_cookiename': 'iPlanetDirectoryPro',
    'print_errors': True,  # If true, prints error messages.
    'print_messages': False,  # If true, prints debugging/success messages.
}


def sosmag_get_auth_cookie():
    '''
    Authenticates a user against OpenAM.

    Uses the sosmag_parameters dictionary for the parameters needed.
    Returns whether authentication was successful and the obtained cookie.
    If an error occurs, the exception is caught and the error printed.

    Parameters
    ----------
    None.

    Returns
    -------
    success: bool
        True, if authentication was successful
    auth_cookie: str
        The obtained authentication cookie
    '''
    success = False
    auth_cookie = ''
    try:
        # Send a POST request to the authentication url
        response = requests.post(
            sosmag_parameters['authenticate_url'],
            headers={
                    'Content-Type': 'application/json',
                    'X-OpenAM-Username': sosmag_parameters['username'],
                    'X-OpenAM-Password': sosmag_parameters['password'],
                },
            data='{}')
        # form the response, extract the auth cookie and return it
        token_dict = json.loads(response.content)
        auth_cookie = token_dict['tokenId']
        success = True
    except Exception as exc:
        success = False
        auth_cookie = ''
        if sosmag_parameters['print_errors']:
            print(exc)
    finally:
        return success, auth_cookie


def sosmag_get_session(auth_cookie):
    '''
    Establishes a session with the ESA HAPI server.

    Uses the authentication cookie obtained from sosmag_get_auth_cookie().
    Returns whether a session was established successfully and if so,
        the obtained session cookies.
    If an error occurs, the exception is caught and the error is printed.

    Parameters
    ----------
    auth_cookie: str
        The obtained authentication cookie from sosmag_get_auth_cookie()

    Returns
    -------
    success: bool
        True, if authentication was successful
    jsession_id: str
        The obtained session cookie
    xsrf_token: str
        The obtained xsrf token
    '''
    success = False
    jsession_id = ''
    xsrf_token = ''
    try:
        # Try to access the HAPI/capabilities using the auth_cookie
        init_response = requests.get(
            sosmag_parameters['portal_url'] + '/hapi/capabilities',
            cookies={
                sosmag_parameters['sso_cookiename']: auth_cookie,
            }
        )
        # Extract the session cookies from the very first response from HAPI
        cookie_jar = init_response.history[0].cookies
        jsession_id = cookie_jar.get('JSESSIONID')
        xsrf_token = cookie_jar.get('XSRF-TOKEN')
        # Extract the consent url we are being requested to send our consent to
        # (in case we didn't consent yet)
        consent_url = init_response.url
        content = init_response.content

        # If we consented already, we should have received HAPI/capabilities.
        if '/hapi/capabilities' not in consent_url:
            # If not, we need to give our consent in the next step.
            # Send the consent along with all cookies to the consent url.
            consent_response = requests.post(
                consent_url,
                cookies={
                    sosmag_parameters['sso_cookiename']: auth_cookie,
                    'JSESSIONID': jsession_id,
                    'XSRF_TOKEN': xsrf_token,
                },
                data={
                    'decision': 'Allow',
                    'save_consent': 'on',
                }
            )
            content = consent_response.content
        # This will result in a redirect to the initial HAPI/capabilities.
        capabilities = json.loads(content)
        # The json output is supposed to look something like this:
        #   {'version':'2.1.0','status':{'code':1200,'message':'OK'},'outputFormats':['csv','json']}
        version = capabilities['version']
        status = capabilities['status']
        # If the output is what we expect, return True and the session cookies
        if version != '' and status != {} and status['message'] == 'OK':
            success = True
        else:
            success = False
            jsession_id = ''
            xsrf_token = ''
    except Exception as exc:
        if sosmag_parameters['print_errors']:
            print(exc)
        success = False
        jsession_id = ''
        xsrf_token = ''

    return success, jsession_id, xsrf_token


def sosmag_get_capabilities(jsession_id, xsrf_token):
    '''
    Gets HAPI/capabilities from server.

    Uses the two cookies obtained using sosmag_get_session_cookies().
    If an error occurs, the exception is caught and the error printed.

    Parameters
    ----------
    jsession_id: str
        The obtained session cookie
    xsrf_token: str
        The obtained xsrf token

    Returns
    -------
    success: bool
        True, if function was successful
    capabilities: dict of str
        The obtained capabilities as a json dictionary of strings
    '''
    success = False
    capabilities = {}
    try:
        # Send a GET request to the HAPI/capabilities.
        test_response = requests.get(
            sosmag_parameters['portal_url'] + '/hapi/capabilities',
            cookies={
                'JSESSIONID': jsession_id,
                'XSRF_TOKEN': xsrf_token,
            }
        )
        # Extract the capabilities from the response.
        capabilities = json.loads(test_response.content)
        version = capabilities['version']
        status = capabilities['status']
        # If the capabilities are as expected, return True.
        if version != '' and status != {} and status['message'] == 'OK':
            success = True
        else:
            success = False
            capabilities = {}
    except Exception as exc:
        if sosmag_parameters['print_errors']:
            print(exc)
        success = False
        capabilities = {}

    return success, capabilities


def sosmag_get_data(
    jsession_id, xsrf_token,  # HAPI session cookies.
    datatype='',   # Data type, either '' (recalibrated) or '1m' (real time)
    timemin='2022-01-31T01:00:00.000Z',  # Start time
    timemax='2022-01-31T01:10:00.000Z',  # End time
):
    '''
    Gets either HAPI/data or HAPI/info from server.

    Uses the two cookies obtained from sosmag_get_session_cookies().
    If an error occurs, the exception is caught and the error printed.

    Parameters
    ----------
    jsession_id: str
        The obtained session cookie.
    xsrf_token: str
        The obtained xsrf token cookie.
    datatype: str
        Data type, either '' (recalibrated) or '1m' (1 minute, real time).
    timemin: str
        Start time, for example: '2022-01-31T01:00:00.000Z'.
    timemax: str
        End time, for example: '2022-01-31T01:10:00.000Z'.

    Returns
    -------
    success: bool
        True, if function was successful.
    data: dict of str
        The obtained data as a json dictionary of strings.
    parameters: dict of str
        The obtained parameters for the data as a json dictionary of strings.
    description: str
        The obtained description of data.
    '''
    success = False
    data = {}
    parameters = {}
    description = ''
    dataid = 'spase://SSA/NumericalData/GEO-KOMPSAT-2A/'
    if datatype == '1m':
        dataid = dataid + 'esa_gk2a_sosmag_1m'
    else:
        dataid = dataid + 'esa_gk2a_sosmag_recalib'

    # This query string can also be used in a browser.
    hquery = ('data?id=' + dataid +
              '&time.min=' + timemin +
              '&time.max=' + timemax +
              '&format=json')
    fullurl = sosmag_parameters['portal_url'] + '/hapi/' + hquery
    if sosmag_parameters['print_messages']:
        print(fullurl)

    try:
        # send a GET request to the HAPI server
        test_response = requests.get(
            fullurl,
            cookies={
                'JSESSIONID': jsession_id,
                'XSRF_TOKEN': xsrf_token,
            }
        )
        # extract the content from the response
        dat = json.loads(test_response.content)
        data = dat['data']
        parameters = dat['parameters']
        description = dat['description']
        status = dat['status']

        # if the status are as expected, return True along with the data dict
        if data != '' and status != {} and status['message'] == 'OK':
            success = True
        else:
            success = False
            data = {}
            parameters = {}
            description = ''
    except Exception as exc:
        if sosmag_parameters['print_errors']:
            print(exc)
        success = False
        data = {}
        parameters = {}
        description = ''

    return success, data, parameters, description


def sosmag_to_tplot(
    data,  # Data, array with 14 fields
    parameters,  # Description of data, array with 14 fields
    desc,   # Single string description of the data set
    datatype='',  # Either '' (recalibrated) or '1m' (real time)
    prefix='',  # To be added as prefix of tplot variable
    suffix=''  # To be added as suffix of tplot variable
):
    '''
    Saves SOSMAG data as tplot variables.

    Creates three tplot variables:
        1. Magnetic Field B in GSE coordinates, sosmag_b_gse.
        2. Magnetic Field B in HPEN coordinates, sosmag_b_hpen.
        3. Spacecraft Position in GSE, sosmag_pos.

    Parameters
    ----------
    data: dict of str
        The obtained data as a json dictionary of strings.
    parameters: dict of str
        The obtained parameters for the data as a json dictionary of strings.
    description: str
        The obtained description for this set of data.
    datatype: str
        Data type can be either '' (recalibrated) or '1m' (1 minute real time).
    prefix: str
        Prefix for tplot names. Default is ''.
    suffix: str
        Suffix for tplot names. Default is ''.

    Returns
    -------
    success: bool
        True, if function was successful.
    var_names: list of str
        Names of tplot variables created.
    '''
    success = False
    var_names = []
    try:
        # Construct tplot variable names.
        if datatype == '':
            pre = prefix + 'sosmag'
        else:
            pre = prefix + 'sosmag_' + datatype

        # Get data
        d = np.array(data)  # data
        p = np.array(parameters)  # parameters

        if len(d.shape) != 2 or len(p.shape) != 1 or d.shape[1] != 14:
            print('SOSMAG data has wrong shape. Abort.')
            return False

        # Time is the 12th field
        td = np.array(time_double(d[:, 12]))

        # Magnetic field in GSE 'b_gse_x', 'b_gse_y', 'b_gse_z'
        # Data fields: [0, 1, 2]
        yd = np.array(d[:, 0:3], dtype=float)
        var_name0 = pre + '_b_gse' + suffix
        pnames = [p[0]['name'], p[1]['name'], p[2]['name']]
        pd = 'Magnetic Field B in GSE coordinates'
        attr_dict = {'description': pd}
        store_data(var_name0, data={'x': td, 'y': yd}, attr_dict=attr_dict)
        options(var_name0, 'legend_names', pnames)
        options(var_name0, 'ysubtitle', '[nT]')
        options(var_name0, 'coord_sys', 'gse')
        options(var_name0, 'description', desc)

        # Magnetic field in HPEN 'b_hpen_x', 'b_hpen_y', 'b_hpen_z'
        # Data fields: [3, 4, 5]
        yd = np.array(d[:, 3:6], dtype=float)
        var_name1 = pre + '_b_hpen' + suffix
        pnames = [p[3]['name'], p[4]['name'], p[5]['name']]
        pd = 'Magnetic Field B in HPEN coordinates'
        attr_dict = {'description': pd}
        store_data(var_name1, data={'x': td, 'y': yd}, attr_dict=attr_dict)
        options(var_name1, 'legend_names', pnames)
        options(var_name1, 'ysubtitle', '[nT]')
        options(var_name1, 'coord_sys', 'hpen')
        options(var_name1, 'description', desc)

        # Spacecraft Position in GSE 'position_x', 'position_y', 'position_z'
        # Data fields: [9, 10, 11]
        yd = np.array(d[:, 9:12], dtype=float)
        var_name2 = pre + '_position' + suffix
        pnames = [p[9]['name'], p[10]['name'], p[11]['name']]
        pd = 'Spacecraft Position in GSE'
        attr_dict = {'description': pd}
        store_data(var_name2, data={'x': td, 'y': yd}, attr_dict=attr_dict)
        options(var_name2, 'legend_names', pnames)
        options(var_name2, 'ysubtitle', '[km]')
        options(var_name2, 'coord_sys', 'gse')
        options(var_name2, 'description', desc)

        # Print the variable names created
        var_names = [var_name0, var_name1, var_name2]
        print('Tplot variables created!')
        print(var_names)
        success = True
    except Exception as exc:
        if sosmag_parameters['print_errors']:
            print(exc)
        success = False

    return success, var_names


def sosmag_load(
    trange=['2022-01-31T01:00:00.000Z',
            '2022-01-31T01:01:00.000Z'],  # Default 10 minutes of data
    datatype='',  # Either '' (recalibrated) or '1m' (real time)
    prefix='',  # Prefix for tplot names
    suffix='',  # Suffix for tplot names
):
    '''
    This function loads data from SOSMAG.

    Gets data from the ESA web server as a json string.
    Creates three tplot variables:
        1. Magnetic Field B in GSE coordinates, sosmag_b_gse
        2. Magnetic Field B in HPEN coordinates, sosmag_b_hpen
        3. Spacecraft Position in GSE, sosmag_pos

    Parameters
    ----------
    trange: list of str
        Start and end times.
        Many time formats are supported, see function time_double().
    datatype: str
        Either '' (recalibrated) or '1m' (real time).
    prefix: str
        Prefix for tplot names. Default is ''.
    suffix: str
        Suffix for tplot names. Default is ''.

    Returns
    -------
    success: bool
        True, if function was successful.
    var_names: list of str
        Names of tplot variables created.
    '''
    success = False
    var_names = []
    # Make sure that time is in the correct format for the ESA server.
    trange = time_string(time_double(trange), fmt='%Y-%m-%dT%H:%M:%S.000Z')
    if sosmag_parameters['print_messages']:
        print('trange', trange)

    # Authenticate with the HAPI server and receive a cookie.
    authenticated, auth_cookie = sosmag_get_auth_cookie()
    if authenticated:
        if sosmag_parameters['print_messages']:
            print('SOSMAG authentication successful.')
    else:
        print('SOSMAG authentication failed. \
        Please check username and password in the file sosmag:load.py.')
        return

    # Set a session with the server.
    capok = False
    if authenticated:
        sessionοκ, jsession_id, xsrf_token = sosmag_get_session(auth_cookie)
        if sessionοκ:
            # Session successfully established. Obtained session cookies.
            # Testing session cookies on hapi/capabilities.
            if sosmag_parameters['print_messages']:
                print('SOSMAG session established successfully.')
            capok, capabilities = sosmag_get_capabilities(jsession_id,
                                                          xsrf_token)
            if capok:
                if sosmag_parameters['print_messages']:
                    print('SOSMAG HAPI server capabilities: ')
                    print(capabilities)
            else:
                print('Problem communicating with server. Aborting.')
                return
        else:
            print('SOSMAG session could not be established. Aborting.')
            return

    # Get data.
    dataok = False
    if capok:
        dataok, data, parameters, desc = sosmag_get_data(
            jsession_id, xsrf_token, datatype=datatype,
            timemin=trange[0], timemax=trange[1])
        if dataok:
            tplotok, var_names = sosmag_to_tplot(
                data, parameters, desc, datatype=datatype,
                prefix=prefix, suffix=suffix)
            if tplotok:
                if sosmag_parameters['print_messages']:
                    print('Data was loaded.')
                success = True
            else:
                print('Could load data into pytplot. Aborting.')
                return
        else:
            print('Could not get any data. Aborting.')
            return

    return success, var_names

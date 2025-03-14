"""
Load data from the Korean GEO-KOMPSAT-2A satellite.
    - Magnetometer data from SOSMAG instrument.
    - Particle data (electrons and protons) from KSEM particle instrument.

Data is downloaded from the ESA HAPI server, which requires authentication.
Users have to register with the ESA server 
    and replace their username and password in the code below.

Notes
-----
https://swe.ssa.esa.int/sosmag
https://swe.ssa.esa.int/hapi

Data types available:
    1. SOSMAG real time (datatype='1m', d3s_gk2a_sosmag_1m)
        Near-realtime Magnetic Field Data with 1-16Hz from SOSMAG
        on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.
        'spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_1m'

    2. SOSMAG calibrated (default, datatype='', d3s_gk2a_sosmag_recalib)
        Recalibrated L2 Magnetic Field Data with 1-16Hz from SOSMAG
        on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.
        'spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_recalib'

    3. Electrons real time:
        'spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_e_l1'
    4. Protons real time:
        'spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_p_l1'

"""

import logging
import requests
import json
import numpy as np
from pytplot import store_data, options
from pytplot import time_double, time_string


# Global parameters for the functions in this file.
# Users must replace username and password with their ESA credentials.
esa_hapi_parameters = {
    "username": "spedas",  # Users must replace with their ESA username.
    "password": "acQ4pG6u9Bh26v2",  # User ESA password.
    "portal_url": "https://swe.ssa.esa.int/",
    "authenticate_url": "https://sso.ssa.esa.int/am/json/authenticate",
    "sso_cookiename": "iPlanetDirectoryPro",
    "print_errors": True,  # If true, prints error messages.
    "print_messages": False,  # If true, prints debugging/success messages.
}


def esa_get_auth_cookie():
    """
    Authenticates a user against OpenAM.

    Uses the esa_hapi_parameters dictionary for the parameters needed.
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
    """
    success = False
    auth_cookie = ""
    try:
        # Send a POST request to the authentication url
        response = requests.post(
            esa_hapi_parameters["authenticate_url"],
            headers={
                "Content-Type": "application/json",
                "X-OpenAM-Username": esa_hapi_parameters["username"],
                "X-OpenAM-Password": esa_hapi_parameters["password"],
            },
            data="{}",
        )
        # form the response, extract the auth cookie and return it
        token_dict = json.loads(response.content)
        auth_cookie = token_dict["tokenId"]
        success = True
    except Exception as exc:
        success = False
        auth_cookie = ""
        if esa_hapi_parameters["print_errors"]:
            logging.info(exc)
    finally:
        return success, auth_cookie


def esa_get_session(auth_cookie):
    """
    Establishes a session with the ESA HAPI server.

    Uses the authentication cookie obtained from esa_get_auth_cookie().
    Returns whether a session was established successfully and if so,
        the obtained session cookies.
    If an error occurs, the exception is caught and the error is printed.

    Parameters
    ----------
    auth_cookie: str
        The obtained authentication cookie from esa_get_auth_cookie()

    Returns
    -------
    success: bool
        True, if authentication was successful
    jsession_id: str
        The obtained session cookie
    xsrf_token: str
        The obtained xsrf token
    """
    success = False
    jsession_id = ""
    xsrf_token = ""
    try:
        # Try to access the HAPI/capabilities using the auth_cookie
        init_response = requests.get(
            esa_hapi_parameters["portal_url"] + "/hapi/capabilities",
            cookies={
                esa_hapi_parameters["sso_cookiename"]: auth_cookie,
            },
        )
        # Extract the session cookies from the very first response from HAPI
        cookie_jar = init_response.history[0].cookies
        jsession_id = cookie_jar.get("JSESSIONID")
        xsrf_token = cookie_jar.get("XSRF-TOKEN")
        # Extract the consent url we are being requested to send our consent to
        # (in case we didn't consent yet)
        consent_url = init_response.url
        content = init_response.content

        # If we consented already, we should have received HAPI/capabilities.
        if "/hapi/capabilities" not in consent_url:
            # If not, we need to give our consent in the next step.
            # Send the consent along with all cookies to the consent url.
            consent_response = requests.post(
                consent_url,
                cookies={
                    esa_hapi_parameters["sso_cookiename"]: auth_cookie,
                    "JSESSIONID": jsession_id,
                    "XSRF_TOKEN": xsrf_token,
                },
                data={
                    "decision": "Allow",
                    "save_consent": "on",
                },
            )
            content = consent_response.content
        # This will result in a redirect to the initial HAPI/capabilities.
        capabilities = json.loads(content)
        # The json output should be:
        #  2022/10/24: {'HAPI':'2.1.0','status':{'code':1200,'message':'OK'},'outputFormats':['csv','json']}
        #  previous: {'version':'2.1.0','status':{'code':1200,'message':'OK'},'outputFormats':['csv','json']}
        version = capabilities["HAPI"]
        status = capabilities["status"]
        # If the output is what we expect, return True and the session cookies
        if version != "" and status != {} and status["message"] == "OK":
            success = True
        else:
            success = False
            jsession_id = ""
            xsrf_token = ""
    except Exception as exc:
        if esa_hapi_parameters["print_errors"]:
            logging.info(exc)
        success = False
        jsession_id = ""
        xsrf_token = ""

    return success, jsession_id, xsrf_token


def esa_get_capabilities(jsession_id, xsrf_token):
    """
    Gets HAPI/capabilities from server.

    Uses the two cookies obtained using esa_get_session_cookies().
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
    """
    success = False
    capabilities = {}
    try:
        # Send a GET request to the HAPI/capabilities.
        test_response = requests.get(
            esa_hapi_parameters["portal_url"] + "/hapi/capabilities",
            cookies={
                "JSESSIONID": jsession_id,
                "XSRF_TOKEN": xsrf_token,
            },
        )
        # Extract the capabilities from the response.
        capabilities = json.loads(test_response.content)
        version = capabilities["HAPI"]
        status = capabilities["status"]
        # If the capabilities are as expected, return True.
        if version != "" and status != {} and status["message"] == "OK":
            success = True
        else:
            success = False
            capabilities = {}
    except Exception as exc:
        if esa_hapi_parameters["print_errors"]:
            logging.info(exc)
        success = False
        capabilities = {}

    return success, capabilities


def esa_hapi_get_data(
    jsession_id,
    xsrf_token,  # HAPI session cookies.
    instrument="sosmag",  # Instrument name, either 'sosmag', 'electrons', or 'protons'
    datatype="",  # Data type for sosmag, either '' (recalibrated) or '1m' (real time)
    timemin="2022-01-31T01:00:00.000Z",  # Start time
    timemax="2022-01-31T01:10:00.000Z",  # End time
):
    """
    Gets either HAPI/data or HAPI/info from server.

    Uses the two cookies obtained from esa_get_session_cookies().
    If an error occurs, the exception is caught and the error printed.

    Parameters
    ----------
    jsession_id: str
        The obtained session cookie.
    xsrf_token: str
        The obtained xsrf token cookie.
    datatype: str
        Data type for sosmag, either '' (recalibrated) or '1m' (1 minute, real time).
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
    """
    success = False
    data = {}
    parameters = {}
    description = ""
    if instrument in ["electrons", "e"]:
        dataid = "spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_e_l1"
    elif instrument in ["protons", "p"]:
        dataid = "spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_p_l1"
    else:
        if datatype == "1m":
            dataid = "spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_1m"
        else:
            dataid = "spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_recalib"

    # This query string can also be used in a browser.
    hquery = (
        "data?id="
        + dataid
        + "&time.min="
        + timemin
        + "&time.max="
        + timemax
        + "&format=json"
    )
    fullurl = esa_hapi_parameters["portal_url"] + "/hapi/" + hquery
    if esa_hapi_parameters["print_messages"]:
        logging.info(fullurl)

    try:
        # send a GET request to the HAPI server
        test_response = requests.get(
            fullurl,
            cookies={
                "JSESSIONID": jsession_id,
                "XSRF_TOKEN": xsrf_token,
            },
        )
        # extract the content from the response
        dat = json.loads(test_response.content)
        data = dat["data"]
        parameters = dat["parameters"]
        description = dat["description"]
        status = dat["status"]

        # if the status are as expected, return True along with the data dict
        if data != "" and status != {} and status["message"] == "OK":
            success = True
        else:
            success = False
            data = {}
            parameters = {}
            description = ""
    except Exception as exc:
        if esa_hapi_parameters["print_errors"]:
            logging.info(exc)
        success = False
        data = {}
        parameters = {}
        description = ""

    return success, data, parameters, description


def sosmag_to_tplot(
    data,  # Data, array with 14 fields
    parameters,  # Description of data, array with 14 fields
    desc,  # Single string description of the data set
    datatype="",  # Either '' (recalibrated) or '1m' (real time)
    get_support_data=False,  # Download flags and other supporting data
    prefix="",  # To be added as prefix of tplot variable
    suffix="",  # To be added as suffix of tplot variable
):
    """
    Stores magnetometer data as tplot variables.

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
    get_support_data: bool
        If True, loads everything into tplot variables, including flags.
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
    """
    success = False
    var_names = []
    try:
        # Construct tplot variable names.
        if datatype == "":
            pre = prefix + "sosmag"
        else:
            pre = prefix + "sosmag_" + datatype

        # Get data
        d = np.array(data)  # data
        p = np.array(parameters)  # parameters

        if len(d.shape) != 2 or len(p.shape) != 1 or d.shape[1] != 14:
            logging.info("SOSMAG data has wrong shape. Abort.")
            return False

        # Time is the 0th field
        td = np.array(time_double(d[:, 0]))

        # Data version identifier
        # version, Data field: [1]
        if get_support_data:
            yd = np.array(d[:, 1], dtype=int)
            var_name1 = pre + "_version" + suffix
            pd = "Version"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name1, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name1, "legend_names", "version")
            options(var_name1, "ytitle", "version")
            options(var_name1, "ysubtitle", "")
            var_names.append(var_name1)

        # Magnetic field in GSE 'b_gse_x', 'b_gse_y', 'b_gse_z'
        # Data fields: [2, 3, 4]
        yd = np.array(d[:, 2:5], dtype=float)
        var_name2 = pre + "_b_gse" + suffix
        pnames = [p[2]["name"], p[3]["name"], p[4]["name"]]
        pd = "Magnetic Field B in GSE coordinates"
        attr_dict = {"description": desc, "var_desc": pd}
        store_data(var_name2, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name2, "legend_names", pnames)
        options(var_name2, "ytitle", "b_gse")
        options(var_name2, "ysubtitle", "[nT]")
        options(var_name2, "coord_sys", "gse")
        var_names.append(var_name2)

        # Magnetic field in HPEN 'b_hpen_x', 'b_hpen_y', 'b_hpen_z'
        # Data fields: [5, 6, 7]
        if get_support_data:
            yd = np.array(d[:, 5:8], dtype=float)
            var_name3 = pre + "_b_hpen" + suffix
            pnames = [p[5]["name"], p[6]["name"], p[7]["name"]]
            pd = "Magnetic Field B in HPEN coordinates"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name3, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name3, "legend_names", pnames)
            options(var_name3, "ytitle", "b_hpen")
            options(var_name3, "ysubtitle", "[nT]")
            options(var_name3, "coord_sys", "hpen")
            var_names.append(var_name3)

        # Spacecraft Position in GSE 'position_x', 'position_y', 'position_z'
        # Data fields: [8, 9, 10]
        yd = np.array(d[:, 8:11], dtype=float)
        var_name4 = pre + "_position" + suffix
        pnames = [p[8]["name"], p[9]["name"], p[10]["name"]]
        pd = "Spacecraft Position in GSE"
        attr_dict = {"description": desc, "var_desc": pd}
        store_data(var_name4, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name4, "legend_names", pnames)
        options(var_name4, "ytitle", "pos_gse")
        options(var_name4, "ysubtitle", "[km]")
        options(var_name4, "coord_sys", "gse")
        var_names.append(var_name4)

        # Data flags
        # data_flags, Data field: [11]
        if get_support_data:
            yd = np.array(d[:, 11], dtype=int)
            var_name5 = pre + "_data_flags" + suffix
            pd = "Data Flags"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name5, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name5, "legend_names", p[11]["name"])
            options(var_name5, "ytitle", "data_flag")
            options(var_name5, "ysubtitle", "")
            var_names.append(var_name5)

        # Calibration status
        # final, Data_field: [12]
        if get_support_data:
            ydb = np.array(d[:, 12])  #  string
            yd1 = [0 if x == "0" or x == "false" or x == "False" else 1 for x in ydb]
            yd = np.array(yd1, dtype=bool)
            var_name6 = pre + "_final" + suffix
            pd = "Final"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name6, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name6, "legend_names", "final_flag")
            options(var_name6, "ytitle", "calib")
            options(var_name6, "ysubtitle", "")
            var_names.append(var_name6)

        # Current sampling frequency flag
        # frequency, Data field: [13]
        if get_support_data:
            yd = np.array(d[:, 13], dtype=int)
            var_name7 = pre + "_frequency_flag" + suffix
            pd = "Frequency flag"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name7, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name7, "legend_names", "freq_flag")
            options(var_name7, "ytitle", "freq_flag")
            options(var_name7, "ysubtitle", "")
            var_names.append(var_name7)

        # Print the variable names created
        logging.info("Tplot variables created!")
        logging.info(var_names)
        success = True
    except Exception as exc:
        if esa_hapi_parameters["print_errors"]:
            logging.info(exc)
        success = False

    return success, var_names


def particle_to_tplot(
    data,  # Data, array with 34 fields
    parameters,  # Description of data, array with 34 fields
    desc,  # Single string description of the data set
    ptype="p",  # Either 'p' or 'e'
    get_support_data=False,  # Download flags and other supporting data
    prefix="",  # To be added as prefix of tplot variable
    suffix="",  # To be added as suffix of tplot variable
):
    """
    Stores proton or electron flux data as tplot variables.

    Parameters
    ----------
    data: dict of str
        The obtained data as a json dictionary of strings.
    parameters: dict of str
        The obtained parameters for the data as a json dictionary of strings.
    description: str
        The obtained description for this set of data.
    ptype: str
        Particle type can be either 'p' (protons) or 'e' (electrons).
    get_support_data: bool
        If True, loads everything into tplot variables, including flags.
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
    """
    success = False
    var_names = []
    try:
        # Construct tplot variable names.
        if len(prefix) != 0 and prefix[-1] != "_":
            prefix = prefix + "_"

        pre = prefix + "kompsat_" + ptype + "_"

        # Get data
        d = np.array(data)  # data
        p = np.array(parameters)  # parameters

        if len(d.shape) != 2 or len(p.shape) != 1 or d.shape[1] != 34:
            logging.info("Particle data has wrong shape. Abort.")
            return False

        # Time is the 0th field
        td = np.array(time_double(d[:, 0]))

        flux_bands = []
        if ptype == "e":
            # Electron flux 'e_flux'
            # Data fields: [1 - 11]
            # Ten energy bands for electrons
            flux_start = [
                "100",
                "150",
                "225",
                "325",
                "450",
                "700",
                "1350",
                "1800",
                "2600",
                "3800",
            ]
            for i in range(0, len(flux_start) - 1):
                flux_bands.append(flux_start[i] + "-" + flux_start[i + 1] + " keV")
            flux_bands.append("2000_3800 keV")  # Last band is 2000-3800 keV
        else:
            # Proton flux 'p_flux'
            # Data fields: [1 - 11]
            # Ten energy bands for protons
            flux_start = [
                "77",
                "119",
                "148",
                "229",
                "354",
                "548",
                "681",
                "1052",
                "2021",
                "3123",
                "6000",
            ]
            for i in range(0, len(flux_start) - 1):
                flux_bands.append(flux_start[i] + "-" + flux_start[i + 1] + " keV")

        for i in range(1, 11):
            yd = np.array(d[:, i], dtype=float)
            pname = p[i]["name"]  # e1, e2, ..., e10
            if ptype == "p":
                pname = pname.replace("e", "p")
            var_name0 = pre + pname + suffix
            pd = p[i]["description"]
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name0, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name0, "legend_names", pname + " (" + flux_bands[i - 1] + ")")
            options(var_name0, "ytitle", pname)
            options(var_name0, "ysubtitle", "[cm^-2 sr^-1 s^-1 keV^-1]")
            options(var_name0, "coord_sys", "gse")
            options(var_name0, "units", "cm^-2 sr^-1 s^-1 keV^-1")
            var_names.append(var_name0)

        # Attenuator is opened ('0') or closed ('1')
        # att_flag, One data field: [11]
        if get_support_data:
            ydb = np.array(d[:, 11])
            yd1 = [0 if x == "0" or x == "false" or x == "False" else 1 for x in ydb]
            yd = np.array(yd1, dtype=bool)
            pname = p[11]["name"]
            var_name1 = pre + pname + suffix
            pd = "Attenuator flag"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name1, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name1, "legend_names", pname)
            options(var_name1, "ytitle", pname)
            options(var_name1, "ysubtitle", "")
            var_names.append(var_name1)

        # Indicates if detector is in normal status ('0') or disable status ('1')
        # det_flag1-8, Eight data fields: [12 - 19]
        if get_support_data:
            for i in range(12, 20):
                ydb = np.array(d[:, i])
                yd1 = [
                    0 if x == "0" or x == "false" or x == "False" else 1 for x in ydb
                ]
                yd = np.array(yd1, dtype=bool)
                pname = p[i]["name"]  # det_flag1, det_flag2, ..., det_flag8
                var_name2 = pre + pname + suffix
                pd = "Detector flag " + pname[-1]
                attr_dict = {"description": desc, "var_desc": pd}
                store_data(var_name2, data={"x": td, "y": yd}, attr_dict=attr_dict)
                options(var_name2, "legend_names", pname)
                options(var_name2, "ytitle", pname)
                options(var_name2, "ysubtitle", "")
                var_names.append(var_name2)

        # Quality flags, '0' means that the observation value is between min-value and max-value,
        # '1' means out of max-value, and '2' means out of min-value"
        # e1_qef-e10_qef, Ten data fields: [20 - 29]
        if get_support_data:
            for i in range(20, 30):
                yd = np.array(d[:, i], dtype=int)
                pname = p[i]["name"]  # e1_qef, e2_qef, ..., e10_qef
                var_name3 = pre + pname + suffix
                pd = "Observation value quality flag " + pname[-1]
                attr_dict = {"description": desc, "var_desc": pd}
                store_data(var_name3, data={"x": td, "y": yd}, attr_dict=attr_dict)
                options(var_name3, "legend_names", pname)
                options(var_name3, "ytitle", pname)
                options(var_name3, "ysubtitle", "")
                var_names.append(var_name3)

        # Number of acquisitions for 1-minute average data
        # integ_num, One data field: [30]
        if get_support_data:
            yd = np.array(d[:, 30], dtype=int)
            pname = p[30]["name"]  # integ_num
            var_name4 = pre + pname + suffix
            pd = "Number of acquisitions for 1-minute average data"
            attr_dict = {"description": desc, "var_desc": pd}
            store_data(var_name4, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name4, "legend_names", pname)
            options(var_name4, "ytitle", pname)
            options(var_name4, "ysubtitle", "")
            var_names.append(var_name4)

        # Spacecraft Position in GSE 'position_x', 'position_y', 'position_z'
        # position_x, z, y, Three data fields: [31, 32, 33]
        yd = np.array(d[:, 31:34], dtype=float)
        var_name2 = pre + "pos_gse" + suffix
        pnames = [p[31]["name"], p[32]["name"], p[33]["name"]]
        pd = "Spacecraft Position in GSE"
        attr_dict = {"description": desc, "var_desc": pd}
        store_data(var_name2, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name2, "legend_names", pnames)
        options(var_name2, "ytitle", "pos_gse")
        options(var_name2, "ysubtitle", "[km]")
        options(var_name2, "coord_sys", "gse")
        var_names.append(var_name2)

        # Print the variable names created
        logging.info("Variables created!")
        logging.info(var_names)
        success = True
    except Exception as exc:
        if esa_hapi_parameters["print_errors"]:
            logging.info(exc)
        success = False

    return success, var_names


def load(
    trange=[
        "2024-03-31T01:00:00.000Z",
        "2024-03-31T01:30:00.000Z",
    ],  # Default 30 minutes of data
    instrument="sosmag",  # Instrument name
    datatype="",  # Either '' (recalibrated) or '1m' (real time)
    get_support_data=False,  # Download flags and other supporting data
    prefix="",  # Prefix for tplot names
    suffix="",  # Suffix for tplot names
):
    """
    This function loads data from the ESA HAPI server.

    Parameters
    ----------
    trange: list of str
        Start and end times.
        Many time formats are supported, see function time_double().
    instrument: str
        Instrument name. Default is 'sosmag'.
        Valid values are: 'sosmag' or 'mag', 'electrons' or 'e', 'protons' or 'p'.
    datatype: str
        Either '' (recalibrated) or '1m' (real time).
        Valid only for sosmag data. Ignored for particle data.
    get_support_data: bool
        If True, loads everything into tplot variables, including flags.
    prefix: str
        Prefix for tplot names. Default is ''.
    suffix: str
        Suffix for tplot names. Default is ''.

    Returns
    -------
    var_names: list of str
        Names of tplot variables created.

    Examples
    --------
    >>> from pyspedas import tplot
    >>> from pyspedas import kompsat_load

    >>> # Plot L2 magnetometer data
    >>> var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], datatype="1m")
    >>> tplot(var_names)

    >>> # Plot electron data
    >>> var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], instrument="e")
    >>> tplot(var_names)

    >>> # Plot proton data
    >>> var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], instrument="p")
    >>> tplot(var_names)

    Notes
    -----
    Data links that can be tested on a browser:

    SOSMAG data:

    https://swe.ssa.esa.int/hapi/data?id=spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_recalib&time.min=2021-01-31T01:00:00.000Z&time.max=2021-01-31T01:01:00.000Z&format=json

    https://swe.ssa.esa.int/hapi/data?id=spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_1m&time.min=2021-01-31T01:00:00.000Z&time.max=2021-01-31T01:01:00.000Z&format=json

    Particle data:

    https://swe.ssa.esa.int/hapi/data?id=spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_p_l1&time.min=2024-03-31T01:00:00.000Z&time.max=2024-03-31T02:00:00.000Z&format=json

    https://swe.ssa.esa.int/hapi/data?id=spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_e_l1&time.min=2024-03-31T01:00:00.000Z&time.max=2024-03-31T02:00:00.000Z&format=json
    """
    var_names = []
    # Make sure that time is in the correct format for the ESA server.
    trange = time_string(time_double(trange), fmt="%Y-%m-%dT%H:%M:%S.000Z")
    if esa_hapi_parameters["print_messages"]:
        logging.info("trange", trange)

    # Authenticate with the HAPI server and receive a cookie.
    authenticated, auth_cookie = esa_get_auth_cookie()
    if authenticated:
        if esa_hapi_parameters["print_messages"]:
            logging.info("SOSMAG authentication successful.")
    else:
        logging.info(
            "SOSMAG authentication failed. \
        Please check username and password in the file sosmag:load.py."
        )
        return

    # Set a session with the server.
    capok = False
    if authenticated:
        sessionοκ, jsession_id, xsrf_token = esa_get_session(auth_cookie)
        if sessionοκ:
            # Session successfully established. Obtained session cookies.
            # Testing session cookies on hapi/capabilities.
            if esa_hapi_parameters["print_messages"]:
                logging.info("SOSMAG session established successfully.")
            capok, capabilities = esa_get_capabilities(jsession_id, xsrf_token)
            if capok:
                if esa_hapi_parameters["print_messages"]:
                    logging.info("SOSMAG HAPI server capabilities: ")
                    logging.info(capabilities)
            else:
                logging.info("Problem communicating with server. Aborting.")
                return
        else:
            logging.info("SOSMAG session could not be established. Aborting.")
            return

    # Get data.
    dataok = False
    if capok:
        dataok, data, parameters, desc = esa_hapi_get_data(
            jsession_id,
            xsrf_token,
            instrument=instrument,
            datatype=datatype,
            timemin=trange[0],
            timemax=trange[1],
        )
        if dataok:
            if instrument in ["electrons", "electron", "e", "protons", "proton", "p"]:
                ptype = instrument[0]  #'e' or 'p'
                tplotok, var_names = particle_to_tplot(
                    data,
                    parameters,
                    desc,
                    ptype=ptype,
                    get_support_data=get_support_data,
                    prefix=prefix,
                    suffix=suffix,
                )
            else:
                tplotok, var_names = sosmag_to_tplot(
                    data,
                    parameters,
                    desc,
                    datatype=datatype,
                    get_support_data=get_support_data,
                    prefix=prefix,
                    suffix=suffix,
                )
            if tplotok:
                if esa_hapi_parameters["print_messages"]:
                    logging.info("Data was loaded.")
                success = True
            else:
                logging.info("Could load data into pytplot. Aborting.")
                return
        else:
            logging.info("Could not get any data. Aborting.")
            return

    return var_names

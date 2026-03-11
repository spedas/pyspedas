"""
Load data from the Korean GEO-KOMPSAT-2A satellite.
    - Magnetometer data from SOSMAG instrument.
    - Particle data (electrons and protons) from KSEM particle instrument.

Data is downloaded from the ESA HAPI server, which requires authentication.

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
import json
import numpy as np
from pyspedas.tplot_tools import store_data, options, time_double, time_string, set_units, set_coords
from pyspedas.projects.kompsat.esa_hapi_data import get_esa_hapi_data, check_esa_hapi_connection


def kompsat_to_tplot(ktype, data):
    """
    Convert a KOMPSAT ESA-HAPI JSON data to pytplot variables.

    Parameters
    ----------
    ktype : {'e', 'p', '1m', 'recalib'}
        Data type selector.
    data : str or dict
        ESA HAPI JSON string response.

    Returns
    -------
    list of str
        Names of created tplot variables. Returns an empty list if parsing or
        variable creation fails.
    """
    var_names = []
    try:
        payload = json.loads(data) if isinstance(data, str) else data
        d = np.array(payload["data"], dtype=object)
        p = np.array(payload["parameters"], dtype=object)
        desc = payload.get("description", "")

        if len(d.shape) != 2 or len(p.shape) != 1:
            return []

        td = np.array(time_double(d[:, 0]))

        if ktype in ["e", "p"]:
            pre = "kompsat_" + ktype + "_"

            flux_bands = []
            if ktype == "e":
                flux_start = [
                    "100",
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
                flux_bands.append("2000_3800 keV")
            else:
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
                pname = p[i]["name"]
                if ktype == "p":
                    pname = pname.replace("e", "p")
                var_name0 = pre + pname
                attr_dict = {"description": desc, "var_desc": p[i]["description"]}
                store_data(var_name0, data={"x": td, "y": yd}, attr_dict=attr_dict)
                options(var_name0, "legend_names", pname + " (" + flux_bands[i - 1] + ")")
                options(var_name0, "ytitle", pname)
                options(var_name0, "ysubtitle", "[cm^-2 sr^-1 s^-1 keV^-1]")
                set_coords(var_name0, "gse")
                set_units(var_name0, "cm^-2 sr^-1 s^-1 keV^-1")
                var_names.append(var_name0)

            ydb = np.array(d[:, 11])
            yd1 = [0 if x == "0" or x == "false" or x == "False" else 1 for x in ydb]
            yd = np.array(yd1, dtype=bool)
            pname = p[11]["name"]
            var_name1 = pre + pname
            attr_dict = {"description": desc, "var_desc": "Attenuator flag"}
            store_data(var_name1, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name1, "legend_names", pname)
            options(var_name1, "ytitle", pname)
            options(var_name1, "ysubtitle", "")
            var_names.append(var_name1)

            for i in range(12, 20):
                ydb = np.array(d[:, i])
                yd1 = [0 if x == "0" or x == "false" or x == "False" else 1 for x in ydb]
                yd = np.array(yd1, dtype=bool)
                pname = p[i]["name"]
                var_name2 = pre + pname
                attr_dict = {"description": desc, "var_desc": "Detector flag " + pname[-1]}
                store_data(var_name2, data={"x": td, "y": yd}, attr_dict=attr_dict)
                options(var_name2, "legend_names", pname)
                options(var_name2, "ytitle", pname)
                options(var_name2, "ysubtitle", "")
                var_names.append(var_name2)

            for i in range(20, 30):
                yd = np.array(d[:, i], dtype=int)
                pname = p[i]["name"]
                var_name3 = pre + pname
                attr_dict = {"description": desc, "var_desc": "Observation value quality flag " + pname[-1]}
                store_data(var_name3, data={"x": td, "y": yd}, attr_dict=attr_dict)
                options(var_name3, "legend_names", pname)
                options(var_name3, "ytitle", pname)
                options(var_name3, "ysubtitle", "")
                var_names.append(var_name3)

            yd = np.array(d[:, 30], dtype=int)
            pname = p[30]["name"]
            var_name4 = pre + pname
            attr_dict = {"description": desc, "var_desc": "Number of acquisitions for 1-minute average data"}
            store_data(var_name4, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name4, "legend_names", pname)
            options(var_name4, "ytitle", pname)
            options(var_name4, "ysubtitle", "")
            var_names.append(var_name4)

            yd = np.array(d[:, 31:34], dtype=float)
            var_name2 = pre + "pos_gse"
            pnames = [p[31]["name"], p[32]["name"], p[33]["name"]]
            attr_dict = {"description": desc, "var_desc": "Spacecraft Position in GSE"}
            store_data(var_name2, data={"x": td, "y": yd}, attr_dict=attr_dict)
            options(var_name2, "legend_names", pnames)
            options(var_name2, "ytitle", "pos_gse")
            options(var_name2, "ysubtitle", "[km]")
            set_coords(var_name2, "gse")
            set_units(var_name2, "km")
            var_names.append(var_name2)

            return var_names

        pre = "sosmag_1m" if ktype == "1m" else "sosmag"

        yd = np.array(d[:, 1], dtype=int)
        var_name1 = pre + "_version"
        attr_dict = {"description": desc, "var_desc": "Version"}
        store_data(var_name1, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name1, "legend_names", "version")
        options(var_name1, "ytitle", "version")
        options(var_name1, "ysubtitle", "")
        var_names.append(var_name1)

        yd = np.array(d[:, 2:5], dtype=float)
        var_name2 = pre + "_b_gse"
        pnames = [p[2]["name"], p[3]["name"], p[4]["name"]]
        attr_dict = {"description": desc, "var_desc": "Magnetic Field B in GSE coordinates"}
        store_data(var_name2, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name2, "legend_names", pnames)
        options(var_name2, "ytitle", "b_gse")
        options(var_name2, "ysubtitle", "[nT]")
        set_coords(var_name2, "gse")
        set_units(var_name2, "nT")
        var_names.append(var_name2)

        yd = np.array(d[:, 5:8], dtype=float)
        var_name3 = pre + "_b_hpen"
        pnames = [p[5]["name"], p[6]["name"], p[7]["name"]]
        attr_dict = {"description": desc, "var_desc": "Magnetic Field B in HPEN coordinates"}
        store_data(var_name3, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name3, "legend_names", pnames)
        options(var_name3, "ytitle", "b_hpen")
        options(var_name3, "ysubtitle", "[nT]")
        set_coords(var_name3, "hpen")
        set_units(var_name3, "nT")
        var_names.append(var_name3)

        yd = np.array(d[:, 8:11], dtype=float)
        var_name4 = pre + "_position"
        pnames = [p[8]["name"], p[9]["name"], p[10]["name"]]
        attr_dict = {"description": desc, "var_desc": "Spacecraft Position in GSE"}
        store_data(var_name4, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name4, "legend_names", pnames)
        options(var_name4, "ytitle", "pos_gse")
        options(var_name4, "ysubtitle", "[km]")
        set_coords(var_name4, "gse")
        set_units(var_name4, "km")
        var_names.append(var_name4)

        yd = np.array(d[:, 11], dtype=int)
        var_name5 = pre + "_data_flags"
        attr_dict = {"description": desc, "var_desc": "Data Flags"}
        store_data(var_name5, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name5, "legend_names", p[11]["name"])
        options(var_name5, "ytitle", "data_flag")
        options(var_name5, "ysubtitle", "")
        var_names.append(var_name5)

        ydb = np.array(d[:, 12])
        yd1 = [0 if x == "0" or x == "false" or x == "False" else 1 for x in ydb]
        yd = np.array(yd1, dtype=bool)
        var_name6 = pre + "_final"
        attr_dict = {"description": desc, "var_desc": "Final"}
        store_data(var_name6, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name6, "legend_names", "final_flag")
        options(var_name6, "ytitle", "calib")
        options(var_name6, "ysubtitle", "")
        var_names.append(var_name6)

        yd = np.array(d[:, 13], dtype=int)
        var_name7 = pre + "_frequency_flag"
        attr_dict = {"description": desc, "var_desc": "Frequency flag"}
        store_data(var_name7, data={"x": td, "y": yd}, attr_dict=attr_dict)
        options(var_name7, "legend_names", "freq_flag")
        options(var_name7, "ytitle", "freq_flag")
        options(var_name7, "ysubtitle", "")
        var_names.append(var_name7)

        return var_names
    except Exception as exc:
        logging.info(exc)
        return []


def load(
    trange=[
        "2024-03-31T01:00:00.000Z",
        "2024-03-31T01:30:00.000Z",
    ],  # Default 30 minutes of data
    datatype="recalib",  # "recalib" or "1m" for SOSMAG, 'p' or 'e' for KSEM particle data
):
    """
    This function loads data from the ESA HAPI server.

    Parameters
    ----------
    trange: list of str
        Start and end times.
        Many time formats are supported, see function time_double().
    datatype: str
        Data type selector. For SOSMAG data, use "recalib" (default) for
        recalibrated L2 data or "1m" for near-realtime 1-minute data. For KSEM
        particle data, use "p" for protons or "e" for electrons.
        Any value except "p" ("protons", "proton", "p"), "e" ("electrons", "electron", "e"),
        and "1m" ("1m", "1min", "realtime"]) will be treated as "recalib".

    Returns
    -------
    var_names: list of str
        Names of tplot variables created.

    Examples
    --------
    >>> from pyspedas import tplot
    >>> from pyspedas import kompsat_load

    >>> # Plot L2 magnetometer data
    >>> var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"])
    >>> tplot(var_names)

    >>> # Plot electron data
    >>> var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], datatype="e")
    >>> tplot(var_names)

    >>> # Plot proton data
    >>> var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], datatype="p")
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

    var_names = []  # Return variable names
    server_url = "https://swe.ssa.esa.int/hapi/data?"

    # Check connection to ESA HAPI server before doing anything.
    if not check_esa_hapi_connection():
        logging.info("No connection to ESA HAPI server. Aborting.")
        return var_names

    # Make sure that time is in the correct format for the ESA server.
    trange = time_string(time_double(trange), fmt="%Y-%m-%dT%H:%M:%S.000Z")
    if trange is None or len(trange) != 2:
        logging.info("Invalid time range. Aborting.")
        return var_names

    # Find type of data based on the datatype parameter.
    ktype = "recalib"  # Default
    dataid = "spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_recalib"  # Default
    if datatype in ["electrons", "electron", "e"] or "ksem_pd_e" in datatype:
        ktype = "e"
        dataid = "spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_e_l1"
    elif datatype in ["protons", "proton", "p"] or "ksem_pd_p" in datatype:
        ktype = "p"
        dataid = "spase://SSA/NumericalData/GEO-KOMPSAT-2A/kma_gk2a_ksem_pd_p_l1"
    elif datatype in ["1m", "1min", "realtime"] or "sosmag_1m" in datatype:
        ktype = "1m"
        dataid = "spase://SSA/NumericalData/D3S/d3s_gk2a_sosmag_1m"

    # Construct the query URL for the ESA HAPI server.
    url = server_url + "id=" + dataid + "&time.min=" + trange[0] + "&time.max=" + trange[1] + "&format=json"

    # Get data from the ESA HAPI server.
    res = get_esa_hapi_data(url)

    # If data retrieval was successful, load data into tplot variables.
    if res:
        var_names = kompsat_to_tplot(ktype, res)

    return var_names


if __name__ == "__main__":
    # Print variable names created by load() for all possible datatypes.
    v = load(trange=["2026-01-31 02:00:00", "2026-01-31 03:00:00"])
    print("recalib", v)
    v = load(trange=["2026-01-31 02:00:00", "2026-01-31 03:00:00"], datatype="1m")
    print("1m", v)
    v = load(trange=["2026-01-31 02:00:00", "2026-01-31 03:00:00"], datatype="p")
    print("p", v)
    v = load(trange=["2026-01-31 02:00:00", "2026-01-31 03:00:00"], datatype="e")
    print("e", v)

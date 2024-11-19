import cdflib
import numpy as np

from pytplot import tnames
from pytplot import get_data, store_data, options, clip, ylim, zlim

from ...satellite.erg.load import load
from ...satellite.erg.get_gatt_ror import get_gatt_ror


from typing import List, Optional, Union


def isee_vlf(
    trange: List[str] = ["2017-03-30/12:00:00", "2017-03-30/15:00:00"],
    suffix: str = "",
    site: Union[str, List[str]] = "all",
    get_support_data: bool = False,
    varformat: Optional[str] = None,
    varnames: List[str] = [],
    downloadonly: bool = False,
    notplot: bool = False,
    no_update: bool = False,
    uname: Optional[str] = None,
    passwd: Optional[str] = None,
    time_clip: bool = False,
    ror: bool = True,
    cal_gain: bool = False,
    force_download: bool = False,
):
    """
    Load ISEE VLF data from ERG Science Center

    Parameters
    ----------
    trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-03-30/12:00:00', '2017-03-30/15:00:00']

    suffix: str
            The tplot variable names will be given this suffix.  Default: ''

    site: str or list of str
            The site or list of sites to load. Valid values: 'ath', 'gak', 'hus', 'ist', 'kap', 'mam', 'nai', 'all'
            Default: ['all']

    get_support_data: bool
            If true, data with an attribute "VAR_TYPE" with a value of "support_data"
            or 'data' will be loaded into tplot. Default: False

    varformat: str
            The CDF file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables will be loaded).

    varnames: list of str
            List of variable names to load. Default: [] (all variables will be loaded)

    downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables. Default: False

    notplot: bool
            Return the data in hash tables instead of creating tplot variables. Default: False

    no_update: bool
            If set, only load data from your local cache. Default: False

    uname: str
            User name.  Default: None

    passwd: str
            Password. Default: None

    time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword. Default: False

    ror: bool
            If set, print PI info and rules of the road. Default: True

    cal_gain: bool
        If True, use calibration parameters in the CDF file to apply a gain calibration.
        Default: False

    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------

    Examples
    ________
    >>> import pyspedas
    >>> vlf_vars=pyspedas.projects.erg.isee_vlf(trange=['2017-03-30/12:00:00', '2017-03-30/15:00:00'],site='ath')
    >>> print(vlf_vars)

    """

    site_code_all = ["ath", "gak", "hus", "ist", "kap", "mam", "nai"]

    if isinstance(site, str):
        site_code = site.lower()
        site_code = site_code.split(" ")
    elif isinstance(site, list):
        site_code = []
        for i in range(len(site)):
            site_code.append(site[i].lower())
    if "all" in site_code:
        site_code = site_code_all

    site_code = list(set(site_code).intersection(site_code_all))

    if notplot:
        loaded_data = {}
    else:
        loaded_data = []
    for site_input in site_code:
        prefix = "isee_vlf_" + site_input + "_"
        file_res = 3600.0
        pathformat = (
            "ground/vlf/"
            + site_input
            + "/%Y/%m/isee_vlf_"
            + site_input
            + "_%Y%m%d%H_v??.cdf"
        )

        loaded_data_temp = load(
            pathformat=pathformat,
            file_res=file_res,
            trange=trange,
            prefix=prefix,
            suffix=suffix,
            get_support_data=get_support_data,
            varformat=varformat,
            downloadonly=downloadonly,
            notplot=notplot,
            time_clip=time_clip,
            no_update=no_update,
            uname=uname,
            passwd=passwd,
            force_download=force_download,
        )

        if notplot:
            loaded_data.update(loaded_data_temp)
        else:
            loaded_data += loaded_data_temp
        if (len(loaded_data_temp) > 0) and ror:
            try:
                # Most of the load routines use the last variable loaded to get the ROR metadata, but in this
                # case, it seems to want the first variable instead.  So we'll only pass that one.

                gatt = get_gatt_ror(downloadonly, [loaded_data[0]])
                print(
                    "**************************************************************************"
                )
                print(gatt["Logical_source_description"])
                print("")
                print(f'Information about {gatt["Station_code"]}')
                print(f'PI {gatt["PI_name"]}')
                print("")
                print(f'Affiliations: {gatt["PI_affiliation"]}')
                print("")
                print("Rules of the Road for ISEE VLF Data Use:")
                print("")
                for gatt_text in gatt["TEXT"]:
                    print(gatt_text)
                print(gatt["LINK_TEXT"])
                print(
                    "**************************************************************************"
                )
            except:
                print("printing PI info and rules of the road was failed")

        if (not downloadonly) and (not notplot):
            t_plot_name_list = list(
                set(
                    tnames([prefix + "ch1" + suffix, prefix + "ch2" + suffix])
                ).intersection(loaded_data)
            )
            options(t_plot_name_list, "zlog", 1)
            options(t_plot_name_list, "ytitle", "Frequency [Hz]")
            options(t_plot_name_list, "ysubtitle", "")
            if not cal_gain:
                options(t_plot_name_list, "ztitle", "V^2/Hz")
            else:
                print("Calibrating the gain of VLF antenna system...")
                file_name = get_data(t_plot_name_list[0], metadata=True)["CDF"][
                    "FILENAME"
                ]
                if isinstance(file_name, list):
                    file_name = file_name[0]
                cdf_file = cdflib.CDF(file_name)

                ffreq = cdf_file.varget("freq_vlf")
                gain_ch1 = cdf_file.varget("amplitude_cal_vlf_ch1")
                gain_ch2 = cdf_file.varget("amplitude_cal_vlf_ch2")

                gain_ch1_mod = np.interp(ffreq, gain_ch1[0], gain_ch1[1]) * 1.0e-9
                gain_ch2_mod = np.interp(ffreq, gain_ch2[0], gain_ch2[1]) * 1.0e-9

                t_plot_name = prefix + "ch1" + suffix
                tmp1 = get_data(t_plot_name)
                if tmp1 is not None:
                    tmp1_metadata = get_data(t_plot_name, metadata=True)
                    tmp1_y = tmp1[1] / gain_ch1_mod / gain_ch1_mod
                    store_data(
                        t_plot_name,
                        data={"x": tmp1[0], "y": tmp1_y, "v": tmp1[2]},
                        attr_dict=tmp1_metadata,
                    )

                t_plot_name = prefix + "ch2" + suffix
                tmp2 = get_data(t_plot_name)
                if tmp2 is not None:
                    tmp2_metadata = get_data(t_plot_name, metadata=True)
                    tmp2_y = tmp1[1] / gain_ch2_mod / gain_ch2_mod
                    store_data(
                        t_plot_name,
                        data={"x": tmp2[0], "y": tmp2_y, "v": tmp2[2]},
                        attr_dict=tmp2_metadata,
                    )

                options(t_plot_name_list, "ztitle", "nT^2/Hz")

    return loaded_data

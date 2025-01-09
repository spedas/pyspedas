import logging
import calendar
import numpy as np
from .utilities import maven_kp_l2_regex
from .utilities import maven_param_list
from .utilities import remove_inst_tag
from .utilities import (
    get_latest_files_from_date_range,
    get_latest_iuvs_files_from_date_range,
)
from .utilities import get_header_info
from .orbit_time import orbit_time
from .read_iuvs_file import read_iuvs_file
import pytplot
from collections import OrderedDict
import builtins
import os

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def maven_kp_to_tplot(
    filename=None,
    input_time=None,
    instruments=None,
    insitu_only=False,
    specified_files_only=False,
    ancillary_only=False,
    notplot=False
):
    """
    Convert MAVEN insitu (KP) data files to tplot variables.

    Parameters
    ----------
    filename : str or list, optional
        Name of the file(s) to read in. Defaults to None.
    input_time : str or list or int, optional
        Time frame in which to search for downloaded files.
        Can be a single date string, a list of two date strings representing a time range, or an orbit number.
        Defaults to None.
    instruments : str or list, optional
        List of instruments to include. Defaults to None.
    insitu_only : bool, optional
        Flag to include only insitu data files. Defaults to False.
    specified_files_only : bool, optional
        If True, specifies that only filenames given in 'filename' should be read in. Defaults to False.
    ancillary_only : bool, optional
        If True, only the spacecraft and APP info will be loaded. Defaults to False.
    notplot: bool, optional
        If true, return the kp_insitu data as a dict rather than tplot variables. Defaults to False.

    Returns
    -------
    dict
        A dictionary containing up to all of the columns included in a MAVEN in-situ Key parameter data file.
    """

    import pandas as pd
    import re
    from datetime import datetime, timedelta
    from dateutil.parser import parse

    filenames = []
    iuvs_filenames = []
    param_dict = maven_param_list()

    if instruments is not None:
        if not isinstance(instruments, builtins.list):
            instruments = [instruments]

    if filename is None and input_time is None:
        logging.warning(
            "You must specify either a set of filenames to read in, or a time frame in which "
            "you want to search for downloaded files."
        )

    if ancillary_only:
        instruments = ["SPACECRAFT"]

    if filename is not None:
        if not isinstance(filename, builtins.list):
            filename = [filename]

        dates = []
        for file in filename:
            date = re.findall(r"_(\d{8})", file)[0]
            dates.append(date)
            if "iuvs" in file:
                iuvs_filenames.append(file)
            else:
                filenames.append(file)
        dates.sort()

        # To keep the rest of the code consistent, if someone gave a files, or files, to load, but no input_time,
        # go ahead and create an 'input_time'
        if input_time is None:
            if len(dates) == 1:
                input_time = (
                    str(dates[0][:4])
                    + "-"
                    + str(dates[0][4:6])
                    + "-"
                    + str(dates[0][6:])
                )

            else:
                beg_date = min(dates)
                end_date = max(dates)
                input_time = [
                    str(beg_date[:4])
                    + "-"
                    + str(beg_date[4:6])
                    + "-"
                    + str(beg_date[6:]),
                    str(end_date[:4])
                    + "-"
                    + str(end_date[4:6])
                    + "-"
                    + str(end_date[6:]),
                ]

    # Check for orbit num rather than time string
    if isinstance(input_time, builtins.list):
        if isinstance(input_time[0], int):
            input_time = orbit_time(input_time[0], input_time[1])
    elif isinstance(input_time, int):
        input_time = orbit_time(input_time)

    # Turn string input into datetime objects
    if isinstance(input_time, list):
        if len(input_time[0]) <= 10:
            input_time[0] = input_time[0] + " 00:00:00"
        if len(input_time[1]) <= 10:
            input_time[1] = input_time[1] + " 23:59:59"
        date1 = parse(input_time[0])
        date2 = parse(input_time[1])
    else:
        if len(input_time) <= 10:
            input_time += " 00:00:00"
        date1 = parse(input_time)
        date2 = date1 + timedelta(days=1)

    date1_unix = calendar.timegm(date1.timetuple())
    date2_unix = calendar.timegm(date2.timetuple())

    # Grab insitu and iuvs files for the specified/created date ranges
    date_range_filenames = get_latest_files_from_date_range(date1, date2)
    date_range_iuvs_filenames = get_latest_iuvs_files_from_date_range(date1, date2)

    # Add date range files to respective file lists if desired
    if not specified_files_only:
        filenames.extend(date_range_filenames)
        iuvs_filenames.extend(date_range_iuvs_filenames)

    if not date_range_filenames and not date_range_iuvs_filenames:
        if not filenames and not iuvs_filenames:
            logging.warning(
                "No files found for the input date range, and no specific filenames were given. Exiting."
            )
            return

    # Going to look for files between time frames, but as we might have already specified
    # certain files to load in, we don't want to load them in 2x... so doing a check for that here
    filenames = list(set(filenames))
    iuvs_filenames = list(set(iuvs_filenames))

    kp_regex, l2_regex = maven_kp_l2_regex()
    kp_insitu = []
    if filenames:
        # Get column names
        names, inst = [], []
        crus_name, crus_inst = [], []
        c_found = False
        r_found = False
        for f in filenames:
            if is_fsspec_uri(f):
                protocol, path = f.split("://")
                fs = fsspec.filesystem(protocol)

                basename = f.rstrip("/").split("/")[-1]
            else:
                basename = os.path.basename(f)
            if (
                kp_regex.match(basename).group("description") == "_crustal"
                and not c_found
            ):
                name, inss = get_header_info(f)
                # Strip off the first name for now (Time), and use that as the dataframe index.
                # Seems to make sense for now, but will it always?
                crus_name.extend(name[1:])
                crus_inst.extend(inss[1:])
                c_found = True
            elif (
                kp_regex.match(basename).group("description") == ""
                and not r_found
            ):
                name, ins = get_header_info(f)
                # Strip off the first name for now (Time), and use that as the dataframe index.
                # Seems to make sense for now, but will it always?
                names.extend(name[1:])
                inst.extend(ins[1:])
                r_found = True
        all_names = names + crus_name
        all_inst = inst + crus_inst

        # Break up dictionary into instrument groups
        (
            lpw_group,
            euv_group,
            swe_group,
            swi_group,
            sta_group,
            sep_group,
            mag_group,
            ngi_group,
            app_group,
            sc_group,
            crus_group,
        ) = ([], [], [], [], [], [], [], [], [], [], [])

        for i, j in zip(all_inst, all_names):
            if re.match("^LPW$", i.strip()):
                lpw_group.append(j)
            elif re.match("^LPW-EUV$", i.strip()):
                euv_group.append(j)
            elif re.match("^SWEA$", i.strip()):
                swe_group.append(j)
            elif re.match("^SWIA$", i.strip()):
                swi_group.append(j)
            elif re.match("^STATIC$", i.strip()):
                sta_group.append(j)
            elif re.match("^SEP$", i.strip()):
                sep_group.append(j)
            elif re.match("^MAG$", i.strip()):
                mag_group.append(j)
            elif re.match("^NGIMS$", i.strip()):
                ngi_group.append(j)
            elif re.match("^MODELED_MAG$", i.strip()):
                crus_group.append(j)
            elif re.match("^SPICE$", i.strip()):
                # NB Need to split into APP and SPACECRAFT
                if re.match("(.+)APP(.+)", j):
                    app_group.append(j)
                else:  # Everything not APP is SC in SPICE
                    # But do not include Orbit Num, or IO Flag
                    # Could probably stand to clean this line up a bit
                    if not re.match("(.+)(Orbit Number|Inbound Outbound Flag)", j):
                        sc_group.append(j)
            else:
                pass

        delete_groups = []
        if instruments is not None:
            if "LPW" not in instruments and "lpw" not in instruments:
                delete_groups += lpw_group
            if "MAG" not in instruments and "mag" not in instruments:
                delete_groups += mag_group
            if "EUV" not in instruments and "euv" not in instruments:
                delete_groups += euv_group
            if "SWI" not in instruments and "swi" not in instruments:
                delete_groups += swi_group
            if "SWE" not in instruments and "swe" not in instruments:
                delete_groups += swe_group
            if "NGI" not in instruments and "ngi" not in instruments:
                delete_groups += ngi_group
            if "SEP" not in instruments and "sep" not in instruments:
                delete_groups += sep_group
            if "STA" not in instruments and "sta" not in instruments:
                delete_groups += sta_group
            if "MODELED_MAG" not in instruments and "modeled_mag" not in instruments:
                delete_groups += crus_group

        # Read in all relavent data into a pandas dataframe called "temp"
        temp_data = []
        filenames.sort()
        for filename in filenames:
            # Determine number of header lines
            nheader = 0
            if is_fsspec_uri(filename):
                protocol, path = filename.split("://")
                fs = fsspec.filesystem(protocol)
                fo = fs.open(filename, "rt")
            else:
                fo = open(filename)
            with fo as f:
                for line in f:
                    if line.startswith("#"):
                        nheader += 1
                if is_fsspec_uri(filename):
                    protocol, path = filename.split("://")
                    fs = fsspec.filesystem(protocol)

                    basename = filename.rstrip("/").split("/")[-1]
                else:
                    basename = os.path.basename(filename)
                if (
                    kp_regex.match(basename).group("description")
                    == "_crustal"
                ):
                    temp_data.append(
                        pd.read_fwf(
                            filename,
                            skiprows=nheader,
                            index_col=0,
                            widths=[19] + len(crus_name) * [16],
                            names=crus_name,
                        )
                    )
                else:
                    temp_data.append(
                        pd.read_fwf(
                            filename,
                            skiprows=nheader,
                            index_col=0,
                            widths=[19] + len(names) * [16],
                            names=names,
                        )
                    )
                for i in delete_groups:
                    del temp_data[-1][i]

        temp_unconverted = pd.concat(temp_data, axis=0, sort=True)

        # Need to convert columns
        # This is kind of a hack, but I can't figure out a better way for now

        if (
            "SWEA.Electron Spectrum Shape" in temp_unconverted
            and "NGIMS.Density NO" in temp_unconverted
        ):
            temp = temp_unconverted.astype(
                dtype={
                    "SWEA.Electron Spectrum Shape": np.float64,
                    "NGIMS.Density NO": np.float64,
                }
            )
        elif (
            "SWEA.Electron Spectrum Shape" in temp_unconverted
            and "NGIMS.Density NO" not in temp_unconverted
        ):
            temp = temp_unconverted.astype(
                dtype={"SWEA.Electron Spectrum Shape": np.float64}
            )
        elif (
            "SWEA.Electron Spectrum Shape" not in temp_unconverted
            and "NGIMS.Density NO" in temp_unconverted
        ):
            temp = temp_unconverted.astype(dtype={"NGIMS.Density NO": np.float64})
        else:
            temp = temp_unconverted

        # Cut out the times not included in the date range
        time_unix = [
            calendar.timegm(datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").timetuple())
            for i in temp.index
        ]
        start_index = 0
        for t in time_unix:
            if t >= date1_unix:
                break
            start_index += 1
        end_index = 0
        for t in time_unix:
            if t >= date2_unix:
                break
            end_index += 1

        # Assign the first-level only tags
        time_unix = time_unix[start_index:end_index]
        temp = temp[start_index:end_index]
        time = temp.index
        time_unix = pd.Series(time_unix)  # convert into Series for consistency
        time_unix.index = temp.index

        if "SPICE.Orbit Number" in list(temp):
            orbit = temp["SPICE.Orbit Number"]
        else:
            orbit = None
        if "SPICE.Inbound Outbound Flag" in list(temp):
            io_flag = temp["SPICE.Inbound Outbound Flag"]
        else:
            io_flag = None

        # Build the sub-level DataFrames for the larger dictionary/structure
        app = temp[app_group]
        spacecraft = temp[sc_group]
        if instruments is not None:
            if "LPW" in instruments or "lpw" in instruments:
                lpw = temp[lpw_group]
            else:
                lpw = None
            if "MAG" in instruments or "mag" in instruments:
                mag = temp[mag_group]
            else:
                mag = None
            if "EUV" in instruments or "euv" in instruments:
                euv = temp[euv_group]
            else:
                euv = None
            if "SWE" in instruments or "swe" in instruments:
                swea = temp[swe_group]
            else:
                swea = None
            if "SWI" in instruments or "swi" in instruments:
                swia = temp[swi_group]
            else:
                swia = None
            if "NGI" in instruments or "ngi" in instruments:
                ngims = temp[ngi_group]
            else:
                ngims = None
            if "SEP" in instruments or "sep" in instruments:
                sep = temp[sep_group]
            else:
                sep = None
            if "STA" in instruments or "sta" in instruments:
                static = temp[sta_group]
            else:
                static = None
            if "MODELED_MAG" in instruments or "modeled_mag" in instruments:
                crus = temp[crus_group]
            else:
                crus = None
        else:
            lpw = temp[lpw_group]
            euv = temp[euv_group]
            swea = temp[swe_group]
            swia = temp[swi_group]
            static = temp[sta_group]
            sep = temp[sep_group]
            mag = temp[mag_group]
            ngims = temp[ngi_group]
            crus = temp[crus_group]

        # Strip out the duplicated instrument part of the column names
        # (this is a bit hardwired and can be improved)
        for i in [lpw, euv, swea, swia, sep, static, ngims, mag, crus, app, spacecraft]:
            if i is not None:
                i.columns = remove_inst_tag(i)

        if lpw is not None:
            lpw = lpw.rename(index=str, columns=param_dict)
        if euv is not None:
            euv = euv.rename(index=str, columns=param_dict)
        if swea is not None:
            swea = swea.rename(index=str, columns=param_dict)
        if swia is not None:
            swia = swia.rename(index=str, columns=param_dict)
        if sep is not None:
            sep = sep.rename(index=str, columns=param_dict)
        if static is not None:
            static = static.rename(index=str, columns=param_dict)
        if ngims is not None:
            ngims = ngims.rename(index=str, columns=param_dict)
        if mag is not None:
            mag = mag.rename(index=str, columns=param_dict)
        if crus is not None:
            crus = crus.rename(index=str, columns=param_dict)
        if app is not None:
            app = app.rename(index=str, columns=param_dict)
        if spacecraft is not None:
            spacecraft = spacecraft.rename(index=str, columns=param_dict)

        if orbit is not None and io_flag is not None:
            # Do not forget to save units
            # Define the list of first level tag names
            tag_names = [
                "TimeString",
                "Time",
                "Orbit",
                "IOflag",
                "LPW",
                "EUV",
                "SWEA",
                "SWIA",
                "STATIC",
                "SEP",
                "MAG",
                "NGIMS",
                "MODELED_MAG",
                "APP",
                "SPACECRAFT",
            ]

            # Define list of first level data structures
            data_tags = [
                time,
                time_unix,
                orbit,
                io_flag,
                lpw,
                euv,
                swea,
                swia,
                static,
                sep,
                mag,
                ngims,
                crus,
                app,
                spacecraft,
            ]
        else:
            # Do not forget to save units
            # Define the list of first level tag names
            tag_names = [
                "TimeString",
                "Time",
                "LPW",
                "EUV",
                "SWEA",
                "SWIA",
                "STATIC",
                "SEP",
                "MAG",
                "NGIMS",
                "MODELED_MAG",
                "APP",
                "SPACECRAFT",
            ]

            # Define list of first level data structures
            data_tags = [
                time,
                time_unix,
                lpw,
                euv,
                swea,
                swia,
                static,
                sep,
                mag,
                ngims,
                crus,
                app,
                spacecraft,
            ]

        kp_insitu = OrderedDict(zip(tag_names, data_tags))

    # Now for IUVS
    kp_iuvs = []
    if not insitu_only and iuvs_filenames:
        for file in iuvs_filenames:
            kp_iuvs.append(read_iuvs_file(file))

    if notplot:
        return kp_insitu

    if not kp_iuvs:
        return tplot_varcreate(kp_insitu)
    else:
        # return kp_insitu, kp_iuvs
        insitu_vars = tplot_varcreate(kp_insitu)
        # The kp_iuvs structure can't be converted using tplot_varcreate.  Not clear
        # what needs to be done in order to use them. We'll punt on it for now and just
        # return the insitu variables.
        # iuvs_vars = tplot_varcreate(kp_iuvs)
        return insitu_vars


def tplot_varcreate(insitu):
    """Creates tplot variables from the insitu variable"""
    # initialize each instrument
    created_vars = []
    for obs in insitu["SPACECRAFT"]:
        obs_specific = "mvn_kp::spacecraft::" + obs.lower()
        try:
            pytplot.store_data(
                obs_specific, data={"x": insitu["Time"], "y": insitu["SPACECRAFT"][obs]}
            )
            created_vars.append(obs_specific)
        except:
            pass

    # Join together the matricies and remove the individual points
    pytplot.join_vec(
        [
            "mvn_kp::spacecraft::t11",
            "mvn_kp::spacecraft::t12",
            "mvn_kp::spacecraft::t13",
            "mvn_kp::spacecraft::t21",
            "mvn_kp::spacecraft::t22",
            "mvn_kp::spacecraft::t23",
            "mvn_kp::spacecraft::t31",
            "mvn_kp::spacecraft::t32",
            "mvn_kp::spacecraft::t33",
        ],
        newname="mvn_kp::geo_to_mso_matrix",
    )

    pytplot.del_data(
        [
            "mvn_kp::spacecraft::t11",
            "mvn_kp::spacecraft::t12",
            "mvn_kp::spacecraft::t13",
            "mvn_kp::spacecraft::t21",
            "mvn_kp::spacecraft::t22",
            "mvn_kp::spacecraft::t23",
            "mvn_kp::spacecraft::t31",
            "mvn_kp::spacecraft::t32",
            "mvn_kp::spacecraft::t33",
        ]
    )

    pytplot.join_vec(
        [
            "mvn_kp::spacecraft::spacecraft_t11",
            "mvn_kp::spacecraft::spacecraft_t12",
            "mvn_kp::spacecraft::spacecraft_t13",
            "mvn_kp::spacecraft::spacecraft_t21",
            "mvn_kp::spacecraft::spacecraft_t22",
            "mvn_kp::spacecraft::spacecraft_t23",
            "mvn_kp::spacecraft::spacecraft_t31",
            "mvn_kp::spacecraft::spacecraft_t32",
            "mvn_kp::spacecraft::spacecraft_t33",
        ],
        newname="mvn_kp::spacecraft_to_mso_matrix",
    )

    pytplot.del_data(
        [
            "mvn_kp::spacecraft::spacecraft_t11",
            "mvn_kp::spacecraft::spacecraft_t12",
            "mvn_kp::spacecraft::spacecraft_t13",
            "mvn_kp::spacecraft::spacecraft_t21",
            "mvn_kp::spacecraft::spacecraft_t22",
            "mvn_kp::spacecraft::spacecraft_t23",
            "mvn_kp::spacecraft::spacecraft_t31",
            "mvn_kp::spacecraft::spacecraft_t32",
            "mvn_kp::spacecraft::spacecraft_t33",
        ]
    )

    created_vars.remove("mvn_kp::spacecraft::t11")
    created_vars.remove("mvn_kp::spacecraft::t12")
    created_vars.remove("mvn_kp::spacecraft::t13")
    created_vars.remove("mvn_kp::spacecraft::t21")
    created_vars.remove("mvn_kp::spacecraft::t22")
    created_vars.remove("mvn_kp::spacecraft::t23")
    created_vars.remove("mvn_kp::spacecraft::t31")
    created_vars.remove("mvn_kp::spacecraft::t32")
    created_vars.remove("mvn_kp::spacecraft::t33")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t11")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t12")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t13")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t21")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t22")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t23")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t31")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t32")
    created_vars.remove("mvn_kp::spacecraft::spacecraft_t33")

    inst_list = ["EUV", "LPW", "STATIC", "SWEA", "SWIA", "MAG", "SEP", "NGIMS"]
    for instrument in inst_list:
        # for each observation for each instrument
        if instrument in insitu:
            if insitu[instrument] is not None:
                for obs in insitu[instrument]:
                    # create variable name
                    obs_specific = "mvn_kp::" + instrument.lower() + "::" + obs.lower()
                    try:
                        # store data in tplot variable
                        pytplot.store_data(
                            obs_specific,
                            data={"x": insitu["Time"], "y": insitu[instrument][obs]},
                        )
                        created_vars.append(obs_specific)
                        pytplot.link(
                            obs_specific,
                            "mvn_kp::spacecraft::altitude",
                            link_type="alt",
                        )
                        pytplot.link(
                            obs_specific, "mvn_kp::spacecraft::mso_x", link_type="x"
                        )
                        pytplot.link(
                            obs_specific, "mvn_kp::spacecraft::mso_y", link_type="y"
                        )
                        pytplot.link(
                            obs_specific, "mvn_kp::spacecraft::mso_z", link_type="z"
                        )
                        pytplot.link(
                            obs_specific, "mvn_kp::spacecraft::geo_x", link_type="geo_x"
                        )
                        pytplot.link(
                            obs_specific, "mvn_kp::spacecraft::geo_y", link_type="geo_y"
                        )
                        pytplot.link(
                            obs_specific, "mvn_kp::spacecraft::geo_z", link_type="geo_z"
                        )
                        pytplot.link(
                            obs_specific,
                            "mvn_kp::spacecraft::sub_sc_longitude",
                            link_type="lon",
                        )
                        pytplot.link(
                            obs_specific,
                            "mvn_kp::spacecraft::sub_sc_latitude",
                            link_type="lat",
                        )
                    except:
                        pass
    return created_vars

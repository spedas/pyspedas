import logging
import re
import os
from . import download_files_utilities as utils
from .file_regex import maven_kp_l2_regex
import numpy as np
import collections

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def remove_inst_tag(df):
    """
    Remove the leading part of the column name that includes the instrument
    identifier for use in creating the parameter names for the toolkit.

    Parameters:
        A DataFrame produced from the insitu KP data
    Output:
        A new set of column names
    """

    newcol = []
    for i in df.columns:
        if len(i.split(".")) >= 2:
            j = i.split(".")
            newcol.append(".".join(j[1:]))

    return newcol


def get_latest_files_from_date_range(date1, date2):
    """
    Retrieves the latest files from a given date range.

    Parameters:
        date1 (datetime): The start date of the range.
        date2 (datetime): The end date of the range.

    Returns:
        list: A list of file paths representing the latest files within the date range.
    """

    from datetime import timedelta

    mvn_root_data_dir = utils.get_root_data_dir()
    sep = "/" if is_fsspec_uri(mvn_root_data_dir) else os.path.sep
    maven_data_dir = sep.join([
        mvn_root_data_dir, "maven", "data", "sci", "kp", "insitu"
    ])

    # Each file starts at midnight, so lets cut off the hours and just pay attention to the days
    date1 = date1.replace(hour=0, minute=0, second=0)
    date2 = date2.replace(hour=0, minute=0, second=0) + timedelta(days=1)

    time_spanned = date2 - date1
    num_days = time_spanned.days

    filenames = []
    kp_regex, l2_regex = maven_kp_l2_regex()

    for i in range(num_days):
        current_date = date1 + timedelta(days=i)
        year = str(current_date.year)
        month = str("%02d" % current_date.month)
        day = str("%02d" % current_date.day)
        full_path = sep.join([maven_data_dir, year, month])
        listdir = []
        if is_fsspec_uri(full_path):
            protocol, path = maven_data_dir.split("://")
            fs = fsspec.filesystem(protocol)

            exists = fs.exists(full_path)
            if exists:
                listdir = fs.listdir(full_path, detail=False)
                # fsspec alternative to os.path.basename
                listdir = [f.rstrip("/").split("/")[-1] for f in listdir]
        else:
            exists = os.path.exists(full_path)
            if exists: listdir = os.listdir(full_path)
        if exists:
            # Grab only the most recent version/revision of regular and crustal insitu files for each
            # day
            insitu = {}
            c_insitu = {}
            for f in listdir:
                # logging.warning(f)
                if kp_regex.match(f).group("day") == day and not kp_regex.match(
                    f
                ).group("description"):
                    v = kp_regex.match(f).group("version")
                    r = kp_regex.match(f).group("revision")
                    insitu[f] = [v, r]
                elif (
                    kp_regex.match(f).group("day") == day
                    and kp_regex.match(f).group("description") == "_crustal"
                ):
                    v = kp_regex.match(f).group("version")
                    r = kp_regex.match(f).group("revision")
                    c_insitu[f] = [v, r]

            if insitu:
                # Get max version
                insitu_file = max(insitu.keys(), key=(lambda k: insitu[k][0]))
                max_v = re.search(r"v\d{2}", insitu_file).group(0)
                # Get max revision
                max_r = max(
                    [re.search(r"r\d{2}", k).group(0) for k in insitu if max_v in k]
                )
                # Get most recent insitu file (based on max version, and then max revision values)
                most_recent_insitu = [
                    f for f in insitu.keys() if max_r in f and max_v in f
                ]
                filenames.append(sep.join([full_path, most_recent_insitu[0]]))

            if c_insitu:
                # Get max version
                c_insitu_file = max(c_insitu.keys(), key=(lambda k: c_insitu[k][0]))
                c_max_v = re.search(r"v\d{2}", c_insitu_file).group(0)
                # Get max revision
                c_max_r = max(
                    [re.search(r"r\d{2}", k).group(0) for k in c_insitu if c_max_v in k]
                )
                # Get most recent insitu file (based on max version, and then max revision values)
                most_recent_c_insitu = [
                    f for f in c_insitu.keys() if c_max_r in f and c_max_v in f
                ]
                filenames.append(sep.join([full_path, most_recent_c_insitu[0]]))

    filenames = sorted(filenames)
    return filenames


def get_latest_iuvs_files_from_date_range(date1, date2):
    """
    Get the latest IUVS files from a given date range.

    Parameters:
        date1 (datetime): The start date of the range.
        date2 (datetime): The end date of the range.

    Returns:
        list: A sorted list of file paths for the latest IUVS files within the date range.
    """

    from datetime import timedelta

    kp_regex, l2_regex = maven_kp_l2_regex()
    mvn_root_data_dir = utils.get_root_data_dir()
    sep = "/" if is_fsspec_uri(mvn_root_data_dir) else os.path.sep
    maven_data_dir = sep.join([
        mvn_root_data_dir, "maven", "data", "sci", "kp", "iuvs"
    ])

    # Each file starts at midnight, so lets cut off the hours and just pay attention to the days
    date1 = date1.replace(hour=0, minute=0, second=0)
    date2 = date2.replace(day=date2.day, hour=0, minute=0, second=0) + timedelta(days=1)

    time_spanned = date2 - date1
    num_days = time_spanned.days

    files_to_return = []
    for i in range(num_days):
        current_date = date1 + timedelta(days=i)
        year = str(current_date.year)
        month = str("%02d" % current_date.month)
        day = str("%02d" % current_date.day)
        # TODO: Fix the path after we fix the iuvs regex
        full_path = sep.join([maven_data_dir,"occ-", "02"])
        listdir = []
        if is_fsspec_uri(full_path):
            protocol, path = maven_data_dir.split("://")
            fs = fsspec.filesystem(protocol)

            exists = fs.exists(full_path)
            if exists:
                listdir = fs.listdir(full_path, detail=False)
                # fsspec alternative to os.path.basename
                listdir = [f.rstrip("/").split("/")[-1] for f in listdir]
        else:
            exists = os.path.exists(full_path)
            if exists: listdir = os.listdir(full_path)
        if exists:
            basenames = []
            # Obtain a list of all the basenames for the day
            for f in listdir:
                if kp_regex.match(f).group("day") == day:
                    description = kp_regex.match(f).group("description")
                    year = kp_regex.match(f).group("year")
                    month = kp_regex.match(f).group("month")
                    day = kp_regex.match(f).group("day")
                    time = kp_regex.match(f).group("time")
                    seq = ("mvn", "kp", "iuvs" + description, year + month + day + time)
                    basenames.append("_".join(seq))

            basenames = list(set(basenames))

            for bn in basenames:
                version = 0
                revision = 0
                for f in listdir:
                    description = kp_regex.match(f).group("description")
                    year = kp_regex.match(f).group("year")
                    month = kp_regex.match(f).group("month")
                    day = kp_regex.match(f).group("day")
                    time = kp_regex.match(f).group("time")
                    seq = ("mvn", "kp", "iuvs" + description, year + month + day + time)
                    if bn == "_".join(seq):
                        v = kp_regex.match(f).group("version")
                        if int(v) > int(version):
                            version = v

                for f in listdir:
                    description = kp_regex.match(f).group("description")
                    year = kp_regex.match(f).group("year")
                    month = kp_regex.match(f).group("month")
                    day = kp_regex.match(f).group("day")
                    time = kp_regex.match(f).group("time")
                    file_version = kp_regex.match(f).group("version")
                    seq = ("mvn", "kp", "iuvs" + description, year + month + day + time)
                    if bn == "_".join(seq) and file_version == version:
                        r = kp_regex.match(f).group("revision")
                        if int(r) > int(revision):
                            revision = r
                if int(version) > 0:
                    seq = (bn, "v" + str(version), "r" + str(revision) + ".tab")
                    files_to_return.append(sep.join([full_path, "_".join(seq)]))
    files_to_return = sorted(files_to_return)
    return files_to_return


def get_l2_files_from_date(date1, instrument):
    """
    Retrieves a list of Level 2 files for a given date and instrument.

    Parameters:
        date1 (datetime.datetime): The date for which to retrieve the files.
        instrument (str): The instrument name.

    Returns:
        list: A sorted list of file paths for the Level 2 files.
    """

    kp_regex, l2_regex = maven_kp_l2_regex()
    mvn_root_data_dir = utils.get_root_data_dir()
    sep = "/" if is_fsspec_uri(mvn_root_data_dir) else os.path.sep
    maven_data_dir = sep.join([mvn_root_data_dir, "maven", "data", "sci", instrument, "l2"])

    # Each file starts at midnight, so lets cut off the hours and just pay attention to the days
    date1 = date1.replace(hour=0, minute=0, second=0)

    filenames = []

    year = str(date1.year)
    month = str("%02d" % date1.month)
    day = str("%02d" % date1.day)
    full_path = sep.join([maven_data_dir, year, month])
    listdir = []
    if is_fsspec_uri(mvn_root_data_dir):
        protocol, path = mvn_root_data_dir.split("://")
        fs = fsspec.filesystem(protocol)

        exists = fs.exists(full_path)
        if exists:
            listdir = fs.listdir(full_path, detail=False)
            # fsspec alternative to os.path.basename
            listdir = [f.rstrip("/").split("/")[-1] for f in listdir]
    else:
        exists = os.path.exists(full_path)
        if exists:
            listdir = os.listdir(full_path)

    if exists:
        for f in listdir:
            if l2_regex.match(f).group("day") == day:
                filenames.append(sep.join([full_path, f]))

    filenames = sorted(filenames)
    return filenames


def get_header_info(filename):
    """
    Extracts header information from a file.

    Parameters:
    filename (str): The path to the file.

    Returns:
    tuple: A tuple containing the names list and inst list.
    """
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

    # Parse the header (still needs special case work)
    read_param_list = False
    start_temp = False
    index_list = []
    if is_fsspec_uri(filename):
        protocol, path = filename.split("://")
        fs = fsspec.filesystem(protocol)
        fo = fs.open(filename, "rt")
    else:
        fo = open(filename)
    with fo as fin:
        icol = -2  # Counting header lines detailing column names
        iname = 1  # for counting seven lines with name info
        ncol = -1  # Dummy value to allow reading of early headerlines?
        col_regex = r"#\s(.{16}){%3d}" % ncol  # needed for column names
        crustal = False
        if "crustal" in filename:
            crustal = True
        for iline in range(nheader):
            line = fin.readline()
            # Define the proper indices change depending on the file type and row
            i = [2, 2, 1] if crustal else [1, 1, 1]
            if re.search("Number of parameter columns", line):
                ncol = int(re.split(r"\s{3}", line)[i[0]])
                # needed for column names
                col_regex = (
                    r"#\s(.{16}){%2d}" % ncol if crustal else r"#\s(.{16}){%3d}" % ncol
                )
            elif re.search("Line on which data begins", line):
                nhead_test = int(re.split(r"\s{3}", line)[i[1]]) - 1
            elif re.search("Number of lines", line):
                ndata = int(re.split(r"\s{3}", line)[i[2]])
            elif re.search("PARAMETER", line):
                read_param_list = True
                param_head = iline
            elif read_param_list:
                icol += 1
                if icol > ncol:
                    read_param_list = False
            elif re.match(col_regex, line):
                # OK, verified match now get the values
                temp = re.findall("(.{16})", line[3:])
                if temp[0] == "               1":
                    start_temp = True
                if start_temp:
                    # Crustal files do not have as much variable info as other insitu files, need
                    # to modify the lines below
                    if crustal:
                        if iname == 1:
                            index = temp
                        elif iname == 2:
                            obs1 = temp
                        elif iname == 3:
                            obs2 = temp
                        elif iname == 4:
                            unit = temp
                            # crustal files don't come with this field
                            # throwing it in here for consistency with other insitu files
                            inst = ["     MODELED_MAG"] * 13
                        else:
                            logging.warning(
                                "More lines in data descriptor than expected."
                            )
                            logging.warning("Line %d" % iline)
                    else:
                        if iname == 1:
                            index = temp
                        elif iname == 2:
                            obs1 = temp
                        elif iname == 3:
                            obs2 = temp
                        elif iname == 4:
                            obs3 = temp
                        elif iname == 5:
                            inst = temp
                        elif iname == 6:
                            unit = temp
                        elif iname == 7:
                            format_code = temp
                        else:
                            logging.warning(
                                "More lines in data descriptor than expected."
                            )
                            logging.warning("Line %d" % iline)
                    iname += 1
            else:
                pass

        # Generate the names list.
        # NB, there are special case redundancies in there
        # (e.g., LPW: Electron Density Quality (min and max))
        # ****SWEA FLUX electron QUALITY *****
        first = True
        parallel = None
        names = []
        if crustal:
            for h, i, j in zip(inst, obs1, obs2):
                combo_name = (" ".join([i.strip(), j.strip()])).strip()
                # Add inst to names to avoid ambiguity
                # Will need to remove these after splitting
                names.append(".".join([h.strip(), combo_name]))
                names[0] = "Time"
        else:
            for h, i, j, k in zip(inst, obs1, obs2, obs3):
                combo_name = (" ".join([i.strip(), j.strip(), k.strip()])).strip()
                if re.match("^LPW$", h.strip()):
                    # Max and min error bars use same name in column
                    # SIS says first entry is min and second is max
                    if re.match("(Electron|Spacecraft)(.+)Quality", combo_name):
                        if first:
                            combo_name = combo_name + " Min"
                            first = False
                        else:
                            combo_name = combo_name + " Max"
                            first = True
                elif re.match("^SWEA$", h.strip()):
                    # electron flux qual flags do not indicate whether parallel or anti
                    # From context it is clear; but we need to specify in name
                    if re.match(".+Parallel.+", combo_name):
                        parallel = True
                    elif re.match(".+Anti-par", combo_name):
                        parallel = False
                    else:
                        pass
                    if re.match("Flux, e-(.+)Quality", combo_name):
                        if parallel:
                            p = re.compile("Flux, e- ")
                            combo_name = p.sub("Flux, e- Parallel ", combo_name)
                        else:
                            p = re.compile("Flux, e- ")
                            combo_name = p.sub("Flux, e- Anti-par ", combo_name)
                    if re.match("Electron eflux (.+)Quality", combo_name):
                        if parallel:
                            p = re.compile("Electron eflux ")
                            combo_name = p.sub("Electron eflux  Parallel ", combo_name)
                        else:
                            p = re.compile("Electron eflux ")
                            combo_name = p.sub("Electron eflux  Anti-par ", combo_name)
                # Add inst to names to avoid ambiguity
                # Will need to remove these after splitting
                names.append(".".join([h.strip(), combo_name]))
                names[0] = "Time"

    return names, inst

def maven_param_list():
    """
    Returns a dictionary of MAVEN parameters and their corresponding keys.

    Returns:
        dict: A dictionary mapping parameter names to their keys.
    """

    param_dict = {
        "Electron Density": "ELECTRON_DENSITY",
        "Electron Density Quality Min": "ELECTRON_DENSITY_QUAL_MIN",
        "Electron Density Quality Max": "ELECTRON_DENSITY_QUAL_MAX",
        "Electron Temperature": "ELECTRON_TEMPERATURE",
        "Electron Temperature Quality Min": "ELECTRON_TEMPERATURE_QUAL_MIN",
        "Electron Temperature Quality Max": "ELECTRON_TEMPERATURE_QUAL_MAX",
        "Spacecraft Potential": "SPACECRAFT_POTENTIAL",
        "Spacecraft Potential Quality Min": "SPACECRAFT_POTENTIAL_QUAL_MIN",
        "Spacecraft Potential Quality Max": "SPACECRAFT_POTENTIAL_QUAL_MAX",
        "E-field Power 2-100 Hz": "EWAVE_LOW_FREQ",
        "E-field 2-100 Hz Quality": "EWAVE_LOW_FREQ_QUAL_QUAL",
        "E-field Power 100-800 Hz": "EWAVE_MID_FREQ",
        "E-field 100-800 Hz Quality": "EWAVE_MID_FREQ_QUAL_QUAL",
        "E-field Power 0.8-1.0 Mhz": "EWAVE_HIGH_FREQ",
        "E-field 0.8-1.0 Mhz Quality": "EWAVE_HIGH_FREQ_QUAL_QUAL",
        "EUV Irradiance 0.1-7.0 nm": "IRRADIANCE_LOW",
        "Irradiance 0.1-7.0 nm Quality": "IRRADIANCE_LOW_QUAL",
        "EUV Irradiance 17-22 nm": "IRRADIANCE_MID",
        "Irradiance 17-22 nm Quality": "IRRADIANCE_MID_QUAL",
        "EUV Irradiance Lyman-alpha": "IRRADIANCE_LYMAN",
        "Irradiance Lyman-alpha Quality": "IRRADIANCE_LYMAN_QUAL",
        "Solar Wind Electron Density": "SOLAR_WIND_ELECTRON_DENSITY",
        "Solar Wind E- Density Quality": "SOLAR_WIND_ELECTRON_DENSITY_QUAL",
        "Solar Wind Electron Temperature": "SOLAR_WIND_ELECTRON_TEMPERATURE",
        "Solar Wind E- Temperature Quality": "SOLAR_WIND_ELECTRON_TEMPERATURE_QUAL",
        "Flux, e- Parallel (5-100 ev)": "ELECTRON_PARALLEL_FLUX_LOW",
        "Flux, e- Parallel (5-100 ev) Quality": "ELECTRON_PARALLEL_FLUX_LOW_QUAL",
        "Flux, e- Parallel (100-500 ev)": "ELECTRON_PARALLEL_FLUX_MID",
        "Flux, e- Parallel (100-500 ev) Quality": "ELECTRON_PARALLEL_FLUX_MID_QUAL",
        "Flux, e- Parallel (500-1000 ev)": "ELECTRON_PARALLEL_FLUX_HIGH",
        "Flux, e- Parallel (500-1000 ev) Quality": "ELECTRON_PARALLEL_FLUX_HIGH_QUAL",
        "Flux, e- Anti-par (5-100 ev)": "ELECTRON_ANTI_PARALLEL_FLUX_LOW",
        "Flux, e- Anti-par (5-100 ev) Quality": "ELECTRON_ANTI_PARALLEL_FLUX_LOW_QUAL",
        "Flux, e- Anti-par (100-500 ev)": "ELECTRON_ANTI_PARALLEL_FLUX_MID",
        "Flux, e- Anti-par (100-500 ev) Quality": "ELECTRON_ANTI_PARALLEL_FLUX_MID_QUAL",
        "Flux, e- Anti-par (500-1000 ev)": "ELECTRON_ANTI_PARALLEL_FLUX_HIGH",
        "Flux, e- Anti-par (500-1000 ev) Quality": "ELECTRON_ANTI_PARALLEL_FLUX_HIGH_QUAL",
        "Electron eflux Parallel (5-100 ev)": "ELECTRON_PARALLEL_FLUX_LOW",
        "Electron eflux Parallel (5-100 ev) Quality": "ELECTRON_PARALLEL_FLUX_LOW_QUAL",
        "Electron eflux Parallel (100-500 ev)": "ELECTRON_PARALLEL_FLUX_MID",
        "Electron eflux Parallel (100-500 ev) Quality": "ELECTRON_PARALLEL_FLUX_MID_QUAL",
        "Electron eflux Parallel (500-1000 ev)": "ELECTRON_PARALLEL_FLUX_HIGH",
        "Electron eflux Parallel (500-1000 ev) Quality": "ELECTRON_PARALLEL_FLUX_HIGH_QUAL",
        "Electron eflux Anti-par (5-100 ev)": "ELECTRON_ANTI_PARALLEL_FLUX_LOW",
        "Electron eflux Anti-par (5-100 ev) Quality": "ELECTRON_ANTI_PARALLEL_FLUX_LOW_QUAL",
        "Electron eflux Anti-par (100-500 ev)": "ELECTRON_ANTI_PARALLEL_FLUX_MID",
        "Electron eflux Anti-par (100-500 ev) Quality": "ELECTRON_ANTI_PARALLEL_FLUX_MID_QUAL",
        "Electron eflux Anti-par (500-1000 ev)": "ELECTRON_ANTI_PARALLEL_FLUX_HIGH",
        "Electron eflux Anti-par (500-1000 ev) Quality": "ELECTRON_ANTI_PARALLEL_FLUX_HIGH_QUAL",
        "Electron Spectrum Shape": "ELECTRON_SPECTRUM_SHAPE_PARAMETER",
        "Spectrum Shape Quality": "ELECTRON_SPECTRUM_SHAPE_PARAMETER_QUAL",
        "H+ Density": "HPLUS_DENSITY",
        "H+ Density Quality": "HPLUS_DENSITY_QUAL",
        "H+ Flow Velocity MSO X": "HPLUS_FLOW_VELOCITY_MSO_X",
        "H+ Flow MSO X Quality": "HPLUS_FLOW_VELOCITY_MSO_X_QUAL",
        "H+ Flow Velocity MSO Y": "HPLUS_FLOW_VELOCITY_MSO_Y",
        "H+ Flow MSO Y Quality": "HPLUS_FLOW_VELOCITY_MSO_Y_QUAL",
        "H+ Flow Velocity MSO Z": "HPLUS_FLOW_VELOCITY_MSO_Z",
        "H+ Flow MSO Z Quality": "HPLUS_FLOW_VELOCITY_MSO_Z_QUAL",
        "H+ Temperature": "HPLUS_TEMPERATURE",
        "H+ Temperature Quality": "HPLUS_TEMPERATURE_QUAL",
        "Solar Wind Dynamic Pressure": "SOLAR_WIND_DYNAMIC_PRESSURE",
        "Solar Wind Pressure Quality": "SOLAR_WIND_DYNAMIC_PRESSURE_QUAL",
        "STATIC Quality Flag": "STATIC_QUALITY_FLAG",
        "O+ Density": "OPLUS_DENSITY",
        "O+ Density Quality": "OPLUS_DENSITY_QUAL",
        "O2+ Density": "O2PLUS_DENSITY",
        "O2+ Density Quality": "O2PLUS_DENSITY_QUAL",
        "O+ Temperature": "OPLUS_TEMPERATURE",
        "O+ Temperature Quality": "OPLUS_TEMPERATURE_QUAL",
        "O2+ Temperature": "O2PLUS_TEMPERATURE",
        "O2+ Temperature Quality": "O2PLUS_TEMPERATURE_QUAL",
        "O2+ Flow Velocity MAVEN_APP X": "O2PLUS_FLOW_VELOCITY_MAVEN_APP_X",
        "O2+ Flow MAVEN_APP X Quality": "O2PLUS_FLOW_VELOCITY_MAVEN_APP_X_QUAL",
        "O2+ Flow Velocity MAVEN_APP Y": "O2PLUS_FLOW_VELOCITY_MAVEN_APP_Y",
        "O2+ Flow MAVEN_APP Y Quality": "O2PLUS_FLOW_VELOCITY_MAVEN_APP_Y_QUAL",
        "O2+ Flow Velocity MAVEN_APP Z": "O2PLUS_FLOW_VELOCITY_MAVEN_APP_Z",
        "O2+ Flow MAVEN_APP Z Quality": "O2PLUS_FLOW_VELOCITY_MAVEN_APP_Z_QUAL",
        "O2+ Flow Velocity MSO X": "O2PLUS_FLOW_VELOCITY_MSO_X",
        "O2+ Flow MSO X Quality": "O2PLUS_FLOW_VELOCITY_MSO_X_QUAL",
        "O2+ Flow Velocity MSO Y": "O2PLUS_FLOW_VELOCITY_MSO_Y",
        "O2+ Flow MSO Y Quality": "O2PLUS_FLOW_VELOCITY_MSO_Y_QUAL",
        "O2+ Flow Velocity MSO Z": "O2PLUS_FLOW_VELOCITY_MSO_Z",
        "O2+ Flow MSO Z Quality": "O2PLUS_FLOW_VELOCITY_MSO_Z_QUAL",
        "H+ Omni Flux": "HPLUS_OMNI_DIRECTIONAL_FLUX",
        "H+ Energy": "HPLUS_CHARACTERISTIC_ENERGY",
        "H+ Energy Quality": "HPLUS_CHARACTERISTIC_ENERGY_QUAL",
        "He++ Omni Flux": "HEPLUS_OMNI_DIRECTIONAL_FLUX",
        "He++ Energy": "HEPLUS_CHARACTERISTIC_ENERGY",
        "He++ Energy Quality": "HEPLUS_CHARACTERISTIC_ENERGY_QUAL",
        "O+ Omni Flux": "OPLUS_OMNI_DIRECTIONAL_FLUX",
        "O+ Energy": "OPLUS_CHARACTERISTIC_ENERGY",
        "O+ Energy Quality": "OPLUS_CHARACTERISTIC_ENERGY_QUAL",
        "O2+ Omni Flux": "O2PLUS_OMNI_DIRECTIONAL_FLUX",
        "O2+ Energy": "O2PLUS_CHARACTERISTIC_ENERGY",
        "O2+ Energy Quality": "O2PLUS_CHARACTERISTIC_ENERGY_QUAL",
        "H+ Direction MSO X": "HPLUS_CHARACTERISTIC_DIRECTION_MSO_X",
        "H+ Direction MSO Y": "HPLUS_CHARACTERISTIC_DIRECTION_MSO_Y",
        "H+ Direction MSO Z": "HPLUS_CHARACTERISTIC_DIRECTION_MSO_Z",
        "H+ Angular Width": "HPLUS_CHARACTERISTIC_ANGULAR_WIDTH",
        "H+ Width Quality": "HPLUS_CHARACTERISTIC_ANGULAR_WIDTH_QUAL",
        "Pickup Ion Direction MSO X": "DOMINANT_PICKUP_ION_CHARACTERISTIC_DIRECTION_MSO_X",
        "Pickup Ion Direction MSO Y": "DOMINANT_PICKUP_ION_CHARACTERISTIC_DIRECTION_MSO_Y",
        "Pickup Ion Direction MSO Z": "DOMINANT_PICKUP_ION_CHARACTERISTIC_DIRECTION_MSO_Z",
        "Pickup Ion Angular Width": "DOMINANT_PICKUP_ION_CHARACTERISTIC_ANGULAR_WIDTH",
        "Pickup Ion Width Quality": "DOMINANT_PICKUP_ION_CHARACTERISTIC_ANGULAR_WIDTH_QUAL",
        "Ion Flux FOV 1 F": "ION_ENERGY_FLUX__FOV_1_F",
        "Ion Flux FOV 1F Quality": "ION_ENERGY_FLUX__FOV_1_F_QUAL",
        "Ion Flux FOV 1 R": "ION_ENERGY_FLUX__FOV_1_R",
        "Ion Flux FOV 1R Quality": "ION_ENERGY_FLUX__FOV_1_R_QUAL",
        "Ion Flux FOV 2 F": "ION_ENERGY_FLUX__FOV_2_F",
        "Ion Flux FOV 2F Quality": "ION_ENERGY_FLUX__FOV_2_F_QUAL",
        "Ion Flux FOV 2 R": "ION_ENERGY_FLUX__FOV_2_R",
        "Ion Flux FOV 2R Quality": "ION_ENERGY_FLUX__FOV_2_R_QUAL",
        "Electron Flux FOV 1 F": "ELECTRON_ENERGY_FLUX___FOV_1_F",
        "Electron Flux FOV 1F Quality": "ELECTRON_ENERGY_FLUX___FOV_1_F_QUAL",
        "Electron Flux FOV 1 R": "ELECTRON_ENERGY_FLUX___FOV_1_R",
        "Electron Flux FOV 1R Quality": "ELECTRON_ENERGY_FLUX___FOV_1_R_QUAL",
        "Electron Flux FOV 2 F": "ELECTRON_ENERGY_FLUX___FOV_2_F",
        "Electron Flux FOV 2F Quality": "ELECTRON_ENERGY_FLUX___FOV_2_F_QUAL",
        "Electron Flux FOV 2 R": "ELECTRON_ENERGY_FLUX___FOV_2_R",
        "Electron Flux FOV 2R Quality": "ELECTRON_ENERGY_FLUX___FOV_2_R_QUAL",
        "Look Direction 1-F MSO X": "LOOK_DIRECTION_1_F_MSO_X",
        "Look Direction 1-F MSO Y": "LOOK_DIRECTION_1_F_MSO_Y",
        "Look Direction 1-F MSO Z": "LOOK_DIRECTION_1_F_MSO_Z",
        "Look Direction 1-R MSO X": "LOOK_DIRECTION_1_R_MSO_X",
        "Look Direction 1-R MSO Y": "LOOK_DIRECTION_1_R_MSO_Y",
        "Look Direction 1-R MSO Z": "LOOK_DIRECTION_1_R_MSO_Z",
        "Look Direction 2-F MSO X": "LOOK_DIRECTION_2_F_MSO_X",
        "Look Direction 2-F MSO Y": "LOOK_DIRECTION_2_F_MSO_Y",
        "Look Direction 2-F MSO Z": "LOOK_DIRECTION_2_F_MSO_Z",
        "Look Direction 2-R MSO X": "LOOK_DIRECTION_2_R_MSO_X",
        "Look Direction 2-R MSO Y": "LOOK_DIRECTION_2_R_MSO_Y",
        "Look Direction 2-R MSO Z": "LOOK_DIRECTION_2_R_MSO_Z",
        "Magnetic Field MSO X": "MSO_X",
        "Magnetic MSO X Quality": "MSO_X_QUAL",
        "Magnetic Field MSO Y": "MSO_Y",
        "Magnetic MSO Y Quality": "MSO_Y_QUAL",
        "Magnetic Field MSO Z": "MSO_Z",
        "Magnetic MSO Z Quality": "MSO_Z_QUAL",
        "Magnetic Field GEO X": "GEO_X",
        "Magnetic GEO X Quality": "GEO_X_QUAL",
        "Magnetic Field GEO Y": "GEO_Y",
        "Magnetic GEO Y Quality": "GEO_Y_QUAL",
        "Magnetic Field GEO Z": "GEO_Z",
        "Magnetic GEO Z Quality": "GEO_Z_QUAL",
        "Magnetic Field RMS Dev": "RMS_DEVIATION",
        "Magnetic RMS Quality": "RMS_DEVIATION_QUAL",
        "Density He": "HE_DENSITY",
        "Density He Precision": "HE_DENSITY_PRECISION",
        "Density He Quality": "HE_DENSITY_QUAL",
        "Density O": "O_DENSITY",
        "Density O Precision": "O_DENSITY_PRECISION",
        "Density O Quality": "O_DENSITY_QUAL",
        "Density CO": "CO_DENSITY",
        "Density CO Precision": "CO_DENSITY_PRECISION",
        "Density CO Quality": "CO_DENSITY_QUAL",
        "Density N2": "N2_DENSITY",
        "Density N2 Precision": "N2_DENSITY_PRECISION",
        "Density N2 Quality": "N2_DENSITY_QUAL",
        "Density NO": "NO_DENSITY",
        "Density NO Precision": "NO_DENSITY_PRECISION",
        "Density NO Quality": "NO_DENSITY_QUAL",
        "Density Ar": "AR_DENSITY",
        "Density Ar Precision": "AR_DENSITY_PRECISION",
        "Density Ar Quality": "AR_DENSITY_QUAL",
        "Density CO2": "CO2_DENSITY",
        "Density CO2 Precision": "CO2_DENSITY_PRECISION",
        "Density CO2 Quality": "CO2_DENSITY_QUAL",
        "Density 32+": "O2PLUS_DENSITY",
        "Density 32+ Precision": "O2PLUS_DENSITY_PRECISION",
        "Density 32+ Quality": "O2PLUS_DENSITY_QUAL",
        "Density 44+": "CO2PLUS_DENSITY",
        "Density 44+ Precision": "CO2PLUS_DENSITY_PRECISION",
        "Density 44+ Quality": "CO2PLUS_DENSITY_QUAL",
        "Density 30+": "NOPLUS_DENSITY",
        "Density 30+ Precision": "NOPLUS_DENSITY_PRECISION",
        "Density 30+ Quality": "NOPLUS_DENSITY_QUAL",
        "Density 16+": "OPLUS_DENSITY",
        "Density 16+ Precision": "OPLUS_DENSITY_PRECISION",
        "Density 16+ Quality": "OPLUS_DENSITY_QUAL",
        "Density 28+": "CO2PLUS_N2PLUS_DENSITY",
        "Density 28+ Precision": "CO2PLUS_N2PLUS_DENSITY_PRECISION",
        "Density 28+ Quality": "CO2PLUS_N2PLUS_DENSITY_QUAL",
        "Density 12+": "CPLUS_DENSITY",
        "Density 12+ Precision": "CPLUS_DENSITY_PRECISION",
        "Density 12+ Quality": "CPLUS_DENSITY_QUAL",
        "Density 17+": "OHPLUS_DENSITY",
        "Density 17+ Precision": "OHPLUS_DENSITY_PRECISION",
        "Density 17+ Quality": "OHPLUS_DENSITY_QUAL",
        "Density 14+": "NPLUS_DENSITY",
        "Density 14+ Precision": "NPLUS_DENSITY_PRECISION",
        "Density 14+ Quality": "NPLUS_DENSITY_QUAL",
        "APP Attitude GEO X": "ATTITUDE_GEO_X",
        "APP Attitude GEO Y": "ATTITUDE_GEO_Y",
        "APP Attitude GEO Z": "ATTITUDE_GEO_Z",
        "APP Attitude MSO X": "ATTITUDE_MSO_X",
        "APP Attitude MSO Y": "ATTITUDE_MSO_Y",
        "APP Attitude MSO Z": "ATTITUDE_MSO_Z",
        "Spacecraft GEO X": "GEO_X",
        "Spacecraft GEO Y": "GEO_Y",
        "Spacecraft GEO Z": "GEO_Z",
        "Spacecraft MSO X": "MSO_X",
        "Spacecraft MSO Y": "MSO_Y",
        "Spacecraft MSO Z": "MSO_Z",
        "Spacecraft GEO Longitude": "SUB_SC_LONGITUDE",
        "Spacecraft GEO Latitude": "SUB_SC_LATITUDE",
        "Spacecraft Solar Zenith Angle": "SZA",
        "Spacecraft Local Time": "LOCAL_TIME",
        "Spacecraft Altitude Aeroid": "ALTITUDE",
        "Spacecraft Attitude GEO X": "ATTITUDE_GEO_X",
        "Spacecraft Attitude GEO Y": "ATTITUDE_GEO_Y",
        "Spacecraft Attitude GEO Z": "ATTITUDE_GEO_Z",
        "Spacecraft Attitude MSO X": "ATTITUDE_MSO_X",
        "Spacecraft Attitude MSO Y": "ATTITUDE_MSO_Y",
        "Spacecraft Attitude MSO Z": "ATTITUDE_MSO_Z",
        "Mars Season (Ls)": "MARS_SEASON",
        "Mars-Sun Distance": "MARS_SUN_DISTANCE",
        "Subsolar Point GEO Longitude": "SUBSOLAR_POINT_GEO_LONGITUDE",
        "Subsolar Point GEO Latitude": "SUBSOLAR_POINT_GEO_LATITUDE",
        "Sub-Mars Point on the Sun Longitude": "SUBMARS_POINT_SOLAR_LONGITUDE",
        "Sub-Mars Point on the Sun Latitude": "SUBMARS_POINT_SOLAR_LATITUDE",
        "Rot matrix MARS -> MSO Row 1, Col 1": "T11",
        "Rot matrix MARS -> MSO Row 1, Col 2": "T12",
        "Rot matrix MARS -> MSO Row 1, Col 3": "T13",
        "Rot matrix MARS -> MSO Row 2, Col 1": "T21",
        "Rot matrix MARS -> MSO Row 2, Col 2": "T22",
        "Rot matrix MARS -> MSO Row 2, Col 3": "T23",
        "Rot matrix MARS -> MSO Row 3, Col 1": "T31",
        "Rot matrix MARS -> MSO Row 3, Col 2": "T32",
        "Rot matrix MARS -> MSO Row 3, Col 3": "T33",
        "Rot matrix SPCCRFT -> MSO Row 1, Col 1": "SPACECRAFT_T11",
        "Rot matrix SPCCRFT -> MSO Row 1, Col 2": "SPACECRAFT_T12",
        "Rot matrix SPCCRFT -> MSO Row 1, Col 3": "SPACECRAFT_T13",
        "Rot matrix SPCCRFT -> MSO Row 2, Col 1": "SPACECRAFT_T21",
        "Rot matrix SPCCRFT -> MSO Row 2, Col 2": "SPACECRAFT_T22",
        "Rot matrix SPCCRFT -> MSO Row 2, Col 3": "SPACECRAFT_T23",
        "Rot matrix SPCCRFT -> MSO Row 3, Col 1": "SPACECRAFT_T31",
        "Rot matrix SPCCRFT -> MSO Row 3, Col 2": "SPACECRAFT_T32",
        "Rot matrix SPCCRFT -> MSO Row 3, Col 3": "SPACECRAFT_T33",
    }
    return param_dict

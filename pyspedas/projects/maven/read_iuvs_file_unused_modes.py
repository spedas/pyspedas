import logging
import re
import os
from . import download_files_utilities as utils
from .file_regex import maven_kp_l2_regex
import numpy as np
import collections


# The code in this file was originally part of read_iuvs_file.py. According to
# justin.deighan@lasp.colorado.edu, these modes will not be supported with KP data.
# We'll keep the code alive here just in case they change their minds in the future.

def read_iuvs_file_unused_modes(file):
    """
    Read an IUVS file and return a dictionary containing the data.

    Parameters:
        file (str): The path to the IUVS file to be read.

    Returns:
        dict: A dictionary containing the data read from the IUVS file.
    """
    iuvs_dict = {}
    periapse_num = 0
    occ_num = 0
    with open(file) as f:
        line = f.readline()
        while line != "":
            if line.startswith("*"):
                # Read the header
                line = f.readline()
                obs_mode = line[19 : len(line) - 1].strip()

                header = {}
                f.readline()
                line = f.readline()
                header["time_start"] = line[19 : len(line) - 1].strip()
                line = f.readline()
                header["time_stop"] = line[19 : len(line) - 1].strip()
                line = f.readline()
                if obs_mode == "OCCULTATION":
                    header["target_name"] = line[19 : len(line) - 1].strip()
                    line = f.readline()
                header["sza"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["local_time"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["lat"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["lon"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["lat_mso"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["lon_mso"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["orbit_number"] = int(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["mars_season"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_geo_x"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_geo_y"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_geo_z"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_mso_x"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_mso_y"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_mso_z"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_geo_x"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_geo_y"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_geo_z"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_geo_lat"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_geo_lon"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_mso_lat"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sun_mso_lon"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["subsol_geo_lon"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["subsol_geo_lat"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_sza"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_local_time"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["sc_alt"] = float(line[19 : len(line) - 1].strip())
                line = f.readline()
                header["mars_sun_dist"] = float(line[19 : len(line) - 1].strip())

                if obs_mode == "CORONA_LORES_HIGH":
                    line = f.readline()
                    n_alt_bins = int(line[19 : len(line) - 1].strip())
                    header["n_alt_bins"] = float(n_alt_bins)

                    iuvs_dict["corona_lores_high"] = {}
                    iuvs_dict["corona_lores_high"].update(header)

                    f.readline()

                    # Read the Half int
                    line = f.readline()
                    half_int_dist_labels = line[19 : len(line) - 1].strip().split()
                    half_int_dist = collections.OrderedDict(
                        (x, []) for x in half_int_dist_labels
                    )
                    half_int_dist_unc = collections.OrderedDict(
                        (x, []) for x in half_int_dist_labels
                    )
                    line = f.readline()
                    vals = line[26 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        half_int_dist[list(half_int_dist.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[26 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        half_int_dist_unc[list(half_int_dist_unc.keys())[index]].append(
                            val
                        )
                        index += 1

                    iuvs_dict["corona_lores_high"]["half_int_dist"] = half_int_dist
                    iuvs_dict["corona_lores_high"][
                        "half_int_dist_unc"
                    ] = half_int_dist_unc

                    # Blank space
                    f.readline()
                    f.readline()

                    # Read in the density
                    line = f.readline()
                    density_labels = line.strip().split()
                    density = collections.OrderedDict((x, []) for x in density_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == "-9.9999990E+09":
                                val = float("nan")
                            else:
                                val = float(val)
                            density[list(density.keys())[index]].append(val)
                            index += 1

                    iuvs_dict["corona_lores_high"]["density"] = density

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density systematic uncertainty
                    density_sys_unc = collections.OrderedDict(
                        (x, []) for x in density_labels
                    )
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        density_sys_unc[list(density.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict["corona_lores_high"]["density_sys_unc"] = density_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density uncertainty
                    density_unc = collections.OrderedDict(
                        (x, []) for x in density_labels
                    )
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == "-9.9999990E+09":
                                val = float("nan")
                            else:
                                val = float(val)
                            density_unc[list(density.keys())[index]].append(val)
                            index += 1

                    iuvs_dict["corona_lores_high"]["density_unc"] = density_unc

                    f.readline()
                    f.readline()

                    line = f.readline()
                    radiance_labels = line.strip().split()
                    if "Cameron" in radiance_labels:
                        radiance_labels.remove("Cameron")
                    radiance = collections.OrderedDict((x, []) for x in radiance_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == "-9.9999990E+09":
                                val = float("nan")
                            else:
                                val = float(val)
                            radiance[list(radiance.keys())[index]].append(val)
                            index += 1

                    iuvs_dict["corona_lores_high"]["radiance"] = radiance

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance systematic uncertainty
                    radiance_sys_unc = collections.OrderedDict(
                        (x, []) for x in radiance_labels
                    )
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        radiance_sys_unc[list(radiance.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict["corona_lores_high"][
                        "radiance_sys_unc"
                    ] = radiance_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance uncertainty
                    radiance_unc = collections.OrderedDict(
                        (x, []) for x in radiance_labels
                    )
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == "-9.9999990E+09":
                                val = float("nan")
                            else:
                                val = float(val)
                            radiance_unc[list(radiance.keys())[index]].append(val)
                            index += 1

                    iuvs_dict["corona_lores_high"]["radiance_unc"] = radiance_unc

                elif obs_mode == "APOAPSE":

                    f.readline()
                    maps = {}
                    for j in range(0, 17):
                        var = f.readline().strip()
                        line = f.readline()
                        lons = line.strip().split()
                        lons = [float(x) for x in lons]
                        lats = []
                        data = []
                        for k in range(0, 45):
                            line = f.readline().strip().split()
                            lats.append(float(line[0]))
                            line_data = line[1:]
                            line_data = [
                                float(x) if x != "-9.9999990E+09" else float("nan")
                                for x in line_data
                            ]
                            data.append(line_data)

                        maps[var] = data
                        f.readline()

                    maps["latitude"] = lats
                    maps["longitude"] = lons

                    iuvs_dict["apoapse"] = {}
                    iuvs_dict["apoapse"].update(header)
                    iuvs_dict["apoapse"].update(maps)

                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance systematic uncertainty
                    line = f.readline()
                    radiance_labels = line.strip().split()
                    radiance_sys_unc = collections.OrderedDict(
                        (x, []) for x in radiance_labels
                    )
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        radiance_sys_unc[list(radiance.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict["apoapse"]["radiance_sys_unc"] = radiance_sys_unc

            line = f.readline()

    return iuvs_dict



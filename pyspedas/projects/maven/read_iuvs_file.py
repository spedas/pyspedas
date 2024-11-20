import logging
import re
import os
from . import download_files_utilities as utils
from .file_regex import maven_kp_l2_regex
import numpy as np
import collections

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def read_iuvs_file(file):
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
    if is_fsspec_uri(file):
        protocol, path = file.split("://")
        fs = fsspec.filesystem(protocol)

        fileobj = fs.open(file, "r")
    else:
        fileobj = open(file, "r")
    with fileobj as f:
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

                if obs_mode == "PERIAPSE":
                    periapse_num += 1
                    line = f.readline()
                    n_alt_bins = int(line[19 : len(line) - 1].strip())
                    header["n_alt_bins"] = float(n_alt_bins)
                    line = f.readline()
                    n_alt_den_bins = int(line[19 : len(line) - 1].strip())
                    header["n_alt_den_bins"] = float(n_alt_den_bins)

                    iuvs_dict["periapse" + str(periapse_num)] = {}
                    iuvs_dict["periapse" + str(periapse_num)].update(header)

                    # Empty space
                    f.readline()

                    # Read the Temperature
                    line = f.readline()
                    temp_labels = line[19 : len(line) - 1].strip().split()
                    temperature = collections.OrderedDict((x, []) for x in temp_labels)
                    temperature_unc = collections.OrderedDict(
                        (x, []) for x in temp_labels
                    )
                    line = f.readline()
                    vals = line[20 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        temperature[list(temperature.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[20 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        temperature_unc[list(temperature_unc.keys())[index]].append(val)
                        index += 1
                    iuvs_dict["periapse" + str(periapse_num)][
                        "temperature"
                    ] = temperature
                    iuvs_dict["periapse" + str(periapse_num)][
                        "temperature_unc"
                    ] = temperature_unc

                    # Empty space
                    f.readline()

                    # Read the Scale Heights
                    line = f.readline()
                    scale_height_labels = line[19 : len(line) - 1].strip().split()
                    scale_height = collections.OrderedDict(
                        (x, []) for x in scale_height_labels
                    )
                    scale_height_unc = collections.OrderedDict(
                        (x, []) for x in scale_height_labels
                    )
                    line = f.readline()
                    vals = line[20 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        scale_height[list(scale_height.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[20 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        scale_height_unc[list(scale_height_unc.keys())[index]].append(
                            val
                        )
                        index += 1

                    iuvs_dict["periapse" + str(periapse_num)][
                        "scale_height"
                    ] = scale_height
                    iuvs_dict["periapse" + str(periapse_num)][
                        "scale_height_unc"
                    ] = scale_height_unc

                    # Empty space
                    f.readline()
                    f.readline()

                    # Read in the density
                    line = f.readline()
                    density_labels = line.strip().split()
                    density = collections.OrderedDict((x, []) for x in density_labels)
                    for i in range(0, n_alt_den_bins):
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
                    iuvs_dict["periapse" + str(periapse_num)]["density"] = density

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

                    iuvs_dict["periapse" + str(periapse_num)][
                        "density_sys_unc"
                    ] = density_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density uncertainty
                    density_unc = collections.OrderedDict(
                        (x, []) for x in density_labels
                    )
                    for i in range(0, n_alt_den_bins):
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
                    iuvs_dict["periapse" + str(periapse_num)][
                        "density_sys_unc"
                    ] = density_sys_unc

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

                    iuvs_dict["periapse" + str(periapse_num)]["radiance"] = radiance

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

                    iuvs_dict["periapse" + str(periapse_num)][
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

                    iuvs_dict["periapse" + str(periapse_num)][
                        "radiance_unc"
                    ] = radiance_unc

                elif obs_mode == "OCCULTATION":
                    occ_num += 1
                    line = f.readline()
                    n_alt_den_bins = int(line[19 : len(line) - 1].strip())
                    header["n_alt_den_bins"] = float(n_alt_den_bins)

                    iuvs_dict["occultation" + str(occ_num)] = {}
                    iuvs_dict["occultation" + str(occ_num)].update(header)

                    # Empty space
                    f.readline()

                    # Read the Scale Heights
                    line = f.readline()
                    scale_height_labels = line[19 : len(line) - 1].strip().split()
                    scale_height = collections.OrderedDict(
                        (x, []) for x in scale_height_labels
                    )
                    scale_height_unc = collections.OrderedDict(
                        (x, []) for x in scale_height_labels
                    )
                    line = f.readline()
                    vals = line[20 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        scale_height[list(scale_height.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[20 : len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        scale_height_unc[list(scale_height_unc.keys())[index]].append(
                            val
                        )
                        index += 1

                    iuvs_dict["occultation" + str(occ_num)][
                        "scale_height"
                    ] = scale_height
                    iuvs_dict["occultation" + str(occ_num)][
                        "scale_height_unc"
                    ] = scale_height_unc

                    # Empty space
                    f.readline()
                    f.readline()

                    # Read in the retrieval
                    line = f.readline()
                    retrieval_labels = line.strip().split()
                    retrieval = collections.OrderedDict(
                        (x, []) for x in retrieval_labels
                    )
                    for i in range(0, n_alt_den_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == "-9.9999990E+09":
                                val = float("nan")
                            else:
                                val = float(val)
                            retrieval[list(retrieval.keys())[index]].append(val)
                            index += 1
                    iuvs_dict["occultation" + str(occ_num)]["retrieval"] = retrieval

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the retrieval systematic uncertainty
                    retrieval_sys_unc = collections.OrderedDict(
                        (x, []) for x in retrieval_labels
                    )
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == "-9.9999990E+09":
                            val = float("nan")
                        else:
                            val = float(val)
                        retrieval_sys_unc[list(retrieval.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict["occultation" + str(occ_num)][
                        "retrieval_sys_unc"
                    ] = retrieval_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the retrieval uncertainty
                    retrieval_unc = collections.OrderedDict(
                        (x, []) for x in retrieval_labels
                    )
                    for i in range(0, n_alt_den_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == "-9.9999990E+09":
                                val = float("nan")
                            else:
                                val = float(val)
                            retrieval_unc[list(retrieval.keys())[index]].append(val)
                            index += 1
                    iuvs_dict["occultation" + str(occ_num)][
                        "retrieval_sys_unc"
                    ] = retrieval_sys_unc

            line = f.readline()

    return iuvs_dict



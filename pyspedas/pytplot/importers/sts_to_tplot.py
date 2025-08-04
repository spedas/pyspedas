import os
import datetime
import logging
import numpy as np
import xarray as xr
import pytplot
import copy
import time


def read_column_names(sts_file):
    """
    Opens an STS file and reads the column names and vector names.

    Parameters
    ----------
    sts_file : str
        The full path to the STS file.

    Returns
    -------
    tuple of list of str
        A tuple containing two lists. The first list contains the column names, and the second list contains the vector names.

    Notes
    -----
        The .sts file format is a text file format used by the MAVEN mission.
        It is a simple format that contains a header section with metadata and a data section with the actual data.
        This function reads the header section to extract the column names and vector names of the data section.

    """
    column_names = []
    vec_names = []
    record_object = False
    in_scalar_and_vector_object = False
    in_vector_object = False
    in_scalar_object = False

    with open(sts_file, "r") as f:
        for line in f:
            line = line.split()
            if line == ["OBJECT", "=", "RECORD"]:
                record_object = True
            if record_object:
                if line == ["OBJECT", "=", "VECTOR"]:
                    in_vector_object = True
                    vec_column_names = []
                if line == ["OBJECT", "=", "SCALAR"]:
                    if in_vector_object:
                        in_scalar_and_vector_object = True
                    else:
                        in_scalar_object = True
                if line == ["END_OBJECT"]:
                    if in_scalar_and_vector_object:
                        in_scalar_and_vector_object = False
                    elif in_vector_object:
                        in_vector_object = False
                        column_names.append(vec_column_names)
                    elif in_scalar_object:
                        in_scalar_object = False
                    else:
                        # This is where we exit
                        return column_names, vec_names
                if line[0] == "NAME":
                    if in_vector_object and not in_scalar_and_vector_object:
                        vec_name = line[-1]
                        vec_names.append(vec_name)
                    if in_scalar_and_vector_object:
                        column_name = vec_name + "_" + line[-1]
                        vec_column_names.append(column_name)
                    if in_scalar_object:
                        column_name = line[-1]
                        column_names.append([column_name])
                        vec_names.append(None)


def sts_to_tplot(
    filenames=None,
    prefix="",
    suffix="",
    merge=False,
    notplot=False,
):
    """
    Convert STS files to tplot variables.

    Parameters
    ----------
    filenames : str or list of str, optional
        The full path(s) to the STS file(s). If a single string is provided, it will be treated as a single file path.
        If a list of strings is provided, each string will be treated as a separate file path.
        Default is None.
    prefix : str, optional
        A prefix to be added to the variable names when creating tplot variables.
        Default is an empty string.
    suffix : str, optional
        A suffix to be added to the variable names when creating tplot variables.
        Default is an empty string.
    merge : bool, optional
        If True, then data from 'filenames' will be merged into existing tplot variables.
        If False (default), then data from 'filenames' will overwrite existing tplot variables.
        Data in 'filenames' will always be merged/combined by themselves.
    notplot : bool, optional
        If True, the STS data will be returned as a dictionary without creating tplot variables.
        If False, tplot variables will be created.
        Default is False.

    Returns
    -------
    list of str or dict
        Returns a list of the tplot variables created.
        If notplot is True, a dictionary containing the STS data is returned.

    Notes
    -----
        The .sts file format is a text file format used by the MAVEN mission.
        It is a simple format that contains a header section with metadata and a data section with the actual data.
        This function reads the data section of the STS file and converts it to tplot variables.

    Examples
    --------
        >>> f = ["/maven/data/sci/mag/l2/2015/01/mvn_mag_l2_2015002ss1s_20150102_v01_r01.sts",
                 "/maven/data/sci/mag/l2/2015/01/mvn_mag_l2_2015001ss1s_20150101_v01_r01.sts"]
        >>> vars = sts_to_tplot(filenames=f)
        >>> print(vars)
        ['DDAY', 'OB_N', 'POSN', 'OB_BDPL']
    """

    # Create a dictionary and list in which we'll store STS variable data and variable names, respectively
    start_t = time.time()
    sts_dict = {}  # this dictionary will store the STS headers and data
    stored_variables = []

    if prefix is None:
        prefix = ""
    if suffix is None:
        suffix = ""

    # Code assumes a list of STS files
    if isinstance(filenames, str):
        filenames = [filenames]
    elif isinstance(filenames, list):
        filenames = filenames
    else:
        logging.error("Invalid filenames input.")
        return stored_variables
    filenames.sort()

    for s_file in filenames:
        column_names, vec_names = read_column_names(s_file)
        headers = [
            item for sublist in column_names for item in sublist
        ]  # a list of headers for the data
        with open(s_file, "r") as f:
            lines = f.readlines()
        # In STS files, the beginning of the data starts after the last time 'END_OBJECT' is found
        end_objects = [l for l, line in enumerate(lines) if "END_OBJECT" in line]
        end_headers = end_objects[-1]
        data = lines[end_headers + 1 :]
        data = [
            d.strip().split() for d in data
        ]  # Remove extra spaces, then split on whitespaces
        # Create the STS dictionary
        for h, head in enumerate(headers):
            data_column = [d[h] for d in data]
            if head not in sts_dict:
                # Store the data column in the dictionary
                sts_dict[head] = data_column
            else:
                # If the header already exists, append the data column to the existing data
                sts_dict[head].extend(data_column)

    # At this point we read all the files and have the data in the sts_dict dictionary

    # We need to create datetime objects from the sts_dict's year, doy, hour, min, sec, and msec data
    year = sts_dict["TIME_YEAR"]
    doy = sts_dict["TIME_DOY"]
    hour = sts_dict["TIME_HOUR"]
    min = sts_dict["TIME_MIN"]
    sec = sts_dict["TIME_SEC"]
    msec = sts_dict["TIME_MSEC"]

    dtimes = [
        datetime.datetime(
            int(yr),
            1,
            1,
            int(hr),
            int(mn),
            int(s),
            int(ms) * 1000,
            tzinfo=datetime.timezone.utc,
        )
        + datetime.timedelta(int(dy) - 1)
        for yr, dy, hr, mn, s, ms in zip(year, doy, hour, min, sec, msec)
    ]

    sts_dict["time_unix"] = [dt.timestamp() for dt in dtimes]
    # These keys are no longer necessary, remove them
    remove_time_keys = [
        "TIME_YEAR",
        "TIME_DOY",
        "TIME_HOUR",
        "TIME_MIN",
        "TIME_SEC",
        "TIME_MSEC",
    ]
    for key in remove_time_keys:
        try:
            sts_dict.pop(key)
        except KeyError:
            logging.info("Key {} was not found".format(key))

    # Don't create tplot vars if that's not what's desired
    if notplot:
        # Return a dictionary of the STS data
        return sts_dict

    # Create tplot variables
    for cn, vn in zip(column_names, vec_names):
        to_merge = False
        var_name = ""
        if vn == "TIME" or cn[0] == "DDAY":
            # We already have a time_unix key in the dictionary
            continue
        if vn is None:
            # Scalar variables
            var_name = prefix + cn[0] + suffix
            var_data = [
                float(c) for c in sts_dict[cn[0]]
            ]  # dict contains strings, convert to floats
        else:
            # Vector variables
            var_name = prefix + vn + suffix
            var_cn = [
                c for c in cn if "RANGE" not in c and "range" not in c
            ]  # do not include RANGE columns
            var_data = [
                [float(sts_dict[c][i]) for c in var_cn]
                for i in range(len(sts_dict[cn[0]]))
            ]  # data has as many dimensions as len(var_cn)

        # Check if we need to merge with existing tplot variables
        if var_name in pytplot.data_quants.keys() and merge:
            prev_data_quant = pytplot.data_quants[var_name]
            to_merge = True

        # Store the new data
        pytplot.store_data(
            var_name,
            data={"x": sts_dict["time_unix"], "y": var_data},
        )
        stored_variables.append(var_name)

        # If merging is needed, merge the new data with the existing data
        if to_merge is True:
            cur_data_quant = pytplot.data_quants[var_name]
            plot_options = copy.deepcopy(pytplot.data_quants[var_name].attrs)
            pytplot.data_quants[var_name] = xr.concat(
                [prev_data_quant, cur_data_quant], dim="time"
            ).sortby("time")
            pytplot.data_quants[var_name].attrs = plot_options

    return stored_variables

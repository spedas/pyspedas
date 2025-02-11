import logging
import os

from .config import CONFIG
from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def month_to_num(month_string):
    """
    Converts a three-letter month abbreviation to its corresponding two-digit number.

    Parameters
    ----------
    month_string : str
        The three-letter month abbreviation (e.g., "JAN", "FEB", etc.).

    Returns
    -------
    str
        The two-digit number corresponding to the month abbreviation.

    Raises
    ------
    ValueError
        If the month string is not a valid abbreviation.

    Examples
    --------
    >>> month_to_num("JAN")
    '01'
    >>> month_to_num("FEB")
    '02'
    """

    month_to_num_dict = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03",
        "APR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12",
    }

    if month_string in month_to_num_dict.keys():
        return month_to_num_dict[month_string]
    else:
        raise ValueError("Month string is not valid")


def orbit_time(begin_orbit, end_orbit=None):
    """
    Calculate the corresponding time range for a given MAVEN orbit number or range of orbit numbers.

    Parameters
    ----------
    begin_orbit : int
        The beginning orbit number.
    end_orbit : int, optional
        The ending orbit number. If not provided, the time range will be calculated for a single orbit.

    Returns
    -------
    list
        A list containing the beginning and ending time in the format [begin_time, end_time].
        If the orbit numbers are not found, [None, None] will be returned.
    """

    toolkit_path = CONFIG["local_data_dir"]
    sep = "/" if is_fsspec_uri(toolkit_path) else os.path.sep
    orbit_files_path = sep.join([toolkit_path, "orbitfiles"])
    orb_file = sep.join([orbit_files_path, "merged_maven_orbits.orb"])
    logging.info("Getting orbit info from file %s", orb_file)
    if is_fsspec_uri(toolkit_path):
        protocol, path = toolkit_path.split("://")
        fs = fsspec.filesystem(protocol)

        fileobj = fs.open(orb_file, "r")
    else:
        fileobj = open(orb_file, "r")

    with fileobj as f:
        if end_orbit is None:
            end_orbit = begin_orbit
        orbit_num = []
        time = []
        f.readline()
        f.readline()
        for line in f:
            line = line[0:28]
            line = line.split(" ")
            line = [x for x in line if x != ""]
            orbit_num.append(int(line[0]))
            time.append(
                line[1] + "-" + month_to_num(line[2]) + "-" + line[3] + "T" + line[4]
            )
        try:
            if orbit_num.index(begin_orbit) > len(time) or orbit_num.index(
                end_orbit
            ) + 1 > len(time):
                logging.warning(
                    "Orbit numbers not found.  Please choose a number between 1 and %s.",
                    orbit_num[-1],
                )
                return [None, None]
            else:
                begin_time = time[orbit_num.index(begin_orbit)]
                end_time = time[orbit_num.index(end_orbit) + 1]
        except ValueError:
            logging.warning('Problem getting begin and end times for orbits %d and %d', begin_orbit, end_orbit+1)
            return [None, None]
    return [begin_time, end_time]

import pathlib
from typing import List, Dict

from pyspedas import time_double

def read_epde_calibration_data(path: pathlib.Path) -> List[Dict]:
    """
    Read ELFIN EPDE calibration data from file and return
    list of parsed calibration datasets.

    Parameters
    ----------
        path : pathlib.Path
            The path to the calibration data file.

    Returns
    ----------
        List of EPDE calibration data parsed from the file.

    """

    def parse_float_line(line: str):
        array_str = line.split(":")[1].strip()
        return [float(f.rstrip(".")) for f in array_str.split(",")]

    lines = []
    with open(path, "r") as f:
        lines = f.readlines()

    date_lines = (i for i, line in enumerate(lines) if line.startswith("Date"))
    calibrations = []
    for i in date_lines:

        date_str = lines[i].split(":")[1].strip()
        gf_str = lines[i+1].split(":")[1].strip()

        cal = {
            "date": time_double(date_str),
            "gf": float(gf_str),
            "overaccumulation_factors": parse_float_line(lines[i+2]),
            "thresh_factors": parse_float_line(lines[i+3]),
            "ch_efficiencies": parse_float_line(lines[i+4]),
            "ebins": parse_float_line(lines[i+5]),
        }

        calibrations.append(cal)

    return calibrations
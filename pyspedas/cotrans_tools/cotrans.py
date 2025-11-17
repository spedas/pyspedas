"""
Coordinate transformations.

Transform from/to the following coordinate systems:
GSE, GSM, SM, GEI, GEO, MAG, J2000

Times are in Unix seconds for consistency.

Notes
-----
This function is similar to cotrans.pro of IDL SPEDAS.
"""

import logging
import numpy as np
import pyspedas
from pyspedas import (
    store_data,
    get_data,
    get_coords,
    set_coords,
    tplot_copy,
)
from pyspedas.cotrans_tools.cotrans_lib import subcotrans


def cotrans(
    name_in=None,
    name_out=None,
    time_in=None,
    data_in=None,
    coord_in=None,
    coord_out=None,
):
    """
    Transform data from coord_in to coord_out.

    Parameters
    ----------
    name_in: str, optional
        Tplot name for input data.
    name_out: str, optional
        Tplot name for output data.
    time_in: list of float, optional
        Time array.
        Ignored if name_in is provided.
    data_in: list of float, optional
        Data in the coord_in system.
        Ignored if name_in is provided.
    coord_in: str
        Name of input coordinate system.
        Valid options: "gse", "gsm", "sm", "gei", "geo", "mag", "j2000"
    coord_out: str
        Name of output coordinate system.
        Valid options: "gse", "gsm", "sm", "gei", "geo", "mag", "j2000"

    Returns
    -------
    Returns 1 for successful completion, 0 for error.
        Fills a new tplot variable with data in the coord_out system.

    np.array
        If name_in and name_out are not provided, returns the transformed data array.
    """
    if coord_out is None:
        logging.error("cotrans error: No output coordinates were provided.")
        return 0

    # Input data may be specified as a bare array rather than a tplot variable
    if name_in is not None:
        var_coord_in = get_coords(name_in)
    else:
        var_coord_in = None

    # If the input coordinate system is supplied as an argument, and the tplot variable has a coordinate system
    # specified in its metadata, check that they match, and if not, log the error and return failure.

    if var_coord_in is not None and coord_in is not None:
        if var_coord_in.lower() != coord_in.lower():
            logging.error(
                f"cotrans error: {name_in} has {var_coord_in.lower()} coordinates, but transform from {coord_in.lower()} was requested."
            )
            return 0

    if coord_in is None:
        coord_in = var_coord_in
        if coord_in is None:
            logging.error("cotrans error: No input coordinates were provided.")
            return 0

    coord_in = coord_in.lower()
    coord_out = coord_out.lower()
    all_coords = ["gse", "gsm", "sm", "gei", "geo", "mag", "j2000"]

    if coord_in not in all_coords:
        logging.error(
            f"cotrans error: Requested input coordinate system {coord_in} not supported."
        )
        return 0
    if coord_out not in all_coords:
        logging.error(
            f"cotrans error: Requested output coordinate system {coord_out} not supported.",
        )
        return 0

    if name_in is not None:
        # If a name_in is provided, use it for data.
        tplot_data = get_data(name_in)
        time_in = tplot_data[0]
        data_in = tplot_data[1]

    if len(data_in[:]) < 1:
        logging.error("cotrans error: Data is empty.")
        return 0

    # Perform coordinate transformation.
    if not isinstance(data_in, np.ndarray) and not isinstance(data_in, list):
        data_in = np.array(data_in)
    if not isinstance(time_in, np.ndarray) and not isinstance(time_in, list):
        time_in = np.array(time_in)

    data_out = subcotrans(time_in, data_in, coord_in, coord_out)

    # If no input or output tplot variable names are provided, return the transformed data.
    if name_in is None and name_out is None:
        return data_out

    # Otherwise, store the data in a tplot variable.
    if name_in is None:
        store_data("cotranstemp", data={"x": time_in, "y": data_in})
        name_in = "cotranstemp"

    # Find the name of the output tplot variable.
    if name_out is None:
        name_out = name_in + "_" + coord_out

    # Save output tplot variable.
    tplot_copy(name_in, name_out)
    pyspedas.tplot_tools.data_quants[name_out].data = data_out

    # We should change an attribute for the coordinate system.
    set_coords(name_out, coord_out.upper())

    # Code to update the legend and axis labels has been moved into cotrans_set_coord().

    logging.info("Output variable: " + name_out)

    return 1

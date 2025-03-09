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
import pytplot
from pytplot import get_coords,set_coords
from pyspedas.cotrans_tools.cotrans_lib import subcotrans


def cotrans(name_in=None, name_out=None, time_in=None, data_in=None,
            coord_in=None, coord_out=None):
    """
    Transform data from coord_in to coord_out.

    Parameters
    ----------
    name_in: str, optional
        Pytplot name for input data.
    name_out: str, optional
        Pytplot name for output data.
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
    Returns 1 for successful completion.
        Fills a new tplot variable with data in the coord_out system.
    """
    if coord_out is None:
        logging.error("cotrans error: No output coordinates were provided.")
        return 0

    # Input data may be specified as a bare array rather than a tplot variable
    if not (name_in is None):
        var_coord_in = get_coords(name_in)
    else:
        var_coord_in = None

    # If the input coordinate system is supplied as an argument, and the tplot variable has a coordinate system
    # specified in its metadata, check that they match, and if not, log the error and return failure.

    if not (var_coord_in is None) and not(coord_in is None):
        if var_coord_in.lower() != coord_in.lower():
            logging.error("cotrans error: " + name_in + " has " +
                          var_coord_in.lower() + " coordinates, but transform from " + coord_in.lower() + " was requested.")
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
        logging.error("cotrans error: Requested input coordinate system %s not supported.",coord_in)
        return 0
    if coord_out not in all_coords:
        logging.error("cotrans error: Requested output coordinate system %s not supported.",coord_out)
        return 0

    if name_in is not None:
        # If a name_in is provided, use it for data.
        tplot_data = pytplot.get_data(name_in)
        time_in = tplot_data[0]
        data_in = tplot_data[1]
    else:
        pytplot.store_data('cotranstemp', data={'x': list(time_in),
                                                'y': list(data_in)})

    if len(data_in[:]) < 1:
        logging.error("cotrans error: Data is empty.")
        return 0

    # Perform coordinate transformation.
    data_out = subcotrans(list(time_in), list(data_in), coord_in, coord_out)

    if name_in is None and name_out is None:
        return data_out

    if name_in is None:
        name_in = 'cotranstemp'

    # Find the name of the output tplot variable.
    if name_out is None:
        name_out = name_in + "_" + coord_out

    # Save output tplot variable.
    pytplot.tplot_copy(name_in, name_out)
    pytplot.data_quants[name_out].data = data_out

    # We should change an attribute for the coordinate system.
    set_coords(name_out, coord_out.upper())

    # Code to update the legend and axis labels has been moved into cotrans_set_coord().

    logging.info("Output variable: " + name_out)

    return 1

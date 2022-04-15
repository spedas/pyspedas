"""
Coordinate transformations.

Transform from/to the following coordinate systems:
GSE, GSM, SM, GEI, GEO, MAG, J2000

Times are in Unix seconds for consistency.

Notes
-----
This function is similar to cotrans.pro of IDL SPEDAS.
"""
import pytplot
from pyspedas.cotrans.cotrans_lib import subcotrans
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord

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
    coord_out: str
        Name of output coordinate system.

    Returns
    -------
    Returns 1 for successful completion.
        Fills a new pytplot variable with data in the coord_out system.
    """
    if coord_out is None:
        print("cotrans error: No output coordinates were provided.")
        return 0

    if coord_in is None:
        coord_in = cotrans_get_coord(name_in)
        if coord_in is None:
            print("cotrans error: No input coordinates were provided.")
            return 0

    coord_in = coord_in.lower()
    coord_out = coord_out.lower()
    all_coords = ["gse", "gsm", "sm", "gei", "geo", "mag", "j2000"]

    if coord_in not in all_coords or coord_out not in all_coords:
        print("cotrans error: Requested coordinate system not supported.")
        return 0

    if name_in is not None:
        # If a name_in is provided, use it for data.
        tplot_data = pytplot.get_data(name_in)
        time_in = tplot_data[0]
        data_in = tplot_data[1]
    else:
        name_in = "cotranstemp"
        pytplot.store_data(name_in, data={'x': list(time_in),
                                          'y': list(data_in)})

    if len(data_in[:]) < 1:
        print("cotrans error: Data is empty.")
        return 0

    # Perform coordinate transformation.
    data_out = subcotrans(list(time_in), list(data_in), coord_in, coord_out)

    # Find the name of the output pytplot variable.
    if name_out is None:
        # If no output tplot name is provided, create one.
        if name_in is None:
            name_out = "data_out_" + coord_out
        else:
            name_out = name_in + "_" + coord_out

    # Save output pytplot variable.
    pytplot.tplot_copy(name_in, name_out)
    pytplot.data_quants[name_out].data = data_out

    # We should change an attribute for the coordinate system.
    cotrans_set_coord(name_out, coord_out.upper())

    # should also update the legend, if it includes the coordinate system
    # for this to work, the coordinate system should be in all upper case
    metadata = pytplot.get_data(name_out, metadata=True)
    if metadata.get('plot_options') is not None:
        if metadata['plot_options'].get('yaxis_opt') is not None:
            if metadata['plot_options']['yaxis_opt'].get('legend_names') is not None:
                legend = metadata['plot_options']['yaxis_opt'].get('legend_names')
                updated_legend = [item.replace(coord_in.upper(), coord_out.upper()) for item in legend]
                metadata['plot_options']['yaxis_opt']['legend_names'] = updated_legend
            if metadata['plot_options']['yaxis_opt'].get('axis_label') is not None:
                ytitle = metadata['plot_options']['yaxis_opt'].get('axis_label')
                metadata['plot_options']['yaxis_opt']['axis_label'] = ytitle.replace(coord_in.upper(), coord_out.upper())

    print("Output variable: " + name_out)

    return 1

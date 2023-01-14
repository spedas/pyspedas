from pytplot import get_data
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord


def cotrans_set_coord(name, coord):
    """
    This function sets the coordinate system of a tplot variable, and updates legend names
    and axis labels if they include the coordinate system.

    Parameters:
        name: str
            name of the tplot variable

        coord: str
            Abbreviated name of the coordinate system (upper case recommended)

    Notes:
        The coordinate system is stored in the variable's metadata at:
            metadata['data_att']['coord_sys']

        See cotrans_get_coord to return the coordinate system

    Returns:
        bool: True/False depending on if the operation was successful
    """

    # check that the variable exists
    data = get_data(name)
    if data is None:
        return False

    metadata = get_data(name, metadata=True)

    # Get the current value of the coordinate system, if present
    coord_in = cotrans_get_coord(name)

    if metadata.get('data_att') is None:
        metadata['data_att'] = {}

    # note: updating the metadata dict directly updates
    # the variable's metadata in memory, so there's 
    # no need to update the variable with store_data
    metadata['data_att'] = {'coord_sys': coord}

    # should also update the legend, if it includes the coordinate system
    # for this to work, the coordinate system should be in all upper case
    if (coord_in is not None) and (metadata.get('plot_options') is not None):
        if metadata['plot_options'].get('yaxis_opt') is not None:
            if metadata['plot_options']['yaxis_opt'].get('legend_names') is not None:
                legend = metadata['plot_options']['yaxis_opt'].get('legend_names')
                updated_legend = [item.replace(coord_in.upper(), coord.upper()) for item in legend]
                metadata['plot_options']['yaxis_opt']['legend_names'] = updated_legend
            if metadata['plot_options']['yaxis_opt'].get('axis_label') is not None:
                ytitle = metadata['plot_options']['yaxis_opt'].get('axis_label')
                metadata['plot_options']['yaxis_opt']['axis_label'] = ytitle.replace(coord_in.upper(),
                                                                                     coord.upper())

    return True

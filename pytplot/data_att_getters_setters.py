import logging
from pytplot import get_data


def get_any(name,tag_name):
    """

    This function returns an arbitrary value from the data_att dictionary of a tplot variable.
    It is intended to be called by other tag-specific getters and setters.

    Parameters:
        name: str
            name of the tplot variable

        tag_name: str
            The name of the attribute to be returned

    Notes:
        The metadata values are stored in the variable's metadata at:
            metadata['data_att'][tag_name]

    Returns:
        Contents of specified tag name in the data_att structure, or None if not present.
    """
    metadata = get_data(name, metadata=True)
    if metadata is None:
        return None

    if metadata.get('data_att'):
        if metadata['data_att'].get(tag_name):
            return metadata['data_att'][tag_name]

    logging.debug('Tag name ' + tag_name + ' not found for variable ' + name)
    return None


def set_any(name, tag_name, tag_value):
    """

    This function sets an arbitrary attribute in the data_att dictionary of a tplot variable.
    It is intended to be called by other tag-specific getters and setters.

    Parameters:
        name: str
            name of the tplot variable

        tag_name: str
            The name of the attribute to be stored

        tag_value: Any
            The value of the attribute to be stored

    Notes:
        The metadata values are stored in the variable's metadata at:
            metadata['data_att'][tag_name]

    Returns:
        Contents of specified tag name in the data_att structure, or None if not present.
    """
    # check that the variable exists
    data = get_data(name)
    if data is None:
        return False

    metadata = get_data(name, metadata=True)

    # note: updating the metadata dict directly updates
    # the variable's metadata in memory, so there's
    # no need to update the variable with store_data

    data_att = metadata.get('data_att')
    if data_att is None:
        metadata['data_att'] = {tag_name:tag_value}
    else:
        data_att[tag_name] = tag_value

    return True


def get_coords(name):
    """

    This function returns the coordinate system of a tplot variable

    Parameters:
        name: str
            name of the tplot variable

    Notes:
        The coordinate system is stored in the variable's metadata at:
            metadata['data_att']['coord_sys']

        See cotrans_set_coord to update the coordinate system

    Returns:
        Coordinate system of the tplot variable
        or
        None if the coordinate system isn't set
    """

    return get_any(name,'coord_sys')

def set_coords(name, coords):
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

        See get_coord to return the coordinate system

    Returns:
        bool: True/False depending on if the operation was successful
    """

    # check that the variable exists
    data = get_data(name)
    if data is None:
        return False

    # Get the current value of the coordinate system, if present
    coord_in = get_coords(name)

    # Set the new coordinate system
    set_any(name,'coord_sys',coords)

    # Update other related metadata fields, if needed
    metadata=get_data(name,metadata=True)

    # should also update the legend, if it includes the coordinate system
    # for this to work, the coordinate system should be in all upper case
    if (coord_in is not None) and (metadata.get('plot_options') is not None):
        if metadata['plot_options'].get('yaxis_opt') is not None:
            if metadata['plot_options']['yaxis_opt'].get('legend_names') is not None:
                legend = metadata['plot_options']['yaxis_opt'].get('legend_names')
                updated_legend = [item.replace(coord_in.upper(), coords.upper()) for item in legend]
                metadata['plot_options']['yaxis_opt']['legend_names'] = updated_legend
            if metadata['plot_options']['yaxis_opt'].get('axis_label') is not None:
                ytitle = metadata['plot_options']['yaxis_opt'].get('axis_label')
                metadata['plot_options']['yaxis_opt']['axis_label'] = ytitle.replace(coord_in.upper(),
                                                                                     coords.upper())
    return True

def get_units(name):
    """

    This function returns the units of a tplot variable

    Parameters:
        name: str
            name of the tplot variable

    Notes:
        The units string is stored in the variable's metadata at:
            metadata['data_att']['units']

        See set_units to update the coordinate system

    Returns:
        Units of the tplot variable
        or
        None if the coordinate system isn't set
    """

    return get_any(name,'units')

def set_units(name, units):
    """
    This function sets the units of a tplot variable, and updates legend names
    and axis labels if they include the units.

    Parameters:
        name: str
            name of the tplot variable

        coord: str
            Units

    Notes:
        The units are stored in the variable's metadata at:
            metadata['data_att']['units']

        See get_units to return the units

    Returns:
        bool: True/False depending on if the operation was successful
    """

    # check that the variable exists
    data = get_data(name)
    if data is None:
        return False

    # Get the current units value, if present
    units_in = get_units(name)

    # Set the new value
    set_any(name,'units',units)

    # Update any other related metadata fields
    metadata = get_data(name, metadata=True)

    # should also update the legend, if it includes the coordinate system
    # for this to work, the coordinate system should be in all upper case
    if (units_in is not None) and (metadata.get('plot_options') is not None):
        if metadata['plot_options'].get('yaxis_opt') is not None:
            if metadata['plot_options']['yaxis_opt'].get('legend_names') is not None:
                legend = metadata['plot_options']['yaxis_opt'].get('legend_names')
                updated_legend = [item.replace(units_in, units) for item in legend]
                metadata['plot_options']['yaxis_opt']['legend_names'] = updated_legend
            if metadata['plot_options']['yaxis_opt'].get('axis_label') is not None:
                ytitle = metadata['plot_options']['yaxis_opt'].get('axis_label')
                metadata['plot_options']['yaxis_opt']['axis_label'] = ytitle.replace(units_in,
                                                                                     units)

    return True

import logging
from pytplot import get_data


def cotrans_get_coord(name):
    '''
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
    '''

    metadata = get_data(name, metadata=True)
    if metadata is None:
        return None

    if metadata.get('data_att'):
        if metadata['data_att'].get('coord_sys'):
            return metadata['data_att']['coord_sys']

    logging.error('Coordinate system not found: ' + name)
    return None

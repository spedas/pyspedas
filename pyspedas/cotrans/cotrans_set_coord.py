
from pytplot import get_data

def cotrans_set_coord(name, coord):
    '''
    This function sets the coordinate system of a tplot variable

    Parameters:
        name: str
            name of the tplot variable

    Notes:
        The coordinate system is stored in the variable's metadata at:
            metadata['data_att']['coord_sys']

        See cotrans_get_coord to return the coordinate system

    Returns:
        bool: True/False depending on if the operation was successful
    '''

    # check that the variable exists
    data = get_data(name)
    if data is None:
        return False

    metadata = get_data(name, metadata=True)

    if metadata.get('data_att') is None:
        metadata['data_att'] = {}

    # note: updating the metadata dict directly updates
    # the variable's metadata in memory, so there's 
    # no need to update the variable with store_data
    metadata['data_att'] = {'coord_sys': coord}
    return True
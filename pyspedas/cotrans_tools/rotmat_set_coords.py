import pyspedas

def rotmat_set_coords(varname:str, in_coords:str, out_coords:str):
    """ Set input and output coordinates on a rotation matrix

    Parameters
    ----------
    varname:str
        Variable name of the rotation matrix
    in_coords:str
        Input coordinates for the vectors to be rotated
    out_coords
        Output coordinates for the vectors to be rotated

    Returns
    -------
    None

    """

    md=pyspedas.get_data(varname, metadata=True)
    data_att = {'input_coord_sys':in_coords, 'output_coord_sys':out_coords}
    md['data_att'] = data_att
    pyspedas.store_data(varname, attr_dict=md)
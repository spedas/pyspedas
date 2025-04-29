import pyspedas
import logging

def rotmat_get_coords(varname:str):
    """ Get input and output coordinates on a rotation matrix

    Parameters
    ----------
    varname:str
        Variable name of the rotation matrix

    Returns
    -------
    (str, str)
    Tuple containing the input and output coordinates (or None if not set)

    """

    md=pyspedas.get_data(varname, metadata=True)
    data_att = md.get('data_att')
    if data_att is None:
        logging.warning(f"Rotation matrix {varname} has no input or output coordinates set")
        return (None, None)
    in_coords = data_att.get('input_coord_sys')
    if in_coords is None:
        logging.warning(f"Rotation matrix {varname} has no input coordinates set")
    out_coords = data_att.get('output_coord_sys')
    if out_coords is None:
        logging.warning(f"Rotation matrix {varname} has no output coordinates set")
    return (in_coords, out_coords)

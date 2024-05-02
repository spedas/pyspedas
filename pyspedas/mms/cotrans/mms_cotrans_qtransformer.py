"""
This module contains the function mms_cotrans_qtransformer, which performs a quaternion rotation on a tplot variable from one coordinate system to another. It does this by recursively rotating through the ECI coordinate system.

The mms_cotrans_qtransformer function takes in four required arguments:

in_name: the name of the tplot variable to be transformed
out_name: the name of the tplot variable to be created with the transformed data
in_coord: the coordinate system of the input data
out_coord: the coordinate system to rotate to
It also takes an optional argument:

probe: the spacecraft probe number (default is '1')
The function returns the name of the output tplot variable.
"""
from pytplot import tplot_copy, get
from .mms_cotrans_qrotate import mms_cotrans_qrotate


def mms_cotrans_qtransformer(in_name, out_name, in_coord, out_coord, probe='1'):
    """
    Support routine for mms_qcotrans; recursively goes from one coordinate system to
    another by going through ECI

    Operates on a single variable/transformation at a time

    Parameters
    -----------
        in_name: str
            Tplot variable to be transformed

        out_name: str
            Tplot variable to be created with the transformed data

        in_coord: str
            Coordinate system of the input data

        out_coord: str
            Coordinate system to rotate to

        probe: str
            Spacecraft probe #

    """

    # Final coordinate system reached
    if in_coord == out_coord:
        if in_name != out_name:
            tplot_copy(in_name, out_name)
        return out_name

    if in_coord == 'eci':
        q_name = 'mms' + probe + '_mec_quat_eci_to_' + out_coord
        q_data = get(q_name)
        if q_data is None:
            return
        mms_cotrans_qrotate(in_name, q_name, out_name, out_coord)
        recursive_in_coord = out_coord
    else:
        q_name = 'mms' + probe + '_mec_quat_eci_to_' + in_coord
        q_data = get(q_name)
        if q_data is None:
            return
        mms_cotrans_qrotate(in_name, q_name, out_name, out_coord, inverse=True)
        recursive_in_coord = 'eci'

    return mms_cotrans_qtransformer(out_name, out_name, recursive_in_coord, out_coord, probe=probe)

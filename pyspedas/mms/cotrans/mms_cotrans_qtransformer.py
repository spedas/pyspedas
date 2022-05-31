from pytplot import tplot_copy
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
        mms_cotrans_qrotate(in_name, q_name, out_name, out_coord)
        recursive_in_coord = out_coord
    else:
        q_name = 'mms' + probe + '_mec_quat_eci_to_' + in_coord
        mms_cotrans_qrotate(in_name, q_name, out_name, out_coord, inverse=True)
        recursive_in_coord = 'eci'

    return mms_cotrans_qtransformer(out_name, out_name, recursive_in_coord, out_coord, probe=probe)
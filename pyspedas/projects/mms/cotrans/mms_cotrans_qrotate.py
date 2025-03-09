"""
This module provides functions for transforming MMS vector fields from one coordinate system to another using quaternion rotation.

To use this module, you will need to install the SpacePy package: pip install spacepy.

The main function of this module is mms_cotrans_qrotate, which performs a quaternion rotation on a tplot variable. The function takes in the names of the input and quaternion tplot variables, the name of the output tplot variable, and the coordinate system for the output data. An optional inverse flag allows the user to use the quaternion conjugate on the quaternion data prior to rotating. If the data and quaternion tplot variables are not the same length, the function will interpolate the data to the quaternion timestamps.
"""
import logging
from pytplot import get_data, store_data, set_coords
from pyspedas import tinterpol


def mms_cotrans_qrotate(in_name, q_name, out_name, out_coord, inverse=False):
    """
    Performs a quaternion rotation on a tplot variable.

    Note: this routine will interpolate the input data to the quaternion
    timestamps if the data aren't the same length as the quaternions

    Parameters
    ----------
        in_name: str
            Tplot variable to be transformed

        q_name: str
            Tplot variable containing the quaternions

        out_name: str
            Tplot variable to be created

        inverse: bool:
            Flag to use the quaternionConjugate on the quaternion data prior to rotating
    """
    try:
        import spacepy.coordinates as coord
    except ImportError:
        logging.error("SpacePy must be installed to use this module.")
        logging.error("Please install it using: pip install spacepy")

    data = get_data(in_name)
    metadata = get_data(in_name, metadata=True)

    q_data = get_data(q_name)

    if data is None:
        logging.error(f"Problem reading input tplot variable: {in_name}")
        return

    if q_data is None:
        logging.error(f"Problem reading quaternion variable: {q_name}")
        return

    if len(data.times) != len(q_data.times):
        logging.info("Interpolating the data to the MEC quaternion time stamps.")
        tinterpol(in_name, q_name)
        data = get_data(in_name + "-itrp")

    if inverse:
        quaternion = coord.quaternionConjugate(q_data.y)
    else:
        quaternion = q_data.y

    out_data = coord.quaternionRotateVector(quaternion, data.y)

    saved = store_data(
        out_name, data={"x": data.times, "y": out_data}, attr_dict=metadata
    )
    if saved:
        set_coords(out_name, out_coord)

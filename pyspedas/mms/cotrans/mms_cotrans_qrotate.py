import logging
from pytplot import get_data, store_data
from pyspedas import cotrans_set_coord, tinterpol

try:
    import spacepy.coordinates as coord
except ImportError:
    logging.error('SpacePy must be installed to use this module.')
    logging.error('Please install it using: pip install spacepy')


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
    data = get_data(in_name)
    metadata = get_data(in_name, metadata=True)

    q_data = get_data(q_name)

    if len(data.times) != len(q_data.times):
        logging.info('Interpolating the data to the MEC quaternion time stamps.')
        tinterpol(in_name, q_name)
        data = get_data(in_name + '-itrp')

    if inverse:
        quaternion = coord.quaternionConjugate(q_data.y)
    else:
        quaternion = q_data.y

    out_data = coord.quaternionRotateVector(quaternion, data.y)

    saved = store_data(out_name, data={'x': data.times, 'y': out_data}, attr_dict=metadata)
    if saved:
        cotrans_set_coord(out_name, out_coord)


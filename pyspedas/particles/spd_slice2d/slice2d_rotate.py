import numpy as np
from .spd_cal_rot import spd_cal_rot


def slice2d_rotate(rotation=None, vectors=None, bfield=None, vbulk=None, sunvec=None):
    """

    """

    # Check for presence of required support data
    req_bfield = ['bv', 'be', 'perp', 'perp2', 'perp_xy', 'perp_xz', 'perp_yz', 'b_exb', 'perp1-perp2']
    req_vbulk = ['bv', 'be', 'xvel', 'perp', 'perp2', 'b_exb', 'perp1-perp2']

    if bfield is None and rotation in req_bfield:
        print('Rotation: ' + rotation + ' requires B-field data')
        return

    if vbulk is None and rotation in req_vbulk:
        print('Rotation: ' + rotation + ' requires bulk velocity data')
        return

    if rotation == 'bv':
        matrix = spd_cal_rot(bfield, vbulk)
    elif rotation == 'be':
        # [B, BxV] (this is the parallel - perp 2 plane)
        matrix = spd_cal_rot(bfield, np.cross(bfield, vbulk))
    elif rotation == 'xy':
        matrix = spd_cal_rot([1, 0, 0], [0, 1, 0])
    elif rotation == 'xz':
        matrix = spd_cal_rot([1, 0, 0], [0, 0, 1])
    elif rotation == 'yz':
        matrix = spd_cal_rot([0, 1, 0], [0, 0, 1])
    elif rotation == 'xvel':
        matrix = spd_cal_rot([1, 0, 0], vbulk)
    elif rotation == 'perp':
        # perp 2 - perp 1 plane; should be: [(BxV)xB, BxV]
        matrix = spd_cal_rot(np.cross(np.cross(bfield, vbulk), bfield), np.cross(bfield, vbulk))
    elif rotation == 'perp1-perp2':
        # perp 1 - perp 2 plane; should be: [BxV, (BxV)xB]
        matrix = spd_cal_rot(np.cross(bfield, vbulk), np.cross(np.cross(bfield, vbulk), bfield))
    elif rotation == 'perp_yz':
        matrix = spd_cal_rot(np.cross(np.cross(bfield, [0, 1, 0]), bfield), np.cross(np.cross(bfield, [0, 0, 1]), bfield))
    elif rotation == 'perp_xy':
        matrix = spd_cal_rot(np.cross(np.cross(bfield, [1, 0, 0]), bfield), np.cross(np.cross(bfield, [0, 1, 0]), bfield))
    elif rotation == 'perp_xz':
        matrix = spd_cal_rot(np.cross(np.cross(bfield, [1, 0, 0]), bfield), np.cross(np.cross(bfield, [0, 0, 1]), bfield))
    elif rotation == 'b_exb':
        # [B, (BxV)xB] (this is the parallel - perp 2 plane)
        matrix = spd_cal_rot(bfield, np.cross(np.cross(bfield, vbulk), bfield))
    else:
        print('Unknown rotation: ' + rotation)
        return

    if rotation != 'xy':
        print('Aligning slice plane to: ' + rotation)

    return {'matrix': matrix, 'vectors': vectors, 'bfield': bfield, 'vbulk': vbulk, 'sunvec': sunvec}

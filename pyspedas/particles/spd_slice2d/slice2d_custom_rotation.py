import numpy as np
from .slice2d_get_support import slice2d_get_support


def slice2d_custom_rotation(custom_rotation=None,
                            trange=None,
                            vectors=None,
                            bfield=None,
                            vbulk=None,
                            sunvec=None,
                            determ_tolerance=1e-6):
    """

    """

    if custom_rotation is None:
        matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        return {'matrix': matrix,
                'vectors': vectors,
                'vbulk': vbulk,
                'bfield': bfield,
                'sunvec': sunvec}

    matrix = slice2d_get_support(custom_rotation, trange, matrix=True)

    print('Applying custom rotation')

    # Transform particle and support vectors
    if vectors is not None:
        vectors = matrix @ vectors
    if vbulk is not None:
        vbulk = matrix @ vbulk
    if bfield is not None:
        bfield = matrix @ bfield
    if sunvec is not None:
        sunvec = matrix @ sunvec

    return {'matrix': matrix,
            'vectors': vectors,
            'vbulk': vbulk,
            'bfield': bfield,
            'sunvec': sunvec}
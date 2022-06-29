import numpy as np


def slice2d_orientslice(vectors=None, vbulk=None, bfield=None, sunvec=None, slice_x=None, slice_z=None):
    """
    Performs transformation into user specified coordinates.
    This transformation is applied after the CUSTOM_ROTATION and ROTATION transformation have been performed.
    """
    if slice_z is None:
        slice_z = np.array([0, 0, 1])

    # normalize
    z = slice_z/np.linalg.norm(slice_z)

    # if the x-axis direction is not specified, use projection
    # of the ordinate closest to the slice plane
    if slice_x is None:
        ordinate = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        angles = (180.0/np.pi)*np.arccos(np.array([np.sum(ordinate[:, 0]*z),
                                                   np.sum(ordinate[:, 1]*z),
                                                   np.sum(ordinate[:, 2]*z)]))

        # use ordinate that is closest to perpendicular with norm
        ind = np.argmin(np.abs(angles-90.0))

        slice_x = ordinate[:, ind]

    # normalize vector used to define slice's x-axis
    xp = slice_x/np.linalg.norm(slice_x)

    # get the slice's y-axis
    y = np.cross(z, xp)

    # get the slice's x-axis
    x = np.cross(y, z)

    # now normalize the x-axis
    x = x/np.linalg.norm(x)

    # get the rotation matrix
    matrix = np.array([x, y, z])

    # Transform particle and support vectors
    if vectors is not None:
        transformed = np.zeros(vectors.shape)
        num_vectors = vectors.shape[0]
        for vector_idx in range(num_vectors):
            transformed[vector_idx] = (matrix.T @ vectors[vector_idx, :]).flatten()
        vectors = transformed
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

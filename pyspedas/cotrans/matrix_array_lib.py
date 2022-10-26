import numpy as np

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum


def ctv_err_test(vals, val, err = 1e-5):
    """ used to determine if values are equal within some standard of computational error """
    return (vals >= val-err) & (vals <= val+err)


def ctv_determ_mats(m):
    """ returns the determinant of a list of 3x3 matrices """
    return np.linalg.det(m)


def ctv_identity_mats(m):
    """
    determines if a list of 3x3 matrices are identity matrices
    will return the indexes of the identity matrices in the list of matrices
    """
    return ctv_err_test(m[:, 0, 0], 1) & ctv_err_test(m[:, 0, 1], 0) & ctv_err_test(m[:, 0, 2], 0) \
        & ctv_err_test(m[:, 1, 0], 0) & ctv_err_test(m[:, 1, 1], 1) & ctv_err_test(m[:, 1, 2], 0) \
        & ctv_err_test(m[:, 2, 0], 0) & ctv_err_test(m[:, 2, 1], 0) & ctv_err_test(m[:, 2, 2], 1)


def ctv_mm_mult(m1, m2):
    """ multiplication of two lists of 3x3 matrices """
    out = np.zeros(m1.shape)
    out[:, 0, 0] = nansum(m1[:, 0, :] * m2[:, :, 0], axis=1)
    out[:, 1, 0] = nansum(m1[:, 1, :] * m2[:, :, 0], axis=1)
    out[:, 2, 0] = nansum(m1[:, 2, :] * m2[:, :, 0], axis=1)
    out[:, 0, 1] = nansum(m1[:, 0, :] * m2[:, :, 1], axis=1)
    out[:, 1, 1] = nansum(m1[:, 1, :] * m2[:, :, 1], axis=1)
    out[:, 2, 1] = nansum(m1[:, 2, :] * m2[:, :, 1], axis=1)
    out[:, 0, 2] = nansum(m1[:, 0, :] * m2[:, :, 2], axis=1)
    out[:, 1, 2] = nansum(m1[:, 1, :] * m2[:, :, 2], axis=1)
    out[:, 2, 2] = nansum(m1[:, 2, :] * m2[:, :, 2], axis=1)
    return out


def ctv_verify_mats(m):
    """
    verifies whether a list of matrices
    contains valid rotation matrices.
    This is determined using 2 constraints.
    #1 Where determ(matrix) eq 1
    #2 Where matrix#transpose(matrix) eq I

    returns 0 if the matrices use a mixed system
    returns 1 if there are no valid mats
    returns 2 if the data are all nans
    returns 3 if there are some invalid mats
    returns 4 if there are some nans
    returns 5 win!
    """
    identity_mats = ctv_identity_mats(ctv_mm_mult(m, np.transpose(m, (0,2,1))))
    # make sure matrix is self-inverting and the determinate is either 1 in all cases or -1 in all cases
    idx = np.argwhere(ctv_err_test(ctv_determ_mats(m),1) & identity_mats)
    c_right = idx.shape[0]
    idx = np.argwhere(ctv_err_test(ctv_determ_mats(m),-1) & identity_mats)
    c_left = idx.shape[0]
    idx = np.argwhere(~np.isfinite(ctv_determ_mats(m)))
    c_nan = idx.shape[0]
    if (c_left != 0) and (c_right != 0): # mixed system
        return 0
    elif (c_left == 0) and (c_right == 0): # all matrices fail
        return 1
    elif c_nan == m.shape[0]: # all nans
        return 2
    elif (c_left+c_right+c_nan < 0): # some matrices fail
        return 3
    elif c_nan != 0: # some nans
        return 4
    else: # all mats are rotation mats and there is no missing data
        return 5


def ctv_left_mats(m):
    """
    Is this a set of left-handed permutation matrices?
    """
    idx = np.argwhere(ctv_err_test(ctv_determ_mats(m),-1))
    c = idx.shape[0]
    if c > 0:
        return 1
    else:
        return 0


def ctv_swap_hands(m):
    """
    Turns a 3x3 matrix with a left-handed basis into a right-handed basis and vice-versa
    """
    out = m.copy()
    out[:,0,:] *= -1
    return out


def ctv_norm_vec_rot(v):
    """
    Helper function
    Calculates the norm of a bunch of vectors simultaneously
    """
    if v is None:
        return -1
    if v.ndim != 2:
        return -1
    return np.sqrt(np.sum(v**2, axis=1))


def ctv_normalize_vec_rot(v):
    """
    Helper function
    Normalizes a bunch of vectors simultaneously
    """
    if v is None:
        return -1
    if v.ndim != 2:
        return -1
    n_a = ctv_norm_vec_rot(v)
    if (n_a.ndim == 0) and (n_a == -1):
        return -1
    v_s = v.shape
    # calculation is pretty straight forward
    # we turn n_a into an N x D so computation can be done element by element
    n_b = np.repeat(n_a, v_s[1]).reshape(v_s)
    return v/n_b


def ctv_mx_vec_rot(m, x):
    """
    Helper function
    Vectorized fx to multiply n matrices by n vectors
    """
    # input checks
    if m is None:
        return -1
    if x is None:
        return -1
    m_s = m.shape
    x_s = x.shape
    # make sure number of dimensions in input arrays is correct
    if len(m_s) != 3:
        return -1
    if len(x_s) != 2:
        return -1
    # make sure dimensions match
    if not np.array_equal(x_s, [m_s[0], m_s[1]]):
        return -1
    if not np.array_equal(m_s, [x_s[0], x_s[1], x_s[1]]):
        return -1
    # calculation is pretty straight forward
    # we turn x into an N x 3 x 3 so computation can be done element by element
    y_t = np.repeat(x, x_s[1]*x_s[1]).reshape(x_s[0], x_s[1], x_s[1])
    # custom multiplication requires rebin to stack vector across rows,
    # not columns
    y_t = np.transpose(y_t, (0, 2, 1))
    # 9 multiplications and 3 additions per matrix
    y = np.sum(y_t*m, axis=2)
    return y


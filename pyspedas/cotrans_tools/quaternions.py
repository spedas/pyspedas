import logging
from copy import deepcopy
import numpy as np
from pyspedas.utilities.interpol import interpol


def qmult(q1, q2):
    """
    multiply two quaternions or two arrays of quaternions

    Parameters
    ----------
    q1 : array_like
        a 4 element array, or an Nx4 element array, representing quaternion(s)
    q2 : array_like
        a 4 element array, or an Nx4 element array, representing quaternion(s)

    Returns
    -------
    q1*q2, or -1 on failure

    Notes
    -----
    Implementation largely copied from the euve c library for quaternions

    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """
    q1i = np.array(q1)
    q2i = np.array(q2)

    if q1i.ndim != q2i.ndim:
        logging.error('Number of dimensions in quaternion q1 and quaternion q2 do not match')
        return -1

    # check to make sure input has the correct dimensions
    q1i = qvalidate(q1i, 'q1', 'qmult')
    q2i = qvalidate(q2i, 'q2', 'qmult')

    if isinstance(q1i, int):
        return q1i

    if isinstance(q2i, int):
        return q2i

    # make sure elements match
    if q1i.size != q2i.size:
        logging.error('Number of elements in quaternion q1 and quaternion q2 do not match')
        return -1

    # now the actual dirty work
    qtmp0 = q1i[:, 0] * q2i[:, 0] - q1i[:, 1] * q2i[:, 1] - q1i[:, 2] * q2i[:, 2] - q1i[:, 3] * q2i[:, 3]
    qtmp1 = q1i[:, 1] * q2i[:, 0] + q1i[:, 0] * q2i[:, 1] - q1i[:, 3] * q2i[:, 2] + q1i[:, 2] * q2i[:, 3]
    qtmp2 = q1i[:, 2] * q2i[:, 0] + q1i[:, 3] * q2i[:, 1] + q1i[:, 0] * q2i[:, 2] - q1i[:, 1] * q2i[:, 3]
    qtmp3 = q1i[:, 3] * q2i[:, 0] - q1i[:, 2] * q2i[:, 1] + q1i[:, 1] * q2i[:, 2] + q1i[:, 0] * q2i[:, 3]

    qout = np.array([qtmp0, qtmp1, qtmp2, qtmp3]).T

    return qout


def qdecompose(q):
    """
    Decompose quaternions into axes and angles

    Parameters
    ----------
    q:  a 4 element quaternion or an Nx4 element array of quaternions


    Returns
    --------
    a 4 element array with a[0] = angle, and a[1:3] = axis, or
    an Nx4 element array or -1L on failure

    Notes
    ------

    Implementation largely copied from the euve c library for quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs
    As per the euve implementation, if q[0] is outside of the range of
    acos...[-1,1] the value of the quaternion will be turned into an
    identity quaternion...in other words clipped, this seems suspect,
    a better solution may be to wrap the value back into range using
    modular arithmatic, future modifiers of this routine should consider
    adding this.

    This routine is based on the IDL version by Patrick Cruce
    """
    EPSILON = 1.0e-20  # Where sin(theta) is close enough to theta
    # this is to avoid mutating the input variable
    qi = q
    # check to make sure input has the correct dimensions
    qi = qvalidate(qi, 'q', 'qdecompose')
    if isinstance(qi, int):
        return qi
    qdims = qi.shape
    aout = np.zeros(qdims, dtype=np.float64)

    # the following code will clip into range
    idx = np.argwhere(qi[:, 0] >= 1.0).flatten()
    if len(idx) != 0:
        aout[idx, 0] = 0.0
        aout[idx, 1] = 1.0
        aout[idx, 2:3] = 0.0

    idx = np.argwhere(qi[:, 0] <= -1.0).flatten()
    if len(idx) != 0:
        aout[idx, 0] = 2 * np.pi
        aout[idx, 1] = 1.0
        aout[idx, 2:3] = 0.0

    idx = np.argwhere((qi[:, 0] > -1.0) & (qi[:, 0] < 1.0)).flatten()
    if len(idx) != 0:
        theta2 = np.arccos(qi[idx, 0])
        aout[idx, 0] = 2 * theta2

        idx2 = np.argwhere(theta2 < EPSILON).flatten()
        if len(idx2) != 0:
            aout[idx[idx2], 1] = 1.0
            aout[idx[idx2], 2:3] = 0.0

        idx2 = np.argwhere(theta2 >= EPSILON).flatten()
        if len(idx2) != 0:
            aout[idx[idx2], 1] = qi[idx[idx2], 1] / np.sin(theta2[idx2])
            aout[idx[idx2], 2] = qi[idx[idx2], 2] / np.sin(theta2[idx2])
            aout[idx[idx2], 3] = qi[idx[idx2], 3] / np.sin(theta2[idx2])

    return aout.reshape(qdims)


def qvalidate(q, argname, fxname):
    """
    Validate inputs for the PySPEDAS quaternion library

    Parameters
    -----------
    q: a 4 element array, or an Nx4 element array, representing quaternion(s)
    argname: the name of the argument to be used in error messages

    Returns
    -------
    str
    an Nx4 array or -1, it will turn 4 element quaternion arrays into 1x4 element quaternion arrays

    Notes
    -----
    This function is here because I noticed a lot of the error
    checking code was being repeated, and it was making the functions
    long and hard to read

    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """
    # this is to avoid mutating the input variable
    qi = deepcopy(q)

    if isinstance(qi, int):
        return -1

    # check to make sure input has the correct dimensions
    elif np.size(np.shape(qi)) == 1:
        if np.size(qi) != 4:
            logging.error('Wrong number of elements in quaternion ' + argname + '. Found when validating input for ' + fxname)
            return -1
        qi = np.reshape(qi, (1, 4))
    elif np.size(np.shape(qi)) == 2:
        s = np.shape(qi)
        if s[np.size(s)-1] != 4:
            logging.error('Dimension 2 of quaternion ' +argname+' must have 4 elements. Found when validating input for ' + fxname)
            return -1
    else:
        logging.error('Quaternion '+argname+' has the wrong number of dimensions. Found when validating input for ' + fxname)
        return -1

    return qi


def qconj(q):
    """
    Calculate the conjugate of a quaternion or an array of quaternions

    Parameters
    ----------

    q: a 4 element array, or an Nx4 element array, representing quaternion(s)

    Returns
    -------

    q*

    Notes
    -----

    Implementation largely copied from the euve c library for
    quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """
    # this is to avoid mutating the input variable
    qi = deepcopy(q)

    # check to make sure input has the correct dimensions
    qi = qvalidate(qi, 'q', 'qconj')

    if isinstance(qi, int):
        return qi

    # the actual conjugation
    qtmp0 = qi[:, 0]
    qtmp1 = -qi[:, 1]
    qtmp2 = -qi[:, 2]
    qtmp3 = -qi[:, 3]

    qout = np.array([qtmp0, qtmp1, qtmp2, qtmp3]).T

    if len(q.shape) == 1:
        qout = qout.flatten()

    return qout


def qslerp(q, x1, x2, geometric=False, eq_tolerance=1e-12):
    """
    Uses spherical linear interpolation to interpolate quaternions between elements of q

    Parameters
    ----------
    q : array_like
        An Nx4 element array, representing a list of quaternions with N > 1, all quaternions must be unit quaternions(ie length/norm = 1)
    x1 : array_like
        The input abscissa values of the quaternions,an array of length N, abscissa values must also be monotonic
    x2 : array_like
        The output abscissa values for the quaternions, can have as many elements as wanted but must fall on the interval [x[0],x[N-1]], an M element array, abscissa values must also be monotonic
    geometric : bool, optional
        This keyword allows you to specify that it use the geometric formula for the slerp. The default formula is probably faster and more numerically stable, the geometric option is just available for testing
        Testing of the geometric method indicates that the norm of the interpolated quaternions strays easily from unit length, when it renormalizes results may be destabilized
    eq_tolerance : float, optional
        Set to specify the tolerance used when determining whether two numbers are equal (default: 1e-12). This tolerance will be used in checking equivalence of:
            -quaternion lengths
            -input vs. output abscissae
            -quaternion direction (inner product)

    Returns
    -------
    q_out : array_like
        An Mx4 element array of interpolated quaternions or -1L on failure

    Notes
    -----
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as an eigenvalue of the rotation the quaterion performs

    The scalar component can be thought of as the amount of rotation that the quaternion performs

    While the code may seem a little esoteric, it is vectorized and provides the most accurate results it can get

    This routine is based on the IDL version by Patrick Cruce
    """
    qi = deepcopy(q)
    x2i = deepcopy(x2)
    x1i = deepcopy(x1)

    # check that quaternions are consistent with generic quaternion invariants
    qi = qvalidate(qi,'qi','qslerp')

    if isinstance(qi, int):
        return qi

    # check that input quaternions are unit length
    qn = qnorm(qi)

    idx = np.argwhere(np.abs(qn - 1.0) > eq_tolerance).flatten()
    if len(idx) > 0:
        logging.error('At least one input quaternion is not unit length')
        return

    if qi.shape[0] != len(x1i):
        logging.error('Number of input abscissa values does not match the number of input quaternions')
        return

    # check that input abscissa values are monotonic
    if len(x1i) > 1:
        idx = np.argwhere((x1i[1:len(x1i)]-x1i[0:len(x1i)-1]) < 0)
        if len(idx) > 0:
            logging.error('input abscissa values not monotonic')
            return

    # check that output abscissa values are strictly monotonic
    if len(x2i) > 1:
        idx = np.argwhere((x2i[1:len(x2i)]-x2i[0:len(x2i)-1]) < 0)
        if len(idx) > 0:
            logging.error('output abscissa values not monotonic')
            return

    # construct the output array
    q_out = np.zeros((len(x2i), 4))

    # if output abscissa values are outside of the range of input abscissa
    # values constant extrapolation is used
    idx = np.argwhere(x2i < x1i[0]).flatten()

    if len(idx) > 0:
        q_out[idx, :] = np.array(idx.size*[qi[0, :]])

    idx = np.argwhere(x2i > x1i[-1]).flatten()

    if len(idx) > 0:
        q_out[idx, :] = np.array(idx.size*[qi[-1, :]])

    out_idx = np.argwhere((x2i >= x1i[0]) & (x2i <= x1i[-1])).flatten()

    if len(out_idx) == 0:
        return q_out.reshape((-1, 4))

    x2i = x2i[out_idx]

    # construct arguments to the slerp function, this includes the source
    # quaternion list, the target quaternions list, and the proportion of
    # interpolation list for each quaternion pair.  They should all have
    # the same number of elements as the output abscissa value list

    t_temp = interpol(np.arange(qi.shape[0], dtype='float64'), x1i, x2i)

    t_list = t_temp % 1.0

    q_idx = np.int64(np.floor(t_temp))

    # if the last abscissa values are identical,the indexing scheme to
    # generate the q_list could generate an overflow, the two conditionals
    # below prevent this
    idx = np.argwhere(np.abs(t_list) <= eq_tolerance).flatten()  # where t_list =~ 0.0
    if len(idx) > 0:
        q_out[out_idx[idx], :] = qi[q_idx[idx], :]

    slerp_idx = np.argwhere(np.abs(t_list) > eq_tolerance).flatten()  # where t_list !=~ 0.0

    # if there is nothing left, then we're done
    if slerp_idx.size == 0:
        return q_out.reshape((-1, 4))

    q_idx = q_idx[slerp_idx]
    out_idx = out_idx[slerp_idx]
    t_list = t_list[slerp_idx]

    q1_list = qi[q_idx, :]

    q2_list = qi[q_idx + 1, :]

    # calculate the dot product which is needed to to flip the
    # appropriate quaternions to guarantee interpolation is done along the
    # shortest path
    dotp = qdotp(q1_list, q2_list)

    if dotp.ndim == 0 and dotp == -1:
        return -1

    # the following code flips quaternions in q2_list to ensure the
    # shortest path is followed
    idx = np.argwhere(dotp < 0.0).flatten()

    if idx.size != 0:
        q2_list[idx, :] = -q2_list[idx, :]

    # interpolation cannot be performed on colinear quaternions
    # it is assumed that colinear quaternions will be returned unchanged
    # since dotp(q1,q2) = cos(angle between q1,q2) if dotp = 1.0 the
    # quaternions are colinear
    idx = np.argwhere(np.abs(dotp - 1.0) <= eq_tolerance).flatten()  # where dotp = 1.0

    # store colinear quaternions into output array
    if idx.size != 0:
        q_out[out_idx[idx], :] = q1_list[idx, :]

    # copy non-colinear quaternions for processing
    idx = np.argwhere(np.abs(dotp - 1.0) > eq_tolerance).flatten()

    if idx.size == 0:
        return q_out.reshape((-1, 4))  # if no non-colinear quaternions are left, we are done

    dotp = dotp[idx]
    t_list = t_list[idx]
    q1_list = q1_list[idx, :]
    q2_list = q2_list[idx, :]
    out_idx = out_idx[idx]

    # now the actual processing begins

    # testing both methods to verify results
    if geometric:
        theta = np.arccos(dotp)

        sin_theta = np.sin(theta)

        theta_t = theta * t_list

        co1 = np.sin(theta - theta_t) / sin_theta
        co2 = np.sin(theta_t) / sin_theta

        q_out[out_idx, 0] = co1 * q1_list[:, 0] + co2 * q2_list[:, 0]
        q_out[out_idx, 1] = co1 * q1_list[:, 1] + co2 * q2_list[:, 1]
        q_out[out_idx, 2] = co1 * q1_list[:, 2] + co2 * q2_list[:, 2]
        q_out[out_idx, 3] = co1 * q1_list[:, 3] + co2 * q2_list[:, 3]
    else:
        # slerp will be performed by calculating:
        # ((q2*(q1^-1))^t)*q1
        # since the quaternions are unit q1^-1 = conjugate(q1)
        # exponentiation can be calculated by transforming to
        # polar form cos(theta*t)+v*sin(theta*t)
        # theta = acos(q[0])
        # NOTE: this potentially more numerically stable implementation needs
        # to be verified by comparison to the geometric slerp
        q1_conj = qconj(q1_list)

        q2_q1_prod = qdecompose(qmult(q2_list, q1_conj))

        if isinstance(q2_q1_prod, int):
            return -1

        # sometimes a dimension disappears.
        if q2_q1_prod.ndim == 1 and q2_q1_prod.size == 4:
            q2_q1_prod = q2_q1_prod.reshape((1, 4))

        theta_scale = q2_q1_prod[:, 0] * t_list

        q_total = qmult(qcompose(q2_q1_prod[:, 1:4], theta_scale), q1_list)

        if isinstance(q_total, int):
            return -1

        q_out[out_idx, :] = q_total

    return qnormalize(q_out)


def qdotp(q1, q2):
    """
    Calculate the dot product of two quaternions or two arrays of quaternions

    Parameters
    ----------

    q1: a 4 element array, or an Nx4 element array, representing quaternion(s)
    q2: a 4 element array, or an Nx4 element array, representing quaternion(s)

    Returns
    -------

    q1.q2, or -1 on failure

    Notes
    -----

    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    The scalar component can be thought of as the amount of rotation that
    the quaternion performs

    like any vector the if t = the angle between q1 and q2 in 4-space
    the q1.q2 = ||q1||*||q2||*cos(t) where || denotes the norm(length) of
    the quaternion in 4-space

    This routine is based on the IDL version by Patrick Cruce
    """
    q1i = deepcopy(q1)
    q2i = deepcopy(q2)
    qout = np.nansum(q1i*q2i, axis=1)
    return qout


def qnorm(q):
    """
    Calculate the norm a quaternion or an array of quaternions

    Parameters
    ----------

    q: a 4 element array, or an Nx4 element array, representing quaternion(s)

    Returns
    -------

    norm(q): sqrt(a^2+b^2+c^2+d^2) or -1L on fail
                      will be a single element or an N length array

    Notes
    -----

    Implementation largely copied from the euve c library for
    quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This implementation of norm does not apply the squareroot sometimes
    applied to a norm.  If required the sqrt can easily be applied by the user

    This routine is based on the IDL version by Patrick Cruce

    """
    qi = deepcopy(q)
    dotp = qdotp(qi, qi)
    return np.sqrt(dotp)


def qnormalize(q):
    """
    Normalize a quaternion or an array of quaternions

    Parameters
    ----------

    q: a 4 element array, or an Nx4 element array, representing quaternion(s)

    Returns
    -------

    q/(sqrt(norm(q))) or -1L on fail

    Notes
    -----

    Implementation largely copied from the euve c library for
    quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """
    qi = deepcopy(q)
    qn = qnorm(qi)

    qtmp0 = qi[:, 0]/qn
    qtmp1 = qi[:, 1]/qn
    qtmp2 = qi[:, 2]/qn
    qtmp3 = qi[:, 3]/qn

    qout = np.array([qtmp0, qtmp1, qtmp2, qtmp3]).transpose()

    idx = np.argwhere(qout[:, 0] > 1.0).flatten()
    if len(idx) > 0:
        qout[idx, 0] = 1.0
        qout[idx, 1:4] = 0.0

    idx = np.argwhere(qout[:, 0] < -1.0).flatten()
    if len(idx) > 0:
        qout[idx, 0] = -1.0
        qout[idx, 1:4] = 0.0

    return qout


def mtoq(m):
    """
    Transform a rotation matrix into a quaternion.
    If the matrix does not perform a rotation, then its behavior may be ill-defined

    WARNING!!!! - this routine does not conform to the wikipedia definition.  see warning for qtom.pro

    Parameters
    ----------
    m: a 3x3 element array or an Nx3x3 element array

    Returns
    -------

    q

    Notes: Implementation largely copied from the euve c library for
    quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """
    mi = deepcopy(m)

    dims = np.shape(mi)

    if len(dims) == 2:
        if dims[0] != 3 or dims[1] != 3:
            logging.error('Wrong dimensions in input matrix')
            return -1

        mi = np.reshape(m, (1, 3, 3))

        dims = [1, dims]

    elif len(dims) == 3:
        if dims[1] != 3 or dims[2] != 3:
            logging.error('Wrong dimensions in input matrix')
            return -1
    else:
        logging.error('Wrong dimensions in input matrix')
        return -1

    qout = np.zeros((dims[0], 4))

    arg = 1.0 + mi[:, 0, 0] + mi[:, 1, 1] + mi[:, 2, 2]

    idx = np.argwhere(arg < 0.0)

    if len(idx) != 0:
        arg[idx] = 0.0

    qout[:, 0] = 0.5 * np.sqrt(arg)

    arg = 1.0 + mi[:, 0, 0] - mi[:, 1, 1] - mi[:, 2, 2]

    idx = np.argwhere(arg < 0.0)

    if len(idx) != 0:
        arg[idx] = 0.0

    qout[:, 1] = 0.5 * np.sqrt(arg)

    arg = 1.0 - mi[:, 0, 0] + mi[:, 1, 1] - mi[:, 2, 2]

    idx = np.argwhere(arg < 0.0)

    if len(idx) != 0:
        arg[idx] = 0.0

    qout[:, 2] = 0.5 * np.sqrt(arg)

    arg = 1.0 - mi[:, 0, 0] - mi[:, 1, 1] + mi[:, 2, 2]

    idx = np.argwhere(arg < 0.0)

    if len(idx) != 0:
        arg[idx] = 0.0

    qout[:, 3] = 0.5 * np.sqrt(arg)

    imax = np.zeros(dims[0], dtype=int)
    dmax = np.zeros(dims[0])

    for i in range(4):
        idx = np.argwhere(np.abs(qout[:, i]) > dmax)
        if len(idx) != 0:
            imax[idx] = i
            dmax[idx] = qout[idx, i]

    idx = np.argwhere(imax == 0)

    if len(idx) != 0:
        qout[idx, 1] = (mi[idx, 2, 1] - mi[idx, 1, 2]) / (4 * qout[idx, 0])
        qout[idx, 2] = (mi[idx, 0, 2] - mi[idx, 2, 0]) / (4 * qout[idx, 0])
        qout[idx, 3] = (mi[idx, 1, 0] - mi[idx, 0, 1]) / (4 * qout[idx, 0])

    idx = np.argwhere(imax == 1)

    if len(idx) != 0:
        qout[idx, 2] = (mi[idx, 1, 0] + mi[idx, 0, 1]) / (4 * qout[idx, 1])
        qout[idx, 3] = (mi[idx, 2, 0] + mi[idx, 0, 2]) / (4 * qout[idx, 1])
        qout[idx, 0] = (mi[idx, 2, 1] - mi[idx, 1, 2]) / (4 * qout[idx, 1])

    idx = np.argwhere(imax == 2)

    if len(idx) != 0:
        qout[idx, 3] = (m[idx, 2, 1] + m[idx, 1, 2]) / (4 * qout[idx, 2])
        qout[idx, 0] = (m[idx, 0, 2] - m[idx, 2, 0]) / (4 * qout[idx, 2])
        qout[idx, 1] = (m[idx, 1, 0] + m[idx, 0, 1]) / (4 * qout[idx, 2])

    idx = np.argwhere(imax == 3)

    if len(idx) != 0:
        qout[idx, 0] = (mi[idx, 1, 0] - mi[idx, 0, 1]) / (4 * qout[idx, 3])
        qout[idx, 1] = (mi[idx, 2, 0] + mi[idx, 0, 2]) / (4 * qout[idx, 3])
        qout[idx, 2] = (mi[idx, 2, 1] + mi[idx, 1, 2]) / (4 * qout[idx, 3])

    idx = np.argwhere(qout[:, 0] < 0.0)

    if len(idx) != 0:
        qout[idx, :] = -qout[idx, :]

    qret = qnormalize(qout)

    return np.reshape(qret, (dims[0], 4))


def qtom(qi):
    """
    Transforms quaternions into rotation matrices

    WARNING!!! It appears that this routine returns the transpose (inverse) of the rotation matrix!
    It differs from the CSPICE library and Wikipedia

    Parameters
    ----------

    qi: a 4 element array representing a quaternion or a Nx4 element array representing an array of quaternions

    Returns
    -------

    a 3x3 matrix or Nx3x3 array

    Notes
    -----

    Implementation largely copied from the euve c library for
    quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """

    if isinstance(qi, int):
        return -1

    e00 = qi[:, 0] * qi[:, 0]
    e11 = qi[:, 1] * qi[:, 1]
    e22 = qi[:, 2] * qi[:, 2]
    e33 = qi[:, 3] * qi[:, 3]
    e01 = 2 * qi[:, 0] * qi[:, 1]
    e02 = 2 * qi[:, 0] * qi[:, 2]
    e03 = 2 * qi[:, 0] * qi[:, 3]
    e12 = 2 * qi[:, 1] * qi[:, 2]
    e13 = 2 * qi[:, 1] * qi[:, 3]
    e23 = 2 * qi[:, 2] * qi[:, 3]

    mout = np.zeros((len(e00), 3, 3))

    mout[:, 0, 0] = e00 + e11 - e22 - e33
    mout[:, 1, 0] = e12 + e03
    mout[:, 2, 0] = e13 - e02
    mout[:, 0, 1] = e12 - e03
    mout[:, 1, 1] = e00 - e11 + e22 - e33
    mout[:, 2, 1] = e23 + e01
    mout[:, 1, 2] = e23 - e01
    mout[:, 0, 2] = e13 + e02
    mout[:, 2, 2] = e00 - e11 - e22 + e33

    return mout


def qcompose(vec, theta, free=True):
    """
    Compose quaternions from rotation axis vectors and rotation angles

    Parameters
    ----------

    vec: 3 element array or an Nx3 element array
    theta: an angle or an N element array of angles(in radians)
    free: Flag to allow thetas outside [0,pi)

    Returns
    -------

    a 4 element quaternion or an Nx4 element array of quaternions

    Notes
    -----

    Implementation largely copied from the euve c library for
    quaternions
    Represention has::

        q[0] = scalar component
        q[1] = vector x
        q[2] = vector y
        q[3] = vector z

    The vector component of the quaternion can also be thought of as
    an eigenvalue of the rotation the quaterion performs

    This routine is based on the IDL version by Patrick Cruce
    """

    # Constant indicating where sin(theta) is close enough to theta
    epsilon = 1.0e-20

    vi = deepcopy(vec)
    thi = deepcopy(theta)

    # this next block of code moves angles into the range [0,PI)
    if not free:
        thi = thi % np.pi

        idx = np.argwhere(thi < 0)

        if len(idx) > 1:
            thi[idx] += np.pi

    # calculate the vector norm
    norm = np.sqrt(np.nansum(vi*vi, axis=1))

    # decide which quaternions become identity vectors
    idx1 = np.argwhere(norm < epsilon).flatten()
    idx2 = np.argwhere(norm >= epsilon).flatten()

    out_arr = np.zeros((len(norm), 4))

    if len(idx1) > 0:
        out_arr[idx1, 0] = 1.0
        out_arr[idx1, 1:4] = 0.0

    if len(idx2) > 0:
        out_arr[idx2, 0] = np.cos(thi[idx2]/2.0)

        stheta2 = np.sin(thi[idx2]/2.0)

        out_arr[idx2, 1] = (stheta2 * vi[idx2, 0])/norm[idx2]
        out_arr[idx2, 2] = (stheta2 * vi[idx2, 1])/norm[idx2]
        out_arr[idx2, 3] = (stheta2 * vi[idx2, 2])/norm[idx2]

    return out_arr

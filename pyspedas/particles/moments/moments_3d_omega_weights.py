import numpy as np


def moments_3d_omega_weights(theta, phi, dtheta, dphi):
    """
    Helper function used by moments_3d

    Parameters
    ----------
        theta: numpy.ndarray
            theta bin values

        phi: numpy.ndarray
            phi bin values

        dtheta: numpy.ndarray
            Widths of the theta bins
            
        dphi: numpy.ndarray
            Widths of the phi bins

    Note
    ----
        The calculations were heisted from Davin Larson's IDL SPEDAS version

    Returns
    -------
    ndarray
        Omega weights to be used in moments_3d

    """

    omega = np.zeros([13, theta.shape[0], theta.shape[1]])

    # Angular moment integrals
    ph2 = phi + dphi/2.0
    ph1 = phi - dphi/2.0
    th2 = theta + dtheta/2.0
    th1 = theta - dtheta/2.0

    sth1 = np.sin(th1*np.pi/180.0)
    cth1 = np.cos(th1*np.pi/180.0)
    sph1 = np.sin(ph1*np.pi/180.0)
    cph1 = np.cos(ph1*np.pi/180.0)

    sth2 = np.sin(th2*np.pi/180.0)
    cth2 = np.cos(th2*np.pi/180.0)
    sph2 = np.sin(ph2*np.pi/180.0)
    cph2 = np.cos(ph2*np.pi/180.0)

    ip = dphi*np.pi/180.0
    ict = sth2 - sth1
    icp = sph2 - sph1
    isp = -cph2 + cph1
    is2p = dphi/2.0*np.pi/180.0 - sph2*cph2/2.0 + sph1*cph1/2.0
    ic2p = dphi/2.0*np.pi/180.0 + sph2*cph2/2.0 - sph1*cph1/2.0
    ic2t = dtheta/2.0*np.pi/180.0 + sth2*cth2/2.0 - sth1*cth1/2.0
    ic3t = sth2 - sth1 - (sth2**3 - sth1**3)/3.0
    ictst = (sth2**2 - sth1**2)/2.0
    icts2t = (sth2**3 - sth1**3)/3.0
    ic2tst = (-cth2**3 + cth1**3)/3.0
    icpsp = (sph2**2 - sph1**2)/2.0

    omega[0, :, :] = ict*ip
    omega[1, :, :] = ic2t*icp
    omega[2, :, :] = ic2t*isp
    omega[3, :, :] = ictst*ip
    omega[4, :, :] = ic3t*ic2p
    omega[5, :, :] = ic3t*is2p
    omega[6, :, :] = icts2t*ip
    omega[7, :, :] = ic3t*icpsp
    omega[8, :, :] = ic2tst*icp
    omega[9, :, :] = ic2tst*isp
    omega[10, :, :] = omega[1, :, :]
    omega[11, :, :] = omega[2, :, :]
    omega[12, :, :] = omega[3, :, :]

    return omega

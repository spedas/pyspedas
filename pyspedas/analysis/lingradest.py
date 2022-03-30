import numpy as np

def lingradest(Bx1, Bx2, Bx3, Bx4,
               By1, By2, By3, By4,
               Bz1, Bz2, Bz3, Bz4,
               R1, R2, R3, R4):
    """
    Calculate magnetic field gradients, divergence, curl, and field line
    curvature from 4-point observations

    Input
    ------
        B-field components: np.ndarrays
            Components of the B-field from the four probes

        Coordinates: np.ndarrays
            Position vectors for the four probes

    Method used
    ------------
        Linear Gradient/Curl Estimator technique
        see Chanteur, ISSI, 1998, Ch. 11

    Notes
    ------
        Based on the IDL version (lingradest.pro), which was
        originally designed for Cluster by A. Runov (2003)

    Returns
    --------
        Dict containing:
            Bxbc, Bybc, Bzbc, Bbc
            LGBx, LGBy, LGBz,
            LCxB, LCyB, LCzB, LD,
            curv_x_B, curv_y_B, curv_z_B, RcurvB
    """

    datarrLength = len(Bx1)

    if len(Bx1) != datarrLength or len(Bx2) != datarrLength or len(Bx3) != datarrLength or len(Bx4) != datarrLength or \
        len(By1) != datarrLength or len(By2) != datarrLength or len(By3) != datarrLength or len(By4) != datarrLength or \
        len(Bz1) != datarrLength or len(Bz2) != datarrLength or len(Bz3) != datarrLength or len(Bz4) != datarrLength or \
        R1.shape[0] != datarrLength or R2.shape[0] != datarrLength or R3.shape[0] != datarrLength or R4.shape[0] != datarrLength:
            print('Problem with input sizes; all input data should be interpolated to the same time stamps')
            return

    Rb = np.zeros((datarrLength, 3))
    dR1 = np.zeros((datarrLength, 3))
    dR2 = np.zeros((datarrLength, 3))
    dR3 = np.zeros((datarrLength, 3))
    dR4 = np.zeros((datarrLength, 3))
    k1 = np.zeros((datarrLength, 3))
    k2 = np.zeros((datarrLength, 3))
    k3 = np.zeros((datarrLength, 3))
    k4 = np.zeros((datarrLength, 3))
    mu1 = np.zeros(datarrLength)
    mu2 = np.zeros(datarrLength)
    mu3 = np.zeros(datarrLength)
    mu4 = np.zeros(datarrLength)
    Bxbc = np.zeros(datarrLength)
    Bybc = np.zeros(datarrLength)
    Bzbc = np.zeros(datarrLength)
    Bbc = np.zeros(datarrLength)
    LGBx = np.zeros((datarrLength, 3)) # Linear Gradient B estimator
    LGBy = np.zeros((datarrLength, 3))
    LGBz = np.zeros((datarrLength, 3))
    LCxB = np.zeros(datarrLength) # Linear Curl B estimator
    LCyB = np.zeros(datarrLength)
    LCzB = np.zeros(datarrLength)
    LD = np.zeros(datarrLength)
    curv_x_B = np.zeros(datarrLength)
    curv_y_B = np.zeros(datarrLength)
    curv_z_B = np.zeros(datarrLength)
    curvB = np.zeros(datarrLength)
    RcurvB = np.zeros(datarrLength)
    B_cross_R_x = np.zeros(datarrLength)
    B_cross_R_y = np.zeros(datarrLength)
    B_cross_R_z = np.zeros(datarrLength)
    B_cross_R = np.zeros(datarrLength)
    Ncurv_x = np.zeros(datarrLength)
    Ncurv_y = np.zeros(datarrLength)
    Ncurv_z = np.zeros(datarrLength)

    # distances in 1000 km!
    r12 = (R2-R1)/1000.0
    r13 = (R3-R1)/1000.0
    r14 = (R4-R1)/1000.0
    r21 = (R1-R2)/1000.0
    r23 = (R3-R2)/1000.0
    r24 = (R4-R2)/1000.0
    r31 = (R1-R3)/1000.0
    r32 = (R2-R3)/1000.0
    r34 = (R4-R3)/1000.0
    r41 = (R1-R4)/1000.0
    r42 = (R2-R4)/1000.0
    r43 = (R3-R4)/1000.0

    for i in range(datarrLength):
        # Tetrahedrom mesocentre coordinates
        Rb[i, 0] = 0.25 * (R1[i, 0] + R2[i, 0] + R3[i, 0] + R4[i, 0])
        Rb[i, 1] = 0.25 * (R1[i, 1] + R2[i, 1] + R3[i, 1] + R4[i, 1])
        Rb[i, 2] = 0.25 * (R1[i, 2] + R2[i, 2] + R3[i, 2] + R4[i, 2])

        # Difference in 1000 km!
        dR1[i, 0:3] = (Rb[i, 0:3] - R1[i, 0:3]) / 1000.0
        dR2[i, 0:3] = (Rb[i, 0:3] - R2[i, 0:3]) / 1000.0
        dR3[i, 0:3] = (Rb[i, 0:3] - R3[i, 0:3]) / 1000.0
        dR4[i, 0:3] = (Rb[i, 0:3] - R4[i, 0:3]) / 1000.0

        k1[i, 0:3] = np.cross(r23[i, 0:3], r24[i, 0:3])
        k1[i, 0:3] = k1[i, 0:3] / (r21[i, 0] * k1[i, 0] + r21[i, 1] * k1[i, 1] + r21[i, 2] * k1[i, 2])
        k2[i, 0:3] = np.cross(r34[i, 0:3], r31[i, 0:3])
        k2[i, 0:3] = k2[i, 0:3] / (r32[i, 0] * k2[i, 0] + r32[i, 1] * k2[i, 1] + r32[i, 2] * k2[i, 2])
        k3[i, 0:3] = np.cross(r41[i, 0:3], r42[i, 0:3])
        k3[i, 0:3] = k3[i, 0:3] / (r43[i, 0] * k3[i, 0] + r43[i, 1] * k3[i, 1] + r43[i, 2] * k3[i, 2])
        k4[i, 0:3] = np.cross(r12[i, 0:3], r13[i, 0:3])
        k4[i, 0:3] = k4[i, 0:3] / (r14[i, 0] * k4[i, 0] + r14[i, 1] * k4[i, 1] + r14[i, 2] * k4[i, 2])

        mu1[i] = 1. + (k1[i, 0] * dR1[i, 0] + k1[i, 1] * dR1[i, 1] + k1[i, 2] * dR1[i, 2])
        mu2[i] = 1. + (k2[i, 0] * dR2[i, 0] + k2[i, 1] * dR2[i, 1] + k2[i, 2] * dR2[i, 2])
        mu3[i] = 1. + (k3[i, 0] * dR3[i, 0] + k3[i, 1] * dR3[i, 1] + k3[i, 2] * dR3[i, 2])
        mu4[i] = 1. + (k4[i, 0] * dR4[i, 0] + k4[i, 1] * dR4[i, 1] + k4[i, 2] * dR4[i, 2])

        # Magnetic field in the barycentre
        Bxbc[i] = mu1[i] * Bx1[i] + mu2[i] * Bx2[i] + mu3[i] * Bx3[i] + mu4[i] * Bx4[i]
        Bybc[i] = mu1[i] * By1[i] + mu2[i] * By2[i] + mu3[i] * By3[i] + mu4[i] * By4[i]
        Bzbc[i] = mu1[i] * Bz1[i] + mu2[i] * Bz2[i] + mu3[i] * Bz3[i] + mu4[i] * Bz4[i]
        Bbc[i] = np.sqrt(Bxbc[i]**2 + Bybc[i]**2 + Bzbc[i]**2)

        LGBx[i, 0:3] = Bx1[i] * k1[i, 0:3] + Bx2[i] * k2[i, 0:3] + Bx3[i] * k3[i, 0:3] + Bx4[i] * k4[i, 0:3]
        LGBy[i, 0:3] = By1[i] * k1[i, 0:3] + By2[i] * k2[i, 0:3] + By3[i] * k3[i, 0:3] + By4[i] * k4[i, 0:3]
        LGBz[i, 0:3] = Bz1[i] * k1[i, 0:3] + Bz2[i] * k2[i, 0:3] + Bz3[i] * k3[i, 0:3] + Bz4[i] * k4[i, 0:3]

        # Divergence B
        LD[i] = Bx1[i] * k1[i, 0] + By1[i] * k1[i, 1] + Bz1[i] * k1[i, 2] + \
                Bx2[i] * k2[i, 0] + By2[i] * k2[i, 1] + Bz2[i] * k2[i, 2] + \
                Bx3[i] * k3[i, 0] + By3[i] * k3[i, 1] + Bz3[i] * k3[i, 2] + \
                Bx4[i] * k4[i, 0] + By4[i] * k4[i, 1] + Bz4[i] * k4[i, 2]

        LCxB[i] = (k1[i, 1] * Bz1[i] - k1[i, 2] * By1[i]) + (k2[i, 1] * Bz2[i] - k2[i, 2] * By2[i]) + \
                  (k3[i, 1] * Bz3[i] - k3[i, 2] * By3[i]) + (k4[i, 1] * Bz4[i] - k4[i, 2] * By4[i])
        LCyB[i] = (k1[i, 2] * Bx1[i] - k1[i, 0] * Bz1[i]) + (k2[i, 2] * Bx2[i] - k2[i, 0] * Bz2[i]) + \
                  (k3[i, 2] * Bx3[i] - k3[i, 0] * Bz3[i]) + (k4[i, 2] * Bx4[i] - k4[i, 0] * Bz4[i])
        LCzB[i] = (k1[i, 0] * By1[i] - k1[i, 1] * Bx1[i]) + (k2[i, 0] * By2[i] - k2[i, 1] * Bx2[i]) + \
                  (k3[i, 0] * By3[i] - k3[i, 1] * Bx3[i]) + (k4[i, 0] * By4[i] - k4[i, 1] * Bx4[i])

        curv_x_B[i] = (Bxbc[i] * LGBx[i, 0] + Bybc[i] * LGBx[i, 1] + Bzbc[i] * LGBx[i, 2]) / (Bbc[i] * Bbc[i])
        curv_y_B[i] = (Bxbc[i] * LGBy[i, 0] + Bybc[i] * LGBy[i, 1] + Bzbc[i] * LGBy[i, 2]) / (Bbc[i] * Bbc[i])
        curv_z_B[i] = (Bxbc[i] * LGBz[i, 0] + Bybc[i] * LGBz[i, 1] + Bzbc[i] * LGBz[i, 2]) / (Bbc[i] * Bbc[i])

        curvB[i] = np.sqrt(curv_x_B[i] * curv_x_B[i] + curv_y_B[i] * curv_y_B[i] + curv_z_B[i] * curv_z_B[i])

        RcurvB[i] = curvB[i]**(-1)

    print('Calculations completed')

    return {'Bxbc': Bxbc, 'Bybc': Bybc, 'Bzbc': Bzbc, 'Bbc': Bbc,
            'LGBx': LGBx, 'LGBy': LGBy, 'LGBz': LGBz,
            'LCxB': LCxB, 'LCyB': LCyB, 'LCzB': LCzB, 'LD': LD,
            'curv_x_B': curv_x_B, 'curv_y_B': curv_y_B, 'curv_z_B': curv_z_B, 'RcurvB': RcurvB}

import numpy as np
from pyspedas.utilities.interpol import interpol

def gsm2lmn(times, Rxyz, Bxyz, swdata=None):
    '''
    Transforms vector field from GSM to LMN (boundary-normal) coordinate
    system for the magnetopause using the Shue et al. (1998) magnetopause model


    '''

    if swdata is None:
        # swdata is an array containing: [SW times, SW dynamic pressure, SW B-field]
        swdata = np.zeros((len(times), 3))
        swdata[:, 0] = times
        swdata[:, 1] = 2.088 # nPa
    else:
        timessw = swdata[:, 0]
        dparr = swdata[:, 1]
        bzarr = swdata[:, 2]
        # replace NaNs with a standard value
        for nanval in np.argwhere(np.isnan(dparr)):
            dparr[nanval[0]] = 2.088 # nPa
        for nanval in np.argwhere(np.isnan(bzarr)):
            bzarr[nanval[0]] = 0 # nT

        # interpolate (linear) the data from the SW times to the B-field times
        dparra = interpol(dparr, timessw, times)
        bzarra = interpol(bzarr, timessw, times)
        swdata = np.zeros((len(times), 3))
        swdata[:, 0] = times
        swdata[:, 1] = dparra
        swdata[:, 2] = bzarra

    Blmn = np.zeros((len(times), len(Bxyz[0, :])))

    # start the transformation
    # mostly heisted from the IDL version
    for i in np.arange(len(times)):
        bz = swdata[i, 2]
        dp = max(swdata[i, 1], 0.01)
        x = Rxyz[i, 0]
        y = Rxyz[i, 1]
        z = Rxyz[i, 2]

        alpha = (0.58 - 0.007*bz)*(1 + 0.024*np.log(dp))
        theta = np.arccos(x/np.sqrt(x**2+y**2+z**2))
        rho = np.sqrt(y**2+z**2)

        if rho > 0:
            tang1 = np.array([0.0, z, -y])
            tang2 = np.array([value*alpha*np.sin(theta)/(1+np.cos(theta)) for value in [x, y, z]]) + np.array([-rho**2/rho, x*y/rho, x*z/rho])
            tang1 = [value/np.sqrt(np.sum(np.square(tang1))) for value in tang1]
            tang2 = [value/np.sqrt(np.sum(np.square(tang2))) for value in tang2]

            dN = np.cross(tang1, tang2)
            dM = np.cross(dN, [0, 0, 1])
            dM = dM/np.sqrt(np.sum(np.square(dM)))
            dL = np.cross(dM, dN)
        else:
            dN = [1., 0., 0.]
            dM = [0., 1., 0.]
            dL = [0., 0., 1.]

        transm = np.array([dL, dM, dN])
        Blmn[i, :] = np.matmul(transm, Bxyz[i, :])

    return Blmn
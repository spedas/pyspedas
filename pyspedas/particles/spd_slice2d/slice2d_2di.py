import numpy as np
import scipy.interpolate
import scipy.spatial


def slice2d_2di(datapoints, xyz, resolution, thetarange=None, zdirrange=None):
    """
    Produces slice by interpolating projected data. Based on spd_slice2d_2di in IDL
    """

    # cut by theta value
    if thetarange is not None:
        thetarange = [np.nanmin(thetarange), np.nanmax(thetarange)]

        r = np.sqrt(xyz[:, 0]**2 + xyz[:, 1]**2 + xyz[:, 2]**2)
        eachangle = np.arcsin(xyz[:, 2]/r)*180.0/np.pi

        index = np.argwhere((eachangle <= thetarange[1]) & (eachangle >= thetarange[0])).flatten()

        if len(index) != 0:
            if len(index) != len(r):
                xyz = xyz[index, :]
                datapoints = datapoints[index]

    # cut by z-axis value
    if zdirrange is not None:
        zdirrange = [np.nanmin(zdirrange), np.nanmax(zdirrange)]

        index = np.argwhere((xyz[:, 2] >= zdirrange[0]) & (xyz[:, 2] <= zdirrange[1])).flatten()

        if len(index) != 0:
            if len(index) != len(datapoints):
                xyz = xyz[index, :]
                datapoints = datapoints[index]

    x = xyz[:, 0]
    y = xyz[:, 1]

    # average duplicates along the way
    # note: the following algorithm was translated directly
    # from IDL, and apparently came from thm_esa_slice2d
    # originally
    # uni2 = np.unique(x, return_index=True)[1]+1
    uni2 = np.unique(x, return_index=True)[1]
    uni1 = np.insert(uni2[0:len(uni2)-1] + 1, 0, 0)

    kk = 0
    for i in range(0, len(uni2)):
        yi = y[uni1[i]:uni2[i]+1]
        xi = x[uni1[i]:uni2[i]+1]
        datapointsi = datapoints[uni1[i]:uni2[i]+1]

        xi = xi[np.argsort(yi)]
        datapointsi = datapointsi[np.argsort(yi)]
        yi = yi[np.argsort(yi)]

        index2 = np.unique(yi, return_index=True)[1]
        if len(index2) == 1:
            index1 = 0
        else:
            index1 = np.insert(index2[0:len(index2)-1]+1, 0, 0)

        for j in range(0, len(index2)):
            if isinstance(index1, int):
                y[kk] = yi[index1]
                x[kk] = xi[index1]
                if index1 == index2[j]:
                    datapoints[kk] = datapointsi[index1]
                else:
                    datapoints[kk] = np.nanmean(datapointsi[index1:index2[j]+1])
            else:
                y[kk] = yi[index1[j]]
                x[kk] = xi[index1[j]]
                if index1[j] == index2[j]:
                    datapoints[kk] = datapointsi[index1[j]]
                else:
                    datapoints[kk] = np.nanmean(datapointsi[index1[j]:index2[j]+1])
            kk = kk + 1

    y = y[0:kk]
    x = x[0:kk]
    datapoints = datapoints[0:kk]

    xmax = np.nanmax(np.abs(np.array([y, x])))
    xrange = [-1*xmax, xmax]
    xgrid = np.linspace(xrange[0], xrange[1], num=resolution)
    ygrid = np.linspace(xrange[0], xrange[1], num=resolution)
    out = np.zeros((resolution, resolution))
    grid_interpolator = griddata_tri(datapoints, x, y)
    for xi, xp in enumerate(xgrid):
        for yi, yp in enumerate(ygrid):
            out[xi, yi] = grid_interpolator((xp, yp))

    return {'data': out, 'xgrid': xgrid, 'ygrid': ygrid}


def griddata_tri(data, x, y):
    cart_temp = np.array([x, y])
    points = np.stack(cart_temp).T
    delaunay = scipy.spatial.Delaunay(points)
    return scipy.interpolate.LinearNDInterpolator(delaunay, data)

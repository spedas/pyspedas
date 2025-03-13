import numpy as np


def mpause_t96(pd, xgsm=None, ygsm=None, zgsm=None):
    """
    Calculate the location of the magnetopause using the Tsyganenko 1996 (T96) model.

    Parameters
    ----------
        pd (float):
            Solar wind ram pressure in nanopascals.
        xgsm, ygsm, zgsm  (array-like):
            Coordinates of points in Earth radii (Re) to check whether they are inside or outside the magnetopause.

    Returns
    -------
        xmgnp, ymgnp, zmgnp (array-like):
            Locations of the magnetopause boundary in Earth radii (Re).
        id (array-like):
            Array flagging whether the given points are inside (1), outside (-1), or not checked (np.nan).
        distan (array-like):
            Distance from the given points to the nearest point on the magnetopause boundary.

    Notes
    -----
    The pressure-dependent magnetopause that is used in the T96_01 model
    (TSYGANENKO, JGR, V.100, P.5599, 1995; ESA SP-389, P.181, O;T. 1996)

    Similar to mpause_t96.pro in IDL SPEDAS.
    """

    # Constants defined in the T96 model
    a0 = 70.0
    s00 = 1.08
    x00 = 5.48
    pd0 = 2.0  # Average solar wind ram pressure in nPa

    # Adjust magnetopause parameters according to the actual solar wind pressure
    rat = pd / pd0
    rat16 = rat**0.14
    a = a0 / rat16
    s0 = s00
    x0 = x00 / rat16
    xm = x0 - a

    # Calculate the magnetopause boundary
    n = np.arange(1, 46)
    tau = 1 - 10 ** (-5) * n**3
    xmgnp_half = x0 - a * (1 - s0 * tau)
    arg = (s0**2 - 1) * (1 - tau**2)

    # Ensure argument of sqrt is non-negative
    rhomgnp = a * np.sqrt(np.maximum(arg, 0))
    ymgnp_half = rhomgnp
    xmgnp = np.concatenate([xmgnp_half[::-1], xmgnp_half])
    ymgnp = np.concatenate([-ymgnp_half[::-1], ymgnp_half])
    zmgnp = np.concatenate([-ymgnp_half[::-1], ymgnp_half])

    # Initialize output variables
    id = np.full(len(xgsm), np.nan) if xgsm is not None else None
    distan = np.full(len(xgsm), np.nan) if xgsm is not None else None
    xmp0 = np.full(len(xgsm), np.nan) if xgsm is not None else None
    ymp0 = np.full(len(xgsm), np.nan) if xgsm is not None else None
    zmp0 = np.full(len(xgsm), np.nan) if xgsm is not None else None

    # Flag points inside or outside the magnetopause
    if xgsm is not None and ygsm is not None and zgsm is not None:
        if len(xgsm) != len(ygsm) or len(ygsm) != len(zgsm):
            raise ValueError("Input XGSM, YGSM, ZGSM arrays must have the same length")

        phi = np.arctan2(ygsm, zgsm)
        rho = np.sqrt(ygsm**2 + zgsm**2)

        # Inside magnetosphere
        inside_indices = xgsm < xm
        if inside_indices.any():
            rhomgnp_boundary = a * np.sqrt(s0**2 - 1)
            index1_inside = rho[inside_indices] <= rhomgnp_boundary
            id[inside_indices] = np.where(index1_inside, 1, -1)

            xmp0[inside_indices] = xgsm[inside_indices]
            ymp0[inside_indices] = rhomgnp_boundary * np.sin(phi[inside_indices])
            zmp0[inside_indices] = rhomgnp_boundary * np.cos(phi[inside_indices])
            distan[inside_indices] = np.sqrt(
                (xgsm[inside_indices] - xmp0[inside_indices]) ** 2
                + (ygsm[inside_indices] - ymp0[inside_indices]) ** 2
                + (zgsm[inside_indices] - zmp0[inside_indices]) ** 2
            )

        # Outside magnetosphere
        outside_indices = xgsm >= xm
        if outside_indices.any():
            xksi = (xgsm[outside_indices] - x0) / a + 1.0
            xdzt = rho[outside_indices] / a
            sq1 = np.sqrt((1.0 + xksi) ** 2 + xdzt**2)
            sq2 = np.sqrt((1.0 - xksi) ** 2 + xdzt**2)
            sigma = 0.5 * (sq1 + sq2)
            tau = 0.5 * (sq1 - sq2)
            arg = (s0**2 - 1.0) * (1.0 - tau**2)
            arg[arg < 0] = 0  # Clip negative values to zero
            rhomgnp = a * np.sqrt(arg)

            id[outside_indices] = np.where(sigma >= s0, -1, 1)

            xmp0[outside_indices] = x0 - a * (1.0 - s0 * tau)
            ymp0[outside_indices] = rhomgnp * np.sin(phi[outside_indices])
            zmp0[outside_indices] = rhomgnp * np.cos(phi[outside_indices])
            distan[outside_indices] = np.sqrt(
                (xgsm[outside_indices] - xmp0[outside_indices]) ** 2
                + (ygsm[outside_indices] - ymp0[outside_indices]) ** 2
                + (zgsm[outside_indices] - zmp0[outside_indices]) ** 2
            )

    return xmgnp, ymgnp, zmgnp, id, distan

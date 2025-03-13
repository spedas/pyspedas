import numpy as np


def mpause_2(xmp=None, ymp_west=None, short=False, xmp_max=10.78):
    """
    Calculate the magnetopause (X, Y) locations based on the Fairfield model (JGR, 1971).
    An aberration of 4 degrees is assumed.

    Parameters
    ----------
    xmp (array-like, optional):
        Spacecraft position, x component (defaults to a range if not provided).
    ymp_west (deprecated, unused):
        This parameter is kept for compatibility with the IDL version, but it is unused.
    short (bool, optional):
        If True, the function returns a shorter version of the magnetopause (defaults to False).
    xmp_max (float, optional):
        Maximum value of xmp (defaults to 10.78, the value from the Fairfield paper).

    Returns
    -------

    tuple: A tuple containing two elements:
        xmp (numpy.ndarray): The x coordinates of the magnetopause.
        ymp (numpy.ndarray): The y coordinates of the magnetopause.


    Notes
    -----

    Similar to mpause_2.pro in IDL SPEDAS.

    """

    # Define constants
    xp = -15.
    xmp_min = -300
    npoints = 1000
    aberangle = 4.5  # This constant is defined but not used in this implementation

    # Default xmp values if not provided
    if xmp is None:
        xmp = np.linspace(xmp_min, xmp_max, npoints)

    # Ellipse coefficients from the Fairfield model
    a1 = 0.0278
    b1 = 0.3531
    c1 = -0.586
    d1 = 17.866
    e1 = -233.67

    # Split the input xmp array into two parts based on the threshold xp
    ilt15 = xmp < xp
    ige15 = xmp >= xp

    ymp_east = np.copy(xmp)  # Initialize ymp_east with the xmp values
    ymp_west = np.copy(xmp)  # Initialize ymp_west with the xmp values

    # Calculate for xmp >= -15
    if np.any(ige15):
        beta = a1 * xmp[ige15] + c1
        gamma = b1 * xmp[ige15]**2 + d1 * xmp[ige15] + e1
        delta = beta**2 - 4 * gamma

        # Compute ymp_east and ymp_west using the quadratic formula
        ymp_east[ige15] = (-beta - np.sqrt(delta)) / 2.
        ymp_west[ige15] = (-beta + np.sqrt(delta)) / 2.

        # Calculating the slopes for interpolation
        in15 = np.argmin(xmp[ige15])
        ww = -1 if in15 == len(xmp[ige15]) - 1 else 1
        s_east = (ymp_east[ige15][in15 + ww] - ymp_east[ige15]
                  [in15]) / (xmp[ige15][in15 + ww] - xmp[ige15][in15])
        s_west = (ymp_west[ige15][in15 + ww] - ymp_west[ige15]
                  [in15]) / (xmp[ige15][in15 + ww] - xmp[ige15][in15])

        # Interpolate for xmp < -15
        if np.any(ilt15):
            ymp_east[ilt15] = ymp_east[ige15][in15] + \
                s_east * (xmp[ilt15] - xmp[ige15][in15])
            ymp_west[ilt15] = ymp_west[ige15][in15] + \
                s_west * (xmp[ilt15] - xmp[ige15][in15])

    # Construct the output arrays depending on the 'short' parameter
    if not short:
        # Indices of the array in reverse order
        ireverse = np.arange(len(xmp))[::-1]
        # Duplicate xmp with reversed order for symmetry
        xmp = np.concatenate((xmp, xmp[ireverse]))
        # Combine ymp_east and reversed ymp_west
        ymp_east = np.concatenate((ymp_east, ymp_west[ireverse]))
        ymp = ymp_east
    else:
        ymp = ymp_east

    return xmp, ymp

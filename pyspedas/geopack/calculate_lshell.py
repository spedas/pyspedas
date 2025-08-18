def calculate_lshell(sc_pos):
    """
    Calculate the L-shell value for spacecraft position data.

    Parameters:
    sc_pos (numpy.ndarray): Spacecraft position data array with columns [time, x, y, z]
                            where time is in Unix timestamp, and x, y, z are in GSM coordinates.

    Returns:
    numpy.ndarray: L-shell values corresponding to the input spacecraft positions.
    """
    import numpy as np
    import geopack.geopack as geopack

    # Extracting the columns from the spacecraft position data
    times, x, y, z = sc_pos[:, 0], sc_pos[:, 1], sc_pos[:, 2], sc_pos[:, 3]

    lshell_values = []  # List to store the calculated L-shell values

    for time, xi, yi, zi in zip(times, x, y, z):
        # Recalculating geomagnetic dipole parameters
        geopack.recalc(time)

        # Tracing the magnetic field line from the position to the equator
        xf, yf, zf, xx, yy, zz = geopack.trace(xi, yi, zi, dir=1, rlim=60., r0=1.,
                                                      parmod=0, exname='t89', inname='igrf')

        # Calculating the L-shell value as the radial distance at the equator
        lshell = np.sqrt(xf ** 2 + yf ** 2 + zf ** 2)

        lshell_values.append(lshell)

    return np.array(lshell_values)
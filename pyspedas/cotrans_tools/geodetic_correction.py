import numpy as np

def geodetic_correction(lat_deg,flattening=(1/298.26),inverse=False):
        """
        Converts geocentric latitude to geodetic latitude, or vice versa. 

        Parameters
        ----------
        lat_deg : array_like
            Latitude, in degrees. Assumed to be geocentric latitude if 
            `inverse` is False. Assumed to be geodetic latitude if 
            `inverse` is True.
        flattening : float
            Flattening factor for oblate spheroid of interest. By default,
            the flattening factor is assumed to be that of Earth, at a 
            value of 1/298.26.
        inverse : bool
            Indicates whether or not to use the inverse transformation. If
            False, converts geocentric latitude to geodetic latitude. If
            True, converts geodetic latitude to geocentric latitude.

        Returns
        -------
        ndarray
            Geodetic latitude (inverse=False) or geocentric latitude (inverse=True), 
            in degrees.

        Examples
        --------
        Convert geocentric latitude to geodetic latitude:
        >>> lat_geodetic = geodetic_correction(lat_deg=50)
        >>> print(lat_geodetic)
        50.18938768317834

        Convert geodetic latitude to geocentric latitude:
        >>> lat_geocentric = geodetic_correction(lat_deg=50.18938768317834,inverse=True)
        >>> print(lat_geocentric)
        50.0
        """
        if not inverse:
            # Convert geocentric latitude to geodetic latitude:
            return np.rad2deg( np.arctan( np.tan(np.deg2rad(lat_deg))/((1-flattening)**2) ) )
        else:
            # Convert geodetic latitude to geocentric latitude:
            return np.rad2deg( np.arctan( (1-flattening)**2 * np.tan( np.deg2rad(lat_deg) ) ) )
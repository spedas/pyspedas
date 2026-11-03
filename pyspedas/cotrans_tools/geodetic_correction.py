import numpy as np

def geodetic_correction(lat_deg,f=(1/298.26),inverse=False):
        """
        Convert geocentric latitude to geodetic latitude using squashing factor f.
        Forward transformation assumes input is geocentric latitude, returns 
        corresponding geodetic latitude.

        Setting argument 'inverse' to True assumes geodetic latitude 
        and returns corresponding geocentric latitude
        """
        if not inverse:
            # Forward conversion
            geoc_lat_rad = np.deg2rad(lat_deg)
            geod_lat_rad = np.arctan( (1-f)**2 * np.tan(geoc_lat_rad) )
            geod_lat_deg = np.rad2deg(geod_lat_rad)
            return geod_lat_deg
        else:
            # Inverse conversion
            geod_lat_rad = np.deg2rad(lat_deg)
            geoc_lat_rad = np.arctan(np.tan(geod_lat_rad)/((1-f)**2))
            geoc_lat_deg = np.rad2deg(geoc_lat_rad)
            return geoc_lat_deg
        
            
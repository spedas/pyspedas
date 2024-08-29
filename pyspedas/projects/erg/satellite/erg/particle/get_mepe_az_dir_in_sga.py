"""
; --- This program calculates the unit vector of sight direction (in SGI
;     coordinates [satellite spin coordinates]) of the  n-th MEPe/MEPi channel.
;
; --- You can find some documents on the geometory of MEPs in the MEP server
;     directory: /raid/meps/docs. The geometory of MEPe explained in
;     MEPe_EPS_r1_black.pdf is used in this function. The document that
;     describes MEPi geometory is missing now (2017/Oct/01).
;
"""

import numpy as np


def get_mepe_az_dir_in_sga(fluxdir=False):
    """
    ;parameter
    ;channel azimuthal angle
    ; --- starts from -Z(SGI) axis and increases toward -Y(SGI) axis.
    ;     Note that MEPe channel number is clockwise when you see from
    ;     +X(SGI) direction.
    """

    azi_8 = -39.4  # ;[deg] offset of channel 8 from -Z(SGI) axis
    d_azi = 22.5  # ;[deg] interval of each center of aperture

    phi_array = azi_8 + (np.arange(16) - 8.) * d_azi

    """
    ;inclination of apertures (elevation)
    ; --- This value is based on visual speculation of Fig. 3 in
    ;     MEPe_EPS_r1_black.pdf.
    """
    theta_array = np.full(shape=(16), fill_value=2.0)

    """
    ;unit vector of sight direction
    ; --- Note that positive elevation of paertures in MEPe increases
                                    ;     ;X(SGI) component.
    ;; e_array is a 2-D array [ azch, 3 ]
    """

    dtor = np.pi / 180.

    e_array = np.array([
     +1 * np.sin(theta_array*dtor),
     -1 * np.cos(theta_array*dtor) * np.sin(phi_array*dtor),
     -1 * np.cos(theta_array*dtor) * np.cos(phi_array*dtor)
     ])

    if fluxdir:
        e_array *= -1.  # ;;Flip the direction

    return e_array


from pyspedas.particles.moments.moments_3d import moments_3d


def spd_pgs_moments(data_in, sc_pot=0):
    """
    Calculates moments from a simplified particle data structure. Simply a wrapper for moments_3d right now

    Parameters
    ----------
        data_in: dict
            Particle data structure 

        sc_pot: float
            Spacecraft potential

    Returns
    -------
    dict
        Dictionary containing moments
    """

    return moments_3d(data_in, sc_pot=sc_pot)

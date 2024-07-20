from copy import deepcopy
import numpy as np

from pyspedas.particles.moments.moments_3d_omega_weights import moments_3d_omega_weights

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum


def moments_3d(data_in, sc_pot=0, no_unit_conversion=False):
    """
    Calculates plasma moments from 3D data structure

    Parameters
    ----------
        data_in: dict
            Particle data structure with entries::

            'charge'
            'mass'
            'energy'
            'denergy'
            'theta'
            'dtheta'
            'phi'
            'dphi'
            'bins'
            'data'

        sc_pot: float
            Spacecraft potential

        no_unit_conversion: bool
            Flag indicating that datta is already in eflux and no unit
            conversion is required

    Note
    ----
        The calculations were mostly heisted from Davin Larson's IDL SPEDAS version

    Returns
    -------
    dict
        Dictionary of plasma moments with entries::

            'density'
            'flux'
            'mftens'
            'velocity'
            'ptens'
            'ttens'
            'vthermal'
            'avgtemp'

    Examples
    --------

    """

    data = deepcopy(data_in)

    charge = data['charge']
    mass = data['mass']
    energy = data['energy']
    energy[energy < 0.1] = 0.1

    de = data['denergy']
    de_e = de/energy

    e_inf = energy + charge*sc_pot
    e_inf[e_inf < 0] = 0.0

    # mystery line from the IDL version
    weight = (energy + charge*sc_pot)/de + 0.5
    weight[weight < 0] = 0
    weight[weight > 1] = 1

    domega_weight = moments_3d_omega_weights(data['theta'], data['phi'], data['dtheta'], data['dphi'])

    zero_bins = data['bins'] == 0
    if zero_bins.sum() > 0:
        data['data'][zero_bins] = 0

    data_dv = data['data']*de_e*weight*domega_weight[0, :, :]

    # density calculation
    dweight = np.sqrt(e_inf)/energy
    pardens = np.sqrt(mass/2.0)*1e-5*data_dv*dweight
    density = nansum(pardens)

    # flux calculation
    tmp = data['data']*de_e*weight*e_inf/energy
    fx = nansum(tmp*domega_weight[1, :, :])
    fy = nansum(tmp*domega_weight[2, :, :])
    fz = nansum(tmp*domega_weight[3, :, :])

    flux = np.array([fx, fy, fz])

    # velocity flux calculation
    tmp = data['data']*de_e*weight*e_inf**1.5/energy
    vfxx = nansum(tmp*domega_weight[4, :, :])
    vfyy = nansum(tmp*domega_weight[5, :, :])
    vfzz = nansum(tmp*domega_weight[6, :, :])
    vfxy = nansum(tmp*domega_weight[7, :, :])
    vfxz = nansum(tmp*domega_weight[8, :, :])
    vfyz = nansum(tmp*domega_weight[9, :, :])

    vftens = np.array([vfxx, vfyy, vfzz, vfxy, vfxz, vfyz])*np.sqrt(2.0/mass)*1e5
    mftens = vftens*mass/1e10

    # energy flux calculation (extra factor of energy)
    tmp = data['data']*de_e*weight*e_inf**2/energy
    v2f_x = nansum(tmp*domega_weight[1, :, :])
    v2f_y = nansum(tmp*domega_weight[2, :, :])
    v2f_z = nansum(tmp*domega_weight[3, :, :])
    eflux = np.array([v2f_x, v2f_y, v2f_z])

    velocity = flux/density/1e5 # km/s

    mf3x3 = np.array([[mftens[0], mftens[3], mftens[4]], [mftens[3], mftens[1], mftens[5]], [mftens[4], mftens[5], mftens[2]]])
    pt3x3 = mf3x3 - np.outer(velocity, flux)*mass/1e5
    ptens = np.array([pt3x3[0, 0], pt3x3[1, 1], pt3x3[2, 2], pt3x3[0, 1], pt3x3[0, 2], pt3x3[1, 2]])

    t3x3 = pt3x3/density
    avgtemp = (t3x3[0, 0] + t3x3[1, 1] + t3x3[2, 2] )/3.0  # trace/3

    vthermal = np.sqrt(2.0*avgtemp/mass)

    # t3 = sp.linalg.svdvals(t3x3)
    
    output = {'density': density, 
              'flux': flux, 
              'mftens': mftens, 
              'velocity': velocity, 
              'ptens': ptens, 
              'ttens': t3x3, 
              'vthermal': vthermal,
              'avgtemp': avgtemp}
    return output

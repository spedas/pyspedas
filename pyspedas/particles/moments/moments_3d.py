
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

    Input:
        data_in: dict
            Particle data structure 

    Parameters:
        sc_pot: float
            Spacecraft potential

        no_unit_conversion: bool
            Flag indicating that datta is already in eflux and no unit
            conversion is required

    Notes:
        The calculations were mostly heisted from Davin Larson's IDL version

    Returns:
        Dictionary containing moments

    """

    charge = data_in['charge']
    mass = data_in['mass']
    energy = data_in['energy']
    energy[energy < 0.1] = 0.1

    de = data_in['denergy']
    de_e = de/energy

    e_inf = energy + charge*sc_pot
    e_inf[e_inf < 0] = 0.0

    # mystery line from the IDL version
    weight = (energy + charge*sc_pot)/de + 0.5
    weight[weight < 0] = 0
    weight[weight > 1] = 1

    domega_weight = moments_3d_omega_weights(data_in['theta'], data_in['phi'], data_in['dtheta'], data_in['dphi'])

    data_dv = data_in['data']*de_e*weight*domega_weight[0, :, :]

    # density calculation
    dweight = np.sqrt(e_inf)/energy
    pardens = np.sqrt(mass/2.0)*1e-5*data_dv*dweight
    density = nansum(pardens)

    # flux calculation
    tmp = data_in['data']*de_e*weight*e_inf/energy
    fx = nansum(tmp*domega_weight[1, :, :])
    fy = nansum(tmp*domega_weight[2, :, :])
    fz = nansum(tmp*domega_weight[3, :, :])

    flux = np.array([fx, fy, fz])

    # velocity flux calculation
    tmp = data_in['data']*de_e*weight*e_inf**1.5/energy
    vfxx = nansum(tmp*domega_weight[4, :, :])
    vfyy = nansum(tmp*domega_weight[5, :, :])
    vfzz = nansum(tmp*domega_weight[6, :, :])
    vfxy = nansum(tmp*domega_weight[7, :, :])
    vfxz = nansum(tmp*domega_weight[8, :, :])
    vfyz = nansum(tmp*domega_weight[9, :, :])

    vftens = np.array([vfxx, vfyy, vfzz, vfxy, vfxz, vfyz])*np.sqrt(2.0/mass)*1e5
    mftens = vftens*mass/1e10

    # energy flux calculation (extra factor of energy)
    tmp = data_in['data']*de_e*weight*e_inf**2/energy
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
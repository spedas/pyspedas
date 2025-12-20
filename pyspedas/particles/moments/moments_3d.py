from copy import deepcopy
import numpy as np
from scipy.ndimage import shift

from pyspedas.particles.moments.moments_3d_omega_weights import moments_3d_omega_weights
from pyspedas import xyz_to_polar

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum

def rot_mat(v1, v2):
    """
    Create a set of basis vectors based on magnetic field and velocity vectors. Used by moments_3d.

    Parameters
    ----------
    v1: ndarray
    v2: ndarray

    Returns
    -------
    ndarray
    A 3x3 rotation matrix that rotates v1 to the z' axis and v2 to the x' - z' plane
    """

    v1norm = v1/np.linalg.norm(v1)
    v2norm = v2/np.linalg.norm(v2)
    a = v1norm
    b = np.cross(a, v2)
    b = b/np.linalg.norm(b)
    c = np.cross(b,a)
    dd_out = [c, b, a]
    data_out = np.column_stack(dd_out)
    return data_out

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
            'eflux'
            'qflux'
            'mftens'
            'velocity'
            'ptens'
            'ttens'
            'vthermal'
            'avgtemp'
            'magt3'
            't3'
            'symm'
            'symm_theta'
            'symm_phi'
            'symm_ang'

    Examples
    --------

    """

    data = deepcopy(data_in)

    charge = data['charge']
    mass = data['mass']
    energy = data['energy']
    magf = data['magf']

    # Original code set the minumum energy to 0.1 eV.
    # In IDL, the energy was only set to 0.1 where e <= 0.0
    # energy[energy < 0.1] = 0.1
    energy[energy <= 0.0] = 0.1

    de = data['denergy']
    de_e = de/energy

    e_inf = energy + charge*sc_pot
    e_inf[e_inf < 0] = 0.0

    # mystery line from the IDL version
    # Less of a mystery, now that The following comments were added to the IDL version:

    # weight is a function that will decrease the integrand for electrons
    # and positive potential below a certain energy level, a gradual
    # cutoff below the pot value.This will mitigate the effect of
    # photoelectrons that may show up below the value of spacecraft
    # potential.
    # Ions should be unaffected unless the potential is negative.
    # jmm, 2025 - 11 - 24

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

    # Heat flux moments -- derived from code contributed by Terry Liu
    #
    # Terry's code has been modified to work with the units, scaling, and spacecraft potential handling in moments_3d, rather than the older
    # n_3d, j_3d, and v_3d routines.
    # JWL 2025-07-10

    eV_J = 1.602176634e-19  # conversion from eV to J

    mp=data['mass']  # mass units are eV/(km/sec)^2, for working with eflux units.  In these units, proton mass = 0.010453500
    q = eV_J

    v = np.sqrt(2.0 * energy/mp)  # convert energy array to velocity (km/sec)

    vx = v*np.cos(data['theta']/180.*np.pi)*np.cos(data['phi']/180.*np.pi)
    vy = v*np.cos(data['theta']/180.*np.pi)*np.sin(data['phi']/180.*np.pi)
    vz = v*np.sin(data['theta']/180.*np.pi)

    # Subtract bulk velocity to get thermal velocity, km/sec

    wx=vx-velocity[0]
    wy=vy-velocity[1]
    wz=vz-velocity[2]

    # thermal energy, eV
    Eth=0.5*mp*(wx**2+wy**2+wz**2)

    # Repurposed density calculation for integrating heat flux, original code made several calls to n_3d()

    data_dvx = Eth*wx*data['data'] * de_e * weight * domega_weight[0,:,:]
    data_dvy = Eth*wy*data['data'] * de_e * weight * domega_weight[0,:,:]
    data_dvz = Eth*wz*data['data'] * de_e * weight * domega_weight[0,:,:]


    dweight = np.sqrt(e_inf)/energy
    parqx = np.sqrt(mass/2.)* 1e-5 * data_dvx * dweight
    parqy = np.sqrt(mass/2.)* 1e-5 * data_dvy * dweight
    parqz = np.sqrt(mass/2.)* 1e-5 * data_dvz * dweight

    # Conversion to output units
    conv_mw = eV_J*1.0e12  # output in mW/m^2
    conv_ev = 1.0e05 # output in eV/(cm^2-sec)


    heat_x = conv_ev * nansum(parqx)
    heat_y = conv_ev * nansum(parqy)
    heat_z = conv_ev * nansum(parqz)

    qflux = [heat_x, heat_y, heat_z]


    mf3x3 = np.array([[mftens[0], mftens[3], mftens[4]], [mftens[3], mftens[1], mftens[5]], [mftens[4], mftens[5], mftens[2]]])
    pt3x3 = mf3x3 - np.outer(velocity, flux)*mass/1e5
    ptens = np.array([pt3x3[0, 0], pt3x3[1, 1], pt3x3[2, 2], pt3x3[0, 1], pt3x3[0, 2], pt3x3[1, 2]])

    t3x3 = pt3x3/density
    avgtemp = (t3x3[0, 0] + t3x3[1, 1] + t3x3[2, 2] )/3.0  # trace/3

    vthermal = np.sqrt(2.0*avgtemp/mass)

    # t3 = sp.linalg.svdvals(t3x3)

    # Calculate eigenvalues and eigenvectors
    # For some data sets, eigh() may fail to converge. Perhpas eig() is more robust?
    try:
        t3, t3evec = np.linalg.eigh(t3x3, UPLO='U')
        #t3, t3evec = np.linalg.eig(t3x3)
    except np.linalg.LinAlgError:
        # ERG can pass data arrays that are all zeros. This gives zero density and a t3x3 array full of NaNs.
        # That makes the eigenvalue calculation throw LinAlgErrors.
        # In that case, we just silently fill t3 and t3evec with NaNs and let the chips fall where they may.
        # It happens too frequently, at least for ERG HEP, to bother logging it, otherwise the logs will
        # get spammed with warnings.
        t3 = np.array([np.nan, np.nan, np.nan])
        t3evec = np.array([t3, t3, t3])

    # Note: np.linalg.eigh() returns the eigenvalues t3 in ascending order.
    # In IDL, they're not necessarily sorted.

    # Do some magical sorting and shifting
    # SPEDAS moments_3d takes magdir as a parameter, but no one seems to call it that way.
    # In that case, it defaults to [-1,1,0].

    magdir=np.array([-1.,1.,0.])
    magfn = magdir/np.linalg.norm(magdir)

    # Heuristic for identifying the t_parallel direction based on anisotropy of the eigenvalues.
    # If the mid-valued eigenvalue is less than the average of min and max, choose the index of the max,
    # otherwise the index of the min.

    s = np.argsort(t3)
    if t3[s[1]] <.5*(t3[s[0]] + t3[s[2]]):
        num=s[2]
    else:
        num=s[0]

    # Circular shift of the eigenvalue array and the columns of the eigenvector array.  This puts the
    # selected component (t_para) in component 2, and t_perp1 and t_perp2 in columns 0 and 1.
    # The order of t_perp1 and t_perp2 may differ between IDL and Python, but I am told that
    # doesn't really matter in practice.   JWL 2025-07-03

    shft = ([-1,1,0])[num]
    t3 = shift(t3,shft,mode='grid-wrap')
    t3evec = shift(t3evec,[0,shft], mode='grid-wrap')
    # This uses the magdir version of magfn, but this dot product doesn't seem to be used anywhere.
    # Instead, it is recalculated further down from magf (from the input structure) and the velocity vector
    # dot =  np.dot( magfn, t3evec[:,2] )

    bmag = np.linalg.norm(magf)
    magfn = magf/bmag

    # The next few computations are a Python rendering of the following IDL code:
    # b_dot_s = total( (magfn # [1,1,1]) * t3evec , 1)
    # dummy = max(abs(b_dot_s),num)
    #
    # rot = rot_mat(mom.magf,mom.velocity)
    # magt3x3 = invert(rot) # (t3x3 # rot)
    # mom.magt3 = magt3x3[[0,4,8]]

    # Broadcast magfn to a (3,3) matrix: each row is magfn
    magfn_matrix = np.tile(magfn, (3, 1))  # shape (3,3)

    # Element-wise multiplication
    elementwise_product = magfn_matrix * t3evec  # shape (3,3)

    # Sum across columns (axis=1)
    b_dot_s = np.sum(elementwise_product, axis=1)  # shape (3,)
    #dummy = np.max(np.abs(b_dot_s),num)

    rot = rot_mat(magf,velocity)

    # Tensor coordinate transform of t3x3
    magt3x3 = np.linalg.inv(rot) @ (t3x3 @ rot)
    magt3 = magt3x3.ravel()[[0,4,8]]
    dot = np.dot( magfn, t3evec[:,2] )
    symm_ang = np.arccos(np.abs(dot)) * 180.0/np.pi

    if dot < 0:
        t3evec = -t3evec
    symm = t3evec[:,2]

    magdir = symm

    out = xyz_to_polar(np.array([symm]))
    symm_theta = out[0,1]
    symm_phi = out[0,2]


    output = {'density': density, 
              'flux': flux,
              'eflux': eflux,
              'qflux': qflux,
              'mftens': mftens, 
              'velocity': velocity, 
              'ptens': ptens, 
              'ttens': t3x3, 
              'vthermal': vthermal,
              'avgtemp': avgtemp,
              'magt3': magt3,
              't3': t3,
              'symm': symm,
              'symm_theta': symm_theta,
              'symm_phi': symm_phi,
              'symm_ang': symm_ang,
              }
    return output

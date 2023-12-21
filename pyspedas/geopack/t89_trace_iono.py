import numpy as np
from scipy.integrate import RK45
from geopack import geopack, t89

def trace_to_iono(f, pos_init, max_distance=50.0, dt=1.0, south=False):
    """
    Trace the magnetic field line using RK45 until the ionosphere (defined as 1.1 earth radii) is reached

    Parameters:
    - f: Function that returns the normalized magnetic field direction.
    - pos_init: Initial position [x, y, z].
    - max_distance: Maximum distance to trace before stopping.
    - dt: Initial time step for RK45.

    Returns:
    - positions: List of positions along the traced field line.
    """

    # Initialize the RK45 integrator
    # atol = .0008 Re corresponds to an error tolerance of about 5 km
    # debug: set dt to np.inf for now to see what happens
    dt = 0.05
    integrator = RK45(f, 0, pos_init, 10.0, atol=.0008, rtol=2.0e-10, max_step=dt)

    #integrator.direction = -1.0

    # Store the initial position
    positions = [pos_init]
    radius_last=100.0
    while integrator.t < max_distance:
        # Integrate one step
        integrator.step()

        # Get the current position
        pos_current = integrator.y

        radius = np.linalg.norm(pos_current)

        # Store the current position
        positions.append(pos_current)
        print(pos_current, radius)
        radius_last=radius

        # Check if we've reached the ionosphere (1 Re plus 100 km)
        if radius < 1.015696:
            # We're done
            # Use the last two (or three?) points to refine the foot point, then replace last position with foot point
            break


    return np.array(positions)

def trace_iono_89(time, startpos, iopt=3.0, south=False):
    ps = geopack.recalc(time)
    if south:
        direction=-1.0
    else:
        direction=1.0

    def t89_closure(t,pos):
        b_igrf = geopack.igrf_gsm(pos[0],pos[1],pos[2])
        b_t89 = t89.t89(iopt,ps, pos[0],pos[1],pos[2])
        b = np.array(b_igrf)+np.array(b_t89)
        nb = b/np.linalg.norm(b)
        #print(t,pos,b, nb)
        return direction*nb
    trace_points = trace_to_iono(t89_closure,pos_init=startpos,max_distance=100.0,dt=0.05, south=south)
    foot_point = trace_points[-1]
    print(foot_point)


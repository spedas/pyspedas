import numpy as np
from scipy.integrate import RK45
from geopack import geopack, t89

def t89_trace_to_equator(f, pos_init, max_distance=1e5, dt=1.0):
    """
    Trace the magnetic field line using RK45 until the equator is reached.

    Parameters:
    - f: Function that returns the normalized magnetic field direction.
    - pos_init: Initial position [x, y, z].
    - max_distance: Maximum distance to trace before stopping.
    - dt: Initial time step for RK45.

    Returns:
    - positions: List of positions along the traced field line.
    """

    # Initialize the RK45 integrator
    integrator = RK45(f, 0, pos_init, max_distance, max_step=dt)

    # Store the initial position
    positions = [pos_init]

    # Previous radial component
    prev_radial = np.dot(pos_init, f(0, pos_init))

    while integrator.t < max_distance:
        # Integrate one step
        integrator.step()

        # Get the current position
        pos_current = integrator.y

        # Compute the radial component of B using dot product
        radial_component = np.dot(pos_current, f(0, pos_current))

        # Check if the radial component has changed sign
        if radial_component * prev_radial < 0:
            # Crossed the equator
            break

        # Update the previous radial component
        prev_radial = radial_component

        # Store the current position
        positions.append(pos_current)
        print(pos_current, radial_component)

    return np.array(positions)

def trace_equator_89(time, startpos, iopt=3.0):
    ps = geopack.recalc(time)
    b0_t89=t89.t89(iopt,ps,startpos[0],startpos[1],startpos[2])
    b0_igrf=geopack.igrf_gsm(startpos[0],startpos[1],startpos[2])
    b_init=np.array(b0_t89)+np.array(b0_igrf)
    radial_component=np.dot(b_init,startpos)
    if radial_component < 0.0:
        direction=-1.0 # Field points inward, go the opposite direction
    else:
        direction=1.0 # Field points outward, follow that direction

    def t89_closure(t,pos):
        b_igrf = np.array(geopack.igrf_gsm(pos[0],pos[1],pos[2]))
        b_t89 = np.array(t89.t89(iopt,ps, pos[0],pos[1],pos[2]))
        b=b_igrf+b_t89
        return b*direction/np.linalg.norm(b)

    trace_points = t89_trace_to_equator(t89_closure,pos_init=startpos,max_distance=100.0,dt=0.05)
    equator_point = trace_points[-1]
    print(equator_point)

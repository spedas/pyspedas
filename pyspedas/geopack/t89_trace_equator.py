import numpy as np
from scipy.integrate import RK45, solve_ivp
from geopack import geopack, t89
from pyspedas import get_coords, set_coords, get_units, set_units, get_data, store_data, time_string
import logging

R_E_KM = 6371.2
#R_IONO_RE = 1.0 + 100.0 / R_E_KM  # 1 Re + 100 km
R_IONO_RE = 6468.4 / R_E_KM

def trace_to_equator_solveivp(f_B, pos_init, *, direction=1.0, max_s=200.0, max_step=0.05,
                             rtol=1e-6, atol=1e-9, s_min_event=0.1):
    """
    f_B(s, pos) returns the *full* B vector (not normalized).
    We normalize internally for dx/ds, but use B_r=0 as event.
    """

    pos_init = np.asarray(pos_init, dtype=float)

    def rhs(s, pos):
        b = np.asarray(f_B(s, pos), dtype=float)
        bn = np.linalg.norm(b)
        if not np.isfinite(bn) or bn == 0.0:
            return np.zeros(3)
        return direction * (b / bn)

    def br_event(s, pos):
        # avoid triggering immediately at s~0 if you start near equator
        if s < s_min_event:
            return 1.0
        r = np.linalg.norm(pos)
        if r == 0.0:
            return 1.0
        rhat = pos / r
        b = np.asarray(f_B(s, pos), dtype=float)
        return float(np.dot(b, rhat))

    br_event.terminal = True
    br_event.direction = 0.0  # accept either sign crossing

    sol = solve_ivp(rhs, (0.0, max_s), pos_init, method="RK45",
                    max_step=max_step, rtol=rtol, atol=atol,
                    events=[br_event], dense_output=True)

    pts = sol.y.T
    if sol.t_events[0].size > 0:
        s_event = sol.t_events[0][0]
        pts = np.vstack([pts, sol.sol(s_event)])

    return pts, sol

def trace_equator_89(time, startpos, iopt=3.0, km=True):
    ps = geopack.recalc(time)

    # Figure out direction by looking at radial field component at startpos
    b0_t89=t89.t89(iopt,ps,startpos[0],startpos[1],startpos[2])
    b0_igrf=geopack.igrf_gsm(startpos[0],startpos[1],startpos[2])
    b_init=np.array(b0_t89)+np.array(b0_igrf)
    radial_component=np.dot(b_init,startpos)
    if radial_component < 0.0:
        direction=-1.0 # Field points inward, go the opposite direction
    else:
        direction=1.0 # Field points outward, follow that direction

    startpos = np.asarray(startpos, dtype=float)
    if km:
        startpos = startpos / R_E_KM  # to Re

    def t89_dir(s, pos):
        b_igrf = np.array(geopack.igrf_gsm(pos[0], pos[1], pos[2]), dtype=float)
        b_t89  = np.array(t89.t89(iopt, ps, pos[0], pos[1], pos[2]), dtype=float)
        b = b_igrf + b_t89

        bnorm = np.linalg.norm(b)
        if not np.isfinite(bnorm) or bnorm == 0.0:
            # stop integration gracefully by returning zeros
            return np.zeros(3)

        return direction * (b / bnorm)

    trace_points, sol = trace_to_equator_solveivp(
        t89_dir, startpos,
        max_s=200.0,
        max_step=0.05,
        rtol=1e-6,
        atol=1e-9,
    )

    foot_point = trace_points[-1] if len(trace_points) else None

    if km:
        foot_point = foot_point*R_E_KM
        trace_points = trace_points*R_E_KM
        #sol = sol*R_E_KM

    return trace_points, foot_point, sol

def ttrace2equator_89(tvar, foot_name, trace_name, iopt=3.0, km=True):
    coords=get_coords(tvar)
    units=get_units(tvar)
    if coords != 'gsm':
        logging.warning(f"ttrace2iono_89: input variable has coords {coords}, must transform to GSM first")

    data = get_data(tvar)
    if km:
        startpos = data.y/R_E_KM
    else:
        startpos=data.y

    npts = len(data.times)
    all_foot_points = np.zeros((npts, 3))
    max_trace_points = -1
    ragged_list = []
    min_trace_points = 1000000
    min_trace_points_idx=-1
    max_trace_points_idx=-1
    for i,time in enumerate(data.times):
        #print(f"Tracing from point {i} at {startpos[i,:]}")
        if (i> 0) and (i % 100 == 0):
            print(f"Traced {i} points so far, current trace time {time_string(time)}")
        trace_points, foot, sol = trace_equator_89(time, startpos[i,:], iopt=iopt, km=False)
        if km:
            trace_points = trace_points*R_E_KM
            foot = foot*R_E_KM
        trace_count = len(trace_points)
        if trace_count > max_trace_points:
            max_trace_points_idx = i
            max_trace_points = trace_count
        if trace_count < min_trace_points:
            min_trace_points_idx = i
            min_trace_points = trace_count
        all_foot_points[i,:] = foot
        ragged_list.append(trace_points)
        #print(f"Traced {len(trace_points)} points to foot point {foot}")

    # Initialize final trace point array to all-nan
    all_trace_points = np.zeros((npts, max_trace_points, 3))
    all_trace_points[:,:,:] = np.nan
    print(f"Max/min trace points: {max_trace_points} {min_trace_points} at indices {max_trace_points_idx} {min_trace_points_idx}")
    for i,thistrace in enumerate(ragged_list):
        n_trace_points = thistrace.shape[0]
        all_trace_points[i,0:n_trace_points,:] = thistrace

    # Create output tplot variables
    store_data(foot_name, data={'x':data.times, 'y':all_foot_points})
    set_coords(foot_name, 'GSM')
    set_units(foot_name, 'km')
    store_data(trace_name, data={'x':data.times, 'y':all_trace_points})
    set_coords(trace_name, 'GSM')
    set_units(trace_name, 'km')

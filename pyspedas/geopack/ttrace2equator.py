import numpy as np
from pyspedas import get_coords, set_coords, get_units, set_units, get_data, store_data, time_string
import logging

R_E_KM = 6371.2
#R_IONO_RE = 1.0 + 100.0 / R_E_KM  # 1 Re + 100 km
R_IONO_RE = 6468.4 / R_E_KM


def ttrace2equator(tvar, model_str, foot_name, trace_name, iopt=3.0, km=True):
    from .generic_geopack_adapters import make_model
    from pyspedas.geopack import trace_to_event
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
    parmod = np.zeros(10)
    parmod[0] = iopt

    for i,time in enumerate(data.times):
        #print(f"Tracing from point {i} at {startpos[i,:]}")
        model = make_model(model_str,time, parmod)
        if (i> 0) and (i % 100 == 0):
            logging.info(f"Computed {i}/{npts} traces so far, current trace time {time_string(time)}")
        # Figure out direction by looking at radial field component at startpos

        b_init = model.B_gsm(startpos[i,:])

        radial_component = np.dot(b_init, startpos[i,:])
        if radial_component < 0.0:
            direction = -1.0  # Field points inward, go the opposite direction
        else:
            direction = 1.0  # Field points outward, follow that direction

        """
        fdir = make_rhs_direction(model, direction=direction)
        trace_points, sol = trace_to_equator_solveivp(
            fdir, startpos[i,:],
            direction=direction,
            max_s=200.0,
            max_step=0.5,
            rtol=1e-6,
            atol=1e-9,
        )
        """

        trace_points, status, sol = trace_to_event(
            model, startpos[i,:],
            event='equator',
            direction=direction,
            max_s=200.0,
            max_step=0.5,
            rtol=1e-6,
            atol=1e-9,
        )

        foot_point = trace_points[-1] if len(trace_points) else None

        if km:
            trace_points = trace_points*R_E_KM
            foot_point = foot_point*R_E_KM

        trace_count = len(trace_points)
        if trace_count > max_trace_points:
            max_trace_points_idx = i
            max_trace_points = trace_count
        if trace_count < min_trace_points:
            min_trace_points_idx = i
            min_trace_points = trace_count
        all_foot_points[i,:] = foot_point
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

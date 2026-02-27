import numpy as np
from scipy.integrate import RK45
from geopack import geopack, t89
import logging
from pyspedas import get_data, store_data, get_coords, set_coords, get_units, set_units, time_string

import numpy as np
from scipy.integrate import solve_ivp

R_E_KM = 6371.2
#R_IONO_RE = 1.0 + 100.0 / R_E_KM  # 1 Re + 100 km
R_IONO_RE = 6468.4 / R_E_KM

def ttrace2iono(tvar, model_str, foot_name, trace_name, iopt=3.0, km=True, south=False):
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

    direction = 1.0
    if south:
        direction = -1.0

    npts = len(data.times)
    all_foot_points = np.zeros((npts, 3))
    max_trace_points = 1
    ragged_list = []
    parmod = np.zeros(10)
    parmod[0] = iopt
    for i,time in enumerate(data.times):
        #print(f"Tracing from point {i} at {startpos[i,:]}")
        model = make_model(model_str,time, parmod)
        if (i> 0) and (i % 100 == 0):
            logging.info(f"Traced {i} points so far, current trace time {time_string(time)}")

        #fdir = make_rhs_direction(model, direction=direction)
        trace_points, status, sol = trace_to_event(
            model, startpos[i,:],
            direction=direction,
            event='iono',
            max_s=200.0,
            max_step=0.5,
            r_iono_re=R_IONO_RE,
            rtol=1e-6,
            atol=1e-9,
        )

        foot_point = trace_points[-1] if len(trace_points) else None
        if km:
            foot_point = foot_point * R_E_KM
            trace_points = trace_points * R_E_KM

        max_trace_points = np.max((max_trace_points, len(trace_points)))
        all_foot_points[i,:] = foot_point
        ragged_list.append(trace_points)
        #print(f"Traced {len(trace_points)} points to foot point {foot}")

    # Initialize final trace point array to all-nan
    all_trace_points = np.zeros((npts, max_trace_points, 3))
    all_trace_points[:,:,:] = np.nan
    print(f"Max trace points: {max_trace_points}")
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

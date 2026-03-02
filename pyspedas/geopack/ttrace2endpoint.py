import numpy as np
from pyspedas import get_coords, set_coords, get_units, set_units, get_data, store_data, time_string
import logging

R_E_KM = 6371.2
#R_IONO_RE = 1.0 + 100.0 / R_E_KM  # 1 Re + 100 km
R_IONO_RE = 6468.4 / R_E_KM


def ttrace2endpoint(tvar, model_str, endpoint, foot_name, trace_name, iopt=3.0, km=None):
    """
    Trace magnetic field lines to the north ionosphere, south ionosphere, or equator

    Parameters
    ----------
    tvar:str
        A tplot variable name specifying the times and start positions to be traced.  Coordinates should be in GSM.
    model_str:str
        A string specifying the field model to use.  Valid options are 'igrf', 't89', 't96', 't01', 't204'.
    endpoint: str
        A string specifying the endpoint to trace to: 'ionosphere-north', 'ionosphere-south', or 'equator'.
    foot_name:str
        A string specifying the tplot variable to receive the foot point locations.
    trace_name: str
        A string specifying the tplot variable to receive the trace points.
    iopt: float
        The model parameter to use for the t89 model.
    km:bool
        (Optional) Override whatever units may be in the input variable metadata. If True, the
        input variable is assumed to be in units of km, otherwise Re.  If false, the input
        units are determined from metadata.

    Returns
    -------
    None

    Examples
    --------

    >>> from pyspedas.projects.themis import state
    >>> from pyspedas import ttrace2endpoint, tplotxy3
    >>> state(trange=['2007-03-23', '2007-03-23'], probe='a')
    >>> # Trace to north ionosphere with T89 model
    >>> ttrace2endpoint('tha_pos_gsm','t89','iono',foot_name='ifoot89_n', trace_name='tha_trace_iono_n_t89',km=True,south=False)
    >>> tplotxy3('ifoot89_n',legend_names=['North ionosphere foot points',], colors='red', reverse_x=True, show_centerbody=True,save_png='tha_iono_n_foot.png')
    >>>
    >>> # Trace to south ionosphere with T89 model
    >>> ttrace2endpoint('tha_pos_gsm','t89','iono',foot_name='ifoot89_s', trace_name='tha_trace_iono_s_t89',km=True,south=True)
    >>> tplotxy3('ifoot89_s',legend_names=['South ionosphere foot points',], colors='red', reverse_x=True, show_centerbody=True,save_png='tha_iono_s_foot.png')

    >>> # Trace to equator with T89 model
    >>> ttrace2endpoint('tha_pos_gsm','t89','equator',foot_name='eq_foot89', trace_name='tha_trace_equ_t89',km=True)
    >>> tplotxy3('eq_foot89',legend_names=['Equator foot points'], colors='red', reverse_x=True, show_centerbody=True,save_png='tha_equ_foot.png')
    >>> tplotxy3('tha_trace_equ_t89',legend_names=['Traces to equator'], colors='blue', reverse_x=True, show_centerbody=True, save_png='tha_equ_traces.png')

    """

    from .generic_geopack_adapters import make_model
    from pyspedas.geopack import trace_to_event

    if endpoint not in ['ionosphere-north', 'ionosphere-south', 'equator']:
        logging.error('ttrace2endpoint: endpoint must be one of "ionosphere-north", "ionosphere-south", or "equator"')
        return

    if model_str not in ['igrf', 't89', 't96', 't01', 't204']:
        logging.error(f"ttrace2endpoint: Invalid model_str {model_str}, must be one of ['igrf', 't89', 't96', 't01', 't204']")
        return

    coords=get_coords(tvar)
    if coords.lower() != 'gsm':
        logging.error(f"ttrace2endpoint: input variable {tvar} has coords {coords}, must transform to GSM first")
        return

    if km is None:
        units=get_units(tvar)
        if units is None or units.lower() not in ['km', 're']:
            logging.error("ttrace2endpoint: Unable to determine units for input variable {tvar}" )
            return
        elif units.lower() == 'km':
            km = True
        else:
            km = False

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

        if endpoint == 'ionosphere-north':
            # For tracing to ionosphere, direction is -1 for south, 1 otherwise
            direction = 1.0
        elif endpoint == 'ionosphere-south':
            direction = -1.0
        else:
            # For tracing to the equator, we need to look at the radial component of the
            # field at the start point.  If it points outward, direction = 1, otherwise -1

            b_init = model.B_gsm(startpos[i,:])

            radial_component = np.dot(b_init, startpos[i,:])
            if radial_component < 0.0:
                direction = -1.0  # Field points inward, go the opposite direction
            else:
                direction = 1.0  # Field points outward, follow that direction

        trace_points, status, sol = trace_to_event(
            model, startpos[i,:],
            event=endpoint,
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
    logging.info(f"Max/min trace points: {max_trace_points} {min_trace_points} at indices {max_trace_points_idx} {min_trace_points_idx}")
    for i,thistrace in enumerate(ragged_list):
        n_trace_points = thistrace.shape[0]
        all_trace_points[i,0:n_trace_points,:] = thistrace

    # Create output tplot variables
    store_data(foot_name, data={'x':data.times, 'y':all_foot_points})
    set_coords(foot_name, 'GSM')

    if km:
        output_units = 'km'
    else:
        output_units = 'Re'

    set_units(foot_name, output_units)
    store_data(trace_name, data={'x':data.times, 'y':all_trace_points})
    set_coords(trace_name, 'GSM')
    set_units(trace_name, output_units)

import numpy as np
from pyspedas import get_coords, set_coords, get_units, set_units, get_data, store_data, time_string
import logging

R_E_KM = 6371.2
#R_IONO_RE = 1.0 + 100.0 / R_E_KM  # 1 Re + 100 km
R_IONO_RE = 6468.4 / R_E_KM

from .t89 import get_t89_parameters
from .t96 import get_t96_parameters
from .t01 import get_t01_parameters
from .ts04 import get_ts04_parameters

def ttrace2endpoint(tvar:str = None,
                    model_str:str = None,
                    endpoint:str = None,
                    foot_name:str = None,
                    trace_name:str = None,
                    bvec_name:str = None,
                    diag_nevals_name:str = None,
                    diag_reached_name:str = None,
                    diag_s_max_name:str = None,
                    diag_npts_name:str = None,
                    parmod=None,
                    kp=None,
                    iopt=None,
                    igrf_only=None,
                    pdyn=None,
                    dst=None,
                    byimf=None,
                    bzimf=None,
                    g1=None,
                    g2=None,
                    w1=None,
                    w2=None,
                    w3=None,
                    w4=None,
                    w5=None,
                    w6=None,
                    autoload=False,
                    km=None,
                    r_iono_re: float = R_IONO_RE,
                    max_s: float = 200.0,
                    max_step: float = 0.5,
                    rtol: float = 1e-6,
                    atol: float = 1e-9,

                    ):
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
    bvec_name: str
        A string specifying the tplot variable to receive the modeled field vectors at each trace point
    diag_nevals_name: str
        A string specifying the tplot variable to receive the number of evaluations for each line traced.
    diag_reached_name: str
        A string specifing the tplot variable to receive the status of each trace (1=endpoint reached, 0:gave up)
    diag_s_max_name: str
        A string specifying the tplot variable to receive the path length (in Re) of each trace
    diag_npts_name: str
        A string specifying the tplot variable to receive the number of points of each trace
    parmod: Any
        A 10-element or nx10 element array (or equivalent tplot variable) of model parameter values
    kp: Any
        The Kp parameter to use for the t89 model (scalar, array, or tplot variable name)
    iopt: Any
        The model parameter to use for the t89 model (scalar, array, or tplot variable name)
    igrf_only: bool
        For the t89 model, if true, only include the IGRF standard field.
    pdyn: Any
        For the t96, t01, and ts04 models: solar wind dynamic pressure in nPa
    dst: Any
        For the t96, t01, and ts04 models: Dst storm time index in nT
    byimf: Any
        For the t96, t01, and ts04 models: Y component of interplanetary magnetic field
    bzimf: Any
        for the t96, t01, and ts04 models: Z component of interplanetary magnetic field
    g1: Any
        For the t01 model: g1 index value
    g2: Any
        For the t01 model: g2 index value
    w1: Any
        For the ts04 models: w1 index value
    w2: Any
        For the ts04 models: w2 index value
    w3: Any
        For the ts04 models: w3 index value
    w4: Any
        For the ts04 models: w4 index value
    w5: Any
        For the ts04 models: w5 index value
    w6: Any
        For the ts04 models: w6 index value
    km:bool
        (Optional) Override whatever units may be in the input variable metadata. If True, the
        input variable is assumed to be in units of km, otherwise Re.  If false, the input
        units are determined from metadata.
    autoload: boolean
        If true, automatically load model parameters from an appropriate data source.
    max_s:
        Max path length in Re before giving up. Default: 200.0
    max_step:
        Max RK45 step in Re. Default: 0.5
    rtol, atol:
        Integrator tolerances (position units are Re). Defaults: 1e-6, 1e-9
    r_iono_re:
        Ionosphere radius in Re. Default: 6468.4 / R_E_KM

    Returns
    -------
    None

    Examples
    --------

    >>> from pyspedas.projects.themis import state
    >>> from pyspedas import ttrace2endpoint, tplotxy3
    >>> state(trange=['2007-03-23', '2007-03-23'], probe='a')
    >>> # Trace to north ionosphere with T89 model
    >>> ttrace2endpoint('tha_pos_gsm','t89','ionosphere-north',foot_name='ifoot89_n', trace_name='tha_trace_iono_n_t89',km=True)
    >>> tplotxy3('ifoot89_n',legend_names=['North ionosphere foot points',], colors='red', reverse_x=True, show_centerbody=True,save_png='tha_iono_n_foot.png')
    >>>
    >>> # Trace to south ionosphere with T89 model
    >>> ttrace2endpoint('tha_pos_gsm','t89','ionosphere-south',foot_name='ifoot89_s', trace_name='tha_trace_iono_s_t89',km=True)
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

    if model_str not in ['igrf', 't89', 't96', 't01', 'ts04', 't04s', 't04']:
        logging.error(f"ttrace2endpoint: Invalid model_str {model_str}, must be one of ['igrf', 't89', 't96', 't01', 'ts04', 't04s', 't04']")
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

    # Handle optional diagnostic outputs

    trace_flag = False
    min_trace_points = 1000000
    max_trace_points = -1
    min_trace_points_idx = -1
    max_trace_points_idx = -1

    if trace_name is not None:
        trace_flag = True
        ragged_list = []

    bvec_flag = False
    if bvec_name is not None:
        bvec_flag = True
        ragged_bvec_list = []

    reached_flag = False
    if diag_reached_name is not None:
        reached_flag = True
        reached_status = np.zeros(npts)

    nevals_flag = False
    if diag_nevals_name is not None:
        nevals_flag = True
        nevals = np.zeros(npts)

    s_max_flag = False
    if diag_s_max_name is not None:
        s_max_flag = True
        s_max = np.zeros(npts)

    npts_flag = False
    if diag_npts_name is not None:
        npts_flag = True
        npts_trace = np.zeros(npts)

    input_parmod = parmod
    if model_str == 't89':
        parmod = get_t89_parameters(tvar,kp=kp, iopt=iopt, parmod=input_parmod, autoload=autoload, igrf_only=igrf_only)
    elif model_str == 'igrf':
        parmod = np.zeros((npts, 10))
    elif model_str == 't96':
        parmod = get_t96_parameters(tvar,pdyn=pdyn, dst=dst, byimf=byimf, bzimf=bzimf, parmod=input_parmod, autoload=autoload)
    elif model_str == 't01':
        parmod = get_t01_parameters(tvar, pdyn=pdyn, dst=dst, byimf=byimf, bzimf=bzimf, g1=g1, g2=g2,
                                    parmod=input_parmod, autoload=autoload)
    elif model_str == 'ts04':
        parmod = get_ts04_parameters(tvar, pdyn=pdyn, dst=dst, byimf=byimf, bzimf=bzimf, w1=w1, w2=w2,
                                     w3=w3, w4=w4, w5=w5, w6=w6, parmod=input_parmod, autoload=autoload)
    else:
        logging.error(f"Unsupported model {model_str}")
        return

    for i,time in enumerate(data.times):
        #print(f"Tracing from point {i} at {startpos[i,:]}")
        model = make_model(model_str,time, parmod[i,:])
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
            max_s=max_s,
            max_step=max_step,
            rtol=rtol,
            atol=atol,
            r_iono_re=r_iono_re,
        )

        if status == 'max_s':
            thistrace_reached = 0
            logging.warning(f"ttrace2endpoint: Found max_s trace point at index {i} {time_string(time)}")
        else:
            thistrace_reached = 1

        if reached_flag:
            reached_status[i] = thistrace_reached

        if s_max_flag:
            s_max[i] = sol.sol.ts[-1]

        if nevals_flag:
            nevals[i] = sol.nfev

        if npts_flag:
            npts_trace[i] = len(trace_points)

        if bvec_flag:
            # Evaluate the model field at each point in the trace, for diagnostic purposes
            bvec_list = []
            for j in range(len(trace_points)):
                b = model.B_gsm(trace_points[j])
                bvec_list.append(b)
            ragged_bvec_list.append(np.array(bvec_list))

        foot_point = trace_points[-1] if len(trace_points) else None

        if km:
            if trace_flag:
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
        if trace_flag:
            ragged_list.append(trace_points)
        #print(f"Traced {len(trace_points)} points to foot point {foot}")

        # end loop over input positions

    logging.info(f"Max/min trace points: {max_trace_points} {min_trace_points} at indices {max_trace_points_idx} {min_trace_points_idx}")

    if trace_flag:
        # Initialize final trace point array to all-nan
        all_trace_points = np.zeros((npts, max_trace_points, 3))
        all_trace_points[:,:,:] = np.nan
        for i,thistrace in enumerate(ragged_list):
            n_trace_points = thistrace.shape[0]
            all_trace_points[i,0:n_trace_points,:] = thistrace
        store_data(trace_name, data={'x': data.times, 'y': all_trace_points})
        set_coords(trace_name, 'GSM')
        if km:
            output_units = 'km'
        else:
            output_units = 'Re'
        set_units(trace_name, output_units)

    if bvec_flag:
        # Initialize final trace point array to all-nan
        all_trace_vecs = np.zeros((npts, max_trace_points, 3))
        all_trace_vecs[:,:,:] = np.nan
        for i,thistrace in enumerate(ragged_bvec_list):
            n_trace_points = thistrace.shape[0]
            all_trace_vecs[i,0:n_trace_points,:] = thistrace
        store_data(bvec_name, data={'x': data.times, 'y': all_trace_vecs})
        set_coords(bvec_name, 'GSM')
        set_units(trace_name, 'nT')

    if s_max_flag:
        store_data(diag_s_max_name, data={'x':data.times, 'y':s_max})

    if nevals_flag:
        store_data(diag_nevals_name, data={'x':data.times, 'y':nevals})

    if reached_flag:
        store_data(diag_reached_name, data={'x':data.times, 'y':reached_status})

    if npts_flag:
        store_data(diag_npts_name, data={'x':data.times, 'y':npts_trace})

    # Create output tplot variables
    store_data(foot_name, data={'x':data.times, 'y':all_foot_points})
    set_coords(foot_name, 'GSM')

    if km:
        output_units = 'km'
    else:
        output_units = 'Re'

    set_units(foot_name, output_units)
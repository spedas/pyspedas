import logging
import numpy as np
from pyspedas import tinterpol
from pyspedas.geopack.get_w_params import get_w
from pytplot import get_data, store_data, tdeflag


def get_tsy_params(dst_tvar,
                   imf_tvar,
                   Np_tvar,
                   Vp_tvar,
                   model,
                   pressure_tvar=None,
                   newname=None,
                   speed=False,
                   g_variables=None):
    """
    This procedure will interpolate inputs, generate
    Tsyganenko model parameters and store them in a tplot 
    variable that can be passed directly to the model 
    procedure.

    Input
    ------
        dst_tvar: str
            tplot variable containing the Dst index

        imf_tvar: str
            tplot variable containing the interplanetary
            magnetic field vector in GSM coordinates

        Np_tvar: str
            tplot variable containing the solar wind 
            ion density (`cm**-3`)

        Vp_tvar: str
            tplot variable containing the proton velocity

        model: str
            Tsyganenko model; should be: 'T89', T96', 'T01','TS04'

    Parameters
    -----------
        newname: str
            name of the output variable; default: t96_par,
            't01_par' or 'ts04_par', depending on the model

        speed: bool
            Flag to indicate Vp_tvar is speed, and not velocity
            (defaults to False)
        
        pressure_tvar: str
            Set this to specify a tplot variable containing 
            solar wind dynamic pressure data. If not supplied, 
            it will be calculated internally from proton density 
            and proton speed.

    Returns
    --------
    str
        Name of the tplot variable containing the parameters. 

    Notes
    -----

        The parameters are::

            (1) solar wind pressure pdyn (nanopascals),
            (2) dst (nanotesla),
            (3) byimf,
            (4) bzimf (nanotesla)
            (5-10) indices w1 - w6, calculated as time integrals from the beginning of a storm

    """
    model = model.lower()

    if model not in ['t89', 't96', 't01', 'ts04']:
        logging.error('Unknown model: ' + model)
        return

    tdeflag(Np_tvar, method='remove_nan', overwrite=True)
    tdeflag(dst_tvar, method='remove_nan', overwrite=True)
    tdeflag(Vp_tvar, method='remove_nan', overwrite=True)

    # interpolate the inputs to the Np timestamps
    tinterpol(imf_tvar, Np_tvar, newname=imf_tvar+'_interp')
    tinterpol(dst_tvar, Np_tvar, newname=dst_tvar+'_interp')
    tinterpol(Vp_tvar, Np_tvar, newname=Vp_tvar+'_interp')

    if pressure_tvar is not None:
        tdeflag(pressure_tvar, method='remove_nan', overwrite=True)
        tinterpol(pressure_tvar, Np_tvar, newname=pressure_tvar+'_interp')

    Np_data = get_data(Np_tvar)
    dst_data = get_data(dst_tvar+'_interp')
    imf_data = get_data(imf_tvar+'_interp')
    Vp_data = get_data(Vp_tvar+'_interp')

    if pressure_tvar is not None:
        P_data = get_data(pressure_tvar+'_interp')

    if model == 't96':
        out = np.array((P_data.y, 
                        dst_data.y, 
                        imf_data.y[:, 1], 
                        imf_data.y[:, 2], 
                        np.zeros(len(dst_data.y)), 
                        np.zeros(len(dst_data.y)), 
                        np.zeros(len(dst_data.y)), 
                        np.zeros(len(dst_data.y)), 
                        np.zeros(len(dst_data.y)), 
                        np.zeros(len(dst_data.y))))
    elif model == 't01':
        if g_variables is None:
            logging.error('G variables required for T01 model; create a tplot variable containing the G variables, and provide the name of that keyword to the g_variables keyword.')
            return
        else:
            if isinstance(g_variables, str):
                tdeflag(g_variables, method='remove_nan', overwrite=True)
                tinterpol(g_variables, Np_tvar, newname=g_variables+'_interp')
                g_data = get_data(g_variables+'_interp')

                if g_data is None:
                    logging.error('Problem reading G variable: ' + g_variables)
                    return

                g1 = g_data.y[:, 0]
                g2 = g_data.y[:, 1]
            else:
                if isinstance(g_variables, list):
                    g_variables = np.array(g_variables)
                    
                if len(g_variables.shape) > 1:
                    g1 = g_variables[:, 0]
                    g2 = g_variables[:, 1]
                else:
                    g1 = np.repeat(g_variables[0], len(dst_data.y))
                    g2 = np.repeat(g_variables[1], len(dst_data.y))

            out = np.array((P_data.y, 
                            dst_data.y, 
                            imf_data.y[:, 1], 
                            imf_data.y[:, 2], 
                            g1, 
                            g2, 
                            np.zeros(len(dst_data.y)), 
                            np.zeros(len(dst_data.y)), 
                            np.zeros(len(dst_data.y)), 
                            np.zeros(len(dst_data.y))))
    elif model == 'ts04':
        params = get_w(trange=[np.nanmin(Np_data.times), np.nanmax(Np_data.times)], create_tvar=True)
        # Better deflag, just in case...
        tdeflag(params, method='remove_nan',overwrite=True)
        # interpolate the inputs to the Np timestamps
        tinterpol(params, Np_tvar, newname=params+'_interp')
        w_data = get_data(params+'_interp')

        if w_data is None:
            logging.error('Problem loading W variables for TS04 model.')
            return

        out = np.array((P_data.y, 
                        dst_data.y, 
                        imf_data.y[:, 1], 
                        imf_data.y[:, 2], 
                        w_data.y[:, 0], 
                        w_data.y[:, 1], 
                        w_data.y[:, 2], 
                        w_data.y[:, 3], 
                        w_data.y[:, 4], 
                        w_data.y[:, 5]))

    if newname is None:
        newname = model + '_par'

    saved = store_data(newname, data={'x': dst_data.times, 'y': out.T})

    if saved:
        return newname

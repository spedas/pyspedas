import numpy as np
from pyspedas import get_units, tkm2re, tvectot, set_units
from pyspedas.geopack import ttrace2endpoint

def calculate_lshell(pos_tvar: str, newname:str):
    """
    Calculate the L-shell of a position variable (should be in GSM coords)

    The L-shell represents the radial distance of the apex (equator) of the field line passing
    through the input position, in units of Re.

    Parameters
    ----------
    pos_tvar:str
        Name of a tplot variable containing position data in GSM coordinates.  It will be
        converted to units of Re if necessary.

    newname: str
        Name of new tplot variable containing L-shell values, derived by tracing to the equator
        using the IGRF model.

    Returns
    -------
    str
    Name of the variable created.
    """

    units = get_units(pos_tvar)
    if units == 'km':
        tkm2re(pos_tvar,newname=pos_tvar+'_re')
        var_to_trace = pos_tvar+'_re'
    else:
        var_to_trace = pos_tvar

    ttrace2endpoint(var_to_trace,'igrf', 'equator', foot_name='eq_foot', trace_name='eq_trace', km=False)
    tvectot('eq_foot',newname=newname,join_component=False)
    set_units(newname, 'Re')
    return newname



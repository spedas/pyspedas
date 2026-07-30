import logging
import numpy as np
from pyspedas.projects.themis.state_tools.autoload_support import autoload_support
from pyspedas.projects.themis.state_tools.spinmodel.spinmodel import get_spinmodel
from pyspedas import tplot_wildcard_expand, get_data, store_data, replace_data, get_coords
from pyspedas import cotrans
from pyspedas.projects.themis.cotrans.dsl2gse import dsl2gse

def eclipse_spinmodel_corrections_vector(tvars:str,
                                         probe:str,
                                         spin_based:bool=False,
                                        ):
    """
    Use an eclipse spin model to correct a vector quantity in DSL coordinates for errors in despinning during an eclipse.



    Parameters
    ----------
    tvars: str or list[str]
        A list of variables to correct. Wildcards are supported. All variables must be for the same probe.
    probe: str
        The probe for which support data should be loaded.  Valid values: ['a', 'b', 'c', 'd', 'e', 'f']
    spin_based:bool
        If True, apply a constant spin phase correction in addition to the time-varying corrections, to
        correct for the disruption in the onboard spin sectoring algorithm during eclipses.  Use this for
        spin-based data types like spin fits or moments.  Otherwise, only apply the time-varying corrections,
        e.g. FGM, SCM, or EFI waveform data. The same value is used for all input variables. Default: False

    Returns
    -------
    None
    The variables are corrected in-place.
    """

    tvars_exp = tplot_wildcard_expand(tvars)
    if len(tvars_exp) == 0:
        logging.warning(f"No tplot variables found matching input {tvars}")
        return
    if probe not in ['a','b','c','d','e','f']:
        logging.error(f"Invalid probe {probe}. Must be one of ['a', 'b', 'c', 'd', 'e', 'f']")

    for v in tvars_exp:
        # The correction must be done in DSL coordinates
        coords=get_coords(v)
        if coords is None:
            logging.warning(f"Input variable {v} has no coordinate system metadata, assuming DSL")
            coords_in='dsl'
            dsl_var = v
        else:
            coords_in=coords.lower()
            # Some of the L2 MOM variables have extra junk afterthe coordinate system ("DSL (Despun Spacecraft")
            # If that's the case, we need to fix coords_in for this routine to work.
            if 'dsl' in coords_in:
                dsl_var = v
                coords_in='dsl'
            elif coords_in == 'gse':
                dsl2gse(v, 'temp_dsl', probe=probe, isgsetodsl=True)
                dsl_var = 'temp_dsl'
            else:
                cotrans(v,'temp_gse',coord_in=coords_in,coord_out='gse')
                dsl2gse('temp_gse','temp_dsl',probe=probe, isgsetodsl=True)
                dsl_var='temp_dsl'

        d=get_data(dsl_var)
        t=d.times
        x = d.y[:,0]
        y = d.y[:,1]
        autoload_support(v,probe=probe,spinmodel=True)
        if spin_based:
            sm = get_spinmodel(probe=probe, correction_level=2, quiet=True)
        else:
            sm = get_spinmodel(probe=probe, correction_level=1, quiet=True)
        result=sm.interp_t(t, quiet=True)
        delta_phi = result.eclipse_delta_phi
        theta = delta_phi * np.pi/180.0
        cs = np.cos(theta)
        sn = np.sin(theta)
        xp = x*cs - y*sn
        yp = x*sn + y*cs
        new_data=np.zeros(d.y.shape,dtype=d.y.dtype)
        new_data[:,0] = xp
        new_data[:,1] = yp
        new_data[:,2] = d.y[:,2]
        replace_data(dsl_var,new_data)

        # Now convert back to the original coordinate system
        if coords_in == 'dsl':
            pass;
        elif coords_in == 'gse':
            dsl2gse(dsl_var,v,probe=probe,isgsetodsl=False)
        else:
            dsl2gse(dsl_var,'temp_gse',probe=probe, isgsetodsl=False)
            cotrans('temp_gse',v,coord_out=coords_in)


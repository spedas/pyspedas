import logging
import numpy as np
from pyspedas.projects.themis.state_tools.autoload_support import autoload_support
from pyspedas.projects.themis.state_tools.spinmodel.spinmodel import get_spinmodel
from pyspedas import tplot_wildcard_expand, get_data, replace_data
def eclipse_spinmodel_corrections_tensor(tvars:str,
                                         probe:str,
                                         spin_based:bool=False,
                                        ):
    """
    Use an eclipse spin model to correct a tensor quantity in DSL coordinates for errors in despinning during an eclipse.

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

    map3x3 = np.array([[0, 3, 4], [3, 1, 5], [4, 5, 2]])
    mapt = np.array([0, 4, 8, 1, 2, 5])

    for v in tvars_exp:
        # The tensor-valued THEMIS data quantities don't have coordinate system metadata, so we'll
        # assume DSL.

        d=get_data(v)
        t=d.times
        if d.y.shape[1] != 6:
            raise ValueError(f"Data array for variable {v} with shape {d.y.shape} is not a 6-element tensor")
        elif d.y.shape[0] != len(t):
            raise ValueError(f"Mismatched time ({t.shape}) and data {d.y.shape} arrays for variable {v}")
        autoload_support(v,probe=probe,spinmodel=True)
        if spin_based:
            sm = get_spinmodel(probe=probe, correction_level=2, quiet=True)
        else:
            sm = get_spinmodel(probe=probe, correction_level=1, quiet=True)
        result=sm.interp_t(t, quiet=True)
        delta_phi = result.eclipse_delta_phi
        theta = delta_phi * np.pi/180.0
        new_data=np.zeros(d.y.shape,dtype=d.y.dtype)
        cs = np.cos(theta)
        sn = np.sin(theta)

        # Looping here is not as efficient as it could be, but probably more understandable
        for idx in range(0,len(t)):
            tensor = d.y[idx,:]
            # Convert the 6-element representation to a 3x3 matrix
            matrix = tensor[map3x3]
            # Define a rotation matrix for this value od delta_phi
            rot = np.array([[cs[idx], sn[idx], 0.0], [-sn[idx], cs[idx], 0.0], [0.0, 0.0, 1.0]])

            # Apply the rotation, tensor-style.  Python is row-major while IDL is column-major, so
            # the conversion is slightly different.

            # NumPy equivalent of:
            #
            # rot # (tens3x3 # transpose(rot))
            matrix_rotated = rot.T @ matrix @ rot

            # Replace the old value with the corrected value
            new_data[idx,:] = matrix_rotated.reshape(-1)[mapt]

        replace_data(v,new_data)



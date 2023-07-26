import logging
from pytplot import get_data, store_data, options
import numpy as np

def epd_l2_omniflux(
    tvar, 
    ):

    """
    Produce OMNI flux spectra from ELF EPD L2 data

    Parameters
    ----------
        tvar: str
            Tplot variable name of a 3d energy time spectra 

    Return
    ----------
        omni_var: str
            Tplot variable name of 2d omni spectra
    """

    # energy bin
    energy = [63.245541, 97.979584, 138.56409, 183.30309, 238.11758, 
    305.20490, 385.16229, 520.48047, 752.99396, 1081.6653, 1529.7061, 
    2121.3203, 2893.9602, 3728.6064, 4906.1206, 6500.0000] # TODO: need to be removed and read from cdf

    # load L2 t-PA-E 3D flux 
    data = get_data(tvar)
    nspinsavailable, nPAsChannel, nEngChannel= np.shape(data.y)
    nspinsectors = (nPAsChannel - 2)*2 # TODO: check if this is true for full spin data
    
    # calculate domega in PA
    pas2plot = data.v1
    spec2plot = data.y
    pas2plot_domega = (2. * np.pi / nspinsectors) * np.sin(np.pi * pas2plot / 180.)
    index1, index2 = np.where((pas2plot < 360. / nspinsectors / 2) | (pas2plot > 180. - 360. / nspinsectors / 2))
    pas2plot_domega[index1, index2] = (np.pi/nspinsectors)*np.sin(np.pi/nspinsectors) 
    pas2plot_repeat = np.repeat(pas2plot[:, :, np.newaxis], nEngChannel, axis=2)
    
    # calculate omni flux
    omniflux = np.nansum(spec2plot * pas2plot_repeat, axis=1) / np.nansum(pas2plot_repeat, axis=1)
    
    # output omni tvar
    omni_var = f"{tvar.replace('Epat_','')}_omni"
    store_data(omni_var, data={'x': data.times, 'y': omniflux, 'v': energy}, attr_dict=get_data(tvar, metadata=True))
    options(omni_var, 'spec', True)
    options(omni_var, 'yrange', [55., 6800])
    options(omni_var, 'zrange', [10, 2e7])
    options(omni_var, 'ylog', True)
    options(omni_var, 'zlog', True)
    options(omni_var, 'ytitle', omni_var)
    breakpoint()
    return omni_var
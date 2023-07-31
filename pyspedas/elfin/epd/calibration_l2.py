import logging
from pytplot import get_data, store_data, options
import numpy as np


def epd_l2_flux4dir(
    flux_tvar, 
    LC_tvar,
    ):

    """
    Produce omni/para/perp/anti flux spectra for ELF EPD L2 data

    Parameters
    ----------
        flux_tvar: str
            Tplot variable name of a 3d energy time spectra 
        LC_tvar: str
            Tplot variable name of loss cone

    Return
    ----------
        omni_var: str
            Tplot variable name of 2d omni spectra
        para_var: str
            Tplot variable name of 2d parallel spectra
        perp_var: str
            Tplot variable name of 2d perpendicualr spectra
        anti_var: str
            Tplot variable name of 2d antiparallel spectra
    """

    # load L2 t-PA-E 3D flux 
    data = get_data(flux_tvar)

    # parameters setup
    nspinsavailable, nPAsChannel, nEngChannel= np.shape(data.y)
    nspinsectors = (nPAsChannel - 2)*2 # TODO: check if this is true for full spin data
    FOVo2 = 11.  # Field of View divided by 2 (deg)
    dphsect = 360./nspinsectors 
    SectWidtho2 = dphsect/2.
    LCfatol = FOVo2 + SectWidtho2 # tolerance of pitch angle in field aligned direction
    LCfptol = -FOVo2  # tolerance of pitch angel in perpendicular direction

    # calculate domega in PA
    pas2plot = data.v1
    spec2plot = data.y
    energy = data.v2
    pas2plot_domega = (2. * np.pi / nspinsectors) * np.sin(np.pi * pas2plot / 180.)
    index1, index2 = np.where((pas2plot < 360. / nspinsectors / 2) | (pas2plot > 180. - 360. / nspinsectors / 2))
    pas2plot_domega[index1, index2] = (np.pi/nspinsectors)*np.sin(np.pi/nspinsectors) 
    #pas2plot_repeat = np.repeat(pas2plot[:, :, np.newaxis], nEngChannel, axis=2)
    pas2plot_bcast = np.broadcast_to(pas2plot[:, :, np.newaxis], (nspinsavailable, nPAsChannel, nEngChannel))
    #===========================
    #        OMNI FLUX
    #=========================== 
    # calculate omni flux
    omniflux = np.nansum(spec2plot * pas2plot_bcast, axis=1) / np.nansum(pas2plot_bcast, axis=1)
    
    # output omni tvar
    omni_var = f"{flux_tvar.replace('Epat_','')}_omni"
    store_data(omni_var, data={'x': data.times, 'y': omniflux, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    options(omni_var, 'spec', True)
    options(omni_var, 'yrange', [55., 6800])
    options(omni_var, 'zrange', [10, 2e7])
    options(omni_var, 'ylog', True)
    options(omni_var, 'zlog', True)
    options(omni_var, 'ytitle', omni_var)

    #===========================
    #        PARA FLUX
    #=========================== 
    # load loss cone data
    data = get_data(LC_tvar)
    
    # southern hemisphere 
    paraedgedeg = np.array([lc if lc < 90 else 180-lc for lc in data.y])
    paraedgedeg_bcast = np.broadcast_to(paraedgedeg[:, np.newaxis, np.newaxis], (nspinsavailable, nPAsChannel, nEngChannel))
    
    # select index 
    iparapas, jparapas, kparapas = np.where(pas2plot_bcast < -LCfatol+paraedgedeg_bcast)
    spec2plot_allowable = np.zeros((nspinsavailable, nPAsChannel, nEngChannel))
    spec2plot_allowable[iparapas, jparapas, kparapas] = 1
    paraflux = np.nansum(spec2plot * pas2plot_bcast * spec2plot_allowable, axis=1) / np.nansum(pas2plot_bcast * spec2plot_allowable, axis=1)

    # output omni tvar
    para_var = f"{flux_tvar.replace('Epat_','')}_para"
    store_data(para_var, data={'x': data.times, 'y': paraflux, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    options(para_var, 'spec', True)
    options(para_var, 'yrange', [55., 6800])
    options(para_var, 'zrange', [10, 2e7])
    options(para_var, 'ylog', True)
    options(para_var, 'zlog', True)
    options(para_var, 'ytitle', para_var)

    return [omni_var, para_var]
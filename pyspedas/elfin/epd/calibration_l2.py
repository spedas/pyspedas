import logging
from pytplot import get_data, store_data, options
import numpy as np

def epd_l2_flux4dir_option(
    flux_var,
):
    """
    Add options for omni/para/anti/perp flux spectra

    Parameters
    ----------
        flux_var: str
            Tplot variable name of 2d omni/para/anti/perp flux spectra

    """
    unit_ = '#/(s-cm$^2$-str-MeV)' if "nflux" in flux_var else 'keV/(s-cm$^2$-str-MeV)'
    zrange = [10, 2e7] if "nflux" in flux_var else [1e4, 1e9]

    options(flux_var, 'spec', True)
    options(flux_var, 'yrange', [55., 6800])  # energy range
    options(flux_var, 'zrange', zrange)
    options(flux_var, 'ylog', True)
    options(flux_var, 'zlog', True)
    flux_var_ytitle = flux_var[0:10] + "\n" + flux_var[11:]
    options(flux_var, 'ytitle', flux_var_ytitle)
    options(flux_var, 'ysubtitle', 'Energy (keV)')
    options(flux_var, 'ztitle', unit_)

    
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
    LCfatol = FOVo2 + SectWidtho2 # tolerance of pitch angle in field aligned direction, default 22.25 deg
    LCfptol = -FOVo2  # tolerance of pitch angel in perpendicular direction, default -11. deg

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
    epd_l2_flux4dir_option(omni_var)

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

    # output para tvar
    para_var = f"{flux_tvar.replace('Epat_','')}_para"
    store_data(para_var, data={'x': data.times, 'y': paraflux, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_flux4dir_option(para_var)

    #===========================
    #        ANTI FLUX
    #=========================== 
    # select index 
    iantipas, jantipas, kantipas = np.where(pas2plot_bcast > 180+LCfatol-paraedgedeg_bcast)
    spec2plot_allowable = np.zeros((nspinsavailable, nPAsChannel, nEngChannel))
    spec2plot_allowable[iantipas, jantipas, kantipas] = 1
    antiflux = np.nansum(spec2plot * pas2plot_bcast * spec2plot_allowable, axis=1) / np.nansum(pas2plot_bcast * spec2plot_allowable, axis=1)

    # output anti tvar
    anti_var = f"{flux_tvar.replace('Epat_','')}_anti"
    store_data(anti_var, data={'x': data.times, 'y': antiflux, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_flux4dir_option(anti_var)

    #===========================
    #        PERP FLUX
    #=========================== 
    # select index 
    iperppas, jperppas, kperppas = np.where(
        (pas2plot_bcast < 180-LCfptol-paraedgedeg_bcast) & (pas2plot_bcast > LCfptol+paraedgedeg_bcast))
    spec2plot_allowable = np.zeros((nspinsavailable, nPAsChannel, nEngChannel))
    spec2plot_allowable[iperppas, jperppas, kperppas] = 1
    perpflux = np.nansum(spec2plot * pas2plot_bcast * spec2plot_allowable, axis=1) / np.nansum(pas2plot_bcast * spec2plot_allowable, axis=1)

    # output anti tvar
    perp_var = f"{flux_tvar.replace('Epat_','')}_perp"
    store_data(perp_var, data={'x': data.times, 'y': perpflux, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_flux4dir_option(perp_var)
    
    return [omni_var, para_var, anti_var, perp_var]
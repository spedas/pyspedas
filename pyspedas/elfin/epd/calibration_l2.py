import logging
from pytplot import get_data, store_data, options
import numpy as np
import bisect

def epd_l2_Espectra_option(
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

    
def epd_l2_Espectra(
    flux_tvar, 
    LC_tvar,
    LCfatol=None,
    LCfptol=None,
    ):

    """
    Produce omni/para/perp/anti flux spectra for ELF EPD L2 data

    Parameters
    ----------
        flux_tvar: str
            Tplot variable name of a 3d energy time spectra 
        LC_tvar: str
            Tplot variable name of loss cone
        LCfatol: float, optional
            Tolerance angle for para and anti flux. A positive value makes the loss 
            cone/antiloss cone smaller by this amount. 
            Default is 22.25 deg.
        LCfptol: float, optional
            Tolerance angle for perp flux. A negative value means a wider angle for 
            perp flux.
            Default is -11 deg.

    Return
    ----------
        List of four elements.
            omni_var: str. Tplot variable name of 2d omni spectra
            para_var: str. Tplot variable name of 2d parallel spectra
            perp_var: str. Tplot variable name of 2d perpendicualr spectra
            anti_var: str. Tplot variable name of 2d antiparallel spectra
    """
    
    # load L2 t-PA-E 3D flux 
    data = get_data(flux_tvar)

    # parameters setup
    nspinsavailable, nPAsChannel, nEngChannel= np.shape(data.y)
    nspinsectors = (nPAsChannel - 2)*2 
    FOVo2 = 11.  # Field of View divided by 2 (deg)
    dphsect = 360./nspinsectors 
    SectWidtho2 = dphsect/2.
    LCfatol = FOVo2 + SectWidtho2 # tolerance of pitch angle in field aligned direction, default 22.25 deg
    LCfptol = -FOVo2  # tolerance of pitch angel in perpendicular direction, default -11. deg
    # TODO: make sure these default values are correct

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
    Espectra_omni = np.nansum(spec2plot * pas2plot_bcast, axis=1) / np.nansum(pas2plot_bcast, axis=1)
    
    # output omni tvar
    omni_var = f"{flux_tvar.replace('Epat_','')}_omni"
    store_data(omni_var, data={'x': data.times, 'y': Espectra_omni, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_Espectra_option(omni_var)

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
    Espectra_para = np.nansum(spec2plot * pas2plot_bcast * spec2plot_allowable, axis=1) / np.nansum(pas2plot_bcast * spec2plot_allowable, axis=1)

    # output para tvar
    para_var = f"{flux_tvar.replace('Epat_','')}_para"
    store_data(para_var, data={'x': data.times, 'y': Espectra_para, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_Espectra_option(para_var)

    #===========================
    #        ANTI FLUX
    #=========================== 
    # select index 
    iantipas, jantipas, kantipas = np.where(pas2plot_bcast > 180+LCfatol-paraedgedeg_bcast)
    spec2plot_allowable = np.zeros((nspinsavailable, nPAsChannel, nEngChannel))
    spec2plot_allowable[iantipas, jantipas, kantipas] = 1
    Espectra_anti = np.nansum(spec2plot * pas2plot_bcast * spec2plot_allowable, axis=1) / np.nansum(pas2plot_bcast * spec2plot_allowable, axis=1)

    # output anti tvar
    anti_var = f"{flux_tvar.replace('Epat_','')}_anti"
    store_data(anti_var, data={'x': data.times, 'y': Espectra_anti, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_Espectra_option(anti_var)

    #===========================
    #        PERP FLUX
    #=========================== 
    # select index 
    iperppas, jperppas, kperppas = np.where(
        (pas2plot_bcast < 180-LCfptol-paraedgedeg_bcast) & (pas2plot_bcast > LCfptol+paraedgedeg_bcast))
    spec2plot_allowable = np.zeros((nspinsavailable, nPAsChannel, nEngChannel))
    spec2plot_allowable[iperppas, jperppas, kperppas] = 1
    Espectra_perp = np.nansum(spec2plot * pas2plot_bcast * spec2plot_allowable, axis=1) / np.nansum(pas2plot_bcast * spec2plot_allowable, axis=1)

    # output anti tvar
    perp_var = f"{flux_tvar.replace('Epat_','')}_perp"
    store_data(perp_var, data={'x': data.times, 'y': Espectra_perp, 'v': energy}, attr_dict=get_data(flux_tvar, metadata=True))
    epd_l2_Espectra_option(perp_var)
    
    return [omni_var, para_var, anti_var, perp_var]


def epd_l2_PAspectra_option(
    flux_var,
    set_zrange = True,
):
    """
    Add options for pitch angle spectra

    Parameters
    ----------
        flux_var: str
            Tplot variable name of 2d pitch angle spectra

        set_zrange: bool, optonal 
            Default is True. Only works for default four channels.
    """

    unit_ = '#/(s-\ncm$^2$-str-MeV)' if "nflux" in flux_var else 'keV/(s-\ncm$^2$-str-MeV)'
    if set_zrange is True:
        if "nflux" in flux_var:
            zrange_list = {
                0: [2.e3, 5.e6], 
                1: [1.e3, 3.e6], 
                2: [1.e2, 1.e6], 
                3: [1.e1, 5.e3], 
            }
        else:
            zrange_list = {
                0: [5.e5, 1.e10], 
                1: [5.e5, 5.e9], 
                2: [5.e5, 2.5e9], 
                3: [1.e5, 1.e8], 
            }
        ch_num = int(flux_var.split("ch")[-1])
        zrange = zrange_list.get(ch_num, [1e1, 1e2]) if "nflux" in flux_var else zrange_list.get(ch_num, [1.e4, 1.e7])
        options(flux_var, 'zrange', zrange)

    options(flux_var, 'spec', True)
    #options(flux_var, 'yrange', [-180, 180])  # energy range
    options(flux_var, 'ylog', False)
    options(flux_var, 'zlog', True)
    flux_var_ytitle = flux_var[0:10] + "\n" + flux_var[11:]
    options(flux_var, 'ytitle', flux_var_ytitle)
    options(flux_var, 'ysubtitle', 'PA (deg)')
    options(flux_var, 'ztitle', unit_)


def epd_l2_PAspectra(
    flux_tvar, 
    energybins = None,
    energies = None,
    ):
    """
    This function processes a 3D energy-time spectra from ELF EPD L2 data 
    to produce pitch angle spectra, applying either specified energy bins 
    or a defined energy range. 

    Parameters
    ----------
        flux_tvar: str
            Tplot variable name of a 3d energy time spectra 

        energybins: list of int, optional
            Specified the energy bins used for generating pitch angle spectra. 
            Default is [0, 3, 6, 9], which bins energy as follows:
                ch0: Energy channels 0-2,
                ch1: Energy channels 3-5, 
                ch2: Energy channels 6-8, 
                ch3: Energy channels 9-15
            If both 'energybins' and 'energies' are set, 'energybins' takes precedence
            energy 

        energies: list of tuple of float, optional
            Specifies the energy range for each bin in the pitch angle spectra.
            Example: energies=[(50.,160.),(160.,345.),(345.,900.),(900.,7000.)]
            If both 'energybins' and 'energies' are set, 'energybins' takes precedence.
            Energy and energybin table:
            channel     energy_range    energy_midbin
            0           50-80           63.2
            1           80-120          97.9
            2           120-160         138.5
            3           160-210         183.3
            4           210-270         238.1
            5           270-345         305.2
            6           345-430         385.1
            7           430-630         520.4
            8           630-900         752.9
            9           900-1300        1081.6
            10          1300-1800       1529.7
            11          1800-2500       2121.3
            12          2500-3350       2893.9
            13          3350-4150       3728.6
            14          4150-5800       4906.1
            15          5800+           6500.0
            

    Return
    ----------
        List of tplot variable names for pitch angle spectra
    """
    # constant energy range
    EMINS = np.array([
        50.000008, 79.999962, 120.00005, 159.99998, 210.00015, 269.99973,
        345.00043, 429.99945, 630.00061, 899.99890, 1300.0013, 1799.9985,
        2500.0022, 3349.9990, 4150.0034, 5800.0000])  # TODO: make sure it's safe to hardcode here
    EMAXS = np.array([
        79.999962, 120.00005, 159.99998, 210.00015, 269.99973, 345.00043, 
        429.99945, 630.00061, 899.99890, 1300.0013, 1799.9985, 2500.0022, 
        3349.9990, 4150.0034, 5800.0000, 7200.0000])
    
    # load L2 t-PA-E 3D flux 
    data = get_data(flux_tvar)
    energy_midbin = data.v2
    pas2plot = data.v1
    spec2plot = data.y
    nspinsavailable, nPAsChannel, nEngChannel= np.shape(data.y)
    nspinsectors = (nPAsChannel - 2)*2 

    # sort all spins in ascending order of, otherwise can't plot with tplot
    for i in range(pas2plot.shape[0]):
        line = pas2plot[i, :]
        # If the line is in descending order
        if np.array_equal(line, np.sort(line)[::-1]):
            # Flip the line
            pas2plot[i, :] = line[::-1]
            for j in range(nEngChannel):
                spec2plot[i, :, j] = spec2plot[i, :, j][::-1]

    # get energy bin for pitch angle spectra
    if energybins is not None:
        MinE_channels = energybins
        MaxE_channels = [e-1 for e in MinE_channels[1:]] + [15]
        if energies is not None:
            logging.warning("both energis and energybins are set, 'energybins' takes precedence!")  
    elif energies is not None:
        MinE_channels = [bisect.bisect_left(energy_midbin, min_energy) for min_energy, max_energy in energies]
        MaxE_channels = [bisect.bisect_right(energy_midbin, max_energy) - 1 for min_energy, max_energy in energies]
    else:
        MinE_channels = [0, 3, 6, 9]
        MaxE_channels = [2, 5, 8, 15]
    logging.info(f"Energy channel {list(zip(MinE_channels, MaxE_channels))} are used for epd l2 pitch angle spectra.") 

    # broadcast Emax and Emin so that they have the same size of spec2plot    
    Emaxs_bcast = np.broadcast_to(EMAXS[np.newaxis, np.newaxis, :], (nspinsavailable, nPAsChannel, nEngChannel))
    Emins_bcast = np.broadcast_to(EMINS[np.newaxis, np.newaxis, :], (nspinsavailable, nPAsChannel, nEngChannel))
    
    # define PAspectra, size is time * pa * energy channel
    numchannels = len(MinE_channels)
    PAspectra = np.full((nspinsavailable, nPAsChannel, numchannels), np.nan)
    PA_tvars = []

    # loop over specified energy channels
    for ichannel in range(numchannels):
        min_channel =  MinE_channels[ichannel]
        max_channel =  MaxE_channels[ichannel]
        PAspectra_single = np.nansum(spec2plot[:,:,min_channel:max_channel+1] * \
                    (Emaxs_bcast[:,:,min_channel:max_channel+1] - Emins_bcast[:,:,min_channel:max_channel+1]), axis=2) \
                    / np.nansum(Emaxs_bcast[:,:,min_channel:max_channel+1] - Emins_bcast[:,:,min_channel:max_channel+1], axis=2)
        
        # output tvariable
        PA_var = f"{flux_tvar.replace('Epat_','')}_ch{ichannel}"

        store_data(PA_var, data={'x': data.times, 'y': PAspectra_single, 'v': pas2plot})
        epd_l2_PAspectra_option(PA_var)
        PA_tvars.append(PA_var)
    
    return PA_tvars

import logging

import numpy as np
from copy import deepcopy
from pyspedas import tnames
from pyspedas.utilities.time_double import time_double
from pyspedas.utilities.time_string import time_string
from pytplot import get_data
from scipy import interpolate


logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def erg_xep_get_dist(tname,
                      index=None,
                      units='flux',
                      level='l2',
                      species='e',
                      time_only=False,
                      single_time=None,
                      trange=None):

    if len(tnames(tname)) > 0:
        input_name = tnames(tname)[0]
    else:
        print(f'Variable: {tname} not found!')
        return 0

    level = level.lower()
    """
    ;; Extract some information from a tplot variable name
    ;; e.g., erg_xep_l2_FEDU_SSD
    """

    vn_info = input_name.split('_')
    instrument = vn_info[1]
    level = vn_info[2]

    if instrument == 'xep':
        species = 'e'
    else:
        print(f'ERROR: given an invalid tplot variable: {input_name}')
        return 0

    # ;; Get a reference to data and metadata

    data_in = get_data(input_name)
    data_in_metadata = get_data(input_name, metadata=True)

    if data_in is None:
        print('Problem extracting the mepe 3dflux data.')
        return 0
    else:
        if len(data_in) != 4:
            print(f'Variable: {input_name} contains wrong number of elements!')

    # ;; Return time labels
    if time_only:
        return data_in[0]

    #  ;; Estimate the spin periods
    t_phtime = deepcopy(data_in[0])
    sc0_dt = t_phtime[1:] - t_phtime[:-1]
    sc0_dt = np.insert(sc0_dt, sc0_dt.shape[0], sc0_dt[-1])
    n_times = len(t_phtime)
    sctintgt = np.repeat(np.array([sc0_dt / 16.]).T, 16, axis=1)
    phtime = np.repeat(np.array([t_phtime]).T, 16, axis=1)\
            + sctintgt\
            * np.repeat(np.array([np.arange(16,dtype = 'float')]),
                        n_times, axis=0)


    if single_time is not None:
        single_time_double = time_double(single_time)
        if (data_in[0][0] <= single_time_double)\
                and (single_time_double <= data_in[0][-1]):
            nearest_time = interpolate.interp1d(data_in[0], data_in[0],
                                                kind="nearest")(single_time_double)
        elif (single_time_double < data_in[0][0])\
                or (data_in[0][-1] < single_time_double):
            nearest_time = interpolate.interp1d(data_in[0], data_in[0],
                                                kind="nearest", fill_value='extrapolate')(single_time_double)
        index = np.where(data_in[0] == nearest_time)[0]
        n_times = index.size
    else:
        # index supersedes time range
        if index is None:
            if trange is not None:
                trange_double_array = np.array(time_double(trange))
                trange_minmax = np.array([trange_double_array.min(),
                                          trange_double_array.max()])
                index = np.where((data_in[0] >= trange_minmax[0])
                                 & (data_in[0] <= trange_minmax[1]))[0]
                n_times = index.size
                if n_times == 0:
                    print('No data in time range: '
                          + ' '.join(time_string(trange_minmax)))
                    return 0
            else:
                n_times = data_in[0].size
                index = np.arange(n_times)
        else:
            n_times = np.array([index]).size

    """
    ;; --------------------------------------------------------------

    ;; XEP data arr: [10080(time), 9(energy), 16(spin ph)]
    ;; Dimensions
    """

    dim_array = np.array(data_in[1].shape[1:])  #  ;; [energy, spin phase(azimuth) ]
    # ;;dim_array[0] = 12  #  ;; Use only the SSD channels for now

    if species.lower() == 'e':
        mass = 5.68566e-06
        charge = -1.
        data_name = 'XEP Electron 2dflux'
        integ_time = 7.99 / 16  # ;; currently hard-coded
    else:
        print('given species is not supported by this routine.')
        return 0

    #  ;; basic template structure compatible with other routines

    dist = {
        'project_name': 'ERG',
        'spacecraft': 1,  # always 1 as a dummy value
        'data_name': data_name,
        'units_name': 'flux',  # MEP-e data in [/keV-s-sr-cm2]
                               # should be converted to [/eV-s-sr-cm2]
        'units_procedure': 'erg_convert_flux_units',
        'species': species,
        'valid': 1,

        'charge': charge,
        'mass': mass,

    }

    # other keys (members) will added in below processing, sequentially.

    """
    ;; Then, fill in arrays in the data structure
    ;;   dim[ nenergy, nspinph(azimuth), napd(elevation), ntime]
    """

    dist['time'] = data_in[0][tuple([index])]
    dist['end_time'] = dist['time'] + integ_time  # ;; currently hard-coded

    """
    ;; Shuffle the original data array [time,energy,spin phase] to
    ;; be energy-azimuth-time.
    ;; The factor 1d-3 is to convert [/keV-s-sr-cm2] (default unit of
    ;; XEP Lv2 2dflux data) to [/eV-s-sr-cm2].
    ;; Again only SSD channels are used (0:11 for ene. ch.).
    """
    dist['data'] = data_in[1][tuple([index])].reshape(
                    n_times, dim_array[0], dim_array[1]).transpose([1, 2, 0]) * 1e-3

    dist['bins'] = np.ones(shape=np.insert(dim_array, dim_array.shape[0],
                                           n_times), dtype='int8')
    # must be set or data will be consider invalid

    """
    ;; No invalid ch is set for XEP currently.
    """
    #  ;; dist['bins'][0] = 0

    #  ;; Energy ch
    e0_array = data_in[2] * 1e+3  # ;; [MeV] 
                            # (default of XEP Lv2 FEDU tplot var) to [eV]
    energy_reform = np.reshape(e0_array, [dim_array[0], 1, 1])
    energy_rebin1 = np.repeat(energy_reform, dim_array[1],
                             axis=1)  # repeated across apd(elevation)
    dist['energy'] =  np.repeat(energy_rebin1, n_times,
                              axis=2)  # repeated across n_times

    #  ;; Energy bin width
    e0bnd = np.sqrt(e0_array[:-1] * e0_array[1:])  # ;;[8]
    # ;; [9]  upper boundary of energy bin
    e0bnd_p = np.insert(e0bnd, e0bnd.shape[0], e0bnd[7])
    e0bnd_p[8] = e0_array[8] + (e0_array[8]-e0bnd[7])

    # ;; [9] lower boundary of energy bin
    e0bnd_m = np.insert(e0bnd, 0, e0bnd[0])
    e0bnd_m[0] = e0bnd_m[1]
    e0bnd_m[0] = e0_array[0] - (e0bnd[0]-e0_array[0])

    de_array = e0bnd_p-e0bnd_m  # ;; width of energy bin [9]
    de_reform = np.reshape(de_array, [dim_array[0], 1, 1])
    de_rebin1 = np.repeat(de_reform, dim_array[1],
                         axis=1)  # repeated across spin phase(azimuth)
    dist['denergy'] = np.repeat(de_rebin1, n_times,
                         axis=2)  # repeated across n_times

    dist['n_energy'] = dim_array[0]

    dist['n_bins'] = np.product(dim_array[1:])  #   # phis
   
    #  ;; azimuthal angle in spin direction

    angarr = np.zeros(shape=(2,3))
    angarr[1] = 90.-10.  # ;; these angles should be given as particle flux dirs.
    
    spinper = sc0_dt[tuple([index])]  # ;; spin period [n_times]
    if spinper.size == 1:
        spinper = np.array([spinper])
    rel_sct_time = np.zeros(shape=(n_times, 16))
    rel_sct_time = phtime[tuple([index])] + sctintgt[tuple([index])] / 2.\
                    - np.repeat(np.reshape( phtime[tuple([index]), 0],
                                    (n_times, 1)), 16, axis=1)
    
    phissi = np.array([angarr[1, 1]]) - (90. + 21.6)  # ;; [(1)]
    
    spinph_ofst = (rel_sct_time / np.repeat(spinper.reshape(n_times, 1), 16, axis=1)).T * 360.

    phi0_1_reform = np.reshape(phissi, [1, 1, 1])
    phi0_1_rebin1 = np.repeat(phi0_1_reform, dim_array[1],
                             axis=1)  # repeated across spin phase(azimuth)
    phi0_1_rebin2 = np.repeat(phi0_1_rebin1, dim_array[0],
                             axis=0)  # repeated across energy
    phi0_1 = np.repeat(phi0_1_rebin2,     n_times,
                              axis=2)  # repeated across n_times
    phi0_2_reform = np.reshape(spinph_ofst, [1, dim_array[1], n_times])
    phi0_2 = np.repeat(phi0_2_reform, dim_array[0],
                             axis=0)  # repeated across energy
    phi0 = phi0_1 + phi0_2

    """
    ;;  phi angle for the start of each spin phase
    ;;    + offset angle for each spin phase
    """
    dist['phi'] = np.fmod((phi0 + 360.), 360.)
    dist['dphi'] = np.full(shape=np.insert(dim_array, dim_array.shape[0],
                                           n_times), fill_value=22.5)
    #  ;; 22.5 deg as a constant

    del phi0  # ;; Clean huge arrays

    dist['n_phi'] = dim_array[1]

    #  ;; elevation angle
    elev = np.array([angarr[0, 1]])  # ;; [(1)]
    elev_reform = np.reshape(elev, [1, 1, 1])
    elev_rebin1 = np.repeat(elev_reform, dim_array[1],
                             axis=1)  # repeated across spin phase(azimuth)
    elev_rebin2 = np.repeat(elev_rebin1, dim_array[0],
                             axis=0)  # repeated across energy
    dist['theta'] = np.repeat(elev_rebin2, n_times,
                             axis=2)  # repeated across n_times

    dist['dtheta'] = np.full(shape=np.insert(dim_array, dim_array.shape[0],
                                             n_times), fill_value=20.)  # ;; 20 deg (+/- 10 deg)  as a constant

    dist['n_theta'] = 1

    return dist
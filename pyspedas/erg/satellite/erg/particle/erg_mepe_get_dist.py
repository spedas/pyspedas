
import logging

import numpy as np
from pytplot import tnames
from pytplot import time_double
from pytplot import time_string
from pytplot import get_data
from scipy import interpolate

from .get_mepe_flux_angle_in_sga import get_mepe_flux_angle_in_sga

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def erg_mepe_get_dist(tname,
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
    ;; e.g., erg_mepe_l2_3dflux_FEDU
    """

    vn_info = input_name.split('_')
    instrument = vn_info[1]
    level = vn_info[2]
    vn_spph = '_'.join(vn_info[0:4]) + '_spin_phase'

    if instrument == 'mepe':
        species = 'e'
    else:
        print(f'ERROR: given an invalid tplot variable: {input_name}')
        return 0

    #  If index is provided, ensure it's a list

    if index is not None and not isinstance(index, list) and not isinstance(index, np.ndarray):
        index = [index]

    # ;; Get a reference to data and metadata

    data_in = get_data(input_name)
    data_in_metadata = get_data(input_name, metadata=True)

    if data_in is None:
        print('Problem extracting the mepe 3dflux data.')
        return 0

    # ;; Return time labels
    if time_only:
        return data_in[0]

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

    ;; MEPe data arr: [9550(time), 32(spin phase), 16(energy), 16(apd)]
    ;; Dimensions
    """

    # ;; to [ energy, spin phase(azimuth), apd(elevation) ]
    dim_array = np.array(data_in[1].shape[1:])[[1, 0, 2]]

    n_sp = dim_array[1]  # ;; # of spin phases in 1 spin

    if species.lower() == 'e':
        mass = 5.68566e-06
        charge = -1.
        data_name = 'MEP-e Electron 3dflux'
        integ_time = 7.99 / 32 / 16  # ;; currently hard-coded
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

    dist['time'] = data_in[0][index]
    dist['end_time'] = dist['time'] + integ_time  # ;; currently hard-coded

    """
    ;; Shuffle the original data array [time,spin phase,energy,apd] to
    ;; be energy-azimuth-elevation-time.
    ;; The factor 1d-3 is to convert [/keV-s-sr-cm2] (default unit of
    ;; MEP-e Lv2 flux data) to [/eV-s-sr-cm2]
    """
    dist['data'] = data_in[1][index].transpose([2, 1, 3, 0]) * 1e-3

    dist['bins'] = np.ones(shape=np.insert(dim_array, dim_array.shape[0],
                                           n_times), dtype='int8')
    # must be set or data will be consider invalid

    """
    ;; Energy ch. 0 is excluded due to difficulty in defining
    ;; the representative energy and energy bin width.
    """
    dist['bins'][0] = 0

    #  ;; Energy ch
    e0_array = data_in[3] * 1e+3  # ;; [keV] 
                            #(default of MEP-e Lv2 flux data) to [eV]
    energy_reform = np.reshape(e0_array, [dim_array[0], 1, 1, 1])
    energy_rebin1 = np.repeat(energy_reform, dim_array[2],
                             axis=2)  # repeated across apd(elevation)
    energy_rebin2 = np.repeat(energy_rebin1, dim_array[1],
                              axis=1)  # repeated across spin phase(azimuth)
    dist['energy'] = np.repeat(energy_rebin2, n_times,
                              axis=3)  # repeated across n_times

    #  ;; Energy bin width
    e0bnd = np.sqrt(e0_array[:-1] * e0_array[1:])
    # ;; [16]  upper boundary of energy bin
    e0bnd_p = np.insert(e0bnd, 0, e0bnd[0])
    e0bnd_p[[0, 1]] = e0_array[1] + (e0_array[1]-e0bnd[1])

    # ;; [16] lower boundary of energy bin
    e0bnd_m = np.insert(e0bnd, e0bnd.shape[0], e0bnd[-1])
    e0bnd_m[0] = e0bnd_m[1]
    e0bnd_m[15] = e0_array[15] - (e0bnd[14]-e0_array[15])

    de_array = e0bnd_p-e0bnd_m  # ;; width of energy bin
    de_reform = np.reshape(de_array, [dim_array[0], 1, 1, 1])
    de_rebin1 = np.repeat(de_reform, dim_array[2],
                         axis=2)  # repeated across apd(elevation)
    de_rebin2 = np.repeat(de_rebin1, dim_array[1],
                         axis=1)  # repeated across spin phase(azimuth)
    dist['denergy'] = np.repeat(de_rebin2, n_times,
                         axis=3)  # repeated across n_times

    dist['n_energy'] = dim_array[0]

    dist['n_bins'] = dim_array[1] * dim_array[2]  #   # thetas * # phis
   
    #  ;; azimuthal angle in spin direction

    angarr = get_mepe_flux_angle_in_sga()
    phissi = angarr[1, 1, :] - (90. + 21.6)  # ;; [(apd)]
    spinph_ofst = data_in[2] * 11.25

    phi0_1_reform = np.reshape(phissi, [1, 1, dim_array[2], 1])
    phi0_1_rebin1 = np.repeat(phi0_1_reform, dim_array[1],
                             axis=1)  # repeated across spin phase(azimuth)

    phi0_1_rebin2 = np.repeat(phi0_1_rebin1, dim_array[0],
                             axis=0)  # repeated across energy
    phi0_1 = np.repeat(phi0_1_rebin2,     n_times,
                              axis=3)  # repeated across n_times
    phi0_2_reform = np.reshape(spinph_ofst, [1, dim_array[1], 1, 1])
    phi0_2_rebin1 = np.repeat(phi0_2_reform, dim_array[2],
                             axis=2)  # repeated across apd(elevation)
   
    phi0_2_rebin2 = np.repeat(phi0_2_rebin1, dim_array[0],
                             axis=0)  # repeated across energy
    phi0_2 = np.repeat(phi0_2_rebin2, n_times,
                              axis=3)  # repeated across n_times
    phi0 = phi0_1 + phi0_2

    ofst_sv = (np.arange(dim_array[0]) + 0.5) * \
        11.25/dim_array[0]  # ;; [(energy)]
    phi_ofst_for_sv_reform = np.reshape(ofst_sv, [dim_array[0], 1, 1, 1])
    phi_ofst_for_sv_rebin1 = np.repeat(
        phi_ofst_for_sv_reform, dim_array[2],
                                 axis=2)  # repeated across apd(elevation)

    phi_ofst_for_sv_rebin2 = np.repeat(
        phi_ofst_for_sv_rebin1,dim_array[1],
                                 axis=1)  # repeated across spin phase(azimuth)
    phi_ofst_for_sv = np.repeat(phi_ofst_for_sv_rebin2,         n_times,
                                 axis=3)  # repeated across n_times
    """
    ;;  phi angle for the start of each spin phase
    ;;    + offset angle foreach sv step
    """
    dist['phi'] = np.fmod((phi0 + phi_ofst_for_sv + 360.), 360.)
    dist['dphi'] = np.full(shape=np.insert(dim_array, dim_array.shape[0],
                                           n_times), fill_value=11.25)

    del phi0, phi_ofst_for_sv  # ;; Clean huge arrays

    dist['n_phi'] = dim_array[1]

    #  ;; elevation angle
    elev = angarr[0, 1, :]  # ;; [(apd)]
    elev_reform = np.reshape(elev, [1, 1, dim_array[2], 1])
    elev_rebin1 = np.repeat(elev_reform, dim_array[1],
                             axis=1)  # repeated across spin phase(azimuth)
    elev_rebin2 = np.repeat(elev_rebin1, dim_array[0],
                             axis=0)  # repeated across energy
    dist['theta'] = np.repeat(elev_rebin2, n_times,
                             axis=3)  # repeated across n_times

    dist['dtheta'] = np.full(shape=np.insert(dim_array, dim_array.shape[0],
                                             n_times), fill_value=11.25)  # ;; 11.25 deg is set for the moment calculation

    dist['n_theta'] = dim_array[2]

    return dist
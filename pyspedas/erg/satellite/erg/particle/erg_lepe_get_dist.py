import cdflib
import logging
import numpy as np


from copy import deepcopy
from scipy.spatial import KDTree
from pytplot import tnames
from pytplot import time_double
from pytplot import time_string
from pytplot import get_data
from scipy import interpolate

from astropy.coordinates import spherical_to_cartesian, cartesian_to_spherical

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
def erg_lepe_get_dist(tname,
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

    #  If index is provided, ensure it's a list

    if index is not None and not isinstance(index, list) and not isinstance(index, np.ndarray):
        index = [index]


    """
    ;; Extract some information from a tplot variable name
    ;; e.g., erg_lepi_l2_3dflux_FPDU
    """
    vn_info = input_name.split('_')
    instrument = vn_info[1]
    level = vn_info[2]
    arrnm = vn_info[4]
    if species is None:
        if instrument == 'lepe':
            species = 'e'
        else:
            print(f'RROR: given an invalid tplot variable: {input_name}')
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
    ;; LEP-e data Array[10269(time), 32(energy), 12(anode), 16(spin
    ;; phase)] for the normal 3-D flux mode (fine channels are averaged
    ;;into two coarse channels)
    """
    # ;; to [ energy, spin phase(azimuth), apd(elevation) ]
    dim_array = np.array(data_in[1].shape[1:])[[0, 2, 1]]
    if species.lower() == 'e':
        mass = 5.68566e-06
        charge = -1.
        data_name = 'LEP-e Electron 3dflux'
        integ_time = 7.99 / 32 / 16  # ;; currently hard-coded
    else:
        print('given species is not supported by this routine.')
        return 0
    #  ;; basic template structure compatible with other routines
    dist = {
        'project_name': 'ERG',
        'spacecraft': 1,  # always 1 as a dummy value
        'data_name': data_name,
        'units_name': 'flux',  # ; LEP-e data in [/eV-s-sr-cm2
        'units_procedure': 'erg_convert_flux_units',
        'species': species,
        'valid': 1,
        'charge': charge,
        'mass': mass,
    }
    # other keys (members) will added in below processing, sequentially.
    """
    ;; Then, fill in arrays in the data structure
    ;;   dim[ nenergy, nspinph(azimuth), nanode(elevation), ntime]
    """
    dist['time'] = data_in[0][index]
    dist['end_time'] = dist['time'] + integ_time  # ;; currently hard-coded
    """
    ;; Shuffle the original data array [time,energy, anode, spin phase] to
    ;; be energy-azimuth(spin phase)-elevation-time.
    """
    dist['data'] = data_in[1][index].transpose([1, 3, 2, 0])
    dist['bins'] = np.ones(shape=np.insert(dim_array, dim_array.shape[0],
                                           n_times), dtype='int8')
    # must be set or data will be consider invalid
    # ;; fishy negative flux values are all replaced with zero.
    # ;; dist['data'] = np.where(dist['data'] < 0.,0.,dist['data'])
    file_name_raw= get_data(input_name, metadata=True)['CDF']['FILENAME']
    if isinstance(file_name_raw, str):
        cdf_path = file_name_raw
    elif isinstance(file_name_raw, list):
        cdf_path = file_name_raw[-1]

    cdf_file = cdflib.CDF(cdf_path)

    #  ;; Energy ch
    """
    ;; Default unit of v in F?DU tplot variables [keV/q] should be
    ;; converted to [eV] by multiplying (1000 * charge number).
    """
    e0_array_raw = data_in[2][index]# ;; [time, 32]
    e0_array = e0_array_raw.T
    energy_reform = np.reshape(e0_array, [dim_array[0], 1, 1, n_times])
    energy_rebin1 = np.repeat(energy_reform, dim_array[2],
                             axis=2)  # repeated across apd(elevation)
    dist['energy'] = np.repeat(energy_rebin1, dim_array[1],
                              axis=1)  # repeated across spin phase(azimuth)

    # denergy member
    
    de_array = e0_array + np.nan  #  ;; initialized as [ time, 32 ]  
    for i in range(n_times):
        enec0_array = deepcopy(e0_array[:, i])
        id_array = np.argwhere(np.isfinite(enec0_array))
        if len(id_array) < 2:
            continue
        #  ;sorting and picks up only uniq elements. nominally 30, 28, 5, 4.
        enec_array = np.sort(np.unique(enec0_array[id_array[:,0].tolist()]))
        n_enec = enec_array.size
        if (n_enec < 3) or (np.nansum(enec_array) < 0.):
            continue  # ;; invalid energy value found
        logenec_array = np.log10(enec_array)
        logmn_array = (logenec_array[1:] + logenec_array[:-1]) / 2.
        logdep_array = enec_array * 0.
        logdem_array = enec_array * 0.
        logdep_array[:-1] = deepcopy(logmn_array)
        logdem_array[1:] = deepcopy(logmn_array)
        logdem_array[0] = logenec_array[0] - (logmn_array[0] - logenec_array[0])
        logdep_array[-1] = logenec_array[-1] + (logenec_array[-1] - logmn_array[-1])
        de_array_i= 10.**logdep_array - 10.**logdem_array

        # getting nearest neighbor indices, 'id = nn( enec, enec0 ) ' in IDL
        enec0_array_temp = np.nan_to_num(enec0_array, copy=True,nan=np.nanmin(enec0_array))
        enec0_array_temp_repeat= np.repeat(np.array([enec0_array_temp]).T, 2, 1)
        enec_array_repeat= np.repeat(np.array([enec_array]).T, 2, 1)
        tree = KDTree(enec_array_repeat, leafsize=1)
        _, id_array = tree.query(enec0_array_temp_repeat)
        # getting nearest neighbor indices, 'id = nn( enec, enec0 ) ' in IDL
        de_array[:, i] = de_array_i[id_array].T

    de_reform = np.reshape(de_array, [dim_array[0], 1, 1, n_times])
    de_rebin1 = np.repeat(de_reform, dim_array[2],
                         axis=2)  # repeated across apd(elevation)
    dist['denergy'] = np.repeat(de_rebin1, dim_array[1],
                         axis=1)  # repeated across spin phase(azimuth)

    dist['n_energy'] = dim_array[0]
    dist['n_bins'] = dim_array[1] * dim_array[2]  #   # thetas * # phis
    """
    ;; Array elements containing NaN are excluded from the further
    ;; calculations, by setting bins to be zero.
    """
    dist['bins'] = np.where((np.isfinite(dist['data']))
                               &(np.isfinite(dist['energy'])),
                               1,0)
    
    #  ;; azimuthal angle in spin direction
    angarr = cdf_file.varget('FEDU_Angle_SGA') # ;;[elev/phi, (anode)] in SGA  (looking dir)

    # ;; Flip the looking dirs to the flux dirs
    n_anode = angarr[0].size
    r_array = np.ones(n_anode)
    elev_array = deepcopy(angarr[0])
    phi_array = deepcopy(angarr[1])
    deg_to_rad = np.pi / 180.
    x_array, y_array, z_array = spherical_to_cartesian(
                                     r_array,
                                     elev_array * deg_to_rad,
                                     phi_array* deg_to_rad
                                     )
    r_array, elev_array, phi_array = cartesian_to_spherical(
                                        -x_array,
                                        -y_array,
                                        -z_array)
    elev_array = elev_array.value / deg_to_rad
    phi_array = phi_array.value / deg_to_rad
    angarr = np.array([elev_array, phi_array])

    phissi = angarr[1] - (90. + 21.6)  # ;; [(anode)] (21.6 = degree between sun senser and satellite coordinate)
    spinph_ofst = data_in[4] * 22.5
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
        22.5/dim_array[0]  # ;; [(energy)]
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
                                           n_times), fill_value=22.5)  # ;; 22.5 deg as a constant
    del phi0, phi_ofst_for_sv  # ;; Clean huge arrays
    dist['n_phi'] = dim_array[1]
    #  ;; elevation angle
    elev = angarr[0]  # ;; [(anode)]
    elev_reform = np.reshape(elev, [1, 1, dim_array[2], 1])
    elev_rebin1 = np.repeat(elev_reform, dim_array[1],
                             axis=1)  # repeated across spin phase(azimuth)
    elev_rebin2 = np.repeat(elev_rebin1, dim_array[0],
                             axis=0)  # repeated across energy
    dist['theta'] = np.repeat(elev_rebin2, n_times,
                             axis=3)  # repeated across n_times

    #  ;; elevation angle for fine channel  
    
    if 'fine_ch' in vn_info:
        dist['dtheta'] = np.full(shape=np.insert(dim_array, dim_array.shape[0],
                                             n_times), fill_value=22.5/6.)  #  ;; Fill all with 22.5/6.
    else:
        dist['dtheta'] = np.full(shape=np.insert(dim_array, dim_array.shape[0],
                                             n_times), fill_value=22.5)  #  ;; Fill all with 22.5. first
        #  ;; give half weight for ch1,2,3,4, 19,20,21,22
        dist['dtheta'][:, :, 0:4, :] = 11.25
        dist['dtheta'][:, :, dim_array[2]-4:dim_array[2], :] = 11.25
        if dim_array[2] == 22:  #  ;; with full fine channels
            dist['dtheta'][:, :, 5:17, :] = 22.5/6

    dist['n_theta'] = dim_array[2]
    
    return dist

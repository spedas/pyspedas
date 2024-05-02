import numpy as np

from copy import deepcopy

from pyspedas import tinterpol
from pytplot import time_double
from pytplot import time_string
from pytplot import tnames

from pyspedas.particles.moments.spd_pgs_moments import spd_pgs_moments
from pyspedas.particles.spd_part_products.spd_pgs_regrid import spd_pgs_regrid
from pytplot import get_timespan, get_data, store_data

from .erg_xep_get_dist import erg_xep_get_dist
from .erg_pgs_clean_data import erg_pgs_clean_data
from .erg_pgs_limit_range import erg_pgs_limit_range
from .erg_convert_flux_units import erg_convert_flux_units
from .erg_pgs_moments_tplot import erg_pgs_moments_tplot
from .erg_pgs_make_fac import erg_pgs_make_fac
from .erg_pgs_make_e_spec import erg_pgs_make_e_spec
from .erg_pgs_make_theta_spec import erg_pgs_make_theta_spec
from .erg_pgs_make_phi_spec import erg_pgs_make_phi_spec
from .erg_pgs_do_fac import erg_pgs_do_fac
from .erg_pgs_progress_update import erg_pgs_progress_update
from .erg_pgs_make_tplot import erg_pgs_make_tplot

def erg_xep_part_products(
    in_tvarname,
    species=None,
    outputs=['energy'],
    no_ang_weighting=True,
    suffix='',
    units='flux',
    datagap=15.0,
    regrid=[16, 12],
    pitch=[0., 180.],
    theta=[-90., 90.],
    phi_in=[0., 360.],
    gyro=[0., 360.],
    energy=None,
    fac_type='mphism',
    trange=None,
    mag_name=None,
    pos_name=None,
    relativistic=False,
    no_regrid=False
    ):

    if len(tnames(in_tvarname)) < 1:
        print('No input data, please specify tplot variable!')
        return 0

    in_tvarname = tnames(in_tvarname)[0]
    instnm = in_tvarname.split('_')[1]  #  ;; xep

    
    #  ;; no_regrid is always on, otherwise QHULL hangs in gridding
    no_regrid = True
    
    if no_ang_weighting:
        no_regrid = True

    if isinstance(outputs, str):
        outputs_lc = outputs.lower()
        outputs_lc = outputs_lc.split(' ')
    elif isinstance(outputs, list):
        outputs_lc = []
        for output in outputs:
            outputs_lc.append(output.lower())

    units_lc = units.lower()

    if phi_in != [0., 360.]:
        if abs(phi_in[1] - phi_in[0]) > 360.:
            print('ERROR: Phi restrictions must have range no larger than 360 deg')
            return 0
        
        phi = phi_in  # Survey or implement of spd_pgs_map_azimuth() have not conducted yet.
        if phi[0] == phi[1]:
            phi = [0., 360.]


    if abs(gyro[1] - gyro[0]) > 360.:
        print('ERROR: Gyro restrictions must have range no larger than 360 deg')
        return 0
    if gyro[0] == gyro[1]:
        gyro = [0., 360.]


    """
    ;;Create energy spectrogram after FAC transformation if limits are not 
    ;;identical to the default.
    """
    if (gyro != [0., 360.]) or (pitch != [0.,180.]):
        idx = np.where(np.array(outputs_lc) == 'energy')[0]
        if (idx.shape[0] > 0) and ('fac_energy' not in outputs_lc):
            idx = idx[0]
            outputs_lc[idx] = 'fac_energy'

        idx = np.where(np.array(outputs_lc) == 'moments')[0]
        if (idx.shape[0] > 0) and ('fac_moments' not in outputs_lc):
            idx = idx[0]
            outputs_lc[idx] = 'fac_moments'

    #  ;;Preserve the original time range
    tr_org = get_timespan(in_tvarname)

    if instnm == 'xep':
        times_array = erg_xep_get_dist(in_tvarname, species=species, units=units_lc, time_only=True)
    else:
        print(f'ERROR: Cannot find "xep" in the given tplot variable name: {in_tvarname}')
        return 0

    if trange is not None:
        
        trange_double = time_double(trange)
        time_indices = np.where((times_array >= trange_double[0]) \
                                & (times_array <= trange_double[1]))[0]
        
        if time_indices.shape[0] < 1:
            print(f'No ,{in_tvarname}, data for time range ,{time_string(trange_double)}')

    elif trange is None:
        time_indices = np.arange(times_array.shape[0])

    times_array = times_array[time_indices]



    if instnm == 'xep':
        dist = erg_xep_get_dist(in_tvarname, 0, species=species, units=units_lc)

    if 'energy' in outputs_lc:
        out_energy = np.zeros((times_array.shape[0], dist['n_energy']))
        out_energy_y = np.zeros((times_array.shape[0], dist['n_energy']))
    if 'phi' in outputs_lc:
        out_phi = np.zeros((times_array.shape[0], dist['n_phi']))
        out_phi_y = np.zeros((times_array.shape[0], dist['n_phi']))
    if 'pa' in outputs_lc:
        out_pad = np.zeros((times_array.shape[0], regrid[1]))
        out_pad_y = np.zeros((times_array.shape[0], regrid[1]))

    if 'fac_energy' in outputs_lc:
        out_fac_energy = np.zeros((times_array.shape[0], dist['n_energy']))
        out_fac_energy_y = np.zeros((times_array.shape[0], dist['n_energy']))

    out_vars = []
    last_update_time = None

    """
    ;;--------------------------------------------------------
    ;;Prepare support data
    ;;--------------------------------------------------------
    """
    # ;;create rotation matrix to B-field aligned coordinates if needed
    
    fac_outputs = ['pa', 'fac_energy']
    fac_requested = len(set(outputs_lc).intersection(fac_outputs)) > 0
    if fac_requested:

        fac_matrix = erg_pgs_make_fac(times_array, mag_name, pos_name, fac_type=fac_type)

        if fac_matrix is None:
            # problem creating the FAC matrices
            fac_requested = False

    magf = np.array([0., 0., 0.])
    no_mag_for_moments = False

    """
    ;;-------------------------------------------------
    ;; Loop over time to build spectrograms and/or moments
    ;;-------------------------------------------------
    """
    for index in range(time_indices.shape[0]):

        last_update_time = erg_pgs_progress_update(last_update_time=last_update_time,
             current_sample=index, total_samples=time_indices.shape[0], type_string=in_tvarname)

        #  ;; Get the data structure for this sample

        if instnm == 'xep':
            dist = erg_xep_get_dist(in_tvarname, time_indices[index], species=species, units=units_lc)
        else:
            print(f'ERROR: Cannot find "xep" in the given tplot variable name: {in_tvarname}')
            return 0
        if magf.ndim == 2:
            magvec = magf[index]
        elif magf.ndim == 1:
            magvec = magf

        clean_data = erg_pgs_clean_data(dist, units=units_lc,relativistic=relativistic, magf=magvec)

        if fac_requested:
            pre_limit_bins = deepcopy(clean_data['bins'])

        clean_data = erg_pgs_limit_range(clean_data, phi=phi_in, theta=theta, energy=energy, no_ang_weighting=no_ang_weighting)

        #  ;;Build energy spectrogram
        if 'energy' in outputs_lc:
            out_energy_y[index, :], out_energy[index, :] = erg_pgs_make_e_spec(clean_data)

        #  ;;Build phi spectrogram
        if 'phi' in outputs_lc:
            out_phi_y[index, :], out_phi[index, :] = erg_pgs_make_phi_spec(clean_data, resolution=dist['n_phi'],no_ang_weighting=no_ang_weighting)

        #  ;;Perform transformation to FAC, (regrid data), and apply limits in new coords
        
        if fac_requested:
            
            # ;limits will be applied to energy-aligned bins
            clean_data['bins'] = deepcopy(pre_limit_bins)
            clean_data = erg_pgs_limit_range(clean_data, phi=phi_in, theta=theta, energy=energy, no_ang_weighting=no_ang_weighting)

            # ;perform FAC transformation and interpolate onto a new, regular grid 
            clean_data = erg_pgs_do_fac(clean_data, fac_matrix[index, :, :])

            #;nearest neighbor interpolation to regular grid in FAC
            if not no_regrid:
                if (not np.all(np.isnan(clean_data['theta']))) and (not np.all(np.isnan(clean_data['phi']))):
                    clean_data = spd_pgs_regrid(clean_data, regrid)

            clean_data['theta'] = 90.0-clean_data['theta']  #  ;pitch angle is specified in co-latitude

            # ;apply gyro & pitch angle limits(identical to phi & theta, just in new coords)
            clean_data = erg_pgs_limit_range(clean_data, theta=pitch, phi=gyro, no_ang_weighting=no_ang_weighting)

            if 'pa' in outputs_lc:
                # ;Build pitch angle spectrogram
                out_pad_y[index, :], out_pad[index, :] = erg_pgs_make_theta_spec(clean_data, colatitude=True, resolution=regrid[1], no_ang_weighting=no_ang_weighting)

            if 'fac_energy' in outputs_lc:
                out_fac_energy_y[index, :], out_fac_energy[index, :] = erg_pgs_make_e_spec(clean_data)


    if 'energy' in outputs_lc:
        output_tplot_name = in_tvarname+'_energy' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_energy_y, z=out_energy, units=units, ylog=True, ytitle=dist['data_name'] + ' \\ energy (eV)',relativistic=relativistic)
        out_vars.append(output_tplot_name)
    if 'phi' in outputs_lc:
        output_tplot_name = in_tvarname+'_phi' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_phi_y, z=out_phi, units=units, ylog=False, ytitle=dist['data_name'] + ' \\ phi (deg)',relativistic=relativistic)
        out_vars.append(output_tplot_name)

    #  ;;Pitch Angle Spectrograms
    if 'pa' in outputs_lc:
        output_tplot_name = in_tvarname+'_pa' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_pad_y, z=out_pad, units=units, ylog=False, ytitle=dist['data_name'] + ' \\ PA (deg)',relativistic=relativistic)
        out_vars.append(output_tplot_name)


    if 'fac_energy' in outputs_lc:

        output_tplot_name = in_tvarname+'_energy_mag' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_fac_energy_y, z=out_fac_energy, units=units, ylog=True, ytitle=dist['data_name'] + ' \\ energy (eV)',relativistic=relativistic)
        out_vars.append(output_tplot_name)

    return out_vars

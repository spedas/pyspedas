import numpy as np

from copy import deepcopy

from pyspedas import tnames, tinterpol, tcopy
from pyspedas.utilities.time_double import time_double
from pyspedas.utilities.time_string import time_string

from pyspedas.particles.moments.spd_pgs_moments import spd_pgs_moments
from pyspedas.particles.spd_part_products.spd_pgs_regrid import spd_pgs_regrid
from pytplot import get_timespan, get_data, store_data

from .erg_hep_get_dist import erg_hep_get_dist
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

def erg_hep_part_products(
    in_tvarname,
    species=None,
    outputs=['energy'],
    no_ang_weighting=True,
    suffix='',
    units='flux',
    datagap=8.1,
    regrid=[16, 16],
    pitch=[0., 180.],
    theta=[-90., 90.],
    phi_in=[0., 360.],
    gyro=[0., 360.],
    energy=None,
    fac_type='phigeo',
    trange=None,
    mag_name=None,
    pos_name=None,
    relativistic=False,
    no_regrid=True,
    include_allazms=False,
    muconv=False
    ):

    if len(tnames(in_tvarname)) < 1:
        print('No input data, please specify tplot variable!')
        return 0

    in_tvarname = tnames(in_tvarname)[0]
    vn_info = in_tvarname.split('_')
    instnm = vn_info[1]  #  ;; 'hep' 

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

    #  ;; Currently no_regrid is always on and regrid is just ignored. 
    no_regrid = True

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

    #  ;;Preserve the original time range
    tr_org = get_timespan(in_tvarname)

    times_array = erg_hep_get_dist(in_tvarname, species=species, units=units_lc, time_only=True)


    if trange is not None:
        
        trange_double = time_double(trange)
        time_indices = np.where((times_array >= trange_double[0]) \
                                & (times_array <= trange_double[1]))[0]
        
        if time_indices.shape[0] < 1:
            print(f'No ,{in_tvarname}, data for time range ,{time_string(trange_double)}')

    elif trange is None:
        time_indices = np.arange(times_array.shape[0])

    times_array = times_array[time_indices]



    dist_all_time_range =  erg_hep_get_dist(in_tvarname, time_indices, species=species, units=units_lc, exclude_azms= not include_allazms)
    dist = deepcopy(dist_all_time_range)

    if 'energy' in outputs_lc:
        out_energy = np.zeros((times_array.shape[0], dist['n_energy']))
        out_energy_y = np.zeros((times_array.shape[0], dist['n_energy']))
    if 'theta' in outputs_lc:
        n_theta_unique = len(np.unique(dist['theta']))
        out_theta = np.zeros((times_array.shape[0], n_theta_unique))
        out_theta_y = np.zeros((times_array.shape[0], n_theta_unique))
    if 'phi' in outputs_lc:
        out_phi = np.zeros((times_array.shape[0], dist['n_phi']))
        out_phi_y = np.zeros((times_array.shape[0], dist['n_phi']))

    if 'gyro' in outputs_lc:
        out_gyro = np.zeros((times_array.shape[0], regrid[0]))
        out_gyro_y = np.zeros((times_array.shape[0], regrid[0]))

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
    
    fac_outputs = ['pa','gyro','fac_energy']
    fac_requested = len(set(outputs_lc).intersection(fac_outputs)) > 0
    if fac_requested:
        """
        ;; Currently triangulation fails, so forcidly no_regrid is set for
        ;; spectum generation in FAC coordinates.
        """
        no_regrid = True

        fac_matrix = erg_pgs_make_fac(times_array, mag_name, pos_name, fac_type=fac_type)

        if fac_matrix is None:
            # problem creating the FAC matrices
            fac_requested = False

    #  ;;create the magnetic field vector array for mu conversion
    magf = np.array([0., 0., 0.])
    no_mag_for_moments = False
    
    if muconv:

        no_mag = mag_name is None
        magnm = tnames(mag_name)
        if (len(magnm) < 1) or no_mag:
            print('the magnetic field data is not given!')
        else:
            magnm = magnm[0]

            """
            ;; Create magnetic field data with times shifted by half of spin
            ;; periods
            """

            magtmp = magnm+'_pgs_temp'
            tcopy(magnm, magtmp)
            tinterpol(magtmp, times_array, newname=magtmp)
            magf = get_data(magtmp)[1]  #  ;; [ time, 3] nT

    """
    ;;-------------------------------------------------
    ;; Loop over time to build the spectragrams
    ;;-------------------------------------------------
    """
    for index in range(time_indices.shape[0]):
        last_update_time = erg_pgs_progress_update(last_update_time=last_update_time,
             current_sample=index, total_samples=time_indices.shape[0], type_string=in_tvarname)

        #  ;; Get the data structure for this sample

        dist = {
            'project_name': deepcopy(dist_all_time_range['project_name']),
            'spacecraft': deepcopy(dist_all_time_range['spacecraft']),
            'data_name': deepcopy(dist_all_time_range['data_name']),
            'units_name': deepcopy(dist_all_time_range['units_name']),
            'units_procedure': deepcopy(dist_all_time_range['units_procedure']),
            'species': deepcopy(dist_all_time_range['species']),
            'valid': deepcopy(dist_all_time_range['valid']),
            'charge': deepcopy(dist_all_time_range['charge']),
            'mass': deepcopy(dist_all_time_range['mass']),
            'time': deepcopy(dist_all_time_range['time'][index]),
            'end_time':  deepcopy(dist_all_time_range['end_time'][index]),
            'data':  deepcopy(dist_all_time_range['data'][:, :, :, index]),
            'bins':  deepcopy(dist_all_time_range['bins'][:, :, :, index]),
            'energy':  deepcopy(dist_all_time_range['energy'][:, :, :, index]),
            'denergy':  deepcopy(dist_all_time_range['denergy'][:, :, :, index]),
            'n_energy': deepcopy(dist_all_time_range['n_energy']),
            'n_bins': deepcopy(dist_all_time_range['n_bins']),
            'phi':  deepcopy(dist_all_time_range['phi'][:, :, :, index]),
            'dphi':  deepcopy(dist_all_time_range['dphi'][:, :, :, index]),
            'n_phi': deepcopy(dist_all_time_range['n_phi']),
            'theta':  deepcopy(dist_all_time_range['theta'][:, :, :, index]),
            'dtheta':  deepcopy(dist_all_time_range['dtheta'][:, :, :, index]),
            'n_theta': deepcopy(dist_all_time_range['n_theta'])
        }

        if magf.ndim == 2:
            magvec = magf[index]
        elif magf.ndim == 1:
            magvec = magf

        clean_data = erg_pgs_clean_data(dist, units=units_lc, relativistic=relativistic ,magf=magvec, muconv=muconv)


        if 'mu_unit' in clean_data:
            val = clean_data['mu_unit']
            ysubtitle = val
        else:
            ysubtitle = None

        if fac_requested:
            pre_limit_bins = deepcopy(clean_data['bins'])

        clean_data = erg_pgs_limit_range(clean_data, phi=phi_in, theta=theta, energy=energy, no_ang_weighting=no_ang_weighting)

        #  ;;Build theta spectrogram
        if 'theta' in outputs_lc:
            out_theta_y[index, :], out_theta[index, :] = erg_pgs_make_theta_spec(clean_data, no_ang_weighting=no_ang_weighting)

        #  ;;Build energy spectrogram
        if 'energy' in outputs_lc:
            out_energy_y[index, :], out_energy[index, :] = erg_pgs_make_e_spec(clean_data)

        #  ;;Build phi spectrogram
        if 'phi' in outputs_lc:
            out_phi_y[index, :], out_phi[index, :] = erg_pgs_make_phi_spec(clean_data, resolution=dist['n_phi'],no_ang_weighting=no_ang_weighting)

        #  ;;Perform transformation to FAC, regrid data, and apply limits in new coords
        
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

            if 'gyro' in outputs_lc:
                # ;Build gyrophase spectrogram
                out_gyro_y[index, :], out_gyro[index, :] = erg_pgs_make_phi_spec(clean_data, resolution=regrid[0], no_ang_weighting=no_ang_weighting)

            if 'fac_energy' in outputs_lc:
                out_fac_energy_y[index, :], out_fac_energy[index, :] = erg_pgs_make_e_spec(clean_data)

    if 'energy' in outputs_lc:
        output_tplot_name = in_tvarname+'_energy' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_energy_y, z=out_energy, units=units, ylog=True, ytitle=dist['data_name'] + ' \\ energy (eV)',
                            relativistic=relativistic, ysubtitle=ysubtitle)
        out_vars.append(output_tplot_name)
    if 'theta' in outputs_lc:
        output_tplot_name = in_tvarname+'_theta' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_theta_y, z=out_theta, units=units, ylog=False, ytitle=dist['data_name'] + ' \\ theta (deg)',
                            relativistic=relativistic)
        out_vars.append(output_tplot_name)
    if 'phi' in outputs_lc:
        output_tplot_name = in_tvarname+'_phi' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_phi_y, z=out_phi, units=units, ylog=False, ytitle=dist['data_name'] + ' \\ phi (deg)',
                            relativistic=relativistic)
        out_vars.append(output_tplot_name)

    #  ;;Pitch Angle Spectrograms
    if 'pa' in outputs_lc:
        output_tplot_name = in_tvarname+'_pa' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_pad_y, z=out_pad, units=units, ylog=False, ytitle=dist['data_name'] + ' \\ PA (deg)',
                            relativistic=relativistic)
        out_vars.append(output_tplot_name)

    if 'gyro' in outputs_lc:
        output_tplot_name = in_tvarname+'_gyro' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_gyro_y, z=out_gyro, units=units, ylog=False, ytitle=dist['data_name'] + ' \\ gyro (deg)',
                            relativistic=relativistic)
        out_vars.append(output_tplot_name)


    if 'fac_energy' in outputs_lc:

        output_tplot_name = in_tvarname+'_energy_mag' + suffix
        erg_pgs_make_tplot(output_tplot_name, x=times_array, y=out_fac_energy_y, z=out_fac_energy, units=units, ylog=True, ytitle=dist['data_name'] + ' \\ energy (eV)',
                            relativistic=relativistic, ysubtitle=ysubtitle)
        out_vars.append(output_tplot_name)

    
    #  ;;Sort a data array by energy for (fac-)energy spectra
    if ('erg_lepe_' in in_tvarname)  and (made_et_spec):
        if 'energy' in outputs_lc:
            t_plot_name = in_tvarname+'_energy' + suffix
            get_data_energy = get_data(t_plot_name)
            energy_meta_data = get_data(t_plot_name, metadata=True)
        elif 'fac_energy' in outputs_lc:
            t_plot_name = in_tvarname+'_energy_mag' + suffix
            get_data_energy = get_data(t_plot_name)
            energy_meta_data = get_data(t_plot_name, metadata=True)
        
        if get_data_energy is not None:
            
            arange_time_indices = np.arange(get_data_energy[0].size)
            time_indices_repeat = np.repeat(np.array([arange_time_indices]).T, get_data_energy[1].shape[1], axis=1)
            time_indices_repeat_reshape =  time_indices_repeat.reshape((time_indices_repeat.size, 1))
            
            if get_data_energy[2].ndim == 1:
                arg_sort_axis_1 = np.repeat(np.argsort([get_data_energy[2]], axis=1), get_data_energy[0].size, axis=0)
            elif get_data_energy[2].ndim == 2:
                arg_sort_axis_1=np.argsort(get_data_energy[2], axis=1)

            arg_sort_axis_1_reshape = arg_sort_axis_1.reshape((arg_sort_axis_1.size, 1))

            indices_array =np.concatenate([time_indices_repeat_reshape, arg_sort_axis_1_reshape], axis=1)
            indices_list_0 = indices_array[:,0].tolist()
            indices_list_1 = indices_array[:,1].tolist()
            y_new_1d = get_data_energy[1][indices_list_0 , indices_list_1 ]
            y_new_2d = y_new_1d.reshape(get_data_energy[1].shape)
            v_new_1d = get_data_energy[2][indices_list_0 , indices_list_1]
            v_new_2d = v_new_1d.reshape(get_data_energy[2].shape)

            store_data(t_plot_name, data={'x':get_data_energy[0],
                                          'y':y_new_2d,
                                          'v':v_new_2d},
                        attr_dict=energy_meta_data)

    return out_vars

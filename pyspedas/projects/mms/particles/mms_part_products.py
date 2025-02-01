import logging
import numpy as np

from pytplot import get_data

from pyspedas.utilities.interpol import interpol
from pyspedas.particles.spd_part_products.spd_pgs_make_tplot import spd_pgs_make_tplot
from pyspedas.particles.spd_part_products.spd_pgs_limit_range import spd_pgs_limit_range
from pyspedas.particles.spd_part_products.spd_pgs_progress_update import spd_pgs_progress_update
from pyspedas.particles.spd_part_products.spd_pgs_do_fac import spd_pgs_do_fac
from pyspedas.particles.spd_part_products.spd_pgs_regrid import spd_pgs_regrid
from pyspedas.particles.moments.spd_pgs_moments import spd_pgs_moments
from pyspedas.particles.moments.spd_pgs_moments_tplot import spd_pgs_moments_tplot

from pyspedas.projects.mms.fpi_tools.mms_get_fpi_dist import mms_get_fpi_dist
from pyspedas.projects.mms.hpca_tools.mms_get_hpca_dist import mms_get_hpca_dist
from pyspedas.projects.mms.particles.mms_convert_flux_units import mms_convert_flux_units
from pyspedas.projects.mms.particles.mms_pgs_clean_data import mms_pgs_clean_data
from pyspedas.projects.mms.particles.mms_pgs_clean_support import mms_pgs_clean_support
from pyspedas.projects.mms.particles.mms_pgs_make_fac import mms_pgs_make_fac
from pyspedas.projects.mms.particles.mms_pgs_split_hpca import mms_pgs_split_hpca
from pyspedas.projects.mms.particles.mms_pgs_make_e_spec import mms_pgs_make_e_spec
from pyspedas.projects.mms.particles.mms_pgs_make_phi_spec import mms_pgs_make_phi_spec
from pyspedas.projects.mms.particles.mms_pgs_make_theta_spec import mms_pgs_make_theta_spec
from pyspedas.projects.mms.particles.mms_part_des_photoelectrons import mms_part_des_photoelectrons

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_part_products(in_tvarname,
                      units='eflux',
                      species='e',
                      data_rate='fast',
                      instrument='fpi',
                      probe='1',
                      output=['energy', 'theta', 'phi'],
                      energy=None,
                      phi=None,
                      theta=None,
                      pitch=None,
                      gyro=None,
                      mag_name=None,
                      pos_name=None,
                      fac_type='mphigeo',
                      sc_pot_name=None,
                      correct_photoelectrons=False,
                      zero_negative_values=False,
                      internal_photoelectron_corrections=False,
                      disable_photoelectron_corrections=False,
                      no_regrid=False,
                      regrid=[32, 16],
                      vel_name=None,
                      prefix='',
                      suffix=''):
    """
    Generate spectra and moments from 3D MMS particle data; note: this routine isn't
    meant to be called directly - see the wrapper mms_part_getspec instead.

    Input
    ----------
        in_tvarname: str
            Name of the tplot variable containing MMS 3D particle distribution data

    Parameters
    ----------
        units: str
            Specify units of output variables; must be 'eflux' to calculate moments

            valid options:
            'flux'   -  # / (cm^2 * s * sr * eV)
            'eflux'  -  eV / (cm^2 * s * sr * eV)  <default>
            'df_cm'  -  s^3 / cm^6
            'df_km'  -  s^3 / km^6

        species: str
            Specify the species of the input tplot variable

        data_rate: str
            Data rate of the input data

        instrument: str
            Instrument (FPI or HPCA)

        probe: int or str
            Spacecraft probe #

        output: str or list of str
            Output variables; options::

                'energy': energy spectrograms
                'theta': theta spectrograms
                'phi': phi spectrograms
                'pa': pitch-angle spectrograms
                'gyro': gyro-phase spectrograms
                'moments': plasma moments
                'fac_energy': energy spectrogram in field-aligned coordinates
                'fac_moments': moments in field-aligned coordinates

        energy: list of float
            Energy range [min, max], in eV

        phi: list of float
            Phi range [min, max], in degrees

        theta: list of float
            Theta range [min, max], in degrees

        pitch: list of float
            Pitch-angle range [min, max], in degrees

        gyro: list of float
            Gyro-angle range [min, max], in degrees

        mag_name: str
            Tplot variable containing magnetic field data for
            moments and FAC transformations

        pos_name: str
            Tplot variable containing spacecraft position for
            FAC transformations

        sc_pot_name: str
            Tplot variable containing spacecraft potential data
            for moments corrections

        fac_type: str
            Field aligned coordinate system variant; default: 'mphigeo'
            options: 'phigeo', 'mphigeo', 'xgse'

        correct_photoelectrons: bool
            Flag to correct FPI data for photoelectrons 
            (defaults to True for FPI electron data - disable with the parameter below)

        disable_photoelectron_corrections: bool
            Flag to disable FPI photoelectron corrections

        internal_photoelectron_corrections: bool
            Apply internal photoelectron corrections

        zero_negative_values: bool
            Turn negative values to 0 after doing the photoelectron corrections (DES)

        no_regrid: bool
            Flag to disable reegridding

        regrid: array of int
            Array giving dimensions of regridded data
            Default: [32,16]

        vel_name: str
            Name of tplot variable containing bulk velocity data

        prefix: str
            Prefix for output tplot variables. Default: ''

        suffix: str
            Suffix for output tplot variables. Default: ''
            
    Returns
    ----------
        Creates tplot variables containing spectrograms and moments

    """

    units = units.lower()
    if isinstance(probe, int):
        probe = str(probe)

    data_in = get_data(in_tvarname)

    if data_in is None:
        logging.error('Error, could not find the variable: ' + in_tvarname)
        return None

    if isinstance(output, str):
        output = output.split(' ')

    # Ensure prefix and suffix are not 'None'.  There are some internally-applied prefixes,
    # so we'll rename the input to user_prefix.

    if prefix is None:
        user_prefix = ''
    else:
        user_prefix = prefix

    if suffix is None:
        suffix = ''

    # If pitch angle or gyro angle limits are specified, replace 'energy' and 'moments'
    # with 'fac_energy' and 'fac_moments'

    output_lc = np.array([item.lower() for item in output])
    output_sub = []
    if pitch is not None or gyro is not None:
        for item in output_lc:
            if item == 'energy' and 'fac_energy' not in output_lc:
                output_sub.append('fac_energy')
            elif item == 'moments' and 'fac_moments' not in output_lc:
                output_sub.append('fac_moments')
            else:
                output_sub.append(item)
        output_lc = output_sub
    output = output_lc

    if instrument == 'fpi':
        dist_in = mms_get_fpi_dist(in_tvarname, species=species, probe=probe, data_rate=data_rate)
    elif instrument == 'hpca':
        dist_in = mms_get_hpca_dist(in_tvarname, species=species, probe=probe, data_rate=data_rate)
    else:
        logging.error('Error, unknown instrument: ' + instrument + '; valid options: fpi, hpca')
        return

    if instrument == 'hpca':
        data_times = mms_get_hpca_dist(in_tvarname, species=species, probe=probe, data_rate=data_rate, times=True)
    else:
        data_times = data_in.times

    # ntimes = len(data_times)
    ntimes = len(dist_in)

    # create rotation matrix to field aligned coordinates if needed
    fac_outputs = ['pa', 'gyro', 'fac_energy', 'fac_moments']
    fac_requested = len(set(output).intersection(fac_outputs)) > 0
    if fac_requested:
        fac_matrix = mms_pgs_make_fac(data_times, mag_name, pos_name, fac_type=fac_type)

        if fac_matrix is None:
            # problem creating the FAC matrices
            fac_requested = False

    out_energy = np.zeros((ntimes, dist_in[0]['n_energy']))
    out_energy_y = np.zeros((ntimes, dist_in[0]['n_energy']))
    out_theta = np.zeros((ntimes, dist_in[0]['n_theta']))
    out_phi = np.zeros((ntimes, dist_in[0]['n_phi']))
    out_theta_y = np.zeros((ntimes, dist_in[0]['n_theta']))
    out_phi_y = np.zeros((ntimes, dist_in[0]['n_phi']))
    if fac_requested:
        out_pad = np.zeros((ntimes, dist_in[0]['n_theta']))
        out_pad_y = np.zeros((ntimes, dist_in[0]['n_theta']))
        out_gyro = np.zeros((ntimes, dist_in[0]['n_phi']))
        out_gyro_y = np.zeros((ntimes, dist_in[0]['n_phi']))
        out_fac_energy = np.zeros((ntimes, dist_in[0]['n_energy']))
        out_fac_energy_y = np.zeros((ntimes, dist_in[0]['n_energy']))

    # moments
    if 'moments' in output:
        out_density = np.zeros(ntimes)
        out_avgtemp = np.zeros(ntimes)
        out_vthermal = np.zeros(ntimes)
        out_flux = np.zeros([ntimes, 3])
        out_velocity = np.zeros([ntimes, 3])
        out_mftens = np.zeros([ntimes, 6])
        out_ptens = np.zeros([ntimes, 6])
        #out_ttens = np.zeros([dist_in['n_times'], 3, 3])

    if 'fac_moments' in output:
        out_fac_density = np.zeros(ntimes)
        out_fac_avgtemp = np.zeros(ntimes)
        out_fac_vthermal = np.zeros(ntimes)
        out_fac_flux = np.zeros([ntimes, 3])
        out_fac_velocity = np.zeros([ntimes, 3])
        out_fac_mftens = np.zeros([ntimes, 6])
        out_fac_ptens = np.zeros([ntimes, 6])
        #out_fac_ttens = np.zeros([dist_in['n_times'], 3, 3])

    out_vars = []
    last_update_time = None

    if 'moments' in output or 'fac_moments' in output or correct_photoelectrons or internal_photoelectron_corrections:
        support_data = mms_pgs_clean_support(data_times, mag_name=mag_name, vel_name=vel_name, sc_pot_name=sc_pot_name)
        mag_data = support_data[0]
        scpot_data = support_data[2]

    if disable_photoelectron_corrections:
        correct_photoelectrons = False
        internal_photoelectron_corrections = False

    # Remind user that l2 moments should be used preferentially and FAC moments are experimental
    if 'moments' in output or 'fac_moments' in output:
        msg = """Moments generated with mms_part_products may be missing several important
corrections, including photoelectron removal and spacecraft potential.
The official moments released by the instrument teams include these and
are the scientific products that should be used for analysis."""
        logging.warning('==================================================================================')
        logging.warning('WARNING:')
        logging.warning(msg)
        logging.warning('==================================================================================')

    # grab the DES photoelectron model if needed
    if (instrument != 'fpi' or species != 'e') and (correct_photoelectrons or internal_photoelectron_corrections):
        logging.error('Photoelectron corrections only valid for DES; no corrections will be applied.')
        correct_photoelectrons = False
        internal_photoelectron_corrections = False

    if correct_photoelectrons or internal_photoelectron_corrections:
        fpi_photoelectrons = mms_part_des_photoelectrons(in_tvarname)

        if fpi_photoelectrons is None:
            logging.error('Photoelectron model missing for this date; re-run without photoelectron corrections')
            return

        # will need stepper parities for burst mode data
        if data_rate == 'brst':
            parity = get_data('mms'+probe+'_des_steptable_parity_brst')

        startdelphi = get_data('mms'+probe+'_des_startdelphi_count_'+data_rate)

    for i in range(0, ntimes):
        last_update_time = spd_pgs_progress_update(last_update_time=last_update_time, current_sample=i, total_samples=ntimes, type_string=in_tvarname)

        if instrument == 'fpi':
            dists = mms_get_fpi_dist(in_tvarname, index=i, species=species, probe=probe, data_rate=data_rate)
        elif instrument == 'hpca':
            dists = mms_get_hpca_dist(in_tvarname, index=i, species=species, probe=probe, data_rate=data_rate)

        if isinstance(dists, list):
            dist_in = dists[0]
        else:
            dist_in = dists

        # apply the DES photoelectron corrections
        if correct_photoelectrons or internal_photoelectron_corrections:
            # From Dan Gershman's release notes on the FPI photoelectron model:
            # Find the index I in the startdelphi_counts_brst or startdelphi_counts_fast array
            # [360 possibilities] whose corresponding value is closest to th = e measured
            # startdelphi_count_brst or startdelphi_count_fast for the skymap of interest. The
            # closest index can be approximated by I = floor(startdelphi_count_brst/16) or I =
            # floor(startdelphi_count_fast/16)
            startdelphi_I = int(np.floor(startdelphi.y[i]/16.0))

            if data_rate == 'brst':
                parity_num = str(int(np.fix(parity.y[i])))

                bg_dist = fpi_photoelectrons['bgdist_p'+parity_num]
                n_value = fpi_photoelectrons['n_'+parity_num]

                fphoto = bg_dist.y[startdelphi_I, :, :, :]

                # need to interpolate using SC potential data to get Nphoto value
                nphoto_scpot_dependent = n_value.y[startdelphi_I, :]
                nphoto = interpol(nphoto_scpot_dependent, n_value.v, scpot_data[i])
            else:
                fphoto = fpi_photoelectrons['bg_dist'].y[startdelphi_I, :, :, :]

                # need to interpolate using SC potential data to get Nphoto value
                nphoto_scpot_dependent = fpi_photoelectrons['n'].y[startdelphi_I, :]
                nphoto = interpol(nphoto_scpot_dependent, fpi_photoelectrons['n'].v, scpot_data[i])

            # now, the corrected distribution function is simply f_corrected = f-fphoto*nphoto
            # note: transpose is to shuffle fphoto*nphoto to energy-azimuth-elevation, to match dist.data
            correction = fphoto*nphoto
            corrected_df = dist_in['data']-correction.transpose([2, 0, 1])

            if zero_negative_values:
                corrected_df[corrected_df < 0] = 0.0

            dist_in['data'] = corrected_df

        data = mms_convert_flux_units(dist_in, units=units)

        clean_data = mms_pgs_clean_data(data)

        # split hpca angle bins to be equal width in phi/theta
        # this is needed when skipping the regrid step
        if instrument == 'hpca':
            clean_data = mms_pgs_split_hpca(clean_data)

        # Apply phi, theta, & energy limits
        if not fac_requested:
            if energy is not None or theta is not None or phi is not None:
                clean_data = spd_pgs_limit_range(clean_data, energy=energy, theta=theta, phi=phi)
        else:
            # Use pitch and gyro for theta and phi
            if energy is not None or pitch is not None or gyro is not None:
                clean_data = spd_pgs_limit_range(clean_data, energy=energy, theta=pitch, phi=gyro)


        # Build energy spectrogram
        if 'energy' in output:
            out_energy_y[i, :], out_energy[i, :] = mms_pgs_make_e_spec(clean_data)

        # Build theta spectrogram
        if 'theta' in output:
            out_theta_y[i, :], out_theta[i, :] = mms_pgs_make_theta_spec(clean_data, resolution=dist_in['n_theta'])

        # Build phi spectrogram
        if 'phi' in output:
            out_phi_y[i, :], out_phi[i, :] = mms_pgs_make_phi_spec(clean_data, resolution=dist_in['n_phi'])

        # Calculate the moments
        if 'moments' in output:
            if scpot_data is not None:
                scpot_val = scpot_data[i]
            else:
                scpot_val = 0.0

            moments = spd_pgs_moments(clean_data, sc_pot=scpot_val)
            out_density[i] = moments['density']
            out_avgtemp[i] = moments['avgtemp']
            out_vthermal[i] = moments['vthermal']
            out_flux[i, :] = moments['flux']
            out_velocity[i, :] = moments['velocity']
            out_mftens[i, :] = moments['mftens']
            out_ptens[i, :] = moments['ptens']

        # Perform transformation to FAC, regrid data, and apply limits in new coords
        if fac_requested:
            fac_data = spd_pgs_do_fac(clean_data, fac_matrix[i, :, :])

            if no_regrid == False:
                fac_data = spd_pgs_regrid(fac_data, regrid)

            fac_data['theta'] = 90.0-fac_data['theta']
            fac_data = spd_pgs_limit_range(fac_data, theta=pitch, phi=gyro)

        if 'pa' in output:
            out_pad_y[i, :], out_pad[i, :] = mms_pgs_make_theta_spec(fac_data, colatitude=True, resolution=dist_in['n_theta'])

        if 'gyro' in output:
            out_gyro_y[i, :], out_gyro[i, :] = mms_pgs_make_phi_spec(fac_data, resolution=dist_in['n_phi'])

        if 'fac_energy' in output:
            out_fac_energy_y[i, :], out_fac_energy[i, :] = mms_pgs_make_e_spec(clean_data)

        if 'fac_moments' in output:
            if scpot_data is not None:
                scpot_val = scpot_data[i]
            else:
                scpot_val = 0.0

            fac_moments = spd_pgs_moments(clean_data, sc_pot=scpot_val)
            out_fac_density[i] = fac_moments['density']
            out_fac_avgtemp[i] = fac_moments['avgtemp']
            out_fac_vthermal[i] = fac_moments['vthermal']
            out_fac_flux[i, :] = fac_moments['flux']
            out_fac_velocity[i, :] = fac_moments['velocity']
            out_fac_mftens[i, :] = fac_moments['mftens']
            out_fac_ptens[i, :] = fac_moments['ptens']

    if 'moments' in output:
        # put all of the moments arrays into a hash table prior to passing to the tplot routine
        moments = {'density': out_density, 
              'flux': out_flux, 
              'mftens': out_mftens, 
              'velocity': out_velocity, 
              'ptens': out_ptens,
              'vthermal': out_vthermal,
              'avgtemp': out_avgtemp}
        moments_vars = spd_pgs_moments_tplot(moments, x=data_times, prefix=user_prefix + in_tvarname, suffix=suffix)
        out_vars.extend(moments_vars)

    if 'fac_moments' in output:
        # put all of the moments arrays into a hash table prior to passing to the tplot routine
        fac_moments = {'density': out_fac_density,
              'flux': out_fac_flux,
              'mftens': out_fac_mftens,
              'velocity': out_fac_velocity,
              'ptens': out_fac_ptens,
              'vthermal': out_fac_vthermal,
              'avgtemp': out_fac_avgtemp}
        fac_moments_vars = spd_pgs_moments_tplot(fac_moments, x=data_times, prefix=user_prefix + in_tvarname+'_fac', suffix=suffix)
        out_vars.extend(fac_moments_vars)

    if 'energy' in output:
        spd_pgs_make_tplot(user_prefix + in_tvarname+'_energy' + suffix, x=data_times, y=out_energy_y, z=out_energy, units=units, ylog=True, ytitle=dist_in['data_name'], ysubtitle='energy (eV)')
        out_vars.append(user_prefix + in_tvarname+'_energy' + suffix)

    if 'fac_energy' in output:
        spd_pgs_make_tplot(user_prefix + in_tvarname+'_fac_energy' + suffix, x=data_times, y=out_fac_energy_y, z=out_fac_energy, units=units, ylog=True, ytitle=dist_in['data_name'], ysubtitle='energy (eV)')
        out_vars.append(user_prefix + in_tvarname+'_fac_energy' + suffix)

    if 'theta' in output:
        spd_pgs_make_tplot(user_prefix + in_tvarname+'_theta' + suffix, x=data_times, y=out_theta_y, z=out_theta, units=units, ytitle=dist_in['data_name'], ysubtitle='theta (deg)')
        out_vars.append(user_prefix + in_tvarname+'_theta' + suffix)

    if 'phi' in output:
        spd_pgs_make_tplot(user_prefix + in_tvarname+'_phi' + suffix, x=data_times, y=out_phi_y, z=out_phi, units=units, ytitle=dist_in['data_name'], ysubtitle='phi (deg)')
        out_vars.append(user_prefix + in_tvarname+'_phi' + suffix)

    if 'pa' in output:
        spd_pgs_make_tplot(user_prefix + in_tvarname+'_pa' + suffix, x=data_times, y=out_pad_y, z=out_pad, units=units, ytitle=dist_in['data_name'], ysubtitle='PA (deg)')
        out_vars.append(user_prefix + in_tvarname+'_pa' + suffix)

    if 'gyro' in output:
        spd_pgs_make_tplot(user_prefix + in_tvarname+'_gyro' + suffix, x=data_times, y=out_gyro_y, z=out_gyro, units=units, ytitle=dist_in['data_name'], ysubtitle='gyro (deg)')
        out_vars.append(user_prefix + in_tvarname+'_gyro' + suffix)

    return out_vars

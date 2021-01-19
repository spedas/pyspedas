import warnings
import numpy as np
from pyspedas import tnames
from pytplot import get_data, store_data, options
from pyspedas.mms.eis.mms_eis_pad_spinavg import mms_eis_pad_spinavg

def mms_eis_pad(scopes=['0', '1', '2', '3', '4', '5'], probe='1', level='l2', data_rate='srvy', datatype='extof', species='proton', data_units='flux', energy=[55, 800], size_pabin=15, suffix=''):
    """
    Calculate pitch angle distributions using data from the MMS Energetic Ion Spectrometer (EIS)
    
    Parameters:
        scopes: list of str
            telescope #s to include in the calculation

        probe: str
            probe #, e.g., '4' for MMS4

        level: str
            data level for calculation (default: 'l2')

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst' (default: 'srvy')

        datatype: str
            'extof' or 'phxtof' (default: 'extof')

        species: str
            species for calculation (default: 'proton')

        data_units: str
            'flux' or 'cps' (default: 'flux')

        energy: list of float
            energy range to include in the calculation (default: [55, 800])

        size_pabin: int
            size of the pitch angle bins, in degrees (default: 15)

        suffix: str
            suffix of the loaded data

    Returns:
        Name of tplot variables created.
    """

    # allow for the user to input probe, datatype and species as a string or a list of strings
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(datatype, list): datatype = [datatype]
    if not isinstance(species, list): species = [species]

    if data_units == 'cps':
        units_label = '1/s'
    else:
        units_label = '1/(cm^2-sr-s-keV)'

    if len(scopes) == 1:
        scope_suffix = '_t' + scopes + suffix
    elif len(scopes) == 6:
        scope_suffix = '_omni' + suffix

    # set up the number of pa bins to create
    n_pabins = 180./size_pabin
    pa_bins = [180.*n_pabin/n_pabins for n_pabin in range(0, int(n_pabins)+1)]
    pa_label = [180.*n_pabin/n_pabins+size_pabin/2. for n_pabin in range(0, int(n_pabins))]

    # Account for angular response (finite field of view) of instruments
    pa_halfang_width = 10.0 # deg
    delta_pa = size_pabin/2.

    out_vars = []

    # the probes will need to be strings beyond this point
    probe = [str(p) for p in probe]

    for probe_id in probe:
        if data_rate == 'brst':
            prefix = 'mms' + probe_id + '_epd_eis_brst_'
        else:
            prefix = 'mms' + probe_id + '_epd_eis_'

        for datatype_id in datatype:
            pa_data = get_data(prefix + datatype_id + '_pitch_angle_t0' + suffix)
            if pa_data is None:
                print('No ' + data_rate + ' ' + datatype_id + ' data is currently loaded for MMS' + probe_id + ' for the selected time period')
                return

            for species_id in species:
                pa_times, pa_data = get_data(prefix + datatype_id + '_pitch_angle_t0' + suffix)

                pa_file = np.zeros([len(pa_times), len(scopes)])

                omni_times, omni_data, omni_energies = get_data(prefix + datatype_id + '_' + species_id + '_' + data_units + '_omni' + suffix)
                erange = get_data(prefix + datatype_id + '_' + species_id + '_energy_range' + suffix)
                inchan_check_low = np.zeros(len(omni_energies))
                inchan_check_hi = np.zeros(len(omni_energies))
                inchan_check_low[np.where((erange[:, 0] >= energy[0]) & (erange[:, 0] <= energy[1]))[0]] = 1
                inchan_check_hi[np.where((erange[:, 1] >= energy[0]) & (erange[:, 1] <= energy[1]))[0]] = 1
                these_energies = np.where((inchan_check_low > 0) | (inchan_check_hi > 0))[0]

                if sum(inchan_check_low) == 0 or sum(inchan_check_hi) == 0:
                    print( 'Energy range selected is not covered by the detector for ' + datatype_id + ' ' + species_id + ' ' + data_units)
                    continue

                flux_file = np.zeros([len(pa_times), len(scopes), len(these_energies)])
                flux_file[:] = 'nan'
                pa_flux = np.zeros([len(pa_times), int(n_pabins), len(these_energies)])
                pa_flux[:] = 'nan'
                pa_num_in_bin = np.zeros([len(pa_times), int(n_pabins), len(these_energies)])

                for t, scope in enumerate(scopes):
                    pa_times, pa_data = get_data(prefix + datatype_id + '_pitch_angle_t' + scope + suffix)

                    pa_file[:, t] = pa_data

                    # use wild cards to figure out what this variable name should be for telescope 0
                    this_variable = tnames(prefix + datatype_id + '_' + species_id + '*_' + data_units + '_t0' + suffix)

                    if level == 'l2' or level == 'l1b':
                        if data_rate == 'brst':
                            pval_num_in_name = 6
                        else:
                            pval_num_in_name = 5
                        pvalue = this_variable[0].split('_')[pval_num_in_name]
                    else:
                        pvalue = ''

                    # get flux from each detector
                    flux_times, flux_data, flux_energies = get_data(prefix + datatype_id + '_' + species_id + '_' + pvalue + '_' + data_units + '_t' + scope + suffix)

                    # get energy range of interest
                    e = flux_energies[these_energies]

                    flux_file[:, t, :] = flux_data[:, these_energies]

                # CREATE PAD VARIABLES FOR EACH ENERGY CHANNEL IN USER-DEFINED ENERGY RANGE
                for i, flux_time in enumerate(flux_times):
                    for j, pa_bin in enumerate(range(0, int(n_pabins))):
                        for ee in range(0, len(these_energies)):
                            ind = np.where((pa_file[i, :] + pa_halfang_width >= pa_label[j] - delta_pa) & (pa_file[i, :] - pa_halfang_width < pa_label[j] + delta_pa))[0]
                            if ind.size != 0:
                                pa_flux[i, j, ee] = np.nanmean(flux_file[i, ind, ee], axis=0)

                for ee in range(0, len(these_energies)):
                    # energy_string = str(int(flux_energies[these_energies[ee]])) + 'keV'
                    energy_string = str(int(erange[these_energies[ee], 0])) + '_' + str(int(erange[these_energies[ee], 1])) + 'keV'
                    new_name = prefix + datatype_id + '_' + energy_string + '_' + species_id + '_' + data_units + scope_suffix + '_pad'
                    store_data(new_name, data={'x': flux_times, 'y': pa_flux[:, :, ee], 'v': pa_label})
                    options(new_name, 'ylog', False)
                    options(new_name, 'zlog', True)
                    options(new_name, 'spec', True)
                    options(new_name, 'Colormap', 'jet')
                    options(new_name, 'ztitle', units_label)
                    options(new_name, 'ytitle', 'MMS' + str(probe_id) + ' ' + datatype_id + ' PA (deg)')
                    out_vars.append(new_name)

                try:
                    store_data(prefix + datatype_id + '_' + species_id + '_' + data_units + scope_suffix + '_pads', data={'x': flux_times, 'y': pa_flux, 'v1': pa_label, 'v2': omni_energies[these_energies]})
                    out_vars.append(prefix + datatype_id + '_' + species_id + '_' + data_units + scope_suffix + '_pads')
                except ValueError: # kludge to avoid crash in case of single energy
                    print('Problem creating: ' + prefix + datatype_id + '_' + species_id + '_' + data_units + scope_suffix + '_pads')

                # only create the integral PAD variable if the user defined energy range covers more than 1 EIS energy channel
                if these_energies.size == 1:
                    continue

                # CREATE PAD VARIABLE INTEGRATED OVER USER-DEFINED ENERGY RANGE
                # energy_range_string = str(int(flux_energies[these_energies[0]])) + '-' + str(int(flux_energies[these_energies[-1]])) + 'keV'
                energy_range_string = str(int(erange[these_energies[0], 0])) + '-' + str(int(erange[these_energies[-1], 1])) + 'keV'
                new_name = prefix + datatype_id + '_' + energy_range_string + '_' + species_id + '_' + data_units + scope_suffix + '_pad'

                avg_pa_flux = np.zeros([len(flux_times), int(n_pabins)])
                avg_pa_flux[:] = 'nan'

                for tt in range(0, len(flux_times)):
                    for bb in range(0, int(n_pabins)):
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", category=RuntimeWarning)
                            avg_pa_flux[tt, bb] = np.nanmean(pa_flux[tt, bb, :])

                store_data(new_name, data={'x': flux_times, 'y': avg_pa_flux, 'v': pa_label})
                options(new_name, 'ylog', False)
                options(new_name, 'zlog', True)
                options(new_name, 'spec', True)
                options(new_name, 'Colormap', 'jet')
                options(new_name, 'ztitle', units_label)
                options(new_name, 'ytitle', 'MMS' + str(probe_id) + ' ' + datatype_id + ' PA (deg)')
                out_vars.append(new_name)

                spin_avg_pads = mms_eis_pad_spinavg(scopes=scopes, probe=probe_id, data_rate=data_rate, datatype=datatype_id, data_units=data_units, species=species_id, energy=energy, size_pabin=size_pabin, suffix=suffix)

                for spin_avg_pad in spin_avg_pads:
                    out_vars.append(spin_avg_pad)

    return out_vars

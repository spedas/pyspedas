import numpy as np
# use nanmean from bottleneck if it's installed, otherwise use the numpy one
# bottleneck nanmean is ~2.5x faster
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean
from pytplot import get_data, store_data, options
from ...utilities.tnames import tnames

def mms_eis_spec_combine_sc(
        species='proton', data_units='flux', datatype='extof', data_rate='srvy',
        level='l2', suffix='',
    ):
    '''
    Combines omni-directional energy spectrogram variable from EIS on multiple
        MMS spacecraft.

    Parameters
    ----------
        datatype: str
            'extof', 'electroenergy', or 'phxtof' (default: 'extof')

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst' (default: 'srvy')

        level: str
            data level ['l1a','l1b','l2pre','l2' (default)]

        data_units: str
            desired units for data, e.g., 'flux' or 'cps' (default: 'flux')

        suffix: str
            suffix of the loaded data; useful for preserving original tplot var

        species: str
            species for calculation, e.g., proton, oxygen, alpha or electron
            (default: 'proton')

    Returns:
        Name of tplot variables created.
    '''
    ## Thoughts for extensions:
    ## - Ensure arguments passed to modules are of lowecase

    if data_units == 'flux':
        units_label = 'Intensity\n[1/cm^2-sr-s-keV]'
    elif data_units == 'cps':
        units_label = 'CountRate\n[counts/s]'
    elif data_units == 'counts':
        units_label = 'Counts\n[counts]'

    #assert type(datatype) is str
    if not isinstance(species, list): species = [species]
    if not isinstance(datatype, list): datatype = [datatype]

    out_vars = []

    for species_id in species:
        for dtype in datatype:
            # retrieve: omni variables of species to determine # of probes
            _species = species_id
            if dtype == 'electronenergy':
                _species = 'electron'
            eis_sc_check = tnames('mms*eis*' + data_rate + '*' + dtype+'*' + _species + '*' + data_units + '*omni'+ suffix)

            # process multiple probes
            probes = []
            for name in eis_sc_check:
                probes.append(name[3:4])
            if len(probes) > 4:
                probes = probes[:-2]
            if len(probes) > 1:
                probe_string = probes[0] + '-' + probes[-1]
            else:
                if probes:
                    probe_string = probes[0]
                else:
                    print('No probes found from eis_sc_check tnames.')
                    return

            allmms_prefix = 'mmsx_epd_eis_' + data_rate + '_' + level + '_' + dtype + '_'

            # DETERMINE SPACECRAFT WITH SMALLEST NUMBER OF TIME STEPS TO USE
            # AS A REFERENCE SPACECRAFT
            omni_vars = tnames('mms?_epd_eis_'+data_rate+'_'+level+'_'+dtype+'_'+_species+'_'+data_units+'_omni'+suffix)

            if not omni_vars:
                print('No EIS '+dtype+'data loaded!')
                return

            time_size = np.zeros(len(probes))
            energy_size = np.zeros(len(probes))

            # Retrieve probe's pitch angle dist for all 6 (omni) telescopes
            for p, probe in enumerate(probes):
                # note: return from get_data here is (times, data, v)
                #       according to https://github.com/MAVENSDC/PyTplot/blob/ec87591521e84bae8d81caccaf64fc2a5785186f/pytplot/get_data.py#L66
                # note: there are also available 'spec_bins' values
                #print(pytplot.data_quants[omni_vars[p]].coords)
                #t, data, v = get_data(omni_vars[p])
                omni_times, omni_data, omni_energies = get_data(omni_vars[p])
                time_size[p] = len(omni_times)
                energy_size[p] = len(omni_energies)

            reftime_sc_loc = np.argmin(time_size)
            ref_sc_time_size = int(min(time_size))
            refenergy_sc_loc = np.argmin(energy_size)
            ref_sc_energy_size = int(min(energy_size))

            prefix = 'mms'+probes[reftime_sc_loc]+'_epd_eis_'+data_rate+'_'+level+'_'+dtype+'_'

            # Retrieve specific probe's data based on minimum time/energy
            # Note: I did not split these tuples as the namespace is reused, i.e., "_refprobe"
            time_refprobe = get_data(omni_vars[reftime_sc_loc])
            energy_refprobe = get_data(omni_vars[refenergy_sc_loc])

            # time x energy x spacecraft
            omni_spec_data = np.empty([len(time_refprobe[0]), len(energy_refprobe[2]), len(probes)])
            omni_spec_data[:] = np.nan
            # time x energy
            omni_spec = np.empty([len(time_refprobe[0]), len(energy_refprobe[2])])
            omni_spec[:] = np.nan

            energy_data = np.zeros([len(energy_refprobe[2]), len(probes)])
            common_energy = np.zeros(len(energy_refprobe[2]))

            # Average omni flux over all spacecraft and define common energy grid
            for pp in range(len(omni_vars)):
                temp_data = get_data(omni_vars[pp])
                energy_data[:,pp] = temp_data[2][0:len(common_energy)]
                omni_spec_data[0:ref_sc_time_size,:,pp] = temp_data[1][0:ref_sc_time_size,0:len(common_energy)]

            for ee in range(len(common_energy)):
                common_energy[ee] = nanmean(energy_data[ee,:], axis=0)

            # Average omni flux over all spacecraft
            for tt in range(len(time_refprobe[0])):
                for ee in range(len(energy_refprobe[2])):
                    omni_spec[tt,ee] = nanmean(omni_spec_data[tt,ee,:], axis=0)

            # store new tplot variable
            omni_spec[np.isnan(omni_spec)] = 0.
            new_name = allmms_prefix+_species+'_'+data_units+'_omni'
            store_data(new_name, data={'x':time_refprobe[0], 'y':omni_spec, 'v':energy_refprobe[2]})
            options(new_name, 'ylog', True)
            options(new_name, 'zlog', True)
            options(new_name, 'spec', True)
            options(new_name, 'Colormap', 'spedas')
            options(new_name, 'ztitle', units_label)
            options(new_name, 'ytitle', ' \\ '.join(['mms'+probe_string, _species.upper(), 'Energy [keV]']))
            out_vars.append(new_name)

            # Spin-average the data
            spin_nums = get_data(prefix+'spin'+suffix)
            if spin_nums is None:
                print('Error: Could not find EIS spin variable -- now ending procedure.')
                return

            # find where the spin starts
            _, spin_starts = np.unique(spin_nums[1], return_index=True)
            spin_sum_flux = np.zeros([len(spin_starts), len(omni_spec[0,:])])

            current_start = 0
            for spin_idx in range(len(spin_starts)):
                spin_sum_flux[spin_idx,:] = nanmean(omni_spec[current_start:spin_starts[spin_idx],:], axis=0)
                current_start = spin_starts[spin_idx] + 1

            sp = '_spin'
            new_name = allmms_prefix+_species+'_'+data_units+'_omni'+sp
            store_data(new_name, data={'x':spin_nums[0][spin_starts], 'y':spin_sum_flux, 'v':energy_refprobe[2]})
            options(new_name, 'spec', True)
            options(new_name, 'zlog', True)
            options(new_name, 'ylog', True)
            options(new_name, 'spec', True)
            out_vars.append(new_name)
    return out_vars

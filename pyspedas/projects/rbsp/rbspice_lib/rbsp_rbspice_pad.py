import logging
import numpy as np
from pytplot import get_data, store_data, options
from pyspedas.projects.rbsp.rbspice_lib.rbsp_rbspice_pad_spinavg import rbsp_rbspice_pad_spinavg

# use nanmean from bottleneck if it's installed, otherwise use the numpy one
# bottleneck nanmean is ~2.5x faster
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean


def rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3', energy=[0, 1000], bin_size=15, scopes=None):
    """
    Calculate pitch angle distributions using data from the
    RBSP Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE)
    
    Parameters
    ----------
    probe : str or list of str, default='a'
        Spacecraft probe name: 'a' or 'b'

    datatype: str, default='TOFxEH'
        desired data type: 'TOFxEH', 'TOFxEnonH'

    level : str, default='l3'
        data level: 'l1','l2','l3'

    energy : list, default=[0,1000]
        user-defined energy range to include in the calculation in keV

    bin_size : float, default=15
        desired size of the pitch angle bins in degrees

    scopes : list, optional
        string array of telescopes to be included in PAD [0-5, default is all]

    Returns
    -------
    out : list
        Tplot variables created

    Examples
    --------
    >>> rbspice_vars = pyspedas.projects.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEH', level='l3')
    >>> tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_spin')

    >>> # Calculate the pitch angle distributions
    >>> from pyspedas.projects.rbsp.rbspice_lib.rbsp_rbspice_pad import rbsp_rbspice_pad
    >>> rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3')
    >>> tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad')
    """
    if datatype == 'TOFxEH':
        species = 'proton'
    elif datatype == 'TOFxEnonH':
        species = ['helium', 'oxygen']
    elif datatype == 'TOFxPHHHELT':
        species = ['proton', 'oxygen']

    if not isinstance(species, list):
        species = [species]

    if level != 'l1':
        units_label = '1/(cm^2-sr-s-keV)'
    else:
        units_label = 'counts/s'
    if not energy:
        energy = [0, 1000]
    if not bin_size:
        bin_size = 15.
    if not scopes:
        scopes = [0, 1, 2, 3, 4, 5]
    
    prefix = 'rbsp'+probe+'_rbspice_'+level+'_'+datatype+'_'
    
    if energy[0] > energy[1]:
        logging.error('Low energy must be given first, then high energy in "energy" keyword')
        return
    
    # set up the number of pa bins to create
    bin_size = float(bin_size)
    n_pabins = int(180./bin_size)
    pa_bins = 180.*np.arange(n_pabins+1)/n_pabins
    pa_label = 180.*np.arange(n_pabins)/n_pabins+bin_size/2.
    
    logging.info('Num PA bins: ' + str(n_pabins))
    logging.info('PA bins: ' + str(pa_bins))
 
    # check to make sure the data exist
    d = get_data(prefix + 'Alpha')
    if d is None:
        logging.error('No '+datatype+' data is currently loaded for probe rbsp-'+probe+' for the selected time period')
        return

    logging.info('Calculating RBSPICE pitch angle distribution..')
    out = []

    for ion_type_idx in range(len(species)):
        # get pitch angle data (all telescopes in single variable)
        d_pa = get_data(prefix + 'Alpha')
        pa_file = np.zeros((len(d_pa.times), len(scopes))) # time steps, look direction
        for aa in range(len(scopes)):
            pa_file[:, scopes[aa]] = d_pa.y[:, scopes[aa]]

        pa_flux = np.zeros((len(d_pa.times), n_pabins, len(scopes)))
        pa_flux_nans = np.argwhere(pa_flux == 0)
        if len(pa_flux_nans) > 0:
            pa_flux[pa_flux_nans] = np.nan
        pa_num_in_bin = np.zeros((len(d_pa.times), n_pabins, len(scopes)))

        for qq in range(len(species)):
            # get flux data (all telescopes in single variable)
            d_flux = get_data(prefix + species[qq])
            d_flux_t0 = get_data(prefix + species[qq] + '_T0')

            logging.info(prefix + species[qq])
            flux_file = np.zeros((len(d_flux.times), len(scopes))) # time steps, look direction
            flux_file_nans = np.argwhere(flux_file == 0)
            if len(flux_file_nans) > 0:
                flux_file[flux_file_nans] = np.nan
            new_pa_flux = np.zeros((len(d_flux.times), n_pabins, len(scopes)))          # the average for each bin

            # get energy range of interest
            e = d_flux_t0.v
            indx = np.argwhere((e < energy[1]) & (e > energy[0]))

            if len(indx) == 0:
                logging.warning('Energy range selected is not covered by the detector for ' + datatype + ' ' + species[ion_type_idx])
                continue

            for t in range(len(scopes)):
                # Loop through each time step and get:
                # 1.  the total flux for the energy range of interest for each detector
                # 2.  flux in each pa bin
                for i in range(len(d_flux.times)): # loop through time
                    flux_file[i, t] = np.nansum(d_flux.y[i, indx, scopes[t]])  # start with lowest energy
                    for j in range(n_pabins): # loop through pa bins
                        if (pa_file[i, t] > pa_bins[j]) and (pa_file[i,t] < pa_bins[j+1]):
                            if not np.isfinite(pa_flux[i, j, t]):
                                pa_flux[i, j, t] = flux_file[i, t]
                            else:
                                pa_flux[i, j, t] = pa_flux[i, j, t] + flux_file[i, t]
                            pa_num_in_bin[i, j, t] += 1.0

                # loop over time
                for i in range(len(pa_flux[:, 0, 0])):
                    # loop over bins
                    for bin_idx in range(len(pa_flux[i, :, 0])):
                        if pa_num_in_bin[i, bin_idx, t] != 0.0:
                            new_pa_flux[i, bin_idx, t] = pa_flux[i, bin_idx, t]/pa_num_in_bin[i, bin_idx, t]
                        else:
                            new_pa_flux[i, bin_idx, t] = np.nan

            en_range_string = str(energy[0]) + '-' + str(energy[1]) + 'keV'
            if len(scopes) == 6:
                new_name = prefix+species[qq]+'_omni_'+en_range_string+'_pad'
                new_omni_pa_flux = np.zeros((len(new_pa_flux[:, 0, 0]),len(new_pa_flux[0, :, 0])))
                for ii in range(len(new_pa_flux[:, 0, 0])):
                    for jj in range(len(new_pa_flux[0, :, 0])):
                        new_omni_pa_flux[ii, jj] = nanmean(new_pa_flux[ii, jj, :])
                store_data(new_name, data={'x': d_flux.times, 'y': new_omni_pa_flux, 'v': pa_label})
                options(new_name, 'yrange', [0, 180])
                options(new_name, 'spec', True)
                options(new_name, 'zlog', True)
                options(new_name, 'ytitle', 'rbsp-'+probe+'\nrbspice\n'+species[ion_type_idx]+'\nomni')
                options(new_name, 'ysubtitle', en_range_string+'\nPA [Deg]')
                options(new_name, 'ztitle', units_label)
                out.append(new_name)
            else:
                new_name = []
                for ii in range(len(scopes)):
                    new_name.append(prefix+species[qq]+'_T'+str(scopes[ii])+'_'+en_range_string+'_pad')
                    store_data(new_name[ii], data={'x': d_flux.times, 'y': new_pa_flux[:, :, ii], 'v': pa_label})
                    options(new_name[ii], 'yrange', [0, 180])
                    options(new_name[ii], 'spec', True)
                    options(new_name[ii], 'zlog', True)
                    options(new_name[ii], 'ytitle', 'rbsp-'+probe+'\nrbspice\n' +species[ion_type_idx]+'\nT'+str(scopes[t]))
                    options(new_name[ii], 'ysubtitle', en_range_string + '\nPA [Deg]')
                    options(new_name[ii], 'ztitle', units_label)
                    out.append(new_name[ii])

            # now do the spin average
            sp_vars = rbsp_rbspice_pad_spinavg(probe=probe, datatype=datatype, species=species[ion_type_idx], energy=energy, bin_size=bin_size, scopes=scopes)
            if sp_vars is not None:
                out.extend(sp_vars)
    return out

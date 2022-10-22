import logging
import numpy as np
import scipy
from pytplot import get_data, store_data, options


def rbsp_rbspice_pad_spinavg(probe='a', datatype='TOFxEH', level='l3', species=None, energy=[0, 1000], bin_size=15., scopes=None):
    """
    Calculates spin-averaged PADs for the RBSPICE instrument
    
    Parameters
    ----------
    probe : str
        RBSP spacecraft indicator [Options: 'a' (default), 'b']
    datatype : str
        desired data type [Options: 'TOFxEH' (default), 'TOFxEnonH']
    level : str
        data level ['l1','l2','l3' (default),'l3pap']
    species : str
        desired ion species [Options: 'proton' (default), 'helium', 'oxygen']
    energy : list
        user-defined energy range to include in the calculation in keV [default = [0,1000]]
    bin_size : float
        desired size of the pitch angle bins in degrees [default = 15]
    scopes : list
        string array of telescopes to be included in PAD [0-5, default is all]
    """
    if probe is None:
        probe = 'a'
    if datatype is None:
        datatype = 'TOFxEH'
    if level is None:
        level = 'l3'
    if level != 'l1':
        units_label = '1/(cm^2-sr-s-keV)'
    else:
        units_label = 'counts/s'
    if species is None and datatype == 'TOFxEH':
        species = 'proton'
    elif species is None and datatype == 'TOFxEnonH':
        species = ['helium', 'oxygen']
    elif species is None and datatype == 'TOFxPHHHELT':
        species = ['proton', 'oxygen']
    if energy is None:
        energy = [0, 1000]
    if bin_size is None:
        bin_size = 15.
    if scopes is None:
        scopes = [0, 1, 2, 3, 4, 5]
    
    en_range_string = str(energy[0]) + '-' + str(energy[1]) + 'keV'
    
    prefix = 'rbsp'+probe+'_rbspice_'+level+'_'+datatype+'_'
    spin_nums = get_data(prefix + 'Spin')

    if spin_nums is None:
        logging.error('Spin variable not found: ' + prefix + 'Spin')
        return

    # find where the spins start
    spin_starts = np.unique(spin_nums.y, return_index=True)[1][1:]-1
    if len(scopes) == 6:
        pad_name = [prefix+species+'_omni_'+en_range_string+'_pad']
    else:
        pad_name = [prefix+species+'_T'+str(i)+'_'+en_range_string+'_pad' for i in scopes]

    for ii in range(len(pad_name)):
        pad_data = get_data(pad_name[ii])
        
        if pad_data is None:
            logging.error('Error, variable containing valid PAD data missing.')
            return

        # the following is for rebinning and interpolating to new_bins
        n_pabins = 180. / bin_size
        new_bins = 180. * np.arange(n_pabins + 1) / n_pabins
        srx = [float(len(pad_data.v)) / (int(n_pabins) + 1) * (x + 0.5) - 0.5 for x in range(int(n_pabins) + 1)]

        spin_sum_flux = np.zeros((len(spin_starts), len(pad_data.y[0, :])))
        rebinned_data = np.zeros((len(spin_starts), len(pad_data.y[0, :])+1))
        spin_times = np.zeros(len(spin_starts))
        
        current_start = 0
        # loop through the spins for this telescope
        for spin_idx in range(len(spin_starts)):
            # loop over energies
            spin_sum_flux[spin_idx,:] = np.nanmean(pad_data.y[current_start:spin_starts[spin_idx]+1,:], axis=0)
            spin_times[spin_idx] = pad_data.times[current_start]
            # rebin the data before storing it
            # the idea here is, for bin_size = 15 deg, rebin the data from center points to:
            #    new_bins = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135 , 150, 165, 180]
            spin_sum_interp = scipy.interpolate.interp1d(np.arange(len(spin_sum_flux[spin_idx, :])), spin_sum_flux[spin_idx, :], fill_value='extrapolate')
            rebinned_data[spin_idx, :] = spin_sum_interp(srx)

            # we want to take the end values instead of extrapolating
            # again, to match the functionality of congrid in IDL
            rebinned_data[spin_idx, 0] = spin_sum_flux[spin_idx, 0]
            rebinned_data[spin_idx, -1] = spin_sum_flux[spin_idx, -1]

            current_start = spin_starts[spin_idx]+1
        
        newname = pad_name[ii]+'_spin'
        if len(scopes) == 6:
            ytitle = 'rbsp-'+probe+'\nrbspice\n'+species+'\nomni'
        else:
            ytitle = 'rbsp-'+probe+'\nrbspice\n'+species+'\nT'+str(scopes[ii])

        store_data(newname, data={'x': spin_times, 'y': rebinned_data, 'v': new_bins})
        options(newname, 'spec', True)
        options(newname, 'zlog', True)
        options(newname, 'ztitle', units_label)
        options(newname, 'ytitle', ytitle)
        options(newname, 'yrange', [0, 180.0])
        options(newname, 'ysubtitle', en_range_string+'\nspin-avg PAD\n(deg)')

        #tdegap(newname, overwrite=True)

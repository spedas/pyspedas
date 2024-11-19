import logging
import numpy as np
from pytplot import get_data, store_data, options
from pytplot import tnames

# use nanmean from bottleneck if it's installed, otherwise use the numpy one
# bottleneck nanmean is ~2.5x faster
try:
    import bottleneck as bn
    nanmean = bn.nanmean
except ImportError:
    nanmean = np.nanmean


def rbsp_rbspice_spin_avg(probe='a', datatype='TOFxEH', level='l3'):
    """
    Calculates spin-averaged fluxes for the RBSPICE instrument
    
    Parameters
    ----------
    probe : str or list of str, default='a'
        Spacecraft probe name: 'a' or 'b'

    datatype: str, default='TOFxEH'
        desired data type: 'TOFxEH', 'TOFxEnonH'

    level : str, default='l3'
        data level: 'l1','l2','l3'

    Returns
    --------
    out, list
        Tplot variables created

    Examples
    --------
    This function is called within pyspedas.projects.rbsp.rbspice
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

    prefix = 'rbsp'+probe+'_rbspice_'+level+'_'+datatype+'_'

    spin_nums = get_data(prefix + 'Spin')
    if spin_nums is None:
        return
    spin_starts = np.unique(spin_nums.y, return_index=True)[1][1:]-1

    if datatype == 'TOFxEH':
        species = 'proton'
    elif datatype == 'TOFxEnonH':
        species = ['helium', 'oxygen']
    elif datatype == 'TOFxPHHHELT':
        species = ['proton', 'oxygen']

    if isinstance(species, list):
        var_data = []
        for spc in species:
            var_data.extend(tnames(prefix + spc + '_T?'))
            var_data.extend(tnames(prefix + spc + '_omni'))
    else:
        var_data = tnames(prefix + species + '_T?')
        var_omni = tnames(prefix + species + '_omni')
        var_data.extend(var_omni)

    logging.info('Calculating spin averaged energy spectra..')
    out = []
    zrange = None

    for n in range(len(var_data)):
        if var_data[n] == '':
            logging.error('Error, problem finding the tplot variables to calculate the spin averages')
            return
        else:
            flux_data = get_data(var_data[n])
            if len(flux_data) < 3:
                logging.error('Error, couldn''t find energy table for the flux/cps data variable')
                continue
            if var_data[n][-2:-1] == 'T':
                species = var_data[n][-9:-3]
            elif var_data[n][-4:] == 'omni':
                species = var_data[n][-11:-5]
            if species == 'proton':
                if datatype != 'TOFxPHHHELT':
                    zrange = [5., 1.e5]
                else:
                    zrange = [2.e2, 1.e6]
            elif species == 'helium':
                zrange = [1., 5.e2]
            elif species == 'oxygen':
                if datatype != 'TOFxPHHHELT':
                    zrange = [1., 1.e2]
                else:
                    zrange = [1e1, 1.e4]

            spin_sum_flux = np.zeros((len(spin_starts), len(flux_data.v)))
            current_start = 0
            for spin_idx in range(len(spin_starts)):
                spin_sum_flux[spin_idx, :] = nanmean(flux_data.y[current_start:spin_starts[spin_idx]+1, :], axis=0)
                current_start = spin_starts[spin_idx]+1
            sp = '_spin'
            if var_data[n][-4:] == 'omni':
                suffix = ''
            elif var_data[n][-2] == 'T'+str(n):
                suffix = '_T'+str(n)
            else:
                suffix = ''
            store_data(var_data[n]+sp+suffix, data={'x': spin_nums.times[spin_starts], 'y': spin_sum_flux, 'v': flux_data.v})
            options(var_data[n]+sp+suffix, 'ylog', True)
            options(var_data[n]+sp+suffix, 'zlog', True)
            options(var_data[n]+sp+suffix, 'spec', True)
            if zrange is not None:
                options(var_data[n]+sp+suffix, 'zrange', zrange)
            if isinstance(species, list):
                options(var_data[n]+sp+suffix, 'ytitle', 'rbsp'+probe+'\nrbspice\n'+datatype+'\n'+suffix)
            else:
                options(var_data[n]+sp+suffix, 'ytitle', 'rbsp'+probe+'\nrbspice\n'+species+'\n'+suffix)
            options(var_data[n]+sp+suffix, 'ysubtitle', '[keV]')
            options(var_data[n]+sp+suffix, 'ztitle', units_label)
            out.append(var_data[n]+sp+suffix)
    return out

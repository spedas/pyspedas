import logging
import numpy as np
from pytplot import get_data, store_data, options
from pyspedas import tnames


def rbsp_rbspice_spin_avg(probe='a', datatype='TOFxEH', level='l3'):
    """
    Calculates spin-averaged fluxes for the RBSPICE instrument
    
    Parameters
    ----------
    probe : str
        RBSP spacecraft indicator [Options: 'a' (default), 'b']
    datatype : str
        RBSPICE data type ['TOFxEH' (default),'TOFxEnonH']
    level : str
        data level ['l1','l2','l3' (default),'l3pap']
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
    probe = probe.strip()
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
    var_data = tnames(prefix + species + '_T?')
    var_omni = tnames(prefix + species + '_omni')
    var_data.extend(var_omni)
    for n in range(len(var_data)):
        if var_data[n] == '':
            logging.error('Error, problem finding the tplot variables to calculate the spin averages')
            return
        else:
            flux_data = get_data(var_data[n])
            if len(flux_data) < 3:
                logging.error('Error, couldn''t find energy table for the flux/cps data variable')
                continue
            if var_data[n][-1] == 'T':
                species = var_data[n][-7:]
            elif var_data[n][-4:] == 'omni':
                species = var_data[n][-7:]
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
                spin_sum_flux[spin_idx, :] = np.nanmean(flux_data.y[current_start:spin_starts[spin_idx]+1, :], axis=0)
                current_start = spin_starts[spin_idx]+1
            sp = '_spin'
            if var_data[n][-4:] == 'omni':
                suffix = '_omni'
            elif var_data[n][-2] == 'T'+str(n):
                suffix = '_T'+str(n)
            else:
                suffix = ''
            store_data(var_data[n]+sp+suffix, data={'x': spin_nums.times[spin_starts], 'y': spin_sum_flux, 'v': flux_data.v})
            options(var_data[n]+sp+suffix, 'ylog', True)
            options(var_data[n]+sp+suffix, 'zlog', True)
            options(var_data[n]+sp+suffix, 'spec', True)
            options(var_data[n]+sp+suffix, 'zrange', zrange)
            breakpoint()
            options(var_data[n]+sp+suffix, 'ytitle', 'rbsp'+probe+'\nrbspice\n'+species+'\n'+suffix)
            options(var_data[n]+sp+suffix, 'ysubtitle', '[keV]')
            options(var_data[n]+sp+suffix, 'ztitle', units_label)

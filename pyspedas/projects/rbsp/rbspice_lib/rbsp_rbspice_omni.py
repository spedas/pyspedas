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


def rbsp_rbspice_omni(probe='a', datatype='TOFxEH', level='l3'):
    """
    Calculates the omni-directional flux for all 6 telescopes
    
    Parameters
    ----------
    probe : str or list of str, default='a'
        Spacecraft probe name: 'a' or 'b'

    datatype: str, default='TOFxEH'
        RBSPICE data type::

         'EBR', 'ESRHELT', 'ESRLEHT', 'IBR', 'ISBR', 'ISRHELT',
         'TOFxEH', 'TOFxEIon', 'TOFxEnonH', 'TOFxPHHHELT', 'TOFxPHHLEHT'

        Values depends on different data levels.

    level : str, default='l3'
        data level: 'l1','l2','l3'

    Returns
    -------
    out : list
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
    
    # find the flux/cps data name(s)
    data_var = tnames(prefix + 'F*DU')
    
    if not data_var:
        logging.error('Error, problem finding the RBSPICE data to calculate omni-directional spectrograms')
        return

    logging.info('Calculating omni directional energy spectra; this might take a few minutes...')
    out = []

    for i in range(len(data_var)):
        species_str = data_var[i][-4:-2]
        if species_str == 'FP':
            species='proton'
            if datatype != 'TOFxPHHHELT':
                zrange = [5., 1.e5]
            else:
                zrange = [2.e2, 1.e6]
        elif species_str == 'He':
            species = 'helium'
            zrange = [1., 5.e2]
        elif species_str == 'FO':
            species = 'oxygen'
            if datatype != 'TOFxPHHHELT':
                zrange = [1., 1.e2]
            else:
                zrange = [1e1, 1.e4]
        
        # load the flux/cps data
        d = get_data(prefix+species)
        d_for_en_table = get_data(prefix+species+'_T0')
        
        if d is not None:
            flux_omni = np.zeros((len(d.times),len(d.y[0, :, 0])))
            for k in range(len(d.times)):
                for l in range(len(d.y[0, :, 0])):
                    flux_omni[k, l] = nanmean(d.y[k, l, :])
            newname = prefix+species+'_omni'
            store_data(newname, data={'x': d.times, 'y': flux_omni, 'v': d_for_en_table.v})
            options(newname, 'ylog', True)
            options(newname, 'zlog', True)
            options(newname, 'spec', True)
            options(newname, 'zrange', zrange)
            options(newname, 'ytitle', 'rbsp-'+probe+'\nrbspice\n'+species+'\nomni')
            options(newname, 'ysubtitle', '[keV]')
            options(newname, 'ztitle', units_label)
            out.append(newname)
    return out

import logging
from pytplot import get_data, store_data, options
from pytplot import tnames


def rbsp_load_rbspice_read(level='l3', probe='a', datatype='TOFxEH'):
    """
    Works on previously loaded RBSPICE tplot variables: adds energy channel energy values to primary data variable, separates non-H species variables,
    creates variables for individual telescopes, and sets appropriate tplot options
    
    Parameters
    ----------
    level : str, default='l3'
        data level 'l1','l2','l3'

    probe : str or list of str, default='a'
        Spacecraft probe name: 'a' or 'b'

    datatype : str, default='TOFxEH'
        RBSPICE data type: 'EBR','ESRHELT','ESRLEHT','IBR','ISBR','ISRHELT','TOFxEH' (default),'TOFxEIon','TOFxEnonH','TOFxPHHHELT','TOFxPHHLEHT'
        but change for different data levels.

    Returns
    -------
    None

    Examples
    --------
    This function is called within pyspedas.projects.rbsp.rbspice
    """
    if level != 'l1':
        units_label = '1/(cm^2-sr-s-keV)'
        convert_factor = 1000.              # to convert flux from 1/MeV to 1/keV
    else:
        units_label = 'counts/s'
        convert_factor = 1.                 # do not need to convert counts/s           

    prefix = 'rbsp'+probe+'_rbspice_'+level+'_'+datatype+'_'
    # find the flux/cps data name(s)
    data_var = tnames(prefix + 'F*DU')
    energy_var = tnames(prefix + 'F*DU_Energy')

    logging.info('Correcting RBSPICE energy tables...')
    for i in range(len(data_var)):
        en_data = get_data(energy_var[i])
        temp_energy = en_data.transpose()
        temp = get_data(data_var[i])
        data = temp.y.transpose([0, 2, 1])
        species_str = data_var[i][-4:-2]
        if species_str == 'FP':
            species='proton'
            yticks = 1
            if datatype != 'TOFxPHHHELT':
                new_energy = temp_energy[:,0] * 1000.           # convert energy from MeV to keV
                new_flux = data / convert_factor                # convert flux from 1/MeV to 1/keV
                zrange = [5.,1.e5]
            else:
                new_energy = temp_energy[11:-1,0] * 1000.       # convert energy from MeV to keV
                new_flux = data[:,11:-1,:] / convert_factor       # convert energy from MeV to keV
                zrange = [2.e2,1.e6]
        elif species_str == 'He':
            species='helium'
            yticks = 1
            new_energy = temp_energy[0:10,0] * 1000.          # convert energy from MeV to keV
            new_flux = data[:,0:10,:] / convert_factor        # convert flux from 1/MeV to 1/keV
            zrange = [1.,1.e3]
        elif species_str == 'FO':
            species='oxygen'
            yticks = 2
            if datatype != 'TOFxPHHHELT':
                new_energy = temp_energy[11:18,0] * 1000.       # convert energy from MeV to keV
                new_flux = data[:,11:18,:] / convert_factor     # convert flux from 1/MeV to 1/keV
                zrange = [1.,1.e2]
            else:
                new_energy = temp_energy[0:10,0] * 1000.        # convert energy from MeV to keV
                new_flux = data[:,0:10,:] / convert_factor      # convert flux from 1/MeV to 1/keV
                zrange = [1e1,1.e4]
        new_name = prefix+species
        # note: can't save the energy table here, due to the shape of new_flux
        # so we'll have to grab the energy table from the individual telescope
        # variables
        store_data(new_name, data={'x':temp.times, 'y':new_flux})
        options(new_name, 'ylog', True)
        options(new_name, 'zlog', True)
        options(new_name, 'zrange', zrange)
        options(new_name, 'ytitle', 'rbsp'+probe+'_rbspice_'+species)
        options(new_name, 'ysubtitle', 'Energy [keV]')
        options(new_name, 'ztitle', units_label)
        for j in range(6):
            store_data(new_name+'_T'+str(j), data={'x':temp.times, 'y':new_flux[:,:,j], 'v':new_energy})
            options(new_name+'_T'+str(j), 'spec', True)
            options(new_name+'_T'+str(j), 'ylog', True)
            options(new_name+'_T'+str(j), 'zlog', True)
            options(new_name+'_T'+str(j), 'zrange', zrange)
            options(new_name+'_T'+str(j), 'ytitle', 'rbsp'+probe+'_rbspice_'+species+'_T'+str(j))
            options(new_name+'_T'+str(j), 'ysubtitle', '[keV]')
            options(new_name+'_T'+str(j), 'ztitle', units_label)

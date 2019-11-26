from pyspedas import tnames
from pytplot import options, get_data, store_data

def mms_hpca_elevations():
    anode_theta = [123.75000, 101.25000, 78.750000, 56.250000, 33.750000, 
        11.250000, 11.250000, 33.750000, 56.250000, 78.750000, 
        101.25000, 123.75000, 146.25000, 168.75000, 168.75000, 
        146.25000]
    anode_theta[6:14] = [anode_val+180. for anode_val in anode_theta[6:14]]
    return anode_theta

def mms_hpca_anodes(fov=[0, 360]):
    anodes = mms_hpca_elevations()
    return [i for i, anode in enumerate(anodes) if anode >= float(fov[0]) and anode <= float(fov[1])]

def mms_hpca_sum_fov(times, data, angles, energies, fov=[0, 360], anodes=None):
    anodes_in_fov = mms_hpca_anodes(fov=fov)
    data_within_fov = data[:,anodes_in_fov,:]
    return data_within_fov.sum(axis=1)

def mms_hpca_avg_fov(times, data, angles, energies, fov=[0, 360], anodes=None):
    anodes_in_fov = mms_hpca_anodes(fov=fov)
    data_within_fov = data[:,anodes_in_fov,:]
    return data_within_fov.mean(axis=1)

def mms_hpca_calc_anodes(fov=[0, 360], probe='1', suffix=''):
    """
    This function will sum (or average, for flux) the HPCA data over the requested field-of-view (fov)
    
    Parameters:
        fov : list of int
            field of view, in angles, from 0-360

        probe : str
            probe #, e.g., '4' for MMS4

        suffix: str
            suffix of the loaded data

    Returns:
        List of tplot variables created.
    """
    sum_anodes = [a+suffix for a in ['*_count_rate', '*_RF_corrected', '*_bkgd_corrected', '*_norm_counts']]
    avg_anodes = ['*_flux'+suffix]
    output_vars = []
    species_map = {'hplus': 'H+', 'oplus': 'O+', 'heplus': 'He+', 'heplusplus': 'He++'}

    fov_str = '_elev_'+str(fov[0])+'-'+str(fov[1])

    for sum_anode in sum_anodes:
        vars_to_sum = tnames(sum_anode)

        for var in vars_to_sum:
            var_species = var.split('_')[2]
            times, data, angles, energies = get_data(var)

            updated_spectra = mms_hpca_sum_fov(times, data, angles, energies, fov=fov)

            store_data(var+fov_str, data={'x': times, 'y': updated_spectra, 'v': energies})
            options(var+fov_str, 'spec', True)
            options(var+fov_str, 'ylog', True)
            options(var+fov_str, 'zlog', True)
            options(var+fov_str, 'ztitle', species_map[var_species] + ' ' + var.split('_')[3] + ' (cm^2-s-sr-eV)^-1')
            options(var+fov_str, 'ytitle', species_map[var_species] + ' Energy (eV)')
            options(var+fov_str, 'Colormap', 'jet')
            output_vars.append(var+fov_str)

    for avg_anode in avg_anodes:
        vars_to_avg = tnames(avg_anode)

        for var in vars_to_avg:
            var_species = var.split('_')[2]
            times, data, angles, energies = get_data(var)

            updated_spectra = mms_hpca_avg_fov(times, data, angles, energies, fov=fov)

            store_data(var+fov_str, data={'x': times, 'y': updated_spectra, 'v': energies})
            options(var+fov_str, 'spec', True)
            options(var+fov_str, 'ylog', True)
            options(var+fov_str, 'zlog', True)
            options(var+fov_str, 'ztitle', species_map[var_species] + ' ' + var.split('_')[3] + ' (cm^2-s-sr-eV)^-1')
            options(var+fov_str, 'ytitle', species_map[var_species] + ' Energy (eV)')
            options(var+fov_str, 'Colormap', 'jet')
            output_vars.append(var+fov_str)
    return output_vars


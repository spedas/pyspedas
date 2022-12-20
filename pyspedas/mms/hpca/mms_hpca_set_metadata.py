
from pytplot import options
from pyspedas import tnames

def mms_hpca_set_metadata(probe='1', fov=[0, 360], suffix=''):
    """
    This function sets the plot metadata for HPCA data products, and is meant 
    to be called from the HPCA load routine

    Parameters:
        fov : list of int
            field of view, in angles, from 0-360

        probe : str
            probe #, e.g., '4' for MMS4
            
        suffix: str
            suffix of the loaded data

    Returns:
        None
    """
    prefix = 'mms'+str(probe)
    valid_density = prefix+'*_number_density'+suffix
    valid_vel = prefix+'*_ion_bulk_velocity*'+suffix
    valid_temp = prefix+'*_scalar_temperature'+suffix

    for var in tnames(valid_density):
        if var == prefix+'_hpca_hplus_number_density'+suffix: options(var, 'ytitle', 'H+ density')
        if var == prefix+'_hpca_heplus_number_density'+suffix: options(var, 'ytitle', 'He+ density')
        if var == prefix+'_hpca_heplusplus_number_density'+suffix: options(var, 'ytitle', 'He++ density')
        if var == prefix+'_hpca_oplus_number_density'+suffix: options(var, 'ytitle', 'O+ density')
        if var == prefix+'_hpca_oplusplus_number_density'+suffix: options(var, 'ytitle', 'O++ density')

    for var in tnames(valid_vel):
        if var == prefix+'_hpca_hplus_ion_bulk_velocity'+suffix:
            options(var, 'legend_names', ['Vx (H+)', 'Vy (H+)', 'Vz (H+)'])
            options(var, 'ytitle', 'H+ velocity')
        if var == prefix+'_hpca_heplus_ion_bulk_velocity'+suffix:
            options(var, 'legend_names', ['Vx (He+)', 'Vy (He+)', 'Vz (He+)'])
            options(var, 'ytitle', 'He+ velocity')
        if var == prefix+'_hpca_heplusplus_ion_bulk_velocity'+suffix:
            options(var, 'legend_names', ['Vx (He++)', 'Vy (He++)', 'Vz (He++)'])
            options(var, 'ytitle', 'He++ velocity')
        if var == prefix+'_hpca_oplus_ion_bulk_velocity'+suffix:
            options(var, 'legend_names', ['Vx (O+)', 'Vy (O+)', 'Vz (O+)'])
            options(var, 'ytitle', 'O+ velocity')
        if var == prefix+'_hpca_oplusplus_ion_bulk_velocity'+suffix:
            options(var, 'legend_names', ['Vx (O++)', 'Vy (O++)', 'Vz (O++)'])
            options(var, 'ytitle', 'O++ velocity')

    for var in tnames(valid_temp):
        if var == prefix+'_hpca_hplus_scalar_temperature'+suffix: options(var, 'ytitle', 'H+ temp')
        if var == prefix+'_hpca_heplus_scalar_temperature'+suffix: options(var, 'ytitle', 'He+ temp')
        if var == prefix+'_hpca_heplusplus_scalar_temperature'+suffix: options(var, 'ytitle', 'He++ temp')
        if var == prefix+'_hpca_oplus_scalar_temperature'+suffix: options(var, 'ytitle', 'O+ temp')
        if var == prefix+'_hpca_oplusplus_scalar_temperature'+suffix: options(var, 'ytitle', 'O++ temp')



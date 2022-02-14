from pyspedas import tnames
from pytplot import options

def mms_eis_set_metadata(tplotnames, data_rate='srvy', datatype='extof', suffix=''):
    """
    This function updates the metadata for the EIS data products
    
    Parameters
    ----------
        tplotnames : list of str
            list of tplot variables loaded by the load routine

        data_rate : str 
            Data rate

        datatype : str 
            EIS datatype loaded (extof or phxtof)
            
        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if datatype == 'extof':
        options(tnames('*_extof_proton_flux_omni*'), 'yrange', [55, 1000])
        # options(tnames('*_extof_alpha_flux_omni*'), 'yrange', [80, 650]) # removed in the latest files as of 3 Aug 2021
        options(tnames('*_extof_helium_flux_omni*'), 'yrange', [80, 650])
        options(tnames('*_extof_oxygen_flux_omni*'), 'yrange', [145, 950])
        options(tnames('*_extof_proton_flux_omni*'), 'x_interp', True)
        options(tnames('*_extof_proton_flux_omni*'), 'y_interp', True)
        options(tnames('*_extof_helium_flux_omni*'), 'x_interp', True)
        options(tnames('*_extof_helium_flux_omni*'), 'y_interp', True)
        options(tnames('*_extof_oxygen_flux_omni*'), 'x_interp', True)
        options(tnames('*_extof_oxygen_flux_omni*'), 'y_interp', True)
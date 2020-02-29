


from pyspedas import tnames
from pytplot import options

def mms_eis_set_metadata(tplotnames, data_rate='srvy', datatype='extof', suffix=''):
    """

    """
    if datatype == 'extof':
        options(tnames('*_extof_proton_flux_omni*'), 'yrange', [55, 1000])
        options(tnames('*_extof_alpha_flux_omni*'), 'yrange', [80, 650])
        options(tnames('*_extof_oxygen_flux_omni*'), 'yrange', [145, 950])

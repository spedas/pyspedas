import numpy as np 
from pytplot import get_data, store_data

def mms_fgm_remove_flags(probe, data_rate, level, suffix=''):
    """
    This function removes data flagged by the FGM 'flag' variable (flags > 0), 
    in order to only show science quality data by default.
    
    Parameters:
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FGM include 'brst' 'fast' 'slow' 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:

                times, flags = get_data('mms'+this_probe+'_fgm_flag_'+this_dr+'_'+this_lvl+suffix)
                times, gse_data = get_data('mms'+this_probe+'_fgm_b_gse_'+this_dr+'_'+this_lvl+suffix)
                times, gsm_data = get_data('mms'+this_probe+'_fgm_b_gsm_'+this_dr+'_'+this_lvl+suffix)
                times, dmpa_data = get_data('mms'+this_probe+'_fgm_b_dmpa_'+this_dr+'_'+this_lvl+suffix)
                times, bcs_data = get_data('mms'+this_probe+'_fgm_b_bcs_'+this_dr+'_'+this_lvl+suffix)

                flagged_data = np.where(flags != 0.0)[0]
                gse_data[flagged_data] = np.nan
                gsm_data[flagged_data] = np.nan
                dmpa_data[flagged_data] = np.nan
                bcs_data[flagged_data] = np.nan

                store_data('mms'+this_probe+'_fgm_b_gse_'+this_dr+'_'+this_lvl+suffix, data={'x': times, 'y': gse_data})
                store_data('mms'+this_probe+'_fgm_b_gsm_'+this_dr+'_'+this_lvl+suffix, data={'x': times, 'y': gsm_data})
                store_data('mms'+this_probe+'_fgm_b_dmpa_'+this_dr+'_'+this_lvl+suffix, data={'x': times, 'y': dmpa_data})
                store_data('mms'+this_probe+'_fgm_b_bcs_'+this_dr+'_'+this_lvl+suffix, data={'x': times, 'y': bcs_data})
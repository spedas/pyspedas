from pytplot import options
from pyspedas import tnames

def mms_fgm_set_metadata(probe, data_rate, level, instrument, suffix=''):
    """
    This function updates the metadata for FGM data products
    
    Parameters
    ----------
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FGM include 'brst' 'fast' 'slow' 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        instrument : str
            instrument; probably 'fgm'
            
        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    tvars = set(tnames())

    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:
                if 'mms'+str(this_probe)+'_'+instrument+'_b_gse_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gse_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gse_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Bx GSE', 'By GSE', 'Bz GSE', 'B total'])
                if 'mms'+str(this_probe)+'_'+instrument+'_b_gsm_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gsm_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gsm_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Bx GSM', 'By GSM', 'Bz GSM', 'B total'])
                if 'mms'+str(this_probe)+'_'+instrument+'_b_dmpa_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_dmpa_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_dmpa_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Bx DMPA', 'By DMPA', 'Bz DMPA', 'B total'])
                if 'mms'+str(this_probe)+'_'+instrument+'_b_bcs_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_bcs_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_bcs_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Bx BCS', 'By BCS', 'Bz BCS', 'B total'])

                if 'mms'+str(this_probe)+'_'+instrument+'_b_gse_'+this_dr+'_'+this_lvl+'_bvec'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gse_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gse_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'legend_names', ['Bx GSE', 'By GSE', 'Bz GSE'])
                if 'mms'+str(this_probe)+'_'+instrument+'_b_gsm_'+this_dr+'_'+this_lvl+'_bvec'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gsm_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_gsm_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'legend_names', ['Bx GSM', 'By GSM', 'Bz GSM'])
                if 'mms'+str(this_probe)+'_'+instrument+'_b_dmpa_'+this_dr+'_'+this_lvl+'_bvec'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_dmpa_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_dmpa_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'legend_names', ['Bx DMPA', 'By DMPA', 'Bz DMPA'])
                if 'mms'+str(this_probe)+'_'+instrument+'_b_bcs_'+this_dr+'_'+this_lvl+'_bvec'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_b_bcs_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'ytitle', 'MMS'+str(this_probe)+' FGM')
                    options('mms'+str(this_probe)+'_'+instrument+'_b_bcs_'+this_dr+'_'+this_lvl+'_bvec'+suffix, 'legend_names', ['Bx BCS', 'By BCS', 'Bz BCS'])

from pytplot import options
from pyspedas import tnames

def mms_edi_set_metadata(probe, data_rate, level, suffix=''):
    """
    This function updates the metadata for EDI data products
    
    Parameters
    ----------
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rate for EDI

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    instrument = 'edi'

    tvars = set(tnames())

    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:
                if 'mms'+str(this_probe)+'_'+instrument+'_vdrift_dsl_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_dsl_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDI drift velocity')
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_dsl_'+this_dr+'_'+this_lvl+suffix, 'color', ['b', 'g', 'r'])
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_dsl_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Vx DSL', 'Vy DSL', 'Vz DSL'])
                if 'mms'+str(this_probe)+'_'+instrument+'_vdrift_gse_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_gse_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDI drift velocity')
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_gse_'+this_dr+'_'+this_lvl+suffix, 'color', ['b', 'g', 'r'])
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_gse_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Vx GSE', 'Vy GSE', 'Vz GSE'])
                if 'mms'+str(this_probe)+'_'+instrument+'_vdrift_gsm_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_gsm_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDI drift velocity')
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_gsm_'+this_dr+'_'+this_lvl+suffix, 'color', ['b', 'g', 'r'])
                    options('mms'+str(this_probe)+'_'+instrument+'_vdrift_gsm_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Vx GSM', 'Vy GSM', 'Vz GSM'])
                if 'mms'+str(this_probe)+'_'+instrument+'_e_dsl_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_e_dsl_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDI e-field')
                    options('mms'+str(this_probe)+'_'+instrument+'_e_dsl_'+this_dr+'_'+this_lvl+suffix, 'color', ['b', 'g', 'r'])
                    options('mms'+str(this_probe)+'_'+instrument+'_e_dsl_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Ex DSL', 'Ey DSL', 'Ez DSL'])
                if 'mms'+str(this_probe)+'_'+instrument+'_e_gse_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_e_gse_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDI e-field')
                    options('mms'+str(this_probe)+'_'+instrument+'_e_gse_'+this_dr+'_'+this_lvl+suffix, 'color', ['b', 'g', 'r'])
                    options('mms'+str(this_probe)+'_'+instrument+'_e_gse_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Ex GSE', 'Ey GSE', 'Ez GSE'])
                if 'mms'+str(this_probe)+'_'+instrument+'_e_gsm_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_e_gsm_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDI e-field')
                    options('mms'+str(this_probe)+'_'+instrument+'_e_gsm_'+this_dr+'_'+this_lvl+suffix, 'color', ['b', 'g', 'r'])
                    options('mms'+str(this_probe)+'_'+instrument+'_e_gsm_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Ex GSM', 'Ey GSM', 'Ez GSM'])
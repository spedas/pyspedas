from pytplot import options
from pytplot import tnames


def mms_mec_set_metadata(probe, data_rate, level, suffix=''):
    """
    This function updates the metadata for MEC data products
    
    Parameters
    ----------
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rate for MEC

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'
            Not used (as of 29May2021)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list):
        probe = [probe]

    instrument = 'mec'

    tvars = set(tnames())

    for this_probe in probe:
        if 'mms'+str(this_probe)+'_'+instrument+'_r_eci'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_r_eci'+suffix, 'ytitle', 'MMS'+str(this_probe)+' position')
            options('mms'+str(this_probe)+'_'+instrument+'_r_eci'+suffix, 'legend_names', ['X ECI', 'Y ECI', 'Z ECI'])
        if 'mms'+str(this_probe)+'_'+instrument+'_r_gsm'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_r_gsm'+suffix, 'ytitle', 'MMS'+str(this_probe)+' position')
            options('mms'+str(this_probe)+'_'+instrument+'_r_gsm'+suffix, 'legend_names', ['X GSM', 'Y GSM', 'Z GSM'])
        if 'mms'+str(this_probe)+'_'+instrument+'_r_geo'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_r_geo'+suffix, 'ytitle', 'MMS'+str(this_probe)+' position')
            options('mms'+str(this_probe)+'_'+instrument+'_r_geo'+suffix, 'legend_names', ['X GEO', 'Y GEO', 'Z GEO'])
        if 'mms'+str(this_probe)+'_'+instrument+'_r_sm'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_r_sm'+suffix, 'ytitle', 'MMS'+str(this_probe)+' position')
            options('mms'+str(this_probe)+'_'+instrument+'_r_sm'+suffix, 'legend_names', ['X SM', 'Y SM', 'Z SM'])
        if 'mms'+str(this_probe)+'_'+instrument+'_r_gse'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_r_gse'+suffix, 'ytitle', 'MMS'+str(this_probe)+' position')
            options('mms'+str(this_probe)+'_'+instrument+'_r_gse'+suffix, 'legend_names', ['X GSE', 'Y GSE', 'Z GSE'])
        if 'mms'+str(this_probe)+'_'+instrument+'_r_gse2000'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_r_gse2000'+suffix, 'ytitle', 'MMS'+str(this_probe)+' position')
            options('mms'+str(this_probe)+'_'+instrument+'_r_gse2000'+suffix, 'legend_names', ['X GSE2000', 'Y GSE2000', 'Z GSE2000'])

        if 'mms'+str(this_probe)+'_'+instrument+'_v_eci'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_v_eci'+suffix, 'ytitle', 'MMS'+str(this_probe)+' velocity')
            options('mms'+str(this_probe)+'_'+instrument+'_v_eci'+suffix, 'legend_names', ['Vx ECI', 'Vy ECI', 'Vz ECI'])
        if 'mms'+str(this_probe)+'_'+instrument+'_v_gsm'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_v_gsm'+suffix, 'ytitle', 'MMS'+str(this_probe)+' velocity')
            options('mms'+str(this_probe)+'_'+instrument+'_v_gsm'+suffix, 'legend_names', ['Vx GSM', 'Vy GSM', 'Vz GSM'])
        if 'mms'+str(this_probe)+'_'+instrument+'_v_geo'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_v_geo'+suffix, 'ytitle', 'MMS'+str(this_probe)+' velocity')
            options('mms'+str(this_probe)+'_'+instrument+'_v_geo'+suffix, 'legend_names', ['Vx GEO', 'Vy GEO', 'Vz GEO'])
        if 'mms'+str(this_probe)+'_'+instrument+'_v_sm'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_v_sm'+suffix, 'ytitle', 'MMS'+str(this_probe)+' velocity')
            options('mms'+str(this_probe)+'_'+instrument+'_v_sm'+suffix, 'legend_names', ['Vx SM', 'Vy SM', 'Vz SM'])
        if 'mms'+str(this_probe)+'_'+instrument+'_v_gse'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_v_gse'+suffix, 'ytitle', 'MMS'+str(this_probe)+' velocity')
            options('mms'+str(this_probe)+'_'+instrument+'_v_gse'+suffix, 'legend_names', ['Vx GSE', 'Vy GSE', 'Vz GSE'])
        if 'mms'+str(this_probe)+'_'+instrument+'_v_gse2000'+suffix in tvars:
            options('mms'+str(this_probe)+'_'+instrument+'_v_gse2000'+suffix, 'ytitle', 'MMS'+str(this_probe)+' velocity')
            options('mms'+str(this_probe)+'_'+instrument+'_v_gse2000'+suffix, 'legend_names', ['Vx GSE2000', 'Vy GSE2000', 'Vz GSE2000'])

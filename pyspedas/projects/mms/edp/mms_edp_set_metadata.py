from pytplot import options
from pytplot import tnames


def mms_edp_set_metadata(probe, data_rate, level, suffix=''):
    """
    This function updates the metadata for EDP data products
    
    Parameters
    ----------
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rate for EDP

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    instrument = 'edp'

    tvars = set(tnames())

    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:
                if 'mms'+str(this_probe)+'_'+instrument+'_dce_gse_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_dce_gse_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDP DCE')
                    options('mms'+str(this_probe)+'_'+instrument+'_dce_gse_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Ex GSE', 'Ey GSE', 'Ez GSE'])
                if 'mms'+str(this_probe)+'_'+instrument+'_dce_dsl_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_dce_dsl_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDP DCE')
                    options('mms'+str(this_probe)+'_'+instrument+'_dce_dsl_'+this_dr+'_'+this_lvl+suffix, 'legend_names', ['Ex DSL', 'Ey DSL', 'Ez DSL'])
                if 'mms'+str(this_probe)+'_'+instrument+'_hfesp_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_hfesp_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' EDP HFesp')
                    options('mms'+str(this_probe)+'_'+instrument+'_hfesp_'+this_dr+'_'+this_lvl+suffix, 'ztitle', '(V/m)^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_hfesp_'+this_dr+'_'+this_lvl+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_hfesp_'+this_dr+'_'+this_lvl+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_hfesp_'+this_dr+'_'+this_lvl+suffix, 'spec', True)

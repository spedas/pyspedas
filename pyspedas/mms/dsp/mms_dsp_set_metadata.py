from pytplot import options
from pyspedas import tnames

def mms_dsp_set_metadata(probe, data_rate, level, suffix=''):
    """
    This function updates the metadata for DSP data products
    
    Parameters:
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rate for DSP

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]

    instrument = 'dsp'

    tvars = set(tnames())

    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:
                if 'mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP BPSD SCM1 [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix, 'ztitle', 'nT^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm1_'+this_dr+'_'+this_lvl+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP BPSD SCM2 [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix, 'ztitle', 'nT^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm2_'+this_dr+'_'+this_lvl+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP BPSD SCM3 [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix, 'ztitle', 'nT^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_scm3_'+this_dr+'_'+this_lvl+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP BPSD [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix, 'ztitle', 'nT^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_bpsd_omni_'+this_dr+'_'+this_lvl+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP EPSD [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix, 'ztitle', '(V/m)^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_omni'+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP EPSD-X [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix, 'ztitle', '(V/m)^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_x'+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP EPSD-Y [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix, 'ztitle', '(V/m)^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_y'+suffix, 'Colormap', 'jet')
                if 'mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix in tvars:
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix, 'ytitle', 'MMS'+str(this_probe)+' DSP EPSD-Z [Hz]')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix, 'ztitle', '(V/m)^2/Hz')
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix, 'spec', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix, 'ylog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix, 'zlog', True)
                    options('mms'+str(this_probe)+'_'+instrument+'_epsd_z'+suffix, 'Colormap', 'jet')
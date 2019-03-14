'''
  This crib sheet produces the MMS basic dayside figure

'''

from pyspedas import mms_load_fgm, mms_load_mec, mms_load_edp, mms_load_dsp, mms_load_fpi, mms_load_hpca
from pytplot import tplot, options, get_data, store_data
import numpy as np

probe = '1'
trange = ['2015-10-16', '2015-10-17']

mms_load_fgm(probe=probe, data_rate='srvy', trange=trange)
mms_load_mec(probe=probe, data_rate='srvy', trange=trange)
mms_load_fpi(probe=probe, data_rate='fast', datatype=['des-moms', 'dis-moms'], trange=trange)
mms_load_edp(probe=probe, datatype='scpot', trange=trange)
mms_load_edp(probe=probe, data_rate='fast', datatype='dce', trange=trange)
mms_load_edp(probe=probe, data_rate='srvy', datatype=['dce', 'hfesp'], trange=trange)
mms_load_dsp(probe=probe, data_rate='fast', datatype='bpsd', trange=trange)
mms_load_hpca(probe=probe, data_rate='srvy', datatype='ion', trange=trange)

times, data = get_data('mms'+probe+'_fgm_b_gsm_srvy_l2')

store_data('mms'+probe+'_b_gsm_vec', data={'x': times, 'y': data[:,0:3]}) # B-field vector
store_data('mms'+probe+'_b_gsm_mag', data={'x': times, 'y': data[:,3]}) # B-field magnitude

times, data = get_data('mms'+probe+'_edp_scpot_fast_l2')
store_data('mms'+probe+'_edp_fast_scpot_ln', data={'x': times, 'y': np.log(data)})

options('mms'+probe+'_dsp_bpsd_omni_fast_l2', 'ylog', True)
options('mms'+probe+'_dsp_bpsd_omni_fast_l2', 'zlog', True)
options('mms'+probe+'_dsp_bpsd_omni_fast_l2', 'Colormap', 'jet')
options('mms'+probe+'_edp_hfesp_srvy_l2', 'ylog', True)
options('mms'+probe+'_edp_hfesp_srvy_l2', 'zlog', True)
options('mms'+probe+'_edp_hfesp_srvy_l2', 'Colormap', 'jet')

tplot(['mms'+probe+'_b_gsm_vec', 
       'mms'+probe+'_b_gsm_mag', 
       'mms'+probe+'_dis_energyspectr_omni_fast', 
       'mms'+probe+'_des_energyspectr_omni_fast', 
       'mms'+probe+'_dis_numberdensity_fast', 
       'mms'+probe+'_edp_fast_scpot_ln', 
       'mms'+probe+'_dis_bulkv_gse_fast', 
                    # '_exb_vperp_z', 
                    # '_hpca_hplus_flux_elev_0-360', 
                    # '_hpca_oplus_flux_elev_0-360', 
        'mms'+probe+'_edp_dce_gse_fast_l2', 
        'mms'+probe+'_edp_hfesp_srvy_l2', 
        'mms'+probe+'_dsp_bpsd_omni_fast_l2'])

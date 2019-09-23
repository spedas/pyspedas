'''

This crib sheet shows how to load and plot DSP data

'''

from pyspedas import mms_load_dsp
from pytplot import tplot, options

# load the electric spectral density
mms_load_dsp(data_rate='fast', probe=1, datatype='epsd', level='l2')

options('mms1_dsp_epsd_omni', 'spec', True)
options('mms1_dsp_epsd_omni', 'zlog', True)
options('mms1_dsp_epsd_omni', 'ylog', True)
options('mms1_dsp_epsd_omni', 'Colormap', 'jet')
options('mms1_dsp_epsd_omni', 'zrange', [1e-14, 1e-4])
options('mms1_dsp_epsd_omni', 'yrange', [30, 1e5])

tplot(['mms1_dsp_epsd_omni'])

# load the magnetic spectral density
mms_load_dsp(data_rate='fast', probe=1, datatype='bpsd', level='l2')

options('mms1_dsp_bpsd_omni_fast_l2', 'spec', True)
options('mms1_dsp_bpsd_omni_fast_l2', 'zlog', True)
options('mms1_dsp_bpsd_omni_fast_l2', 'ylog', True)
options('mms1_dsp_bpsd_omni_fast_l2', 'Colormap', 'jet')
options('mms1_dsp_bpsd_omni_fast_l2', 'zrange', [1e-14, 10])
options('mms1_dsp_bpsd_omni_fast_l2', 'yrange', [10, 1e4])

# show the omni-directional SCM spectral density for MMS-1
tplot('mms1_dsp_bpsd_omni_fast_l2')

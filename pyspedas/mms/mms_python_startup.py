'''
Set the location of this file in the PYTHONSTARTUP environment variable to automatically import the routines below when Python starts
'''

from pyspedas.mms import mms_load_mec, mms_load_fgm, mms_load_scm, mms_load_edi, mms_load_edp, mms_load_eis, mms_load_feeps, mms_load_hpca, mms_load_fpi, mms_load_aspoc, mms_load_dsp, mms_load_fsm

from pytplot import options, ylim, zlim, tplot, tplot_names, get_data, store_data, del_data

from pyspedas import time_string, time_double, mms_eis_pad, mms_feeps_pad
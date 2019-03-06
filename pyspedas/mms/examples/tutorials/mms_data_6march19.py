'''
MMS Data in Python with pySPEDAS
Eric Grimes - egrimes@igpp.ucla.edu

*** Disclaimer: all of this is beta; please submit bug reports! ***
*** Load times can be slow for some MMS data - should be fixed soon! ***

Tentative agenda:
- Introduction
- Loading MMS Data in Python
- Plotting MMS Data in Python
- Analysis Tools
- Future Plans

'''

''' ==========================================================================

Introduction

pySPEDAS bleeding edge:
https://github.com/spedas/pyspedas

pyTplot:
https://github.com/MAVENSDC/PyTplot

MMS Datasets:
https://lasp.colorado.edu/mms/sdc/public/datasets/

========================================================================== ''' 

# installing: pip install pyspedas or download bleeding edge from Github
# configuration: edit mms_config.py
#                MMS_DATA_DIR environment variable
# PYTHONSTARTUP file: mms_python_startup.py - allows you to avoid having to manually import the load routines and basic tools

''' ==========================================================================

Loading MMS Data in Python

Load routines: 
    mms_load_xxx, where xxx is:
        MEC: Magnetic Ephemeris Coordinates
        FGM: Flux-gate Magnetometer
        SCM: Search-coil Magnetometer
        EDP: Electric field Double Probe (SDP+ADP)
        EDI: Electron Drift Instrument
        EIS: Energetic Ion Spectrometer 
        FEEPS: Fly's Eye Energetic Particle Sensor 
        HPCA: Hot Plasma Composition Analyzer
        FPI: Fast Plasma Investigation
        ASPOC: Active Spacecraft Potential Control

========================================================================== ''' 
from pyspedas.mms import mms_load_mec

# start by loading some ephemeris / coordinates data;
# the default trange is Oct 16, 2015, default probe is 1
# and the default data rate is 'srvy'
mms_load_mec(probe=4)

# find info on a load routine
help(mms_load_mec)

from pyspedas.mms import mms_load_fgm

# note that the keywords are the same as in IDL
mms_load_fgm(probe='4', data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'], time_clip=True)

# find which variables were loaded
from pytplot import tplot_names
tplot_names()

from pyspedas.mms import mms_load_edp

# load some burst mode electric field data
mms_load_edp(probe='4', data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'], time_clip=True)

from pyspedas import tnames

# the tnames function supports filtering with wild cards, e.g.,
# to find the E-field variables:
dce_vars = tnames('*_edp_dce_*')

# trange also accepts datetime objects
# note: be aware of potential time zone issues
from pyspedas.mms import mms_load_fpi
from datetime import datetime
from datetime import timezone as tz

start_time = datetime(year=2015, month=10, day=16, hour=13, minute=6, tzinfo=tz.utc)
end_time = datetime(year=2015, month=10, day=16, hour=13, minute=7, tzinfo=tz.utc)

mms_load_fpi(trange=[start_time, end_time], probe='4', datatype='des-moms', data_rate='brst')

# to return the actual data values, use get_data
from pytplot import get_data

times, fgm_data = get_data('mms4_fgm_b_gsm_brst_l2')

# times are unix time (seconds since 1 January 1970)
print(times[0])

# FGM data include the magnitude
fgm_data[0]

# you can convert the unix time to a string with time_string
from pyspedas import time_string

print(time_string(times[0]))

# and convert back to unix time using time_double
from pyspedas import time_double

print(time_double('2015-10-16 13:06:00.00451'))

# create new tplot variables with store_data
from pytplot import store_data

# save the B-field vector
store_data('b_vector', data={'x': times, 'y': fgm_data[:, 0:3]})
# save the B-field magnitude
store_data('b_mag', data={'x': times, 'y': fgm_data[:, 3]})

# the keywords are very flexible, e.g.,
from pyspedas.mms import mms_load_hpca, mms_load_eis, mms_load_feeps, mms_load_aspoc

# specify multiple probes as integers, and multiple datatypes
mms_load_hpca(probe=[1, 2, 4], data_rate='brst', datatype=['moments', 'ion'], trange=['2015-10-16/13:06', '2015-10-16/13:07'])


mms_load_eis(probe='4', data_rate='brst', datatype=['phxtof', 'extof'], trange=['2015-10-16/13:06', '2015-10-16/13:07'])
mms_load_feeps(get_support_data=True, probe=2, data_rate=['srvy', 'brst'], trange=['2015-10-16/13:06', '2015-10-16/13:07'])
mms_load_aspoc()

''' ==========================================================================

Plotting MMS Data in Python

========================================================================== ''' 

from pytplot import tplot

# like in IDL, pyTplot supports strings, lists of strings, as well as tplot variable #s
tplot('mms4_fgm_b_gsm_brst_l2')

tplot(['mms4_fgm_b_gsm_brst_l2', 'mms4_edp_dce_gse_brst_l2'])

# change the plot metadata
from pytplot import options
options('mms4_edp_dce_gse_brst_l2', 'color', ['b', 'g', 'r'])
options('mms4_edp_dce_gse_brst_l2', 'legend_names', ['Ex', 'Ey', 'Ez'])

tplot(['mms4_fgm_b_gsm_brst_l2', 'mms4_edp_dce_gse_brst_l2', 'mms4_des_energyspectr_omni_brst', 'mms4_des_pitchangdist_miden_brst'])

tplot('b_vector')
options('b_vector', 'ytitle', 'MMS4 FGM')
options('b_vector', 'color', ['b', 'g', 'r'])
options('b_vector', 'legend_names', ['Bx', 'By', 'Bz'])

tplot('b_vector')

# add vertical bars at certain times
from pytplot import timebar

timebar([time_double('2015-10-16/13:06:20'), time_double('2015-10-16/13:06:40')], varname='mms4_fgm_b_gsm_brst_l2')
tplot('mms4_fgm_b_gsm_brst_l2')

tplot(['mms4_des_numberdensity_brst', 'mms4_hpca_hplus_number_density'])

# set the y-axis to log scale
options('mms4_des_numberdensity_brst', 'ylog', True)
options('mms4_hpca_hplus_number_density', 'ylog', True)

tplot(['mms4_des_numberdensity_brst', 'mms4_hpca_hplus_number_density'])

''' ==========================================================================

Analysis Tools

========================================================================== ''' 

# subtract_average
from pyspedas import subtract_average

subtract_average('mms4_fgm_b_gsm_brst_l2')

tplot(['mms4_fgm_b_gsm_brst_l2', 'mms4_fgm_b_gsm_brst_l2-d'])

# subtract_median
from pyspedas import subtract_median

subtract_median('mms4_fgm_b_gsm_brst_l2')

tplot(['mms4_fgm_b_gsm_brst_l2', 'mms4_fgm_b_gsm_brst_l2-d', 'mms4_fgm_b_gsm_brst_l2-m'])

# time clip
from pyspedas import time_clip

time_clip(['mms4_fgm_b_gsm_brst_l2', 'mms4_fgm_b_gsm_brst_l2-d', 'mms4_fgm_b_gsm_brst_l2-m'], '2015-10-16/13:06:45', '2015-10-16/13:07', suffix='')

tplot(['mms4_fgm_b_gsm_brst_l2', 'mms4_fgm_b_gsm_brst_l2-d', 'mms4_fgm_b_gsm_brst_l2-m'])

# clip the data
from pyspedas import tclip

tclip(['mms4_fgm_b_gsm_brst_l2', 'mms4_fgm_b_gsm_brst_l2-d', 'mms4_fgm_b_gsm_brst_l2-m'], 0, 20, suffix='')

tplot(['mms4_fgm_b_gsm_brst_l2', 'mms4_fgm_b_gsm_brst_l2-d', 'mms4_fgm_b_gsm_brst_l2-m'])


''' ==========================================================================

Future Plans

- Speed up CDF load times 
- Searchable MMS events database 
- Corrected FEEPS omni-directional spectra 
- Omni-directional HPCA spectra (summed over anodes+spin averaged)
- Spin averaged EIS, FEEPS spectra 
- EIS, FEEPS pitch angle distributions 
- FPI lossy compression, error bars
- Read-only mirror support
- Tests, documentation, crib sheets

========================================================================== ''' 

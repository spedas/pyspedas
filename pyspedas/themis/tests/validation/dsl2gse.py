'''

This script prints several FGM data points in GSE coordinates after cotransing from DSL.

This is meant to be called from the IDL test suite for comparison with the data loaded via IDL SPEDAS

'''

import pyspedas
from pytplot import get_data
from pyspedas.themis.cotrans.dsl2gse import dsl2gse

thm_vars = pyspedas.themis.fgm(probe='a', level='l2')
thm_vars = pyspedas.themis.state(probe='a', get_support_data=True, varnames=['tha_spinras', 'tha_spindec'])

dsl2gse('tha_fgs_dsl', 'tha_spinras', 'tha_spindec', 'tha_fgs_gse_cotrans')

data = get_data('tha_fgs_gse_cotrans')

print(data[0][0:10].round(6).tolist())

print(data[1][1000].tolist())

print(data[1][5000].tolist())

print(data[1][10000].tolist())

print(data[1][20000].tolist())

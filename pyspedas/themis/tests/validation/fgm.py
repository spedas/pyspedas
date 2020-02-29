'''

This script loads and prints FGM data at several data points.

This is meant to be called from the IDL test suite for comparison with the data loaded via IDL SPEDAS

'''


import pyspedas
from pytplot import get_data

thm_vars = pyspedas.themis.fgm(probe='c', level='l2')

data = get_data('thc_fgs_dsl')

print(data[0][0:10].round(6).tolist())

print(data[1][1000].tolist())

print(data[1][5000].tolist())

print(data[1][10000].tolist())

print(data[1][20000].tolist())

# -*- coding: utf-8 -*-
"""
File:
    ex_dsl2gse.py

Description:
    Read tha_fgl_dsl and perform a dsl to gse transformation.

"""
import pyspedas
import pytplot


def ex_dsl2gse():
    """ Example of dsl2dse"""

    time_range = ['2017-03-23 00:00:00', '2017-03-23 23:59:59']
    pyspedas.load_data('themis', time_range, ['tha'], 'state', 'l1',
                       get_support_data=1,
                       varnames=['tha_spinras', 'tha_spindec'])
    pyspedas.load_data('themis', time_range, ['tha'], 'fgm', 'l2',
                       varnames=['tha_fgl_dsl'])

    pyspedas.dsl2gse('tha_fgl_dsl', 'tha_spinras', 'tha_spindec',
                     'tha_fgl_gse')

    d_in = pytplot.get_data('tha_fgl_dsl')
    pytplot.store_data('z_dsl', data={'x': d_in[0], 'y': d_in[1][:, 2]})
    d_out = pytplot.get_data('tha_fgl_gse')
    pytplot.store_data('z_gse', data={'x': d_out[0], 'y': d_out[1][:, 2]})

    pytplot.tplot_options('title', 'tha_fgl DSL and GSE, 2017-03-23')
    pytplot.tplot(['tha_fgl_dsl', 'tha_fgl_gse', 'z_dsl', 'z_gse'])

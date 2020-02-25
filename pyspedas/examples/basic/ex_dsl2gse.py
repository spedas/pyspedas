# -*- coding: utf-8 -*-
"""
File:
    ex_dsl2gse.py

Description:
    Load tha_fgl_dsl and perform a dsl to gse transformation.

Notes:
    To duplicate this example on IDL SPEDAS, run the following code:

    pro thm_crib_fgm4

        timespan, '2017-03-23', 1
        thm_load_state, probe='a', /get_support_data
        thm_load_fgm, lev=2, probe=['a']

        dsl2gse, 'tha_fgl_dsl', 'tha_state_spinras', 'tha_state_spindec',$
            'tha_fgl_gse'

        get_data, 'tha_fgl_dsl', data=d1
        get_data, 'tha_fgl_gse', data=d2
        z1 = d1.y[*,2]
        z2 = d2.y[*,2]
        store_data, 'z_dsl', d1.x, z1
        store_data, 'z_gse', d2.x, z2

        tplot, ['tha_fgl_dsl', 'tha_fgl_gse', 'z_dsl', 'z_gse']
    end

"""
import pyspedas
import pytplot
from pyspedas.themis.cotrans.dsl2gse import dsl2gse


def ex_dsl2gse():
    """ Example of dsl2dse"""

    time_range = ['2017-03-23 00:00:00', '2017-03-23 23:59:59']
    pyspedas.themis.state(probe='a', trange=time_range, get_support_data=True,
                          varnames=['tha_spinras', 'tha_spindec'])
    pyspedas.themis.fgm(probe='a', trange=time_range, varnames=['tha_fgl_dsl'])

    dsl2gse('tha_fgl_dsl', 'tha_spinras', 'tha_spindec', 'tha_fgl_gse')

    # Get the third component only
    d_in = pytplot.get_data('tha_fgl_dsl')
    pytplot.store_data('z_dsl', data={'x': d_in[0], 'y': d_in[1][:, 2]})
    d_out = pytplot.get_data('tha_fgl_gse')
    pytplot.store_data('z_gse', data={'x': d_out[0], 'y': d_out[1][:, 2]})

    # Plot
    pytplot.tplot_options('title', 'tha_fgl DSL and GSE, 2017-03-23')
    pytplot.tplot(['tha_fgl_dsl', 'tha_fgl_gse', 'z_dsl', 'z_gse'])

    # Return 1 as indication that the example finished without problems.
    return 1

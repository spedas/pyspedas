from pyspedas.tplot_tools import store_data, options, set_units, set_coords

def erg_pgs_moments_tplot(
    moments,
    x=None,
    prefix='',
    suffix=''
):

    if x is None:
        print('Error, no x-values specified')
        return

    if not isinstance(moments, dict):
        print('Error, the "moments" variable must be a hash table containing the moments')
        return

    moments_tplot_names = []
    for key in moments.keys():
        tplot_name = prefix + '_' + key + suffix
        store_data(tplot_name, data={'x': x, 'y': moments[key]})
        moments_tplot_names.append(tplot_name)

    options(prefix + '_density' + suffix, 'ysubtitle', '[1/cm^3]')
    options(prefix + '_density' + suffix, 'yrange', [1e-3, 5e+1])
    options(prefix + '_density' + suffix, 'ylog', 1)
    set_units(prefix + '_density' + suffix, '1/cm^3')

    options(prefix + '_velocity' + suffix, 'ysubtitle', '[km/s]')
    options(prefix + '_velocity' + suffix, 'yrange', [-2000., 2000.])
    set_units(prefix + '_velocity' + suffix, 'km/s')
    set_coords(prefix + '_velocity' + suffix, 'dsi')

    options(prefix + '_avgtemp' + suffix, 'ysubtitle', '[eV]')
    options(prefix + '_avgtemp' + suffix, 'yrange', [0., 40000.])
    set_units(prefix + '_avgtemp' + suffix, 'eV')

    options(prefix + '_flux' + suffix, 'ysubtitle', '[1/s/cm2]')
    options(prefix + '_flux' + suffix, 'yrange', [-1e9, 1e9])
    set_units(prefix + '_flux' + suffix, '1/(cm^2-sec)')
    set_coords(prefix + '_flux' + suffix, 'DSI')

    options(prefix + '_eflux' + suffix, 'ysubtitle', '[eV/s/cm2]')
    options(prefix + '_eflux' + suffix, 'yrange', [-1e9, 1e9])
    set_units(prefix + '_eflux' + suffix, 'eV/(cm^2-sec)')
    set_coords(prefix + '_eflux' + suffix, 'DSI')

    options(prefix + '_qflux' + suffix, 'ysubtitle', '[eV/s/cm2]')
    options(prefix + '_qflux' + suffix, 'yrange', [-1e12, 1e12])
    set_units(prefix + '_qflux' + suffix, 'eV/(cm^2-sec)')
    set_coords(prefix + '_qflux' + suffix, 'DSI')

    options(prefix + '_t3' + suffix, 'ysubtitle', '[eV]')
    options(prefix + '_t3' + suffix, 'yrange', [-1e12, 1e12])
    set_units(prefix + '_t3' + suffix, 'eV')
    set_coords(prefix + '_t3' + suffix, 'DSI')

    options(prefix + '_magt3' + suffix, 'ysubtitle', '[eV]')
    options(prefix + '_magt3' + suffix, 'yrange', [-1e12, 1e12])
    set_units(prefix + '_magt3' + suffix, 'eV')
    set_coords(prefix + '_magt3' + suffix, 'FA')

    options(prefix + '_mftens' + suffix, 'ysubtitle', '[eV/cm^3]')
    options(prefix + '_mftens' + suffix, 'Color', ['b', 'g', 'r', 'm', 'c', 'y'])
    options(prefix + '_mftens' + suffix, 'legend_names', ['momf_'+label_suffix
            for label_suffix in 'xx yy zz xy xz yz'.split(' ')])
    set_units(prefix + '_mftens' + suffix, 'eV/cm^3')
    set_coords(prefix + '_mftens' + suffix, 'DSI')

    options(prefix + '_ptens' + suffix, 'ysubtitle', '[eV/cm^3]')
    options(prefix + '_ptens' + suffix, 'Color', ['b', 'g', 'r', 'm', 'c', 'y'])
    options(prefix + '_ptens' + suffix, 'legend_names', ['P_'+label_suffix
            for label_suffix in 'xx yy zz xy xz yz'.split(' ')])
    options(prefix + '_ptens' + suffix, 'yrange', [1e+0, 1e+5])
    options(prefix + '_ptens' + suffix, 'ylog', 1)
    set_units(prefix + '_ptens' + suffix, 'eV/cm^3')
    set_coords(prefix + '_ptens' + suffix, 'DSI')

    options(prefix + '_symm_theta' + suffix, 'ysubtitle', '[deg]')
    set_units(prefix + '_symm_theta' + suffix, 'deg')

    options(prefix + '_symm_phi' + suffix, 'ysubtitle', '[deg]')
    set_units(prefix + '_symm_phi' + suffix, 'deg')

    options(prefix + '_symm_ang' + suffix, 'ysubtitle', '[deg]')
    set_units(prefix + '_symm_ang' + suffix, 'deg')

    return moments_tplot_names

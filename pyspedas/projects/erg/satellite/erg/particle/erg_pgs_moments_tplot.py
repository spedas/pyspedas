from pytplot import store_data, options

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

    options(prefix + '_density' + suffix, 'ysubtitle', '[1/cc]')
    options(prefix + '_density' + suffix, 'yrange', [1e-3, 5e+1])
    options(prefix + '_density' + suffix, 'ylog', 1)

    options(prefix + '_velocity' + suffix, 'ysubtitle', '[km/s]')
    options(prefix + '_velocity' + suffix, 'yrange', [-2000., 2000.])

    options(prefix + '_avgtemp' + suffix, 'ysubtitle', '[eV]')
    options(prefix + '_avgtemp' + suffix, 'yrange', [0., 40000.])
    
    options(prefix + '_flux' + suffix, 'ysubtitle', '[#/s/cm2]')
    options(prefix + '_flux' + suffix, 'yrange', [-1e9, 1e9])

    options(prefix + '_eflux' + suffix, 'ysubtitle', '[eV/s/cm2 ??]')
    options(prefix + '_eflux' + suffix, 'yrange', [-1e9, 1e9])

    options(prefix + '_mftens' + suffix, 'ysubtitle', '[eV/cm^3]')
    options(prefix + '_mftens' + suffix, 'Color', ['b', 'g', 'r', 'm', 'c', 'y'])
    options(prefix + '_mftens' + suffix, 'legend_names', ['momf_'+label_suffix
            for label_suffix in 'xx yy zz xy xz yz'.split(' ')])

    options(prefix + '_ptens' + suffix, 'ysubtitle', '[eV/cm^3]')
    options(prefix + '_ptens' + suffix, 'Color', ['b', 'g', 'r', 'm', 'c', 'y'])
    options(prefix + '_ptens' + suffix, 'legend_names', ['P_'+label_suffix
            for label_suffix in 'xx yy zz xy xz yz'.split(' ')])
    options(prefix + '_ptens' + suffix, 'yrange', [1e+0, 1e+5])
    options(prefix + '_ptens' + suffix, 'ylog', 1)

    return moments_tplot_names

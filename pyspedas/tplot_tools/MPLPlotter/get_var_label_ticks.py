def get_var_label_ticks(var_xr, times):
    out_ticks = []
    extras = var_xr.attrs['plot_options']['extras']
    var_label_format = extras.get('var_label_format')
    if var_label_format is None:
        var_label_format = '{:.2f}'
    for time in times:
        out_ticks.append(var_label_format.format(var_xr.interp(coords={'time': time}, kwargs={'fill_value': 'extrapolate', 'bounds_error': False}).values))
    return out_ticks

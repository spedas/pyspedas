import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
from datetime import datetime, timezone
from matplotlib.colors import LinearSegmentedColormap
import warnings
import pytplot


def specplot(var_data,
             var_times,
             this_axis,
             yaxis_options,
             zaxis_options,
             plot_extras,
             colorbars,
             axis_font_size,
             fig,
             variable,
             time_idxs=None,
             style=None):

    alpha = plot_extras.get('alpha')
    spec_options = {'shading': 'auto', 'alpha': alpha}
    ztitle = zaxis_options['axis_label']
    zlog = zaxis_options['z_axis_type']
    ylog = yaxis_options['y_axis_type']

    yrange = yaxis_options['y_range']
    if not np.isfinite(yrange[0]):
        yrange[0] = None
    if not np.isfinite(yrange[1]):
        yrange[1] = None

    if zaxis_options.get('z_range') is not None:
        zrange = zaxis_options['z_range']
    else:
        zrange = [None, None]
        
    if zaxis_options.get('axis_subtitle') is not None:
        zsubtitle = zaxis_options['axis_subtitle']
    else:
        zsubtitle = ''
    
    if zlog == 'log':
        spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])
    else:
        spec_options['norm'] = None
        spec_options['vmin'] = zrange[0]
        spec_options['vmax'] = zrange[1]

    cmap = None

    if plot_extras.get('colormap') is not None:
        cmap = plot_extras['colormap'][0]
    else:
        # default to the SPEDAS color map if the user doesn't have a MPL style set
        if style is None:
            cmap = 'spedas'
    
    # kludge to add support for the 'spedas' color bar
    if cmap == 'spedas':
        _colors = pytplot.spedas_colorbar
        spd_map = [(np.array([r, g, b])).astype(np.float64)/256 for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
        cmap = LinearSegmentedColormap.from_list('spedas', spd_map)
        
    spec_options['cmap'] = cmap

    out_values = var_data.y[time_idxs, :]

    if len(var_data) == 3:
        out_vdata = var_data.v
    else:
        print('Too many dimensions on the variable: ' + variable)
        return

    if len(out_vdata.shape) > 1:
        # time varying 'v', need to limit the values to those within the requested time range
        out_vdata = out_vdata[time_idxs, :]

    # automatic interpolation options
    if yaxis_options.get('x_interp') is not None:
        x_interp = yaxis_options['x_interp']

        # interpolate along the x-axis
        if x_interp:
            if yaxis_options.get('x_interp_points') is not None:
                nx = yaxis_options['x_interp_points']
            else:
                fig_size = fig.get_size_inches()*fig.dpi
                nx = fig_size[0]

            if zlog == 'log':
                zdata = np.log10(out_values)
            else:
                zdata = out_values

            zdata[zdata < 0.0] = 0.0
            zdata[zdata == np.nan] = 0.0

            spec_unix_times = np.array([(time - np.datetime64('1970-01-01T00:00:00')) / np.timedelta64(1, 's') for time in
                              var_data.times[time_idxs]])

            interp_func = interp1d(spec_unix_times, zdata, axis=0, bounds_error=False)
            out_times = np.arange(0, nx, dtype=np.float64)*(var_data.times[time_idxs][-1]-var_data.times[time_idxs][0])/(nx-1) + var_data.times[time_idxs][0]

            out_values = interp_func(out_times)

            if zlog == 'log':
                out_values = 10**out_values

            var_times = np.array(out_times, dtype='datetime64[s]')
            #var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in out_times]

    if yaxis_options.get('y_interp') is not None:
        y_interp = yaxis_options['y_interp']

        # interpolate along the y-axis
        if y_interp:
            if yaxis_options.get('y_interp_points') is not None:
                ny = yaxis_options['y_interp_points']
            else:
                fig_size = fig.get_size_inches()*fig.dpi
                ny = fig_size[1]

            if zlog == 'log':
                zdata = np.log10(out_values)
            else:
                zdata = out_values

            if ylog =='log':
                vdata = np.log10(out_vdata)
                ycrange = np.log10(yrange)
            else:
                vdata = out_vdata
                ycrange = yrange

            if not np.isfinite(ycrange[0]):
                ycrange = [np.min(vdata), yrange[1]]

            zdata[zdata < 0.0] = 0.0
            zdata[zdata == np.nan] = 0.0

            interp_func = interp1d(vdata, zdata, axis=1, bounds_error=False)
            out_vdata = np.arange(0, ny, dtype=np.float64)*(ycrange[1]-ycrange[0])/(ny-1) + ycrange[0]

            out_values = interp_func(out_vdata)

            if zlog == 'log':
                out_values = 10**out_values

            if ylog == 'log':
                out_vdata = 10**out_vdata

    # check for NaNs in the v values
    nans_in_vdata = np.argwhere(np.isfinite(out_vdata) == False)
    if len(nans_in_vdata) > 0:
        # to deal with NaNs in the energy table, we set those energies to 0
        # then apply a mask to the data values at these locations
        out_vdata_nonan = out_vdata.copy()
        times_with_nans = np.unique(nans_in_vdata[:, 0])
        for nan_idx in np.arange(0, len(times_with_nans)):
            this_time_idx = times_with_nans[nan_idx]
            out_vdata_nonan[this_time_idx, ~np.isfinite(out_vdata[this_time_idx, :])] = 0

        masked = np.ma.masked_where(~np.isfinite(out_vdata), out_values)
        out_vdata = out_vdata_nonan
        out_values = masked

    # check for negatives if zlog is requested
    if zlog =='log':
        out_values[out_values<0.0] = 0.0

    # create the spectrogram (ignoring warnings)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        im = this_axis.pcolormesh(var_times, out_vdata.T, out_values.T, **spec_options)

    # store everything needed to create the colorbars
    colorbars[variable] = {}
    colorbars[variable]['im'] = im
    colorbars[variable]['axis_font_size'] = axis_font_size
    colorbars[variable]['ztitle'] = ztitle
    colorbars[variable]['zsubtitle'] = zsubtitle
    return True

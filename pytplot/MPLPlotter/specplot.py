import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
from datetime import datetime, timezone
from matplotlib.colors import LinearSegmentedColormap
import warnings
import pytplot
import logging
import numpy as np
def specplot_resample(values, vdata, vdata_hi):

    '''This resamples the data given by in the values array, defined
       vdata, onto a higher resolution array given by the variable
       vdata_hi. Values is assumed to be (ntimes, nv), vdata can be 1
       or 2d.
    '''
    
    ny = len(vdata_hi) #vdata_hi is 1d, the same for all time intervals
    ntimes = values.shape[0]
    out_values = np.zeros((ntimes, ny), dtype=values.dtype)

    #need bin edges for V
    if len(vdata.shape) == 1:
        nv = vdata.shape[0]
        vdata_bins = np.zeros((nv+1), dtype=vdata.dtype)
        vdata_bins[0] = vdata[0] - (vdata[1]-vdata[0])/2.0
        vdata_bins[1:nv] = (vdata[0:nv-1]+vdata[1:nv])/2.0
        vdata_bins[nv] = vdata[nv-1]+(vdata[nv-1]-vdata[nv-2])/2.0
    else: #2-d V
        nv = vdata.shape[1]
        vdata_bins = np.zeros((ntimes,nv+1), dtype=vdata.dtype)
        vdata_bins[:,0] = vdata[:,0]-(vdata[:,1]-vdata[:,0])/2.0
        vdata_bins[:,1:nv] = (vdata[:,0:nv-1]+vdata[:,1:nv])/2.0
        vdata_bins[:,nv] = vdata[:,nv-1]+(vdata[:,nv-1]-vdata[:,nv-2])/2.0

    for j in range(ntimes):
        if len(vdata.shape) == 1:
            vtmp = vdata_bins
        else:
            vtmp = vdata_bins[j, :]

        for i in range(nv):
            # cannot do ss_ini = np.where(vdata_hi >= vdata_bins[i] and vdata_hi < vdata_bins[i+1])
            if vtmp[i] < vtmp[i+1]: #increasing values
                xxx = np.where(vdata_hi >= vtmp[i])
                yyy = np.where(vdata_hi <= vtmp[i+1])
                if xxx[0].size > 0 and yyy[0].size > 0:
                    ss_ini = np.intersect1d(xxx[0], yyy[0])
                    out_values[j, ss_ini] = values[j, i]
            elif vtmp[i] > vtmp[i+1]: #decreasing values, (e.g., THEMIS ESA)
                xxx = np.where(vdata_hi >= vtmp[i+1])
                yyy = np.where(vdata_hi <= vtmp[i])
                if xxx[0].size > 0 and yyy[0].size > 0:
                    ss_ini = np.intersect1d(xxx[0], yyy[0])
                    out_values[j, ss_ini] = values[j, i]

    return out_values



def specplot_resample_optimized(values, vdata, vdata_hi):
    """Optimized by ChatGPT
    """
    ny = len(vdata_hi)  # vdata_hi is 1d, the same for all time intervals
    ntimes = values.shape[0]
    out_values = np.zeros((ntimes, ny), dtype=values.dtype)

    # Need bin edges for V
    if len(vdata.shape) == 1:
        nv = vdata.shape[0]
        vdata_bins = np.zeros((nv + 1), dtype=vdata.dtype)
        vdata_bins[0] = vdata[0] - (vdata[1] - vdata[0]) / 2.0
        vdata_bins[1:nv] = (vdata[:-1] + vdata[1:]) / 2.0
        vdata_bins[nv] = vdata[-1] + (vdata[-1] - vdata[-2]) / 2.0
    else:  # 2-d V
        nv = vdata.shape[1]
        vdata_bins = np.zeros((ntimes, nv + 1), dtype=vdata.dtype)
        vdata_bins[:, 0] = vdata[:, 0] - (vdata[:, 1] - vdata[:, 0]) / 2.0
        vdata_bins[:, 1:nv] = (vdata[:, :-1] + vdata[:, 1:nv]) / 2.0
        vdata_bins[:, nv] = vdata[:, nv - 1] + (vdata[:, nv - 1] - vdata[:, nv - 2]) / 2.0

    for j in range(ntimes):
        if len(vdata.shape) == 1:
            vtmp = vdata_bins
        else:
            vtmp = vdata_bins[j, :]

        for i in range(nv):
            # Directly compute the indices for the condition instead of using np.intersect1d
            condition = (vdata_hi >= vtmp[i]) & (vdata_hi <= vtmp[i + 1])
            ss_ini = np.where(condition)[0]
            if ss_ini.size > 0:
                out_values[j, ss_ini] = values[j, i]

    return out_values

specplot_resample = specplot_resample_optimized

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
        # gracefully handle the case of all NaNs in the data, but log scale set
        if np.isnan(var_data.y).all():
            # no need to set a log scale if all the data values are NaNs
            spec_options['norm'] = None
            spec_options['vmin'] = zrange[0]
            spec_options['vmax'] = zrange[1]
        elif not np.any(var_data.y):
            # properly handle all 0s in the data
            spec_options['norm'] = mpl.colors.LogNorm(vmin=np.nanmin(var_data.v), vmax=np.nanmax(var_data.v))
        else:
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
        logging.warning('Too many dimensions on the variable: ' + variable)
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

            # convert to floats for the interpolation
            spec_unix_times = np.int64(var_data.times[time_idxs]) / 1e9

            # interpolate in the x-direction
            interp_func = interp1d(spec_unix_times, zdata, axis=0, bounds_error=False, kind='linear')
            out_times = np.arange(0, nx, dtype=np.float64)*(spec_unix_times[-1]-spec_unix_times[0])/(nx-1) + spec_unix_times[0]
            out_values = interp_func(out_times)

            if zlog == 'log':
                out_values = 10**out_values

            # convert back to datetime64 objects
            var_times = np.array(out_times*1e9, dtype='datetime64[ns]')

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

            if ylog == 'log':
                vdata = np.log10(out_vdata)
                ycrange = np.log10(yrange)
            else:
                vdata = out_vdata
                ycrange = yrange

            if not np.isfinite(ycrange[0]):
                ycrange = [np.min(vdata), yrange[1]]

            zdata[zdata < 0.0] = 0.0
            zdata[zdata == np.nan] = 0.0 #does not work

            #interp1d requires 1d vdata input
            if len(vdata.shape) == 1:
                interp_func = interp1d(vdata, zdata, axis=1, bounds_error=False)
                out_vdata = np.arange(0, ny, dtype=np.float64)*(ycrange[1]-ycrange[0])/(ny-1) + ycrange[0]
                out_values = interp_func(out_vdata)
            else: #2d vdata
                ntime_idxs = vdata.shape[0]
                nynew = int(ny)
                out_vdata = np.arange(0, ny, dtype=np.float64)*(ycrange[1]-ycrange[0])/(ny-1) + ycrange[0]
                out_values = np.zeros((ntime_idxs, nynew), dtype=vdata.dtype)
                for jm in range(len(time_idxs)):
                    interp_func = interp1d(vdata[jm,:], zdata[jm,:], bounds_error=False)
                    out_values[jm,:] = interp_func(out_vdata)

            if zlog == 'log':
                out_values = 10**out_values

            if ylog == 'log':
                out_vdata = 10**out_vdata

#Resample to a higher resolution y grid, similar to interp, but only if y_no_resample is set
    if yaxis_options.get('y_no_resample') is None or yaxis_options.get('y_no_resample') == 0:
        if ylog == 'log':
            #Account for negative or fill vaslues that are not NaN
            vgt0 = np.where(out_vdata > 0)[0]
            if vgt0.size == 0:
                print('ERROR in specplot.py: no nonzero V values')
            vmin = np.min(out_vdata[vgt0])

            vlt0 = np.where(out_vdata <= 0)[0]
            if vlt0.size > 0:
                out_vdata[vlt0] = vmin

            vdata = np.log10(out_vdata)
            
            if yrange[0] <= 0:
                yrange[0] = vmin
            ycrange = np.log10(yrange)
        else:
            vdata = out_vdata
            ycrange = yrange

        fig_size = fig.get_size_inches()*fig.dpi
        ny = fig_size[1]*5 #maybe this will work better
        vdata1 = np.arange(0, ny, dtype=np.float64)*(ycrange[1]-ycrange[0])/(ny-1) + ycrange[0]

        out_values1 = specplot_resample(out_values, vdata, vdata1)
        out_values = out_values1
        if ylog == 'log':
            out_vdata = 10**vdata1
        else:
            out_vdata = vdata1
    
    # check for NaNs in the v values
    nans_in_vdata = np.argwhere(np.isfinite(out_vdata) == False)
    if len(nans_in_vdata) > 0:
        # to deal with NaNs in the energy table, we set those energies to 0
        # then apply a mask to the data values at these locations
        #Allow for 1D vdata
        out_vdata_nonan = out_vdata.copy()
        times_with_nans = np.unique(nans_in_vdata[:, 0])
        for nan_idx in np.arange(0, len(times_with_nans)):
            this_time_idx = times_with_nans[nan_idx]
            out_vdata_nonan[this_time_idx, ~np.isfinite(out_vdata[this_time_idx, :])] = 0

        masked = np.ma.masked_where(~np.isfinite(out_vdata), out_values)
        out_vdata = out_vdata_nonan
        out_values = masked

    # check for negatives if zlog is requested
    if zlog == 'log':
        out_values[out_values < 0.0] = 0.0

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

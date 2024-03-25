import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
from datetime import datetime, timezone
from matplotlib.colors import LinearSegmentedColormap
import warnings
import pytplot
import logging



def specplot_resample(values, vdata, vdata_hi):
    """Specplot energy bin resampling

    Allows for monotonically increasing or decreasing bin values, and bins that change over time.
    Performance optimized by ChatGPT.
    """
    ny = len(vdata_hi)  # vdata_hi is 1d, the same for all time intervals
    ntimes = values.shape[0]
    out_values = np.zeros((ntimes, ny), dtype=values.dtype)

    # Prepare bin edges
    if len(vdata.shape) == 1:
        nv = vdata.shape[0]
        vdata_bins = np.zeros(nv + 1, dtype=vdata.dtype)
        vdata_bins[0] = vdata[0] - (vdata[1] - vdata[0]) / 2.0
        vdata_bins[1:nv] = (vdata[:-1] + vdata[1:]) / 2.0
        vdata_bins[nv] = vdata[-1] + (vdata[-1] - vdata[-2]) / 2.0
    else:  # 2-d V
        nv = vdata.shape[1]
        vdata_bins = np.zeros((ntimes, nv + 1), dtype=vdata.dtype)
        vdata_bins[:, 0] = vdata[:, 0] - (vdata[:, 1] - vdata[:, 0]) / 2.0
        vdata_bins[:, 1:nv] = (vdata[:, :-1] + vdata[:, 1:nv]) / 2.0
        vdata_bins[:, nv] = (
            vdata[:, nv - 1] + (vdata[:, nv - 1] - vdata[:, nv - 2]) / 2.0
        )

    # Note that vdata_hi is always monotonically increasing, but
    # vdata_bins can be monotonically decreasing
    
    for j in range(ntimes):
        if len(vdata.shape) == 1:
            vtmp = vdata_bins
        else:
            vtmp = vdata_bins[j, :]

        bin_start_idx = 0  # Initialize bin start index
        bin_end_idx = ny-1
        for i in range(nv):
            # Find the start and end of the current bin in vdata_hi
            # The assumption that vdata_hi is monotonically increasing
            # or decreasing allows us to break early from the inner
            # loop (k) as soon as we find that an element falls
            # outside the current bin, knowing that no further
            # elements can belong to this bin.
            if vtmp[i] < vtmp[i + 1]:  # increasing bin values
                for k in range(bin_start_idx, ny):
                    # Check if within bin range, count until
                    # either the next value is out of range or
                    # there are no more values
                    if vdata_hi[k] >= vtmp[i] and (
                            k == ny - 1 or vdata_hi[k + 1] >= vtmp[i + 1]
                    ):
                        bin_end_idx = (
                            k + 1 if k != ny - 1 else ny
                        )  # Handle last element edge case
                        out_values[j, bin_start_idx:bin_end_idx] = values[j, i]
                        bin_start_idx = bin_end_idx  # Update for next bin
                        break
            elif vtmp[i] > vtmp[i+1]: # For decreasing vtmp, similar logic in reverse
                for k in range(bin_end_idx, 0, -1):
                    if vdata_hi[k] <= vtmp[i] and (
                            k ==  0 or vdata_hi[k - 1] <= vtmp[i+1]
                    ):
                            bin_start_idx = k -1 if k != 0 else 0
                            out_values[j, bin_start_idx:bin_end_idx] = values[j, i]
                            bin_end_idx = bin_start_idx
                            break

        # It looks like the above loop has some sort of fencepost error, where not all elements of out_values are set.
        # For THEMIS keograms, it's the highest index of out_values[j,:].  Maybe the lowest index is wrong if the
        # bin values are decreasing?  Set both just to be safe.
        out_values[j, 0] = values[j, 0]
        out_values[j, ny - 1] = values[j, nv - 1]

    return out_values



def specplot(
    var_data,
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
    style=None,
):
    alpha = plot_extras.get("alpha")
    spec_options = {"shading": "auto", "alpha": alpha}
    ztitle = zaxis_options["axis_label"]
    zlog = zaxis_options["z_axis_type"]
    ylog = yaxis_options["y_axis_type"]

    yrange = yaxis_options["y_range"]
    if not np.isfinite(yrange[0]):
        yrange[0] = None
    if not np.isfinite(yrange[1]):
        yrange[1] = None

    if zaxis_options.get("z_range") is not None:
        zrange = zaxis_options["z_range"]
    else:
        zrange = [None, None]

    if zaxis_options.get("axis_subtitle") is not None:
        zsubtitle = zaxis_options["axis_subtitle"]
    else:
        zsubtitle = ""


    #set -1.e31 fill values to NaN, jmjm, 2024-02-29
    ytp = np.where(var_data.y==-1.e31,np.nan,var_data.y)
    var_data.y[:,:] = ytp[:,:]
    if hasattr(var_data, 'v'):
        vtp = np.where(var_data.v==-1.e31,np.nan,var_data.v)
        if len(vtp.shape) == 1:
            var_data.v[:] = vtp[:]
        else:
            var_data.v[:,:] = vtp[:,:]
        vmin = np.nanmin(var_data.v)
        vmax = np.nanmax(var_data.v)
    #for v1,v2 too
    if hasattr(var_data, 'v1'):
        if 'spec_dim_to_plot' in plot_extras:
            if plot_extras['spec_dim_to_plot'] == 'v1':
                vtp = np.where(var_data.v1==-1.e31,np.nan,var_data.v1)
                if len(vtp.shape) == 1:
                    var_data.v1[:] = vtp[:]
                else:
                    var_data.v1[:,:] = vtp[:,:]
                vmin = np.nanmin(var_data.v1)
                vmax = np.nanmax(var_data.v1)
    if hasattr(var_data, 'v2'):
        if 'spec_dim_to_plot' in plot_extras:
            if plot_extras['spec_dim_to_plot'] == 'v2':
                vtp = np.where(var_data.v2==-1.e31,np.nan,var_data.v2)
                if len(vtp.shape) == 1:
                    var_data.v2[:] = vtp[:]
                else:
                    var_data.v2[:,:] = vtp[:,:]
                vmin = np.nanmin(var_data.v2)
                vmax = np.nanmax(var_data.v2)

    #could also have a fill in yrange
    #    if yrange[0] == -1e31: #This does not work sometimes?
    if yrange[0] < -0.9e31:
        yrange[0] = vmin
    if yrange[1] < -0.9e31:
        yrange[1] = vmax

    if zlog == "log":
        zmin = np.nanmin(var_data.y)
        zmax = np.nanmax(var_data.y)
        # gracefully handle the case of all NaNs in the data, but log scale set
        # all 0 is also a problem, causes a crash later when creating the colorbar
        if np.isnan(var_data.y).all() or not np.any(var_data.y):
            # no need to set a log scale if all the data values are NaNs, or all zeroes
            spec_options["norm"] = None
            spec_options["vmin"] = zrange[0]
            spec_options["vmax"] = zrange[1]
        elif not np.any(var_data.y):
            # properly handle all 0s in the data   dead code now?
            spec_options["norm"] = mpl.colors.LogNorm(
                vmin=zmin, vmax=zmax
            )
        else:
            spec_options["norm"] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])
    else:
        spec_options["norm"] = None
        spec_options["vmin"] = zrange[0]
        spec_options["vmax"] = zrange[1]

    cmap = None

    if plot_extras.get("colormap") is not None:
        cmap = plot_extras["colormap"][0]
    else:
        # default to the SPEDAS color map if the user doesn't have a MPL style set
        if style is None:
            cmap = "spedas"

    # kludge to add support for the 'spedas' color bar
    if cmap == "spedas":
        _colors = pytplot.spedas_colorbar
        spd_map = [
            (np.array([r, g, b])).astype(np.float64) / 256
            for r, g, b in zip(_colors.r, _colors.g, _colors.b)
        ]
        cmap = LinearSegmentedColormap.from_list("spedas", spd_map)

    spec_options["cmap"] = cmap

    out_values = var_data.y[time_idxs, :]
    #allow use of v1, v2, jmm, 2024-03-20
    if len(var_data) == 3:
        out_vdata = var_data.v
    elif len(var_data) == 4:
        if hasattr(var_data, 'v1'):
            if 'spec_dim_to_plot' in plot_extras:
                if plot_extras['spec_dim_to_plot'] == 'v1':
                    out_vdata = var_data.v1
        if hasattr(var_data, 'v2'):
            if 'spec_dim_to_plot' in plot_extras:
                if plot_extras['spec_dim_to_plot'] == 'v2':
                    out_vdata = var_data.v2
    else:
        breakpoint()
        logging.warning("Too many dimensions on the variable: " + variable)
        return

    if len(out_vdata.shape) > 1:
        # time varying 'v', need to limit the values to those within the requested time range
        out_vdata = out_vdata[time_idxs, :]

    # automatic interpolation options
    if yaxis_options.get("x_interp") is not None:
        x_interp = yaxis_options["x_interp"]

        # interpolate along the x-axis
        if x_interp:
            if yaxis_options.get("x_interp_points") is not None:
                nx = yaxis_options["x_interp_points"]
            else:
                fig_size = fig.get_size_inches() * fig.dpi
                nx = fig_size[0]

            if zlog == "log":
                zdata = np.log10(out_values)
            else:
                zdata = out_values

            zdata[zdata < 0.0] = 0.0
            zdata[zdata == np.nan] = 0.0

            # convert to floats for the interpolation
            spec_unix_times = np.int64(var_data.times[time_idxs]) / 1e9

            # interpolate in the x-direction
            interp_func = interp1d(
                spec_unix_times, zdata, axis=0, bounds_error=False, kind="linear"
            )
            out_times = (
                np.arange(0, nx, dtype=np.float64)
                * (spec_unix_times[-1] - spec_unix_times[0])
                / (nx - 1)
                + spec_unix_times[0]
            )
            out_values = interp_func(out_times)

            if zlog == "log":
                out_values = 10**out_values

            # convert back to datetime64 objects
            var_times = np.array(out_times * 1e9, dtype="datetime64[ns]")

    if yaxis_options.get("y_interp") is not None:
        y_interp = yaxis_options["y_interp"]

        # interpolate along the y-axis
        if y_interp:
            if yaxis_options.get("y_interp_points") is not None:
                ny = yaxis_options["y_interp_points"]
            else:
                fig_size = fig.get_size_inches() * fig.dpi
                ny = fig_size[1]

            if zlog == "log":
                zdata = np.log10(out_values)
            else:
                zdata = out_values

            if ylog == "log":
                vdata = np.log10(out_vdata)
                ycrange = np.log10(yrange)
            else:
                vdata = out_vdata
                ycrange = yrange

            if not np.isfinite(ycrange[0]):
                ycrange = [np.min(vdata), yrange[1]]

            zdata[zdata < 0.0] = 0.0
            zdata[zdata == np.nan] = 0.0  # does not work

            # interp1d requires 1d vdata input
            if len(vdata.shape) == 1:
                interp_func = interp1d(vdata, zdata, axis=1, bounds_error=False)
                out_vdata = (
                    np.arange(0, ny, dtype=np.float64)
                    * (ycrange[1] - ycrange[0])
                    / (ny - 1)
                    + ycrange[0]
                )
                out_values = interp_func(out_vdata)
            else:  # 2d vdata
                ntime_idxs = vdata.shape[0]
                nynew = int(ny)
                out_vdata = (
                    np.arange(0, ny, dtype=np.float64)
                    * (ycrange[1] - ycrange[0])
                    / (ny - 1)
                    + ycrange[0]
                )
                out_values = np.zeros((ntime_idxs, nynew), dtype=vdata.dtype)
                for jm in range(len(time_idxs)):
                    interp_func = interp1d(
                        vdata[jm, :], zdata[jm, :], bounds_error=False
                    )
                    out_values[jm, :] = interp_func(out_vdata)

            if zlog == "log":
                out_values = 10**out_values

            if ylog == "log":
                out_vdata = 10**out_vdata

    # Resample to a higher resolution y grid, similar to interp, but only if y_no_resample is not set
    if (
        yaxis_options.get("y_no_resample") is None
        or yaxis_options.get("y_no_resample") == 0
    ):
        if ylog == "log":
            # Account for negative or fill values that are not NaN
            vgt0 = np.where(out_vdata > 0)[0]
            if vgt0.size == 0:
                print("ERROR in specplot.py: no nonzero V values")
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

        fig_size = fig.get_size_inches() * fig.dpi
        ny = fig_size[1]
        vdata1 = (
            np.arange(0, ny, dtype=np.float64) * (ycrange[1] - ycrange[0]) / (ny - 1)
            + ycrange[0]
        )
        out_values1 = specplot_resample(out_values, vdata, vdata1)
        out_values = out_values1
        if ylog == "log":
            out_vdata = 10**vdata1
        else:
            out_vdata = vdata1

    # check for NaNs in the v values
    nans_in_vdata = np.argwhere(np.isfinite(out_vdata) == False)
    
    if len(nans_in_vdata) > 0:
        # to deal with NaNs in the energy table, we set those energies
        # to the min value for that time (not zero, as this will be
        # bad for log plots) then apply a mask to the data values at
        # these locations 
        out_vdata_nonan = out_vdata.copy()
        if len(out_vdata.shape) == 1:
            keep = np.where(np.isfinite(out_vdata) == True)
            vmin = np.min(out_vdata[keep[0]])
            out_vdata_nonan[~np.isfinite(out_vdata)] = vmin
            #create a masked array to use
            masked = np.ma.masked_where(~np.isfinite(out_values), out_values)
            for nan_idx in range(out_values.shape[0]):
                midx = np.ma.masked_where(~np.isfinite(out_vdata), out_values[nan_idx,:])
                masked[nan_idx,:] = midx
        else:
            times_with_nans = np.unique(nans_in_vdata[:, 0])
            for nan_idx in np.arange(0, len(times_with_nans)):
                this_time_idx = times_with_nans[nan_idx]
                #Get the min value for non-nan
                keep = np.where(np.isfinite(out_vdata[this_time_idx, :]) == True)
                if keep[0].size > 0:
                    vmin = np.min(out_vdata[this_time_idx, keep[0]])
                    out_vdata_nonan[this_time_idx, ~np.isfinite(out_vdata[this_time_idx, :])] = vmin
                else:
                    out_vdata_nonan[this_time_idx, ~np.isfinite(out_vdata[this_time_idx, :])] = yrange[0]

            masked = np.ma.masked_where(~np.isfinite(out_vdata), out_values)
            out_vdata = out_vdata_nonan
            out_values = masked

    # check for negatives if zlog is requested
    if zlog == "log":
        out_values[out_values < 0.0] = 0.0

    # create the spectrogram (ignoring warnings)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        im = this_axis.pcolormesh(var_times, out_vdata.T, out_values.T, **spec_options)

    # store everything needed to create the colorbars
    colorbars[variable] = {}
    colorbars[variable]["im"] = im
    colorbars[variable]["axis_font_size"] = axis_font_size
    colorbars[variable]["ztitle"] = ztitle
    colorbars[variable]["zsubtitle"] = zsubtitle
    return True

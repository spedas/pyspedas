import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
from datetime import datetime, timezone
from matplotlib.colors import LinearSegmentedColormap
import warnings
import pytplot
import logging
from copy import copy

def get_bin_boundaries(bin_centers, ylog=False):
    """ Calculate a list of bin boundaries from a 1-D array of bin center values.

    Parameters
    ----------
    bin_centers: np.ndarray
    Array of Y bin center values

    ylog: bool or str
    If True or "log", compute the bin boundaries in log space

    Returns
    -------
    tuple
    bin_boundaries: np.ndarray[float]
        Floating point array of bin boundaries computed from the bin centers.  Output array will be one element longer thab the input array.
    direction: int
        Flag increasing or decreasing bin order: +1 increasing, -1 decreasing, 0 indeterminate

    """

    # Ensure ylog is boolean
    if isinstance(ylog, str):
        if ylog=="log":
            ylog = True
        else:
            ylog = False

    nbins = len(bin_centers)
    # Bin boundaries need to be floating point, even if the original bin values are
    # integers.  Initialize to all nans. Since the outputs are boundaries, not centers,
    # there is an extra element in the output array.
    outbins = np.zeros(nbins+1,dtype=np.float64)
    outbins[:] = np.nan

    # If we're working in log space, do the transform before filtering for finite values.
    # THEMIS ESA can have 0.0 bin centers with log scaling!


    if ylog:
        # There might be bin centers equal to 0.0 (e.g. THEMIS ESA).  Replace them with half the next larger
        # bin center.  Any bin centers less than zero will get turned to NaNs when we take logs
        # (and the corresponding data bins effectively removed).
        clean_bins = copy(bin_centers)
        zero_idx = np.where(bin_centers == 0.0)
        if len(zero_idx[0]) > 0:
            clean_bins[zero_idx] = np.nan
            clean_bins[zero_idx] = np.nanmin(clean_bins)/2.0
        working_bins = np.log10(clean_bins)
    else:
        working_bins = bin_centers

    # Check for all nans, or only one finite value
    idx_finite = np.where(np.isfinite(working_bins))

    if type(idx_finite) is tuple:
        idx_finite = idx_finite[0]

    if len(idx_finite) == 0:
        # Return all nans, indeterminate direction
        return outbins, 0
    elif len(idx_finite) == 1:
        idx = idx_finite[0]
        # Only a single bin, so we have to make up some bin boundaries
        if ylog:
            outbins[idx] = bin_centers[idx]/2.0
            outbins[idx+1] = bin_centers[idx]*2.0
        else:
            outbins[idx] = bin_centers[idx] - 1.0
            outbins[idx+1] = bin_centers[idx] + 1.0
        logging.warning("get_bin_boundaries: only one finite bin detected at index %d", idx)
        logging.warning("bin center: %f   bin boundaries: [%f, %f]",bin_centers[idx],outbins[idx], outbins[idx+1])
        # Return boundaries around the single finite bin, direction is increasing
        return outbins, 1

    # The usual case: we have at least two finite bins
    # Are they in increasing or decreasing order?

    if working_bins[idx_finite[0]] > working_bins[idx_finite[-1]]:
        direction = -1
    elif working_bins[idx_finite[0]] < working_bins[idx_finite[-1]]:
        direction = 1
    else:
        # All finite bins are the same?  Or nonmonotonic?  I guess it could happen.
        direction = 0
        logging.warning("get_bin_boundaries: First and last finite bin values are identical, may be nonmonotonic or all the same?")


    # We need to make sure that no NaNs are sandwiched between finite values
    good_bin_count = len(idx_finite)
    leading_nan_count = idx_finite[0]
    trailing_nan_count = nbins - idx_finite[-1] - 1

    if good_bin_count + leading_nan_count + trailing_nan_count != nbins:
        logging.warning("get_bin_boundaries: may contain nans between finite values. Total bin count: %d,  leading nans: %d, trailing_nans: %d, finite vals: %d",
                        nbins, leading_nan_count, trailing_nan_count, good_bin_count)

    # Now compute bin boundaries from all the finite bin centers
    finite_bins = np.copy(working_bins[idx_finite])
    edge_count = good_bin_count+1
    goodbins = np.zeros(edge_count, dtype=np.float64)

    goodbins[0] = finite_bins[0] - (finite_bins[1] - finite_bins[0]) / 2.0
    goodbins[1:edge_count-1] = (finite_bins[:-1] + finite_bins[1:]) / 2.0
    goodbins[edge_count-1] = finite_bins[-1] + (finite_bins[-1] - finite_bins[-2]) / 2.0

    # Deal with any possible leading or trailing nans
    if leading_nan_count > 0:
        outbins[0:leading_nan_count] = np.nan
    outbins[leading_nan_count:leading_nan_count+edge_count] = goodbins[:]
    if trailing_nan_count > 0:
        outbins[leading_nan_count+edge_count:nbins+2] = np.nan

    # Go back to linear space
    if ylog:
        outbins = 10.0**outbins

    return outbins, direction



def specplot_make_1d_ybins(values, vdata, ylog, min_ratio=0.001):
    """ Convert 2-D Y-bin arrays of bin center values to a 1-D array and rebin the data array

    We find the union of all the bin boundaries for time-varying bins, and use that
    instead of an arbitrary high-resolution grid as the resampling target y-values.
    Any NaN values found in the input bin centers (1D or 2D) are dealt with.

    Allows for monotonically increasing or decreasing bin values, and bins that change over time.
    2D bin center arrays with some times having ascending values and other times having descending values
    are allowed.

    """
    #logging.info("Starting 1D vbins processing")
    ntimes = values.shape[0]
    bins_1d = False

    # Determine bin boundaries at each time step (or for all time, with 1-d bin center arrays),
    # weeding out NaNs in the bin center values. Form the union of all the individual bin
    # boundary sets (keeping the time-specific boundary sets, to use when rebinning later
    # Also determine the direction of increase at each time step, and flag any time steps
    # where a direction cannot be determined.

    if len(vdata.shape) == 1:
        #logging.info("Starting 1D vbins boundary processing")
        bins_1d = True
        result = get_bin_boundaries(vdata, ylog=ylog)
        vdata_bins = result[0]
        vdata_direction = result[1]
        bin_boundaries_set = set(vdata_bins)
        input_bin_center_count = len(vdata)
    else:  # 2-d V
        #logging.info("Starting 2D vbins boundary processing")
        bins_1d = False
        input_bin_center_count = vdata.shape[1]
        vdata_bins = np.zeros((ntimes, input_bin_center_count + 1), dtype=np.float64)
        vdata_direction = np.zeros(ntimes, dtype=np.int64)

        # The sentinel values are inserted because arrays with nans will not compare equal,
        # even if the nans are in same places
        sentinel = 1e31
        result = get_bin_boundaries(vdata[0, :], ylog=ylog)
        vdata_bins[0,:] = result[0]
        vdatadir_thistime = result[1]
        vdata_direction[0] = vdatadir_thistime
        pbins = vdata_bins[0,:]
        bin_boundaries_set = set(pbins)
        p = np.copy(vdata[0,:])
        p[np.where(~np.isfinite(p))] = sentinel
        # Now that everything is initialized, go through each time index
        # and maintain a set of all the bin boundaries seen so far.
        for i in range(ntimes-1):
            k = i+1
            t=np.copy(vdata[k,:])
            t[np.where(~np.isfinite(t))] = sentinel
            diff=t-p
            if np.any(diff):
                # bin values have changed, recalculate boundaries and add to running set
                #print(k)
                result = get_bin_boundaries(vdata[k,:], ylog=ylog)
                u = result[0]
                vdatadir_thistime = result[1]
                pbins = u
                vdata_bins[k,:] = u
                vdata_direction[k] = vdatadir_thistime
                uset = set(u)
                bin_boundaries_set = bin_boundaries_set | uset
                p = t
            else:
                # bin values have not channged at this time step, use previously computed values
                vdata_bins[k,:] = pbins
                vdata_direction[k] = vdatadir_thistime

    if bins_1d:
        if vdata_direction == 1:
            #print("1d bins are increasing")
            pass
        elif vdata_direction == -1:
            #print("1d bins are decreasing")
            pass
        else:
            logging.warning("specplot_make_1d_ybins: Direction of increase of 1-D input bin centers are indeterminate (all-nan, all-same, or nonmonotonic)")
            pass
    else:
        inc_count = (vdata_direction == 1).sum()
        dec_count = (vdata_direction == -1).sum()
        ind_count = (vdata_direction == 0).sum()
        #print("2d bins increasing: ", str(inc_count))
        #print("2d bins decreasing: ", str(dec_count))
        #print("2d bins indeterminate: ", str(ind_count))
        if ind_count > 0:
            logging.warning("specplot_make_1d_ybins: Direction of increasee of input bin centers was indeterminate (all-nan, all-same, or non-monotonic) at %d of %d time indices.", ind_count, ntimes)

    # Convert the bin boundary set back to an array
    #logging.info("Done finding bin boundaries, sorting")
    vdata_unsorted = np.array(list(bin_boundaries_set))

    # Clean nans and sentinel values (e.g. may be present in FAST y bin values)
    vdata_finite = [val for val in vdata_unsorted if np.isfinite(val)]

    # Sort in ascending order
    output_bin_boundaries = np.sort(vdata_finite)

    output_bin_boundary_len = len(output_bin_boundaries)

    # It is possible (e.g. ELFIN) that some bin boundaries are very close, but not equal
    # (less than a pixel high).  We might want to thin out any bin boundaries within
    # "epsilon" of the previous bin.

    ymax=output_bin_boundaries[output_bin_boundary_len-1]
    ymin=output_bin_boundaries[0]
    yrange = ymax-ymin
    #logging.info("Thinning bin boundaries")
    # With the default min_ratio, epsilon is about one pixel in the y direction for a typical plot size and dpi
    # If min_ratio is 0, the effect is that no bin boundaries will be discarded.

    if ylog == "log":
        epsilon = (np.log10(ymax)-np.log10(ymin)) * min_ratio
    else:
        epsilon = (ymax-ymin)*min_ratio
    diff=output_bin_boundaries[1:]-output_bin_boundaries[:output_bin_boundary_len-1]

    # logging.info("Specplot 1-D y bins before thinning: array size %d, yrange %f, smallest difference %f, epsilon %f,  ratio %f",len(output_bin_boundaries),yrange,np.min(diff),epsilon, (ymax-ymin)/np.min(diff))

    last_val = output_bin_boundaries[0]
    thinned_list = [output_bin_boundaries[0]]
    for i in range(output_bin_boundary_len):
        val = output_bin_boundaries[i]
        if ylog == "log":
            diff = np.log10(val) - np.log10(last_val)
        else:
            diff = val-last_val
        if abs(diff) > epsilon:
            thinned_list.append(val)
            last_val = val

    output_bin_boundaries = np.array(thinned_list)

    #logging.info("Done thinning bin boundaries")
    output_bin_boundary_len = len(output_bin_boundaries)
    # There could be NaNs (e.g. FAST)
    ymax=output_bin_boundaries[output_bin_boundary_len-1]
    ymin=output_bin_boundaries[0]
    yrange = ymax-ymin
    diff=output_bin_boundaries[1:]-output_bin_boundaries[:output_bin_boundary_len-1]

    # logging.info("Specplot 1-D y bins after thinning: array size %d, yrange %f, smallest difference %f, epsilon %f,  ratio %f",len(output_bin_boundaries),yrange,np.min(diff),epsilon, (ymax-ymin)/np.min(diff))

    #logging.info("Started rebinning (new style)")
    if values.dtype.kind == 'f':
        fill = np.nan
    else:
        fill = 0

    # Now we rebin the input data array into the output array, using both the original
    # and combined bin boundaries.

    # The output value array should have a y dimension one less than the bin boundary count
    out_values = np.zeros((ntimes, output_bin_boundary_len - 1), dtype=values.dtype)
    out_values[:,:] = fill

    # Note that output_bin_boundaries is always monotonically increasing, but
    # vdata_bins (the original inputs) can be monotonically decreasing

    for time_index in range(ntimes):
        if len(vdata.shape) == 1:
            input_bin_boundaries = vdata_bins
            input_bin_centers = vdata
            direction = vdata_direction
        else:
            input_bin_boundaries = vdata_bins[time_index, :]
            input_bin_centers = vdata[time_index,:]
            direction = vdata_direction[time_index]

        #print("Time index: " + str(time_index))
        #print("Input bin boundaries:")
        #print(input_bin_boundaries)
        #print("Input bin centers")
        #print(input_bin_centers)
        #print("Output bin boundaries")
        #print(output_bin_boundaries)
        #print("Data values at time step:")
        #print(values[time_index,:])
        if direction == 1:
            # Increasing bin values
            lower_bound_indices = np.searchsorted(output_bin_boundaries, input_bin_boundaries[0:-1],side="left")
            upper_bound_indices = np.searchsorted(output_bin_boundaries, input_bin_boundaries[1:],side="left")
        elif direction == -1:
            lower_bound_indices = np.searchsorted(output_bin_boundaries, input_bin_boundaries[1:],side="left")
            upper_bound_indices = np.searchsorted(output_bin_boundaries, input_bin_boundaries[0:-1],side="left")
        else:
            continue
        #print("Lower bound indices:")
        #print(lower_bound_indices)
        #print("Upper bound indices")
        #print(upper_bound_indices)

        for i in range(input_bin_center_count):
            if not np.isfinite(input_bin_centers[i]):
                pass
            else:
                #print("input bin index: " + str(i))
                #print("input bin center: " + str(input_bin_centers[i]))
                #print("output lower bound index: " + str(lower_bound_indices[i]))
                #print("output upper bound index: " + str(upper_bound_indices[i]))
                #print("output bin value range: " + str(output_bin_boundaries[lower_bound_indices[i]:upper_bound_indices[i]+1]))
                out_values[time_index,lower_bound_indices[i]:upper_bound_indices[i]] = values[time_index, i]
                #print(out_values)
    #logging.info("Done making 1D Y bins")

    return out_values, output_bin_boundaries

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
    """
    Plot a tplot variable as a spectrogram

    Parameters
    ----------
    var_data: dict
        A tplot dictionary containing the data to be plotted
    var_times: array of datetime objects
        An array of datetime objects specifying the time axis
    this_axis
        The matplotlib object for the panel currently being plotted
    yaxis_options: dict
        A dictionary containing the Y axis options to be used for this variable
    zaxis_options: dict
        A dictionary containing the Z axis (spectrogram values) options to be used for this variable
    plot_extras: dict
        A dictionary containing additional plot options for this variable
    colorbars: dict
        The data structure that contains information (for all variables) for creating colorbars.
    axis_font_size: int
        The font size in effect for this axis (used to create colorbars)
    fig: matplotlib.figure.Figure
        A matplotlib figure object to be used for this plot
    variable: str
        The name of the tplxxot variable to be plotted (used for log messages)
    time_idxs: array of int
        The indices of the subset of times to use for this plot. Defaults to None (plot all timestamps).
    style
        A matplotlib style object to be used for this plot. Defaults to None.

    Returns
    -------
        True
    """
    alpha = plot_extras.get("alpha")
    spec_options = {"shading": "auto", "alpha": alpha}
    ztitle = zaxis_options["axis_label"]

    zlog_str = zaxis_options["z_axis_type"]
    ylog_str = yaxis_options["y_axis_type"]
    # Convert zlog_str and ylog_str to bool
    ylog = False
    zlog = False
    if "log" in ylog_str.lower():
        ylog = True
    if "log" in zlog_str.lower():
        zlog = True
    #logging.info("ylog_str is " + str(ylog_str))
    #logging.info("zlog_str is " + str(zlog_str))

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

    # Clean up any fill values in data array
    #set -1.e31 fill values to NaN, jmjm, 2024-02-29
    ytp = np.where(var_data.y==-1.e31,np.nan,var_data.y)
    var_data.y[:,:] = ytp[:,:]

    if zlog:
        zmin = np.nanmin(var_data.y)
        zmax = np.nanmax(var_data.y)
        # gracefully handle the case of all NaNs in the data, but log scale set
        # all 0 is also a problem, causes a crash later when creating the colorbar
        if np.isnan(var_data.y).all():
            # no need to set a log scale if all the data values are NaNs, or all zeroes
            spec_options["norm"] = None
            spec_options["vmin"] = zrange[0]
            spec_options["vmax"] = zrange[1]
            logging.info("Variable %s contains all-NaN data", variable)
        elif not np.any(var_data.y):
            # properly handle all 0s in the data
            spec_options["norm"] = None
            spec_options["vmin"] = zrange[0]
            spec_options["vmax"] = zrange[1]
            logging.info("Variable %s contains all-zero data", variable)
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

    input_zdata = var_data.y[time_idxs, :]
    input_times = var_data.times[time_idxs]

    # Figure out which attribute to use for Y bin centers
    #allow use of v1, v2, jmm, 2024-03-20
    if len(var_data) == 3:
        if hasattr(var_data,'v'):
            input_bin_centers = var_data.v
        elif hasattr(var_data,'v1'):
            input_bin_centers = var_data.v1
        else:
            logging.warning("Multidimensional variable %s has no v or v1 attribute",variable)
    elif len(var_data) == 4:
        if hasattr(var_data, 'v1'):
            if 'spec_dim_to_plot' in plot_extras:
                if plot_extras['spec_dim_to_plot'] == 'v1':
                    input_bin_centers = var_data.v1
        if hasattr(var_data, 'v2'):
            if 'spec_dim_to_plot' in plot_extras:
                if plot_extras['spec_dim_to_plot'] == 'v2':
                    input_bin_centers = var_data.v2
    else:
        logging.warning("Too many dimensions on the variable: " + variable)
        return

    # Clean up any fill values in bin center array
    vtp = np.where(input_bin_centers == -1.e31, np.nan, input_bin_centers)
    if len(vtp.shape) == 1:
        input_bin_centers[:] = vtp[:]
    else:
        input_bin_centers[:, :] = vtp[:, :]

    if len(input_bin_centers.shape) > 1:
        # time varying 'v', need to limit the values to those within the requested time range
        input_bin_centers = input_bin_centers[time_idxs, :]

    # This call flattens any time-varying bin boundaries into a 1-d list (out_vdata)
    # and regrids the data array to the new y bin count (regridded_zdata)

    #logging.info("Starting specplot processing")

    regridded_zdata, bin_boundaries_1d = specplot_make_1d_ybins(input_zdata, input_bin_centers, ylog)

    # At this point, bin_boundaries_1d, the array of bin boundaries, is guaranteed to be
    # 1-dimensional, in ascending order, with all finite values. It has one more element
    # than the Y dimension of regridded_zdata.  The Y dimension of regridded_zdata may have changed
    # as a result of flattening a 2-D out_vdata input.
    # If ylog==True, all values in bin_boundaries_1d will be strictly positive.

    assert(len(bin_boundaries_1d.shape) == 1) # bin boundaries are 1-D
    assert(len(regridded_zdata.shape) == 2) # output array is 2-D
    assert(bin_boundaries_1d.shape[0] == regridded_zdata.shape[1]+1) # bin boundaries have one more element in Y dimension
    assert(np.isfinite(bin_boundaries_1d.all())) # no nans in bin boundaries
    assert(bin_boundaries_1d[-1] > bin_boundaries_1d[0]) # bin boundaries in ascending order
    if ylog:
        assert(np.all(bin_boundaries_1d > 0.0)) # bin boundaries all positive if log scaling

    # Get min and max bin boundaries
    vmin = np.min(bin_boundaries_1d)
    vmax = np.max(bin_boundaries_1d)

    #could also have a fill in yrange
    #    if yrange[0] == -1e31: #This does not work sometimes?
    if yrange[0] < -0.9e31:
        yrange[0] = vmin
    if yrange[1] < -0.9e31:
        yrange[1] = vmax


    #logging.info("Starting specplot time boundary processing")
    input_unix_times = np.int64(input_times) / 1e9
    result = get_bin_boundaries(input_unix_times)
    # For pcolormesh, we also want bin boundaries (not center values) on the time axis
    time_boundaries_dbl = result[0]
    time_boundaries_ns = np.int64(time_boundaries_dbl*1e9)
    # Now back to numpy datetime64
    time_boundaries = np.array(time_boundaries_ns, dtype='datetime64[ns]')
    #logging.info("Done with specplot initial processing")
    # If the user set a yrange with the 'options' command, nothing is needed here
    # since tplot takes care of it.   If not, set it here to the min/max finite bin
    # boundaries.  If left unspecified, pcolormesh might do something weird to the y limits.
    if yaxis_options.get('y_range_user') is None:
        this_axis.set_ylim([vmin, vmax])


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

            if zlog:
                zdata = np.log10(regridded_zdata)
            else:
                zdata = regridded_zdata

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
            regridded_zdata = interp_func(out_times)

            if zlog:
                regridded_zdata = 10**regridded_zdata

            # Convert time bin centers to bin boundaries
            result = get_bin_boundaries(out_times, ylog=False)
            # Convert unix times back to np.datetime64[ns] objects
            unix_time_boundaries_int64 = np.int64(result[0]*1e9)
            time_boundaries = np.array(unix_time_boundaries_int64, dtype="datetime64[ns]")

    if yaxis_options.get("y_interp") is not None:
        y_interp = yaxis_options["y_interp"]

        if y_interp:
            if yaxis_options.get("y_interp_points") is not None:
                ny = yaxis_options["y_interp_points"]
            else:
                fig_size = fig.get_size_inches() * fig.dpi
                ny = fig_size[1]

            if zlog:
                zdata = np.log10(regridded_zdata)
            else:
                zdata = regridded_zdata

            if ylog:
                vdata = np.log10(bin_boundaries_1d)
                ycrange = np.log10(yrange)
            else:
                vdata = bin_boundaries_1d
                ycrange = yrange

            if not np.isfinite(ycrange[0]):
                ycrange = [np.min(vdata), yrange[1]]

            zdata[zdata < 0.0] = 0.0
            zdata[zdata == np.nan] = 0.0  # does not work

            # vdata was calculated from 1-D bin boundaries, not bin centers.
            # We need to go to bin centers for interpolation
            uppers = vdata[1:]
            lowers = vdata[0:-1]
            centers = (uppers+lowers)/2.0

            interp_func = interp1d(centers, zdata, axis=1, bounds_error=False)
            out_vdata_centers = (
                np.arange(0, ny, dtype=np.float64)
                * (ycrange[1] - ycrange[0])
                / (ny - 1)
                + ycrange[0]
            )
            regridded_zdata = interp_func(out_vdata_centers)

            # Now we'll convert from bin centers back to bin boundaries for pcolormesh
            # We're still in linear space at this point
            result = get_bin_boundaries(out_vdata_centers, ylog=False)
            rebinned_boundaries = result[0]

            if zlog:
                regridded_zdata = 10**regridded_zdata

            if ylog:
                bin_boundaries_1d = 10**rebinned_boundaries

    # check for negatives if zlog is requested
    if zlog:
        regridded_zdata[regridded_zdata < 0.0] = 0.0

    ylim_before = this_axis.get_ylim()
    # create the spectrogram (ignoring warnings)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        #logging.info("Starting pcolormesh")
        im = this_axis.pcolormesh(time_boundaries, bin_boundaries_1d.T, regridded_zdata.T, **spec_options)
        #logging.info("Done with pcolormesh")
    ylim_after = this_axis.get_ylim()

    #logging.info("ylim before pcolormesh: %s ",str(ylim_before))
    #logging.info("ylim after pcolormesh: %s", str(ylim_after))

    # store everything needed to create the colorbars
    colorbars[variable] = {}
    colorbars[variable]["im"] = im
    colorbars[variable]["axis_font_size"] = axis_font_size
    colorbars[variable]["ztitle"] = ztitle
    colorbars[variable]["zsubtitle"] = zsubtitle
    return True

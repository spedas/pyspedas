import os
import copy
import calendar
import logging
import numpy as np
import xarray as xr
import pytplot
from pytplot import tplot, store_data
from netCDF4 import Dataset, num2date


def change_time_to_unix_time(time_var):
    '''
    Convert the variable to seconds since epoch.
    '''
    # Capitalization of variable attributes may vary...
    if hasattr(time_var, 'units'):
        units = time_var.units
    elif hasattr(time_var, 'Units'):
        units = time_var.Units
    elif hasattr(time_var,'UNITS'):
        units = time_var.UNITS
    # ICON uses nonstandard units strings
    if units == 'ms':
        units = 'milliseconds since 1970-01-01 00:00:00'
    dates = num2date(time_var[:], units=units)
    unix_times = list()
    for date in dates:
        unix_time = calendar.timegm(date.timetuple())
        unix_times.append(unix_time)
    return unix_times


def netcdf_to_tplot(filenames, time='', prefix='', suffix='', plot=False, merge=False, strict_time=True):
    '''
    Create tplot variables from netCDF files.

    Parameters:
        filenames : str/list of str
            The file names and full paths of netCDF files.
        time: str
            This is not used any more. Remains here for backward compatibility.
            Currently, the name of the time variable is found in the netcdf variables themselves.
        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.
        plot: bool
            The data is plotted immediately after being generated.  All tplot
            variables generated from this function will be on the same plot.
            By default, a plot is not created.
        merge: bool
            If True, then data from different netCDF files will be merged into
            a single pytplot variable.
        strict_time: bool
            If True (default), variables will be loaded into tplot variables only if
            their data length matches the time lenght.
            If False, all variables will be loaded. This is useful because some
            variables may contain general information, like satelite longitude.

    Returns:
        List of tplot variables created.

    Examples:
        >>> #Create tplot variables from a GOES netCDF file
        >>> import pytplot
        >>> file = "/Users/user_name/goes_files/g15_epead_a16ew_1m_20171201_20171231.nc"
        >>> pytplot.netcdf_to_tplot(file, prefix='mvn_')

        >>> #Add a prefix, and plot immediately.
        >>> import pytplot
        >>> file = "/Users/user_name/goes_files/g15_epead_a16ew_1m_20171201_20171231.nc"
        >>> pytplot.netcdf_to_tplot(file, prefix='goes_prefix_', plot=True)

    '''

    stored_variables = []

    if isinstance(filenames, str):
        filenames = [filenames]
    elif isinstance(filenames, list):
        pass
    else:
        logging.error("Invalid filenames input. Must be string or list of strings.")
        return stored_variables

    filenames = sorted(list(set(filenames)))
    for filename in filenames:

        # Read file
        if os.path.isfile(filename):
            vfile = Dataset(filename)
        else:
            logging.error("Cannot find file: " + filename)
            continue

        # Create a dictionary that contains variables and their attributes.
        vars_and_atts = {}
        for name, variable in vfile.variables.items():
            vars_and_atts[name] = {}
            for attrname in variable.ncattrs():
                vars_and_atts[name][attrname] = getattr(variable, attrname)

        # Fill in missing values for each variable with np.nan (if values are not already nan)
        # and save the masked variables to a new dictionary.
        masked_vars = {}  # Dictionary containing properly masked variables
        for var in vars_and_atts.keys():
            reg_var = vfile.variables[var]
            try:
                var_fill_value = vars_and_atts[var]['missing_value']
                if np.isnan(var_fill_value) != True:
                    # We want to force missing values to be nan so that plots don't look strange
                    var_mask = np.ma.masked_where(reg_var == np.float32(var_fill_value), reg_var)
                    var_filled = np.ma.filled(var_mask, np.nan)
                    masked_vars[var] = var_filled
                elif np.isnan(var_fill_value) == True:
                    # missing values are already np.nan, don't need to do anything
                    var_filled = reg_var
                    masked_vars[var] = var_filled
            except:  # continue # Go to next iteration, this variable doesn't have data to mask (probably just a descriptor variable (i.e., 'base_time')
                var_filled = reg_var
                masked_vars[var] = var_filled

        # A dictionary with the time variables in this file.
        times_dict = {}

        # Store each netcdf variable as a tplot variable.
        for i, var in enumerate(vfile.variables):

            # Make sure that the variables are time-based, otherwise don't store them as tplot variables.
            if len(vfile[var].dimensions) > 0 and len(vfile[var].dimensions[0]) > 0:

                # Find the time dependence of the current variable.
                this_time = vfile[var].dimensions[0]
                if this_time not in vars_and_atts.keys():
                    # For GOES satelites, sometimes we get 'record' as time dependance.
                    # In that case, we can try 'time' and 'time_tag' as alternatives.
                    if 'time' in vars_and_atts.keys():
                        this_time = 'time'
                    elif 'time_tag' in vars_and_atts.keys():
                        this_time = 'time_tag'

                if this_time not in vars_and_atts.keys():
                    # If this_time does not exist, we can't save this as tplot variable.
                    continue
                elif this_time == var:
                    # If this_time has the same name as the current variable, do not save it.
                    continue

                # Find the time values (as unix times).
                if this_time in times_dict:
                    unix_times = times_dict[this_time]
                else:
                    try:
                        time_var = vfile[this_time]
                        unix_times = change_time_to_unix_time(time_var)
                        times_dict[this_time] = unix_times
                    except Exception as e:
                        # In this case, we could not handle the time, print an error
                        logging.error("Could not process time variable '" + this_time + "' for the netcdf variable: '" + var + "'")
                        logging.error("Exception details: " + str(e))
                        continue

                if var not in masked_vars:
                    # We don't have any values for this variable, skip it.
                    continue
                this_masked_var = masked_vars[var]
                if len(this_masked_var.shape) < 1:
                    # Values are empty, skip it.
                    continue
                if len(unix_times) != this_masked_var.shape[0] and strict_time:
                    # If strict_time is true, reject all variables that do not have
                    # same length for data and time. These can be inclination and other information
                    # saved as netcdf variables.
                    # If strict_time is false, pytplot.store_data will complain about this
                    # "lengths of x and y do not match", but it will create the tplot variable.
                    # But if we try to plot these variables we may get an error.
                    continue

                # Store the data, and merge variables if that was requested.
                var_name = prefix + var + suffix
                to_merge = False
                # Merge only if the variable has been saved already in the current group of files.
                # Otherwise, the tplot variable will be replaced. 
                if (var_name in stored_variables) and (var_name in pytplot.data_quants.keys() and (merge == True)):
                    prev_data_quant = pytplot.data_quants[var_name]
                    to_merge = True

                tplot_data = {'x': unix_times, 'y': this_masked_var}
                store_data(var_name, tplot_data)
                if var_name not in stored_variables:
                    stored_variables.append(var_name)

                if to_merge == True:
                    cur_data_quant = pytplot.data_quants[var_name]
                    plot_options = copy.deepcopy(pytplot.data_quants[var_name].attrs)
                    merged_data = [prev_data_quant, cur_data_quant]
                    pytplot.data_quants[var_name] = xr.concat(merged_data, dim='time').sortby('time')
                    pytplot.data_quants[var_name].attrs = plot_options

    # If we are interested in seeing a quick plot of the variables, do it
    if plot:
        tplot(stored_variables)

    return stored_variables

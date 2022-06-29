import numpy as np
import xarray as xr
from pytplot import tplot, store_data
import pytplot
import calendar
import copy


def change_time_to_unix_time(time_var):
    from netCDF4 import num2date
    # A function that takes a variable with units of 'seconds/minutes/hours/etc. since YYYY-MM-DD:HH:MM:SS/etc
    # and converts the variable to seconds since epoch
    units = time_var.units
    dates = num2date(time_var[:], units=units)
    unix_times = list()
    for date in dates:
        unix_time = calendar.timegm(date.timetuple())
        unix_times.append(unix_time)
    return unix_times


def netcdf_to_tplot(filenames, time ='', prefix='', suffix='', plot=False, merge=False):
    '''
    This function will automatically create tplot variables from CDF files.

    Parameters:
        filenames : str/list of str
            The file names and full paths of netCDF files.
        time: str
            The name of the netCDF file's time variable.
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.
        plot: bool
            The data is plotted immediately after being generated.  All tplot
            variables generated from this function will be on the same plot.
            By default, a plot is not created.
        merge: bool
            If True, then data from different netCDF files will be merged into
            a single pytplot variable.

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

    from netCDF4 import Dataset

    stored_variables = []

    if isinstance(filenames, str):
        filenames = [filenames]
    elif isinstance(filenames, list):
        filenames = filenames
    else:
        print("Invalid filenames input.")
        #return stored_variables

    for filename in filenames:

        # Read in file
        file = Dataset(filename, "r+")

        # Creating dictionary that will contain variables and their attributes
        vars_and_atts = {}
        for name, variable in file.variables.items():
            vars_and_atts[name] = {}
            for attrname in variable.ncattrs():
                vars_and_atts[name][attrname] = getattr(variable, attrname)

        # Filling in missing values for each variable with np.nan (if values are not already nan)
        # and saving the masked variables to a new dictionary
        masked_vars = {}  # Dictionary containing properly masked variables
        for var in vars_and_atts.keys():
            reg_var = file.variables[var]
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

        # Most files are from GOES data, which seems to usually have 'time_tag' in them that contain time information.
        # There is an exception filter below that will allow a user to pick a different time variable if time_tag doesn't exist.
        if time != '':
            time_var = file[time]
            unix_times = change_time_to_unix_time(time_var)

        elif time == '':
            time = input('Please enter time variable name. \nVariable list: {l}'.format(l=vars_and_atts.keys()))
            while True:
                if time not in vars_and_atts.keys():
                    # Making sure we input a valid response (i.e., the variable exists in the dataset), and also avoiding
                    # plotting a time variable against time.... because I don't even know what that would mean and uncover.
                    print('Not a valid variable name, please try again.')
                    continue
                elif time in vars_and_atts.keys():
                    time_var = time
                    unix_times = change_time_to_unix_time(time_var)

        for i,var in enumerate(file.variables):
            # Here, we are making sure that the variables are time-based, otherwise we don't want to store them as tplot variables!
            if 'record' in file[var].dimensions[0] or 'time' in file[var].dimensions[0]:
                # Store the data now, as well as merge variables if that's desired
                var_name = prefix + var + suffix
                to_merge = False
                if (var_name in pytplot.data_quants.keys() and (merge == True)):
                    prev_data_quant = pytplot.data_quants[var_name]
                    to_merge = True

                tplot_data = {'x': unix_times, 'y': masked_vars[var]}
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
            else:
                # If the variable isn't time-bound, we're going to look at the next variable
                continue

        return stored_variables


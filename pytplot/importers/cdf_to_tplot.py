# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for
# Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import cdflib

# If the user has astropy installed, use the cdflib's CDFAstropy class for time conversion
# (Converting to unix time is much, much faster this way)
try:
    from cdflib.epochs_astropy import CDFAstropy as cdfepoch
except:
    from cdflib.epochs import CDFepoch as cdfepoch

import re
import numpy as np
import xarray as xr
from datetime import timedelta
from pytplot.store_data import store_data
from pytplot.tplot import tplot
from pytplot.options import options
import pytplot
import copy


def cdf_to_tplot(filenames, varformat=None, get_support_data=False, get_metadata=False,
                 get_ignore_data=False, string_encoding='ascii',
                 prefix='', suffix='', plot=False, merge=False,
                 center_measurement=False, notplot=False, varnames=[]):
    """
    This function will automatically create tplot variables from CDF files.  In general, the files should be
    ISTP compliant for this importer to work.  Each variable is read into a new tplot variable (a.k.a an xarray DataArray),
    and all associated file/variable metadata is read into the attrs dictionary.

    .. note::
        Variables must have an attribute named "VAR_TYPE". If the attribute entry
        is "data" (or "support_data"), then they will be added as tplot variables.
        Additionally, data variables should have attributes named "DEPEND_TIME" or
        "DEPEND_0" that describes which variable is x axis.  If the data is 2D,
        then an attribute "DEPEND_1" must describe which variable contains the
        secondary axis.

    Parameters:
        filenames : str/list of str
            The file names and full paths of CDF files.
        varformat : str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.
        plot: bool
            The data is plotted immediately after being generated.  All tplot
            variables generated from this function will be on the same plot.
        merge: bool
            If True, then data from different cdf files will be merged into
            a single pytplot variable.
        get_ignore_data: bool
            Data with an attribute "VAR_TYPE" with a value of "ignore_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".
        center_measurement: bool
            If True, the CDF epoch variables are time-shifted to the middle
            of the accumulation interval by their DELTA_PLUS_VAR and
            DELTA_MINUS_VAR variable attributes
        notplot: bool
            If True, then data are returned in a hash table instead of
            being stored in tplot variables (useful for debugging, and
            access to multi-dimensional data products)
        varnames: str or list of str
            Load these variables only. If [] or ['*'], then load everything.

    Returns:
        List of tplot variables created (unless notplot keyword is used).
    """

    stored_variables = []
    epoch_cache = {}
    output_table = {}
    metadata = {}

    if not isinstance(varnames, list):
        varnames = [varnames]
    
    if len(varnames) > 0:
        if '*' in varnames:
            varnames = []

    # pytplot.data_quants = {}
    if isinstance(filenames, str):
        filenames = [filenames]
    elif isinstance(filenames, list):
        filenames = filenames
    else:
        print("Invalid filenames input.")
        return stored_variables

    var_type = ['data']
    if varformat is None:
        varformat = ".*"
    if get_support_data:
        var_type.append('support_data')
    if get_metadata:
        var_type.append('metadata')
    if get_ignore_data:
        var_type.append('ignore_data')

        
    varformat = varformat.replace("*", ".*")
    var_regex = re.compile(varformat)
    filenames.sort()
    for filename in filenames:
        cdf_file = cdflib.CDF(filename)
        cdf_file.string_encoding = string_encoding
        cdf_info = cdf_file.cdf_info()
        all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']
        # User defined variables.
        if len(varnames) > 0:
            load_cdf_variables = [value for value in varnames if value in all_cdf_variables]
        else:
            load_cdf_variables = all_cdf_variables

        try:
            gatt = cdf_file.globalattsget()
        except:
            gatt={}

        for var in load_cdf_variables:
            if not re.match(var_regex, var):
                continue
            var_atts = cdf_file.varattsget(var)

            if 'VAR_TYPE' in var_atts:
                this_var_type = var_atts['VAR_TYPE'].lower()
            elif 'PARAMETER_TYPE' in var_atts:
                this_var_type = var_atts['PARAMETER_TYPE'].lower()
            else:
                # 'VAR_TYPE' and 'PARAMETER_TYPE' not found in the variable attributes
                continue

            if this_var_type in var_type:
                var_atts = cdf_file.varattsget(var)
                var_properties = cdf_file.varinq(var)

                # Find data name and if it is already in stored variables
                if 'TPLOT_NAME' in var_atts:
                    var_name = prefix + var_atts['TPLOT_NAME'] + suffix
                else:
                    var_name = prefix + var + suffix

                if "DEPEND_TIME" in var_atts:
                    x_axis_var = var_atts["DEPEND_TIME"]
                elif "DEPEND_0" in var_atts:
                    x_axis_var = var_atts["DEPEND_0"]
                else:
                    # non-record varying variables (NRVs)
                    # added by egrimes, 13Jan2021
                    # here we assume if there isn't a DEPEND_TIME or DEPEND_0, there are no other depends
                    try:
                        ydata = cdf_file.varget(var)
                    except:
                        continue

                    if ydata is None:
                        continue

                    # since NRVs don't vary with time, they shouldn't vary across files
                    output_table[var_name] = {'y': ydata}

                    continue

                data_type_description \
                    = cdf_file.varinq(x_axis_var)['Data_Type_Description']

                if epoch_cache.get(filename+x_axis_var) is None:
                    delta_plus_var = 0.0
                    delta_minus_var = 0.0
                    delta_time = 0.0

                    # Skip variables with ValueErrors. 
                    try:
                        xdata = cdf_file.varget(x_axis_var)
                        epoch_var_atts = cdf_file.varattsget(x_axis_var)
                    except ValueError:
                        continue

                    # check for DELTA_PLUS_VAR/DELTA_MINUS_VAR attributes
                    if center_measurement:
                        if 'DELTA_PLUS_VAR' in epoch_var_atts:
                            delta_plus_var = cdf_file.varget(epoch_var_atts['DELTA_PLUS_VAR'])
                            delta_plus_var_att = cdf_file.varattsget(epoch_var_atts['DELTA_PLUS_VAR'])

                            # check if a conversion to seconds is required
                            if 'SI_CONVERSION' in delta_plus_var_att:
                                si_conv = delta_plus_var_att['SI_CONVERSION']
                                delta_plus_var = delta_plus_var.astype(float)*np.float64(si_conv.split('>')[0])
                            elif 'SI_CONV' in delta_plus_var_att:
                                si_conv = delta_plus_var_att['SI_CONV']
                                delta_plus_var = delta_plus_var.astype(float)*np.float64(si_conv.split('>')[0])

                        if 'DELTA_MINUS_VAR' in epoch_var_atts:
                            delta_minus_var = cdf_file.varget(epoch_var_atts['DELTA_MINUS_VAR'])
                            delta_minus_var_att = cdf_file.varattsget(epoch_var_atts['DELTA_MINUS_VAR'])

                            # check if a conversion to seconds is required
                            if 'SI_CONVERSION' in delta_minus_var_att:
                                si_conv = delta_minus_var_att['SI_CONVERSION']
                                delta_minus_var = delta_minus_var.astype(float)*np.float64(si_conv.split('>')[0])
                            elif 'SI_CONV' in delta_minus_var_att:
                                si_conv = delta_minus_var_att['SI_CONV']
                                delta_minus_var = delta_minus_var.astype(float)*np.float64(si_conv.split('>')[0])

                        # sometimes these are specified as arrays
                        if isinstance(delta_plus_var, np.ndarray) and isinstance(delta_minus_var, np.ndarray):
                            delta_time = (delta_plus_var-delta_minus_var)/2.0
                        else: # and sometimes constants
                            if delta_plus_var != 0.0 or delta_minus_var != 0.0:
                                delta_time = (delta_plus_var-delta_minus_var)/2.0

                if epoch_cache.get(filename + x_axis_var) is None:
                    if ('CDF_TIME' in data_type_description) or \
                            ('CDF_EPOCH' in data_type_description):
                        # the old way:
                        # store the times as unix times, and cache them
                        # xdata = cdfepoch.unixtime(xdata)
                        # epoch_cache[filename+x_axis_var] = np.array(xdata)+delta_time
                        # the new way:
                        # store and cache the datetime objects directly
                        # and delay conversion to unix times until get_data is called
                        xdata = np.array(cdflib.cdfepoch.to_datetime(xdata))
                        if isinstance(delta_time, np.ndarray) or isinstance(delta_time, list):
                            delta_t = np.array([timedelta(seconds=dtime) for dtime in delta_time])
                        else:
                            delta_t = timedelta(seconds=delta_time)
                        epoch_cache[filename + x_axis_var] = xdata + delta_t
                else:
                    xdata = epoch_cache[filename + x_axis_var]

                try:
                    ydata = cdf_file.varget(var)
                except:
                    continue

                if ydata is None:
                    continue
                if "FILLVAL" in var_atts:
                    if (var_properties['Data_Type_Description'] ==
                            'CDF_FLOAT' or
                            var_properties['Data_Type_Description'] ==
                            'CDF_REAL4' or
                            var_properties['Data_Type_Description'] ==
                            'CDF_DOUBLE' or
                            var_properties['Data_Type_Description'] ==
                            'CDF_REAL8'):

                        if ydata[ydata == var_atts["FILLVAL"]].size != 0:
                            ydata[ydata == var_atts["FILLVAL"]] = np.nan
                    elif var_properties['Data_Type_Description'][:7] == 'CDF_INT':
                        # NaN is only valid for floating point data
                        # but we still need to handle FILLVAL's for
                        # integer data, so we'll just set those to 0
                        ydata[ydata == var_atts["FILLVAL"]] = 0

                tplot_data = {'x': xdata, 'y': ydata}


                # Data may depend on other data in the CDF.
                depend_1 = None
                depend_2 = None
                depend_3 = None
                if "DEPEND_1" in var_atts:
                    if var_atts["DEPEND_1"] in all_cdf_variables:
                        depend_1 = np.array(cdf_file.varget(var_atts["DEPEND_1"]))
                        # Ignore the depend types if they are strings
                        if depend_1.dtype.type is np.str_:
                            depend_1 = None
                if "DEPEND_2" in var_atts:
                    if var_atts["DEPEND_2"] in all_cdf_variables:
                        depend_2 = np.array(cdf_file.varget(var_atts["DEPEND_2"]))
                        # Ignore the depend types if they are strings
                        if depend_2.dtype.type is np.str_:
                            depend_2 = None
                if "DEPEND_3" in var_atts:
                    if var_atts["DEPEND_3"] in all_cdf_variables:
                        depend_3 = np.array(cdf_file.varget(var_atts["DEPEND_3"]))
                        # Ignore the depend types if they are strings
                        if depend_3.dtype.type is np.str_:
                            depend_3 = None

                nontime_varying_depends = []

                if depend_1 is not None and depend_2 is not None and depend_3 is not None:
                    tplot_data['v1'] = depend_1
                    tplot_data['v2'] = depend_2
                    tplot_data['v3'] = depend_3

                    if len(depend_1.shape) == 1:
                        nontime_varying_depends.append('v1')
                    if len(depend_2.shape) == 1:
                        nontime_varying_depends.append('v2')
                    if len(depend_3.shape) == 1:
                        nontime_varying_depends.append('v3')

                elif depend_1 is not None and depend_2 is not None:
                    tplot_data['v1'] = depend_1
                    tplot_data['v2'] = depend_2
                    if len(depend_1.shape) == 1:
                        nontime_varying_depends.append('v1')
                    if len(depend_2.shape) == 1:
                        nontime_varying_depends.append('v2')
                elif depend_1 is not None:
                    tplot_data['v'] = depend_1
                    if len(depend_1.shape) == 1:
                        nontime_varying_depends.append('v')
                elif depend_2 is not None:
                    tplot_data['v'] = depend_2
                    if len(depend_2.shape) == 1:
                        nontime_varying_depends.append('v')

                metadata[var_name] = {'display_type': var_atts.get("DISPLAY_TYPE", "time_series"),
                                      'scale_type': var_atts.get("SCALE_TYP"),
                                      'y_spec_scale_type': None,
                                      'var_attrs': var_atts,
                                      'labels': None,
                                      'file_name': filename, 
                                      'global_attrs': gatt}

                labl_ptr = var_atts.get('LABL_PTR_1')
                if labl_ptr is not None:
                    try:
                        labl_ptr_arr = cdf_file.varget(labl_ptr)
                        if labl_ptr_arr is not None:
                            metadata[var_name]['labels'] = labl_ptr_arr.flatten().tolist()
                    except:
                        pass

                if metadata[var_name]['scale_type'] is None:
                    alt_scale_type = var_atts.get("SCALETYP", "linear")
                    if alt_scale_type is not None:
                        metadata[var_name]['scale_type'] = alt_scale_type

                # handle y-axis options for spectra
                if 'DEPEND_1' in var_atts:
                    if isinstance(var_atts['DEPEND_1'], str):
                        depend_1_var_atts = cdf_file.varattsget(var_atts['DEPEND_1'])

                        scale_type = depend_1_var_atts.get('SCALETYP')
                        if scale_type is None:
                            scale_type = depend_1_var_atts.get('SCALE_TYP')

                        if scale_type is not None:
                            metadata[var_name]['y_spec_scale_type'] = scale_type

                        depend_1_units = depend_1_var_atts.get('UNITS')

                        if depend_1_units is not None:
                            metadata[var_name]['y_spec_units'] = depend_1_units

                # Check if the variable already exists in the for loop output
                if var_name not in output_table:
                    output_table[var_name] = tplot_data
                else:
                    # If it does, loop though the existing variable's x,y,v,v2,v3,etc
                    var_data = output_table[var_name]
                    for output_var in var_data:
                        if output_var not in nontime_varying_depends:
                            if np.asarray(tplot_data[output_var]).ndim == 0 and np.equal(tplot_data[output_var], None):
                                # If there is nothing in the new variable, then pass
                                pass
                            elif np.asarray(var_data[output_var]).ndim == 0 and np.equal(var_data[output_var], None):
                                # If there is nothing in the old variable, then replace
                                var_data[output_var] = tplot_data[output_var]
                            else:  # If they both have something, then concatenate
                                var_data[output_var] = np.concatenate((var_data[output_var], tplot_data[output_var]))

    if notplot:
        return output_table

    for var_name in output_table.keys():
        to_merge = False
        if var_name in pytplot.data_quants.keys() and merge:
            prev_data_quant = pytplot.data_quants[var_name]
            to_merge = True

        try:
            attr_dict = {}
            if metadata.get(var_name) is not None:
                attr_dict["CDF"] = {}
                attr_dict["CDF"]["VATT"] = metadata[var_name]['var_attrs']
                attr_dict["CDF"]["GATT"] = metadata[var_name]['global_attrs']
                attr_dict["CDF"]["FILENAME"] = metadata[var_name]['file_name']
                attr_dict["CDF"]["LABELS"] = metadata[var_name]['labels']

                # extract the coordinate system, if available
                vatt_keys = list(attr_dict["CDF"]["VATT"].keys())
                vatt_lower = [k.lower() for k in vatt_keys]
                if 'coordinate_system' in vatt_lower:
                    attr_dict['data_att'] = {'coord_sys': attr_dict["CDF"]["VATT"][vatt_keys[vatt_lower.index('coordinate_system')]]}
                if 'labels' in vatt_lower:
                    if attr_dict["CDF"]["VATT"].get('labels') is not None:
                        if isinstance(attr_dict["CDF"]["VATT"]['labels'], str):
                            # check for line separators
                            # this fixes the legend for RBSP L3 EFW data
                            if '\\n' in attr_dict["CDF"]["VATT"]['labels']:
                                attr_dict["CDF"]["VATT"]['labels'] = attr_dict["CDF"]["VATT"]['labels'].split('\\n')
                            if '\\N' in attr_dict["CDF"]["VATT"]['labels']:
                                attr_dict["CDF"]["VATT"]['labels'] = attr_dict["CDF"]["VATT"]['labels'].split('\\N')
            store_data(var_name, data=output_table[var_name], attr_dict=attr_dict)
        except ValueError:
            continue

        if var_name not in stored_variables:
            stored_variables.append(var_name)

        if metadata.get(var_name) is not None:
            if metadata[var_name]['display_type'] == "spectrogram":
                options(var_name, 'spec', 1)
            if metadata[var_name]['scale_type'] == 'log':
                if metadata[var_name]['display_type'] == "spectrogram":
                    options(var_name, 'zlog', 1)
                else:
                    options(var_name, 'ylog', 1)
            if metadata[var_name].get('y_spec_scale_type') is not None:
                if metadata[var_name]['y_spec_scale_type'] == 'log':
                    options(var_name, 'ylog', 1)
            if metadata[var_name].get('y_spec_units') is not None:
                options(var_name, 'ysubtitle', '[' + metadata[var_name].get('y_spec_units') + ']')
            if metadata[var_name].get('var_attrs') is not None:
                if metadata[var_name]['var_attrs'].get('LABLAXIS') is not None:
                    options(var_name, 'ytitle', metadata[var_name]['var_attrs']['LABLAXIS'])
                if metadata[var_name]['var_attrs'].get('UNITS') is not None:
                    if metadata[var_name]['display_type'] == 'spectrogram':
                        options(var_name, 'ztitle', '[' + metadata[var_name]['var_attrs']['UNITS'] + ']')
                    else:
                        options(var_name, 'ysubtitle', '[' + metadata[var_name]['var_attrs']['UNITS'] + ']')

            # Gather up all options in the variable attribute section, toss them into options and see what sticks
            options(var_name, opt_dict=metadata[var_name]['var_attrs'])

        if to_merge is True:
            cur_data_quant = pytplot.data_quants[var_name]
            if isinstance(pytplot.data_quants[var_name], dict):  # non-record varying variable, shouldn't be merged
                continue
            plot_options = copy.deepcopy(pytplot.data_quants[var_name].attrs)
            pytplot.data_quants[var_name] = xr.concat([prev_data_quant, cur_data_quant], dim='time').sortby('time')
            pytplot.data_quants[var_name].attrs = plot_options

    if notplot:
        return output_table

    if plot:
        tplot(stored_variables)

    return stored_variables

# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for
# Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import cdflib
import re
import numpy as np
import pandas as pd
from pytplot.store_data import store_data
from pytplot.tplot import tplot
from pytplot.options import options
from pytplot.get_data import get_data
from pytplot import data_quants


def cdf_to_tplot(filenames, varformat=None, get_support_data=False,
                 prefix='', suffix='', plot=False, merge=False, 
                 center_measurement=False, notplot=False):
    """
    This function will automatically create tplot variables from CDF files.
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
        center_measurement: bool
            If True, the CDF epoch variables are time-shifted to the middle
            of the accumulation interval by their DELTA_PLUS_VAR and
            DELTA_MINUS_VAR variable attributes
        notplot: bool
            If True, then data are returned in a hash table instead of 
            being stored in tplot variables (useful for debugging, and
            access to multi-dimensional data products)

    Returns:
        List of tplot variables created (unless notplot keyword is used).
    """

    stored_variables = []
    epoch_cache = {}
    if notplot:
        output_table = {}

    global data_quants

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

    varformat = varformat.replace("*", ".*")
    var_regex = re.compile(varformat)

    for filename in filenames:
        cdf_file = cdflib.CDF(filename)
        cdf_info = cdf_file.cdf_info()
        all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']

        # Find the data variables
        for var in all_cdf_variables:
            if not re.match(var_regex, var):
                continue
            var_atts = cdf_file.varattsget(var)

            if 'VAR_TYPE' not in var_atts:
                continue

            if var_atts['VAR_TYPE'] in var_type:
                var_atts = cdf_file.varattsget(var)
                var_properties = cdf_file.varinq(var)
                if "DEPEND_TIME" in var_atts:
                    x_axis_var = var_atts["DEPEND_TIME"]
                elif "DEPEND_0" in var_atts:
                    x_axis_var = var_atts["DEPEND_0"]
                else:
                    if var_atts['VAR_TYPE'].lower() == 'data':
                        print("Cannot find x axis.")
                        print("No attribute named DEPEND_TIME or DEPEND_0 in \
                          variable " + var)
                    continue
                data_type_description \
                    = cdf_file.varinq(x_axis_var)['Data_Type_Description']

                # Find data name and if it is already in stored variables
                var_name = prefix + var + suffix
                to_merge = False
                if (var_name in data_quants.keys()) and (merge is True):
                    prev_data_quant = data_quants[var_name].data
                    prev_spec_bins = data_quants[var_name].spec_bins
                    to_merge = True

                if epoch_cache.get(filename+x_axis_var) is None:
                    delta_plus_var = 0.0
                    delta_minus_var = 0.0
                    delta_time = 0.0

                    xdata = cdf_file.varget(x_axis_var)
                    epoch_var_atts = cdf_file.varattsget(x_axis_var)

                    # check for DELTA_PLUS_VAR/DELTA_MINUS_VAR attributes
                    if center_measurement:
                        if 'DELTA_PLUS_VAR' in epoch_var_atts:
                            delta_plus_var = cdf_file.varget(epoch_var_atts['DELTA_PLUS_VAR'])
                            delta_plus_var_att = cdf_file.varattsget(epoch_var_atts['DELTA_PLUS_VAR'])

                            # check if a conversion to seconds is required
                            if 'SI_CONVERSION' in delta_plus_var_att:
                                si_conv = delta_plus_var_att['SI_CONVERSION']
                                delta_plus_var = delta_plus_var.astype(float)*np.float(si_conv.split('>')[0])
                            elif 'SI_CONV' in delta_plus_var_att:
                                si_conv = delta_plus_var_att['SI_CONV']
                                delta_plus_var = delta_plus_var.astype(float)*np.float(si_conv.split('>')[0])

                        if 'DELTA_MINUS_VAR' in epoch_var_atts:
                            delta_minus_var = cdf_file.varget(epoch_var_atts['DELTA_MINUS_VAR'])
                            delta_minus_var_att = cdf_file.varattsget(epoch_var_atts['DELTA_MINUS_VAR'])

                            # check if a conversion to seconds is required
                            if 'SI_CONVERSION' in delta_minus_var_att:
                                si_conv = delta_minus_var_att['SI_CONVERSION']
                                delta_minus_var = delta_minus_var.astype(float)*np.float(si_conv.split('>')[0])
                            elif 'SI_CONV' in delta_minus_var_att:
                                si_conv = delta_minus_var_att['SI_CONV']
                                delta_minus_var = delta_minus_var.astype(float)*np.float(si_conv.split('>')[0])

                        # sometimes these are specified as arrays
                        if isinstance(delta_plus_var, np.ndarray) and isinstance(delta_minus_var, np.ndarray):
                            delta_time = (delta_plus_var-delta_minus_var)/2.0
                        else: # and sometimes constants
                            if delta_plus_var != 0.0 or delta_minus_var != 0.0:
                                delta_time = (delta_plus_var-delta_minus_var)/2.0

                if epoch_cache.get(filename + x_axis_var) is None:
                    if ('CDF_TIME' in data_type_description) or \
                            ('CDF_EPOCH' in data_type_description):
                        xdata = cdflib.cdfepoch.unixtime(xdata)
                        epoch_cache[filename+x_axis_var] = np.array(xdata)+delta_time
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

                tplot_data = {'x': xdata, 'y': ydata}

                depend_1 = None
                depend_2 = None
                depend_3 = None
                if "DEPEND_1" in var_atts:
                    if var_atts["DEPEND_1"] in all_cdf_variables:
                        depend_1 = cdf_file.varget(var_atts["DEPEND_1"])
                if "DEPEND_2" in var_atts:
                    if var_atts["DEPEND_2"] in all_cdf_variables:
                        depend_2 = cdf_file.varget(var_atts["DEPEND_2"])
                if "DEPEND_3" in var_atts:
                    if var_atts["DEPEND_3"] in all_cdf_variables:
                        depend_3 = cdf_file.varget(var_atts["DEPEND_3"])

                if depend_1 is not None and depend_2 is not None and depend_3 is not None:
                    tplot_data['v1'] = depend_1
                    tplot_data['v2'] = depend_2
                    tplot_data['v3'] = depend_3
                elif depend_1 is not None and depend_2 is not None:
                    tplot_data['v1'] = depend_1
                    tplot_data['v2'] = depend_2
                elif depend_1 is not None:
                    tplot_data['v'] = depend_1
                elif depend_2 is not None:
                    tplot_data['v'] = depend_2

                if notplot:
                    output_table[var_name] = tplot_data
                else:
                    store_data(var_name, data=tplot_data)
                    if var_name not in stored_variables:
                        stored_variables.append(var_name)

                    display_type = var_atts.get("DISPLAY_TYPE", "time_series")
                    scale_type = var_atts.get("SCALE_TYP", "linear")
                    if display_type == "spectrogram":
                        options(var_name, 'spec', 1)
                    if scale_type == 'log':
                        options(var_name, 'ylog', 1)

                    if to_merge is True:
                        cur_data_quant = data_quants[var_name].data
                        merged_data = [prev_data_quant, cur_data_quant]
                        data_quants[var_name].data = pd.concat(merged_data)
                        if data_quants[var_name].spec_bins_time_varying:
                            cur_spec_bins = data_quants[var_name].spec_bins
                            merged_spec_bins = [prev_spec_bins, cur_spec_bins]
                            data_quants[var_name].spec_bins = pd.concat(merged_spec_bins)

    # cdf_file.close()

    if plot:
        tplot(stored_variables)

    if notplot:
        return output_table

    return stored_variables
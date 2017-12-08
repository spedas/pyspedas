import cdflib
import re
import numpy as np
from .store_data import store_data
from .tplot import tplot
from .options import options

def cdf_to_tplot(filenames, varformat=None, get_support_data=False,
                 prefix='', suffix='', plot=False):
    """
    This function will automatically create tplot variables from CDF files.    
    
    .. note::
        Variables must have an attribute named "VAR_TYPE".  If the attribute entry 
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
            
    Returns:
        List of tplot variables created.
    
    Examples:
        >>> #Create tplot variables from a MAVEN SWEA instrument
        >>> import pytplot
        >>> file = "C:/mavencdfs/mvn_swe_l2_svyspec_20170725_v04_r04.cdf"
        >>> pytplot.cdf_to_tplot(file, prefix='mvn_')
        
        >>> #Add the prefix "mvn_", and plot immediately. 
        >>> import pytplot
        >>> file = "C:/mavencdfs/mvn_swe_l2_svyspec_20170725_v04_r04.cdf"
        >>> pytplot.cdf_to_tplot(file, prefix='mvn_', plot=True)
        
        >>> #Filter out variables that do not start with "diff"
        >>> import pytplot
        >>> file = "C:/mavencdfs/mvn_swe_l2_svyspec_20170725_v04_r04.cdf"
        >>> pytplot.cdf_to_tplot(file, varformat="diff*")

    """
    stored_variables=[]
    
    if isinstance(filenames, str):
        filenames = [filenames]
    elif isinstance(filenames, list):
        filenames=filenames
    else:
        print("Invalid filenames input.")
        return stored_variables
    
    var_type=['data']
    if varformat == None:
        varformat = ".*"
    if get_support_data:
        var_type.append('support_data')
    
    try:
        varformat = varformat.replace("*", ".*")
        var_regex = re.compile(varformat)
    except:
        print("Error reading the varformat.")
        return
    
    
    
    for filename in filenames:
        cdf_file = cdflib.CDF(filename)
        cdf_info = cdf_file.cdf_info()
        all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']
            
        #Find the data variables
        for var in all_cdf_variables:
            if not re.match(var_regex,var):
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
                    print("Cannot find x axis.")
                    print("No attribute named DEPEND_TIME or DEPEND_0 in variable "+var)
                    continue
                data_type_description = cdf_file.varinq(x_axis_var)['data_type_description']
                xdata=cdf_file.varget(x_axis_var)
                
                if 'CDF_TIME' in data_type_description:
                    xdata = cdflib.cdfepoch.unixtime(xdata)
                ydata=cdf_file.varget(var)
                if ydata is None:
                    continue
                if "FILLVAL" in var_atts:
                    if (var_properties['data_type_description'] == 'CDF_FLOAT' or
                        var_properties['data_type_description'] == 'CDF_REAL4' or 
                        var_properties['data_type_description'] == 'CDF_DOUBLE' or 
                        var_properties['data_type_description'] == 'CDF_REAL8'):
                        
                        if ydata[ydata==var_atts["FILLVAL"]].size != 0:
                            ydata[ydata==var_atts["FILLVAL"]] = np.nan
                        
                    
                
                var_name = prefix+var+suffix
                tplot_data ={'x':xdata,'y':ydata}
                
                depend_1 = None
                depend_2 = None
                if "DEPEND_1" in var_atts:
                    if var_atts["DEPEND_1"] in all_cdf_variables:
                        depend_1 = cdf_file.varget(var_atts["DEPEND_1"])
                if "DEPEND_2" in var_atts:
                    if var_atts["DEPEND_2"] in all_cdf_variables:
                        depend_2 = cdf_file.varget(var_atts["DEPEND_2"])
                if depend_1 is not None and depend_2 is not None:
                    tplot_data['v1'] = depend_1
                    tplot_data['v2'] = depend_2
                elif depend_1 is not None:
                    tplot_data['v'] = depend_1
                elif depend_2 is not None:
                    tplot_data['v'] = depend_2
                    
                    
                store_data(var_name, data=tplot_data)
                stored_variables.append(var_name)
                
                display_type = var_atts.get("DISPLAY_TYPE", "time_series")
                scale_type = var_atts.get("SCALE_TYP", "linear")
                if display_type == "spectrogram": 
                    options(var, 'spec', 1)
                if scale_type == 'log':
                    options(var, 'ylog', 1)
                        
        cdf_file.close()     
    
    if plot:
        tplot(stored_variables)
    
    return stored_variables

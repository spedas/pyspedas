import logging
import re
import numpy as np



def param_list(kp):
    """
    Return a listing of all parameters present in the given
    insitu data dictionary/structure.

    Parameters:
        kp: insitu kp data structure/dictionary read from file(s)
    Output:
        ParamList: a list of all contained items and their indices.
    """
    import pandas as pd

    index = 1
    param_list_ = []
    for base_tag in kp.keys():
        if isinstance(kp[base_tag], pd.DataFrame):
            for obs_tag in kp[base_tag].columns:
                param_list_.append("#%3d %s.%s" % (index, base_tag, obs_tag))
                index += 1
        elif isinstance(kp[base_tag], pd.Series):
            param_list_.append("#%3d %s" % (index, base_tag))
            index += 1
        elif isinstance(kp[base_tag], pd.Index):
            param_list_.append("#%3d %s" % (index, base_tag))
            index += 1
        else:
            logging.warning("Warning: unexpected value type %s for tag %s",str(type(kp[base_tag])), base_tag)

    return param_list_


def param_range(kp, iuvs=None):
    """
    Print the range of times and orbits for the provided insitu data.
    If iuvs data are also provided, return only orbit numbers for IUVS data.

    Caveats:
        At present, not configured to handle (real) IUVS data.
        Current configuration of procedure assumes IUVS has identical
            time information as in-situ.

    Parameters:
        kp: insitu kp data structure/dictionary
        iuvs: IUVS kp data strucure/dictionary
    Output:
        None: prints information to screen
    """

    # First, the case where insitu data are provided
    logging.info("The loaded insitu KP data set contains data between %s and %s (orbits %d and %d)",
                 np.array(kp["TimeString"])[0],
                       np.array(kp["TimeString"])[-1],
                       np.array(kp["Orbit"])[0],
                       np.array(kp["Orbit"])[-1])

    #  Finally, the case where both insitu and IUVS are provided
    if iuvs is not None:
        logging.info("The loaded IUVS KP data set contains data between %s and %s (orbits %d and %d)",
                     np.array(iuvs["TimeString"])[0],
                     np.array(iuvs["TimeString"])[-1],
                     np.array(iuvs["Orbit"])[0],
                     np.array(iuvs["Orbit"])[-1])

        insitu_min, insitu_max = (np.nanmin([kp["Orbit"]]), np.nanmax([kp["Orbit"]]))
        if (
            np.nanmax([iuvs["Orbit"]]) < insitu_min
            or np.nanmin([iuvs["Orbit"]]) > insitu_max
        ):
            logging.warning("Warning: No overlap between supplied insitu and IUVS data structures.")
    return  # No information to return


def range_select(kp, time=None, parameter=None, maximum=None, minimum=None):
    """
    Returns a subset of the input data based on the provided time
    and/or parameter criteria.  If neither Time nor Parameter filter
    information is provided, then no subselection of data will occur.
    Any parameter used as a filtering criterion must be paired with
    either a maximum and/or a minimum value.  Open ended bounds must
    be indicated with either a value of 'None' or an empty string ('').

    Parameters:
        kp: insitu kp data structure/dictionary read from file(s)
        time: two-element time range must be either strings of format
            'yyyy-mm-ddThh:mm:ss' or integers (orbit numbers)
        parameter: Element of provided data structure/dictionary by
            which to filter data.  Parameter(s) must be either integer
            type (search by index) or string type (search by instrument
            name and observation type).  If multiple Parameters are used
            to filter the data, they must be provided as a list (mixing
            data types within a list is permitted).
        maximum: maximum value of Parameter on which to filter.  A value of
            None or '' will leave the Parameter filter unbounded above.
            The number of elements of Maximum *MUST* equal the number of
            elements of Parameter.
        minimum: minimum value of Parameter on which to filter.  A value of
            None or '' will leave the Parameter filter unbounded below.
            The number of elements of Minimum *MUST* equal the number of
            elements of Parameter.
    Output: a dictionary/structure containing the same elements as the provided
        one, but filtered according to the Time and Parameter options.

    ToDo: compartmentalize the filtering and/or argument checks.
    """
    from datetime import datetime

    #  Initialize the filter_list
    filter_list = []

    # First, check the arguments
    if time is None and parameter is None:
        insufficient_input_range_select()
        logging.warning("Neither Time nor Parameter provided")
        return kp
    elif time is None:
        # Then only subset based on parameters
        # Need to check whether one or several Parameters given
        inst = []
        obs = []
        # parameter is not None in this case
        if not isinstance(parameter, list):
            if isinstance(parameter,str) or isinstance(parameter,int):
                parameter = [parameter]
            else:
                logging.warning("*****ERROR*****")
                logging.warning("Cannot identify given parameter: %s" % parameter)
                logging.warning("Suggest using param_list(kp) to identify Parameter")
                logging.warning("by index or by name")
                logging.warning("Returning complete original data dictionary")
                return kp
        if minimum is None and maximum is None:
            insufficient_input_range_select()
            logging.warning("No bounds set for parameter(S)")
            logging.warning("Returning complete original data dictionary")
            return kp

        if minimum is None:
            minimum = np.repeat(-np.inf, len(parameter))
        elif not isinstance(minimum, list):
            minimum = [minimum]
        if maximum is None:
            maximum = np.repeat(np.inf, len(parameter))
        elif not isinstance(maximum, list):
            maximum = [maximum]

        if (len(parameter) != len(minimum)) or (len(parameter) != len(maximum)):
            logging.warning("*****ERROR*****")
            logging.warning("---range_select---")
            logging.warning("Number of minima and maxima provided")
            logging.warning("MUST match number of Parameters provided")
            logging.warning("You provided %4d Parameters" % len(parameter))
            logging.warning("             %4d minima" % len(minimum))
            logging.warning("         and %4d maxima" % len(maximum))
            logging.warning("Returning complete original data dictionary")
            return kp

        for param in parameter:
            if not (isinstance(param, int) or isinstance(param, str)):
                logging.warning("*****ERROR*****")
                logging.warning("Cannot identify given parameter: %s" % param)
                logging.warning("Suggest using param_list(kp) to identify Parameter")
                logging.warning("by index or by name")
                logging.warning("Returning complete original data dictionary")
                return kp
            else:
                a, b = get_inst_obs_labels(kp, param)
                inst.append(a)
                obs.append(b)
    # Should I move this below the Time conditional and move
    # Baselining of Filter List to above time

    else:
        # Time has been provided as a filtering agent
        # Determine whether Time is provided as strings or orbits
        if len(time) != 2:
            if parameter is not None:
                logging.warning("*****WARNING*****")
                logging.warning("Time must be provided as a two-element list")
                logging.warning("of either strings (yyyy-mm-dd hh:mm:ss) ")
                logging.warning("or orbits.  Since a Parameter *was* provided,")
                logging.warning("I will filter on that, but ignore the time input.")
                inst = []
                obs = []
                for param in parameter:
                    a, b = get_inst_obs_labels(kp, param)
                    inst.append(a)
                    obs.append(b)

            else:
                # Cannot proceed with filtering
                insufficient_input_range_select()
                logging.warning("Time is not a 2-element list of strings or orbit numbers, no parameter given.")
                logging.warning("Returning complete original data dictionary")
                return kp
        else:
            # We have a two-element Time list: parse it
            if type(time[0]) !=  type(time[1]):
                if parameter is not None:
                    logging.warning("*****WARNING*****")
                    logging.warning("Both elements of time must be same type")
                    logging.warning("Only strings of format yyyy-mm-dd hh:mm:ss")
                    logging.warning("or integers (orbit numbers) are allowed.")
                    logging.warning("Ignoring time inputs; will filter ONLY")
                    logging.warning("on Parameter inputs.")
                else:
                    logging.warning("*****ERROR*****")
                    logging.warning("Both elements of Time must be same type")
                    logging.warning("Only Strings of format yyyy-mm-dd hh:mm:ss")
                    logging.warning("or integers (orbit numbers) are allowed.")
                    logging.warning("Returning original unchanged data dictionary")
                    return kp
            elif type(time[0]) is int:
                # Filter based on orbit number
                min_t = min(time)
                max_t = max(time)
                filter_list.append(kp["Orbit"] >= min_t)
                filter_list.append(kp["Orbit"] <= max_t)
            elif isinstance(time[0], str):
                # Filter acc to string dat, need to parse it
                time_dt = [datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in time]
                min_dt = min(time_dt)
                max_dt = max(time_dt)
                kp_dt = [
                    datetime.strptime(i, "%Y-%m-%dT%H:%M:%S") for i in kp["TimeString"]
                ]
                delta_tmin = np.array([(i - min_dt).total_seconds() for i in kp_dt])
                delta_tmax = np.array([(i - max_dt).total_seconds() for i in kp_dt])
                filter_list.append(delta_tmin >= 0)
                filter_list.append(delta_tmax <= 0)
            else:
                # Time provided as other than string or Integer
                if parameter is not None:
                    logging.warning("*****WARNING*****")
                    logging.warning("Times must be strings or integer or orbit numbers")
                    logging.warning("Ignoring time inputs; will filter ONLY")
                    logging.warning("on Parameter inputs.")
                else:
                    logging.warning("*****ERROR*****")
                    logging.warning("Times must be either strings or integer orbit numbers.")
                    logging.warning("Returning original unchanged data dictionary")
                    return kp
            # Now, we apply the Parameter selection
            inst = []
            obs = []
            if isinstance(parameter, int) or isinstance(parameter, str):
                # Then we have a single Parameter to filter on
                # Verify that bounds info exists
                if minimum is None and maximum is None:
                    insufficient_input_range_select()
                    logging.warning("No bounds set for parameter %s" % parameter)
                    logging.warning("Applying only Time filtering")
                    parameter = None
                elif minimum is None:
                    minimum = [-np.inf]  # Unbounded below
                elif maximum is None:
                    maximum = [np.inf]  # Unbounded above
                else:
                    pass  # Range fully bounded
                if not isinstance(minimum, list):
                    minimum = [minimum]
                if not isinstance(maximum, list):
                    maximum = [maximum]
                if len(minimum) != 1 or len(maximum) != 1:
                    logging.warning("*****ERROR*****")
                    logging.warning("---range_select---")
                    logging.warning("Number of minima and maxima provided")
                    logging.warning("MUST match number of Parameters provided")
                    logging.warning("You provided %4d Parameters" % 1)
                    logging.warning("             %4d minima" % len(minimum))
                    logging.warning("         and %4d maxima" % len(maximum))
                    logging.warning("Filtering only on Time")
                    parameter = None
                else:
                    if parameter is not None:
                        a, b = get_inst_obs_labels(kp, parameter)
                        inst.append(a)
                        obs.append(b)
                        nparam = 1  # necessary?
            elif type(parameter) is list:
                if minimum is None and maximum is None:
                    insufficient_input_range_select()
                    logging.warning("No bounds set for parameter list")
                    logging.warning("Applying only Time filtering")
                    parameter = None
                    lmin = 0
                    lmax = 0
                elif minimum is None:
                    minimum = np.repeat(-np.inf,len(parameter))
                    lmin = len(parameter)
                    lmax = len(maximum)
                elif maximum is None:
                    maximum = np.repeat(np.inf, len(parameter))
                    lmin = len(minimum)
                    lmax = len(parameter)
                else:
                    lmin = len(minimum)
                    lmax = len(maximum)
                if (parameter is not None) and (len(parameter) != lmin or len(parameter) != lmax):
                    logging.warning("*****ERROR*****")
                    logging.warning("---range_select---")
                    logging.warning("Number of minima and maxima provided")
                    logging.warning("MUST match number of Parameters provided")
                    logging.warning("You provided %4d Parameters" % len(parameter))
                    logging.warning("             %4d minima" % len(minimum))
                    logging.warning("         and %4d maxima" % len(maximum))
                    logging.warning("Filtering only on Time")
                    parameter = None
                elif parameter is not None:
                    nparam = len(parameter)
                    for param in parameter:
                        a, b = get_inst_obs_labels(kp, param)
                        inst.append(a)
                        obs.append(b)

    # Now, apply the filters
    if parameter is not None:
        inst_obs_minmax = list(zip(inst, obs, minimum, maximum))
        for inst, obs, min_obs, max_obs in inst_obs_minmax:
            filter_list.append(kp[inst][obs] >= min_obs)
            filter_list.append(kp[inst][obs] <= max_obs)

    # Filter list built, apply to data
    filter = np.all(filter_list, axis=0)
    new = {}
    for i in kp:
        temp = kp[i]
        new.update({i: temp[filter]})
    return new


def insufficient_input_range_select():
    """
    This error message is called if user calls range_select with
    inputs that result in neither a valid Time range nor a valid
    Parameter range capable of being determined

    ToDo: Is there a way to hide this from the help feature?
    """
    logging.warning("*****ERROR*****")
    logging.warning("Either a time criterion with two values.")
    logging.warning("  or a parameter name with maximum and/or")
    logging.warning("  minimum values must be provided.")
    logging.warning("Returning the complete original data dictionary")


def get_inst_obs_labels(kp, name):
    """
    Given parameter input in either string or integer format,
    identify the instrument name and observation type for use
    in accessing the relevant part of the data structure
    E.g.: 'LPW.EWAVE_LOW_FREQ' would be returned as
          ['LPW', 'EWAVE_LOW_FREQ']

    Parameters:
        kp: insitu kp data structure/dictionary read from file(s)
        name: string identifying a parameter.
            (Indices must be converted to inst.obs strings before
             calling this routine)
    Output:
        inst (1st arg): instrument identifier
        obs (2nd arg): observation type identifier
    """

    # Need to ensure name is a string at this stage
    name = "%s" % name

    # Now, split at the dot (if it exists)
    tags = name.split(".")
    # And consider the various possibilities...
    if len(tags) == 2:
        return tags
    elif len(tags) == 1:
        try:
            int(tags[0])
            return (find_param_from_index(kp, tags[0])).split(".")
        except:
            logging.warning("*****ERROR*****")
            logging.warning("%s is an invalid parameter" % name)
            logging.warning("If only one value is provided, it must be an integer")
            return [],[]
    else:
        logging.warning("*****ERROR*****")
        logging.warning("%s is not a valid parameter" % name)
        logging.warning("because it has %1d elements" % len(tags))
        logging.warning('Only 1 integer or string of form "a.b" are allowed.')
        logging.warning("Please use .param_list attribute to find valid parameters")
        return [],[]


def find_param_from_index(kp, index):
    """
    Given an integer index, find the name of the parameter

    Parameters:
        kp: insitu kp data structure/dictionary read from file(s)
        index: the index of the desired parameter (integer type)
    Output:
        A string of form <instrument>.<observation>
        (e.g., LPW.EWAVE_LOW_FREQ)
    """

    index = "#%3d" % int(index)
    plist = param_list(kp)
    found = False
    for i in plist:
        if re.search(index, i):
            return i[5:]  # clip the '#123 ' string
    if not found:
        logging.warning("*****ERROR*****")
        logging.warning("%s not a valid index." % index)
        logging.warning("Use param_list to list options")
        return



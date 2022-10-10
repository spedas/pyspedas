# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import logging
import re
import os
from . import download_files_utilities as utils
from .file_regex import kp_regex, l2_regex
import numpy as np
import collections


def param_list(kp):
    '''
    Return a listing of all parameters present in the given
    insitu data dictionary/structure.

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
    Output:
        ParamList: a list of all contained items and their indices.
    '''
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
            logging.warning('*****WARNING*****')
            logging.warning('Returning INCOMPLETE Parameter List')
            logging.warning('Base tag neither DataFrame nor Series')
            logging.warning('Plese check read_insitu_file definition')

    return param_list_


# ---------------------------------------------------------------------


def param_range(kp, iuvs=None):
    '''
    Print the range of times and orbits for the provided insitu data.
    If iuvs data are also provided, return only orbit numbers for IUVS data.

    Caveats:
        At present, not configured to handle (real) IUVS data.
        Current configuration of procedure assumes IUVS has identical
            time information as in-situ.

    Input:
        kp: insitu kp data structure/dictionary
        iuvs: IUVS kp data strucure/dictionary
    Output:
        None: prints information to screen
    '''

    # First, the case where insitu data are provided
    print("The loaded insitu KP data set contains data between")
    print("   %s and %s" % (np.array(kp['TimeString'])[0], np.array(kp['TimeString'])[-1]))
    print("Equivalently, this corresponds to orbits")
    print("   %6d and %6d." % (np.array(kp['Orbit'])[0], np.array(kp['Orbit'])[-1]))

    #  Next, the case where IUVS data are provided
    iuvs_data = False
    iuvs_tags = ['CORONA_LO_HIGH', 'CORONA_LO_LIMB', 'CORONA_LO_DISK',
                 'CORONA_E_HIGH', 'CORONA_E_LIMB', 'CORONA_E_DISK',
                 'APOAPSE', 'PERIAPSE', 'STELLAR_OCC']
    if kp.keys() in iuvs_tags:
        print("The loaded IUVS KP data set contains data between orbits")
        print("   %6d and %6d." % (np.array(kp['Orbit'])[0], np.array(kp['Orbit'])[-1]))

    #  Finally, the case where both insitu and IUVS are provided
    if iuvs is not None:
        print("The loaded IUVS KP data set contains data between orbits")
        print("   %6d and %6d." % (np.array(iuvs['Orbit'])[0], np.array(iuvs['Orbit'])[-1]))
        insitu_min, insitu_max = (np.nanmin([kp['Orbit']]), np.nanmax([kp['Orbit']]))
        if np.nanmax([iuvs['Orbit']]) < insitu_min or np.nanmin([iuvs['Orbit']]) > insitu_max:
            print("*** WARNING ***")
            print("There is NO overlap between the supplied insitu and IUVS")
            print("  data structures.  We cannot guarantee your safety ")
            print("  should you attempt to display these IUVS data against")
            print("  these insitu-supplied emphemeris data.")
    return  # No information to return


# --------------------------------------------------------------------------


def range_select(kp, time=None, parameter=None, maximum=None, minimum=None):
    '''
    Returns a subset of the input data based on the provided time
    and/or parameter criteria.  If neither Time nor Parameter filter
    information is provided, then no subselection of data will occur.
    Any parameter used as a filtering criterion must be paired with
    either a maximum and/or a minimum value.  Open ended bounds must
    be indicated with either a value of 'None' or an empty string ('').

    Input:
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
    '''
    from datetime import datetime

    #  Initialize the filter_list
    filter_list = []

    # First, check the arguments
    if time is None and parameter is None:
        insufficient_input_range_select()
        print('Neither Time nor Parameter provided')
        return kp
    elif time is None:
        # Then only subset based on parameters
        # Need to check whether one or several Parameters given
        inst = []
        obs = []
        if isinstance(parameter, int) or isinstance(parameter, str):
            # First, verify that at least one bound exists
            if minimum is None and maximum is None:
                insufficient_input_range_select()
                print('No bounds set for parameter: %s' % parameter)
                return kp
            elif minimum is None:
                # Range only bounded above
                minimum = -np.Infinity
            elif maximum is None:
                # range only bounded below
                maximum = np.Infinity
            else:
                # Range bounded on both ends
                pass
            a, b = get_inst_obs_labels(kp, parameter)
            inst.append(a)
            obs.append(b)
            nparam = 1  # necc?
        elif type(parameter) is list:
            nparam = len(parameter)
            for param in parameter:
                a, b = get_inst_obs_labels(kp, param)
                inst.append(a)
                obs.append(b)
        else:
            print('*****ERROR*****')
            print('Cannot identify given parameter: %s' % parameter)
            print('Suggest using param_list(kp) to identify Parameter')
            print('by index or by name')
            print('Returning complete original data dictionary')
            return kp

    # Should I move this below the Time conditional and move
    # Baselining of Filter List to above time

    else:
        # Time has been provided as a filtering agent
        # Determine whether Time is provided as strings or orbits
        if len(time) != 2:
            if parameter is not None:
                print('*****WARNING*****')
                print('Time must be provided as a two-element list')
                print('of either strings (yyyy-mm-dd hh:mm:ss) ')
                print('or orbits.  Since a Parameter *was* provided,')
                print('I will filter on that, but ignore the time input.')
            else:
                # Cannot proceed with filtering
                insufficient_input_range_select()
                print('Time malformed must be either a string of format')
                print('yyyy-mm-ddThh:mm:ss or integer orbit)')
                print('and no Parameter criterion given')
        else:
            # We have a two-element Time list: parse it
            if not isinstance(type(time[0]), type(time[1])):
                if parameter is not None:
                    print('*****WARNING*****')
                    print('Both elements of time must be same type')
                    print('Only strings of format yyyy-mm-dd hh:mm:ss')
                    print('or integers (orbit numbers) are allowed.')
                    print('Ignoring time inputs; will filter ONLY')
                    print('on Parameter inputs.')
                else:
                    print('*****ERROR*****')
                    print('Both elements of Time must be same type')
                    print('Only Strings of format yyyy-mm-dd hh:mm:ss')
                    print('or integers (orbit numbers) are allowed.')
                    print('Returning original unchanged data dictionary')
                    return kp
            elif type(time[0]) is int:
                # Filter based on orbit number
                min_t = min(time)
                max_t = max(time)
                filter_list.append(kp['Orbit'] >= min_t)
                filter_list.append(kp['Orbit'] <= max_t)
            elif isinstance(time[0], str):
                # Filter acc to string dat, need to parse it
                time_dt = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in time]
                min_dt = min(time_dt)
                max_dt = max(time_dt)
                kp_dt = [datetime.strptime(i, '%Y-%m-%dT%H:%M:%S')
                         for i in kp['TimeString']]
                delta_tmin = np.array([(i - min_dt).total_seconds() for i in kp_dt])
                delta_tmax = np.array([(i - max_dt).total_seconds() for i in kp_dt])
                filter_list.append(delta_tmin >= 0)
                filter_list.append(delta_tmax <= 0)
            else:
                # Time provided as other than string or Integer
                if parameter is not None:
                    print('*****WARNING*****')
                    print('Both elements of time must be same type')
                    print('Only strings of format yyyy-mm-dd hh:mm:ss')
                    print('or integers (orbit numbers) are allowed.')
                    print('Ignoring time inputs; will filter ONLY')
                    print('on Parameter inputs.')
                else:
                    print('*****ERROR*****')
                    print('Both elements of Time must be same type')
                    print('Only Strings of format yyyy-mm-dd hh:mm:ss')
                    print('or integers (orbit numbers) are allowed.')
                    print('Returning original unchanged data dictionary')
                    return kp
            # Now, we apply the Parameter selection
            inst = []
            obs = []
            if isinstance(parameter, int) or isinstance(parameter, str):
                # Then we have a single Parameter to filter on
                # Verify that bounds info exists
                if minimum is None and maximum is None:
                    insufficient_input_range_select()
                    print('No bounds set for parameter %s' % parameter)
                    print('Applying only Time filtering')
                    parameter = None
                elif minimum is None:
                    minimum = -np.Infinity  # Unbounded below
                elif maximum is None:
                    maximum = np.Infinity  # Unbounded above
                else:
                    pass  # Range fully bounded
                a, b = get_inst_obs_labels(kp, parameter)
                inst.append(a)
                obs.append(b)
                nparam = 1  # necessary?
            elif type(parameter) is list:
                if len(parameter) != len(minimum) or len(parameter) != len(maximum):
                    print('*****ERROR*****')
                    print('---range_select---')
                    print('Number of minima and maxima provided')
                    print('MUST match number of Parameters provided')
                    print('You provided %4d Parameters' % len(parameter))
                    print('             %4d minima' % len(minimum))
                    print('         and %4d maxima' % len(maximum))
                    print('Filtering only on Time')
                    parameter = None
                else:
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


# --------------------------------------------------------------------------


def insufficient_input_range_select():
    '''
    This error message is called if user calls range_select with
    inputs that result in neither a valid Time range nor a valid
    Parameter range capable of being determined

    ToDo: Is there a way to hide this from the help feature?
    '''
    print('*****ERROR*****')
    print('Either a time criterion with two values.')
    print('  or a parameter name with maximum and/or')
    print('  minimum values must be provided.')
    print('Returning the complete original data dictionary')


# --------------------------------------------------------------------------

def get_inst_obs_labels(kp, name):
    '''
    Given parameter input in either string or integer format,
    identify the instrument name and observation type for use
    in accessing the relevant part of the data structure
    E.g.: 'LPW.EWAVE_LOW_FREQ' would be returned as
          ['LPW', 'EWAVE_LOW_FREQ']

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
        name: string identifying a parameter.
            (Indices must be converted to inst.obs strings before
             calling this routine)
    Output:
        inst (1st arg): instrument identifier
        obs (2nd arg): observation type identifier
    '''

    # Need to ensure name is a string at this stage
    name = ('%s' % name)

    # Now, split at the dot (if it exists)
    tags = name.split('.')
    # And consider the various possibilities...
    if len(tags) == 2:
        return tags
    elif len(tags) == 1:
        try:
            int(tags[0])
            return (find_param_from_index(kp, tags[0])).split('.')
        except:
            print('*****ERROR*****')
            print('%s is an invalid parameter' % name)
            print('If only one value is provided, it must be an integer')
            return
    else:
        print('*****ERROR*****')
        print('%s is not a valid parameter' % name)
        print('because it has %1d elements' % len(tags))
        print('Only 1 integer or string of form "a.b" are allowed.')
        print('Please use .param_list attribute to find valid parameters')
        return


def find_param_from_index(kp, index):
    '''
    Given an integer index, find the name of the parameter

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
        index: the index of the desired parameter (integer type)
    Output:
        A string of form <instrument>.<observation>
        (e.g., LPW.EWAVE_LOW_FREQ)
    '''

    index = '#%3d' % int(index)
    plist = param_list(kp)
    found = False
    for i in plist:
        if re.search(index, i):
            return i[5:]  # clip the '#123 ' string
    if not found:
        print('*****ERROR*****')
        print('%s not a valid index.' % index)
        print('Use param_list to list options')
        return


def remove_inst_tag(df):
    '''
    Remove the leading part of the column name that includes the instrument
    identifier for use in creating the parameter names for the toolkit.

    Input:
        A DataFrame produced from the insitu KP data
    Output:
        A new set of column names
    '''

    newcol = []
    for i in df.columns:
        if len(i.split('.')) >= 2:
            j = i.split('.')
            newcol.append('.'.join(j[1:]))

    return newcol


def get_latest_files_from_date_range(date1, date2):
    from datetime import timedelta

    mvn_root_data_dir = utils.get_root_data_dir()
    maven_data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', 'kp', 'insitu')

    # Each file starts at midnight, so lets cut off the hours and just pay attention to the days
    date1 = date1.replace(hour=0, minute=0, second=0)
    date2 = date2.replace(hour=0, minute=0, second=0) + timedelta(days=1)

    time_spanned = date2 - date1
    num_days = time_spanned.days

    filenames = []

    for i in range(num_days):
        current_date = date1 + timedelta(days=i)
        year = str(current_date.year)
        month = str('%02d' % current_date.month)
        day = str('%02d' % current_date.day)
        full_path = os.path.join(maven_data_dir, year, month)
        if os.path.exists(full_path):
            # Grab only the most recent version/revision of regular and crustal insitu files for each
            # day
            insitu = {}
            c_insitu = {}
            for f in os.listdir(full_path):
                # print(f)
                if kp_regex.match(f).group('day') == day and not kp_regex.match(f).group('description'):
                    v = kp_regex.match(f).group('version')
                    r = kp_regex.match(f).group('revision')
                    insitu[f] = [v, r]
                elif kp_regex.match(f).group('day') == day and kp_regex.match(f).group('description') == '_crustal':
                    v = kp_regex.match(f).group('version')
                    r = kp_regex.match(f).group('revision')
                    c_insitu[f] = [v, r]

            if insitu:
                # Get max version
                insitu_file = max(insitu.keys(), key=(lambda k: insitu[k][0]))
                max_v = re.search('v\d{2}', insitu_file).group(0)
                # Get max revision
                max_r = max([re.search('r\d{2}', k).group(0) for k in insitu if max_v in k])
                # Get most recent insitu file (based on max version, and then max revision values)
                most_recent_insitu = [f for f in insitu.keys() if max_r in f and max_v in f]
                filenames.append(os.path.join(full_path, most_recent_insitu[0]))

            if c_insitu:
                # Get max version
                c_insitu_file = max(c_insitu.keys(), key=(lambda k: c_insitu[k][0]))
                c_max_v = re.search('v\d{2}', c_insitu_file).group(0)
                # Get max revision
                c_max_r = max([re.search('r\d{2}', k).group(0) for k in c_insitu if c_max_v in k])
                # Get most recent insitu file (based on max version, and then max revision values)
                most_recent_c_insitu = [f for f in c_insitu.keys() if c_max_r in f and c_max_v in f]
                filenames.append(os.path.join(full_path, most_recent_c_insitu[0]))

    filenames = sorted(filenames)
    return filenames


def get_latest_iuvs_files_from_date_range(date1, date2):
    from datetime import timedelta

    mvn_root_data_dir = utils.get_root_data_dir()
    maven_data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', 'kp', 'iuvs')

    # Each file starts at midnight, so lets cut off the hours and just pay attention to the days
    date1 = date1.replace(hour=0, minute=0, second=0)
    date2 = date2.replace(day=date2.day, hour=0, minute=0, second=0) + timedelta(days=1)

    time_spanned = date2 - date1
    num_days = time_spanned.days

    files_to_return = []
    for i in range(num_days):
        current_date = date1 + timedelta(days=i)
        year = str(current_date.year)
        month = str('%02d' % current_date.month)
        day = str('%02d' % current_date.day)
        full_path = os.path.join(maven_data_dir, year, month)
        if os.path.exists(full_path):
            basenames = []
            # Obtain a list of all the basenames for the day
            for f in os.listdir(full_path):
                if kp_regex.match(f).group('day') == day:
                    description = kp_regex.match(f).group('description')
                    year = kp_regex.match(f).group('year')
                    month = kp_regex.match(f).group('month')
                    day = kp_regex.match(f).group('day')
                    time = kp_regex.match(f).group('time')
                    seq = ('mvn', 'kp', 'iuvs' + description, year + month + day + time)
                    basenames.append('_'.join(seq))

            basenames = list(set(basenames))

            for bn in basenames:
                version = 0
                revision = 0
                for f in os.listdir(full_path):
                    description = kp_regex.match(f).group('description')
                    year = kp_regex.match(f).group('year')
                    month = kp_regex.match(f).group('month')
                    day = kp_regex.match(f).group('day')
                    time = kp_regex.match(f).group('time')
                    seq = ('mvn', 'kp', 'iuvs' + description, year + month + day + time)
                    if bn == '_'.join(seq):
                        v = kp_regex.match(f).group('version')
                        if int(v) > int(version):
                            version = v

                for f in os.listdir(full_path):
                    description = kp_regex.match(f).group('description')
                    year = kp_regex.match(f).group('year')
                    month = kp_regex.match(f).group('month')
                    day = kp_regex.match(f).group('day')
                    time = kp_regex.match(f).group('time')
                    file_version = kp_regex.match(f).group('version')
                    seq = ('mvn', 'kp', 'iuvs' + description, year + month + day + time)
                    if bn == '_'.join(seq) and file_version == version:
                        r = kp_regex.match(f).group('revision')
                        if int(r) > int(revision):
                            revision = r
                if int(version) > 0:
                    seq = (bn, 'v' + str(version), 'r' + str(revision) + '.tab')
                    files_to_return.append(os.path.join(full_path, '_'.join(seq)))
    files_to_return = sorted(files_to_return)
    return files_to_return


def get_l2_files_from_date(date1, instrument):
    mvn_root_data_dir = utils.get_root_data_dir()
    maven_data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', instrument, 'l2')

    # Each file starts at midnight, so lets cut off the hours and just pay attention to the days
    date1 = date1.replace(hour=0, minute=0, second=0)

    filenames = []

    year = str(date1.year)
    month = str('%02d' % date1.month)
    day = str('%02d' % date1.day)
    full_path = os.path.join(maven_data_dir, year, month)
    if os.path.exists(full_path):
        for f in os.listdir(full_path):
            if l2_regex.match(f).group('day') == day:
                filenames.append(os.path.join(full_path, f))

    filenames = sorted(filenames)
    return filenames


def get_header_info(filename):
    # Determine number of header lines
    nheader = 0
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                nheader += 1

    # Parse the header (still needs special case work)
    read_param_list = False
    start_temp = False
    index_list = []
    with open(filename) as fin:
        icol = -2  # Counting header lines detailing column names
        iname = 1  # for counting seven lines with name info
        ncol = -1  # Dummy value to allow reading of early headerlines?
        col_regex = '#\s(.{16}){%3d}' % ncol  # needed for column names
        crustal = False
        if 'crustal' in filename:
            crustal = True
        for iline in range(nheader):
            line = fin.readline()
            # Define the proper indices change depending on the file type and row
            i = [2, 2, 1] if crustal else [1, 1, 1]
            if re.search('Number of parameter columns', line):
                ncol = int(re.split("\s{3}", line)[i[0]])
                # needed for column names
                col_regex = '#\s(.{16}){%2d}' % ncol if crustal else '#\s(.{16}){%3d}' % ncol
            elif re.search('Line on which data begins', line):
                nhead_test = int(re.split("\s{3}", line)[i[1]]) - 1
            elif re.search('Number of lines', line):
                ndata = int(re.split("\s{3}", line)[i[2]])
            elif re.search('PARAMETER', line):
                read_param_list = True
                param_head = iline
            elif read_param_list:
                icol += 1
                if icol > ncol:
                    read_param_list = False
            elif re.match(col_regex, line):
                # OK, verified match now get the values
                temp = re.findall('(.{16})', line[3:])
                if temp[0] == '               1':
                    start_temp = True
                if start_temp:
                    # Crustal files do not have as much variable info as other insitu files, need
                    # to modify the lines below
                    if crustal:
                        if iname == 1:
                            index = temp
                        elif iname == 2:
                            obs1 = temp
                        elif iname == 3:
                            obs2 = temp
                        elif iname == 4:
                            unit = temp
                            # crustal files don't come with this field
                            # throwing it in here for consistency with other insitu files
                            inst = ['     MODELED_MAG'] * 13
                        else:
                            print('More lines in data descriptor than expected.')
                            print('Line %d' % iline)
                    else:
                        if iname == 1:
                            index = temp
                        elif iname == 2:
                            obs1 = temp
                        elif iname == 3:
                            obs2 = temp
                        elif iname == 4:
                            obs3 = temp
                        elif iname == 5:
                            inst = temp
                        elif iname == 6:
                            unit = temp
                        elif iname == 7:
                            format_code = temp
                        else:
                            print('More lines in data descriptor than expected.')
                            print('Line %d' % iline)
                    iname += 1
            else:
                pass

        # Generate the names list.
        # NB, there are special case redundancies in there
        # (e.g., LPW: Electron Density Quality (min and max))
        # ****SWEA FLUX electron QUALITY *****
        first = True
        parallel = None
        names = []
        if crustal:
            for h, i, j in zip(inst, obs1, obs2):
                combo_name = (' '.join([i.strip(), j.strip()])).strip()
                # Add inst to names to avoid ambiguity
                # Will need to remove these after splitting
                names.append('.'.join([h.strip(), combo_name]))
                names[0] = 'Time'
        else:
            for h, i, j, k in zip(inst, obs1, obs2, obs3):
                combo_name = (' '.join([i.strip(), j.strip(), k.strip()])).strip()
                if re.match('^LPW$', h.strip()):
                    # Max and min error bars use same name in column
                    # SIS says first entry is min and second is max
                    if re.match('(Electron|Spacecraft)(.+)Quality', combo_name):
                        if first:
                            combo_name = combo_name + ' Min'
                            first = False
                        else:
                            combo_name = combo_name + ' Max'
                            first = True
                elif re.match('^SWEA$', h.strip()):
                    # electron flux qual flags do not indicate whether parallel or anti
                    # From context it is clear; but we need to specify in name
                    if re.match('.+Parallel.+', combo_name):
                        parallel = True
                    elif re.match('.+Anti-par', combo_name):
                        parallel = False
                    else:
                        pass
                    if re.match('Flux, e-(.+)Quality', combo_name):
                        if parallel:
                            p = re.compile('Flux, e- ')
                            combo_name = p.sub('Flux, e- Parallel ', combo_name)
                        else:
                            p = re.compile('Flux, e- ')
                            combo_name = p.sub('Flux, e- Anti-par ', combo_name)
                    if re.match('Electron eflux (.+)Quality', combo_name):
                        if parallel:
                            p = re.compile('Electron eflux ')
                            combo_name = p.sub('Electron eflux  Parallel ', combo_name)
                        else:
                            p = re.compile('Electron eflux ')
                            combo_name = p.sub('Electron eflux  Anti-par ', combo_name)
                # Add inst to names to avoid ambiguity
                # Will need to remove these after splitting
                names.append('.'.join([h.strip(), combo_name]))
                names[0] = 'Time'

    return names, inst


def initialize_list(the_list):
    index = 0
    for i in the_list:
        if hasattr(i, "__len__"):
            the_list[index] = initialize_list(i)
        else:
            the_list[index] = []
        index += 1
    return the_list


def place_values_in_list(the_list, location, to_append):
    testing = the_list
    if hasattr(location, "__len__"):
        for i in range(len(location)):
            testing = testing[location[i]]
        testing.append(to_append)
    else:
        testing = testing[location]
        testing.append(to_append)


def get_values_from_list(the_list, location):
    testing = the_list
    if hasattr(location, "__len__"):
        for i in range(len(location)):
            testing = testing[location[i]]
        return testing
    else:
        testing = testing[location]
        return testing


def orbit_time(begin_orbit, end_orbit=None):
    orb_file = os.path.join(os.path.dirname(__file__),
                            'maven_orb_rec.orb')

    with open(orb_file, "r") as f:
        if end_orbit is None:
            end_orbit = begin_orbit
        orbit_num = []
        time = []
        f.readline()
        f.readline()
        for line in f:
            line = line[0:28]
            line = line.split(' ')
            line = [x for x in line if x != '']
            orbit_num.append(int(line[0]))
            time.append(line[1] + "-" + month_to_num(line[2]) + "-" + line[3] + "T" + line[4])
        try:
            if orbit_num.index(begin_orbit) > len(time) or orbit_num.index(end_orbit) + 1 > len(time):
                print("Orbit numbers not found.  Please choose a number between 1 and %s.", orbit_num[-1])
                return [None, None]
            else:
                begin_time = time[orbit_num.index(begin_orbit)]
                end_time = time[orbit_num.index(end_orbit) + 1]
        except ValueError:
            return [None, None]
    return [begin_time, end_time]


def month_to_num(month_string):
    if month_string == 'JAN':
        return '01'
    if month_string == 'FEB':
        return '02'
    if month_string == 'MAR':
        return '03'
    if month_string == 'APR':
        return '04'
    if month_string == 'MAY':
        return '05'
    if month_string == 'JUN':
        return '06'
    if month_string == 'JUL':
        return '07'
    if month_string == 'AUG':
        return '08'
    if month_string == 'SEP':
        return '09'
    if month_string == 'OCT':
        return '10'
    if month_string == 'NOV':
        return '11'
    if month_string == 'DEC':
        return '12'


def mvn_kp_sc_traj_xyz(dims_x, dims_y, dims_z, values, x_array, y_array, z_array, nn='linear'):
    data = []
    if nn == 'nearest':
        for x, y, z in np.array([a for a in zip(x_array, y_array, z_array)]):
            ix = np.abs(dims_x - x).argmin()
            iy = np.abs(dims_y - y).argmin()
            iz = np.abs(dims_z - z).argmin()
            data.append(values[ix, iy, iz])
    else:
        max_x = np.max(x_array)
        min_x = np.min(x_array)
        max_y = np.max(y_array)
        min_y = np.min(y_array)
        max_z = np.max(z_array)
        min_z = np.min(z_array)

        for x, y, z in np.array([a for a in zip(x_array, y_array, z_array)]):
            if x > max_x:
                data.append(np.NaN)
            elif x < min_x:
                data.append(np.NaN)
            elif y > max_y:
                data.append(np.NaN)
            elif y < min_y:
                data.append(np.NaN)
            elif z > max_z:
                data.append(np.NaN)
            elif z < min_z:
                data.append(np.NaN)

            sorted_x_distance = np.argsort(np.abs(dims_x - x))
            ix1 = dims_x[sorted_x_distance[0]]
            ix2 = dims_x[sorted_x_distance[1]]
            if ix2 < ix1:
                temp = ix2
                ix2 = ix1
                ix1 = temp
            sorted_y_distance = np.argsort(np.abs(dims_y - y))
            iy1 = dims_y[sorted_y_distance[0]]
            iy2 = dims_y[sorted_y_distance[1]]
            if iy2 < iy1:
                temp = iy2
                iy2 = iy1
                iy1 = temp
            sorted_z_distance = np.argsort(np.abs(dims_z - z))
            iz1 = dims_z[sorted_z_distance[0]]
            iz2 = dims_z[sorted_z_distance[1]]
            if iz2 < iz1:
                temp = iz2
                iz2 = iz1
                iz1 = temp

            nx = (x - ix1) / (ix2 - ix1)
            ny = (y - iy1) / (iy2 - iy1)
            nz = (z - iz1) / (iz2 - iz1)

            data.append(values[sorted_x_distance[0], sorted_y_distance[0], sorted_z_distance[0]]
                        * (1 - nx) * (1 - ny) * (1 - nz) +
                        values[sorted_x_distance[1], sorted_y_distance[0], sorted_z_distance[0]]
                        * nx * (1 - ny) * (1 - nz) +
                        values[sorted_x_distance[0], sorted_y_distance[1], sorted_z_distance[0]]
                        * (1 - nx) * ny * (1 - nz) +
                        values[sorted_x_distance[0], sorted_y_distance[0], sorted_z_distance[1]]
                        * (1 - nx) * (1 - ny) * nz +
                        values[sorted_x_distance[1], sorted_y_distance[0], sorted_z_distance[1]]
                        * nx * (1 - ny) * nz +
                        values[sorted_x_distance[0], sorted_y_distance[1], sorted_z_distance[1]]
                        * (1 - nx) * ny * nz +
                        values[sorted_x_distance[1], sorted_y_distance[1], sorted_z_distance[0]]
                        * nx * ny * (1 - nz) +
                        values[sorted_x_distance[1], sorted_y_distance[1], sorted_z_distance[1]]
                        * nx * ny * nz)
    return data


def read_iuvs_file(file):
    iuvs_dict = {}
    periapse_num = 0
    occ_num = 0
    with open(file) as f:
        line = f.readline()
        while line != '':
            if line.startswith('*'):
                # Read the header
                line = f.readline()
                obs_mode = line[19:len(line) - 1].strip()

                header = {}
                f.readline()
                line = f.readline()
                header['time_start'] = line[19:len(line) - 1].strip()
                line = f.readline()
                header['time_stop'] = line[19:len(line) - 1].strip()
                line = f.readline()
                if obs_mode == "OCCULTATION":
                    header['target_name'] = line[19:len(line) - 1].strip()
                    line = f.readline()
                header['sza'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['local_time'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['lat'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['lon'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['lat_mso'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['lon_mso'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['orbit_number'] = int(line[19:len(line) - 1].strip())
                line = f.readline()
                header['mars_season'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_geo_x'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_geo_y'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_geo_z'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_mso_x'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_mso_y'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_mso_z'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_geo_x'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_geo_y'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_geo_z'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_geo_lat'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_geo_lon'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_mso_lat'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sun_mso_lon'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['subsol_geo_lon'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['subsol_geo_lat'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_sza'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_local_time'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['sc_alt'] = float(line[19:len(line) - 1].strip())
                line = f.readline()
                header['mars_sun_dist'] = float(line[19:len(line) - 1].strip())

                if obs_mode == "PERIAPSE":
                    periapse_num += 1
                    line = f.readline()
                    n_alt_bins = int(line[19:len(line) - 1].strip())
                    header['n_alt_bins'] = float(n_alt_bins)
                    line = f.readline()
                    n_alt_den_bins = int(line[19:len(line) - 1].strip())
                    header['n_alt_den_bins'] = float(n_alt_den_bins)

                    iuvs_dict['periapse' + str(periapse_num)] = {}
                    iuvs_dict['periapse' + str(periapse_num)].update(header)

                    # Empty space
                    f.readline()

                    # Read the Temperature
                    line = f.readline()
                    temp_labels = line[19:len(line) - 1].strip().split()
                    temperature = collections.OrderedDict((x, []) for x in temp_labels)
                    temperature_unc = collections.OrderedDict((x, []) for x in temp_labels)
                    line = f.readline()
                    vals = line[20:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        temperature[list(temperature.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[20:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        temperature_unc[list(temperature_unc.keys())[index]].append(val)
                        index += 1
                    iuvs_dict['periapse' + str(periapse_num)]['temperature'] = temperature
                    iuvs_dict['periapse' + str(periapse_num)]['temperature_unc'] = temperature_unc

                    # Empty space
                    f.readline()

                    # Read the Scale Heights
                    line = f.readline()
                    scale_height_labels = line[19:len(line) - 1].strip().split()
                    scale_height = collections.OrderedDict((x, []) for x in scale_height_labels)
                    scale_height_unc = collections.OrderedDict((x, []) for x in scale_height_labels)
                    line = f.readline()
                    vals = line[20:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        scale_height[list(scale_height.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[20:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        scale_height_unc[list(scale_height_unc.keys())[index]].append(val)
                        index += 1

                    iuvs_dict['periapse' + str(periapse_num)]['scale_height'] = scale_height
                    iuvs_dict['periapse' + str(periapse_num)]['scale_height_unc'] = scale_height_unc

                    # Empty space
                    f.readline()
                    f.readline()

                    # Read in the density
                    line = f.readline()
                    density_labels = line.strip().split()
                    density = collections.OrderedDict((x, []) for x in density_labels)
                    for i in range(0, n_alt_den_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            density[list(density.keys())[index]].append(val)
                            index += 1
                    iuvs_dict['periapse' + str(periapse_num)]['density'] = density

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density systematic uncertainty
                    density_sys_unc = collections.OrderedDict((x, []) for x in density_labels)
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        density_sys_unc[list(density.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict['periapse' + str(periapse_num)]['density_sys_unc'] = density_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density uncertainty
                    density_unc = collections.OrderedDict((x, []) for x in density_labels)
                    for i in range(0, n_alt_den_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            density_unc[list(density.keys())[index]].append(val)
                            index += 1
                    iuvs_dict['periapse' + str(periapse_num)]['density_sys_unc'] = density_sys_unc

                    f.readline()
                    f.readline()

                    line = f.readline()
                    radiance_labels = line.strip().split()
                    if "Cameron" in radiance_labels:
                        radiance_labels.remove('Cameron')
                    radiance = collections.OrderedDict((x, []) for x in radiance_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            radiance[list(radiance.keys())[index]].append(val)
                            index += 1

                    iuvs_dict['periapse' + str(periapse_num)]['radiance'] = radiance

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance systematic uncertainty
                    radiance_sys_unc = collections.OrderedDict((x, []) for x in radiance_labels)
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        radiance_sys_unc[list(radiance.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict['periapse' + str(periapse_num)]['radiance_sys_unc'] = radiance_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance uncertainty
                    radiance_unc = collections.OrderedDict((x, []) for x in radiance_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            radiance_unc[list(radiance.keys())[index]].append(val)
                            index += 1

                    iuvs_dict['periapse' + str(periapse_num)]['radiance_unc'] = radiance_unc

                elif obs_mode == "OCCULTATION":
                    occ_num += 1
                    line = f.readline()
                    n_alt_den_bins = int(line[19:len(line) - 1].strip())
                    header['n_alt_den_bins'] = float(n_alt_den_bins)

                    iuvs_dict['occultation' + str(occ_num)] = {}
                    iuvs_dict['occultation' + str(occ_num)].update(header)

                    # Empty space
                    f.readline()

                    # Read the Scale Heights
                    line = f.readline()
                    scale_height_labels = line[19:len(line) - 1].strip().split()
                    scale_height = collections.OrderedDict((x, []) for x in scale_height_labels)
                    scale_height_unc = collections.OrderedDict((x, []) for x in scale_height_labels)
                    line = f.readline()
                    vals = line[20:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        scale_height[list(scale_height.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[20:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        scale_height_unc[list(scale_height_unc.keys())[index]].append(val)
                        index += 1

                    iuvs_dict['occultation' + str(occ_num)]['scale_height'] = scale_height
                    iuvs_dict['occultation' + str(occ_num)]['scale_height_unc'] = scale_height_unc

                    # Empty space
                    f.readline()
                    f.readline()

                    # Read in the retrieval
                    line = f.readline()
                    retrieval_labels = line.strip().split()
                    retrieval = collections.OrderedDict((x, []) for x in retrieval_labels)
                    for i in range(0, n_alt_den_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            retrieval[list(retrieval.keys())[index]].append(val)
                            index += 1
                    iuvs_dict['occultation' + str(occ_num)]['retrieval'] = retrieval

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the retrieval systematic uncertainty
                    retrieval_sys_unc = collections.OrderedDict((x, []) for x in retrieval_labels)
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        retrieval_sys_unc[list(retrieval.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict['occultation' + str(occ_num)]['retrieval_sys_unc'] = retrieval_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the retrieval uncertainty
                    retrieval_unc = collections.OrderedDict((x, []) for x in retrieval_labels)
                    for i in range(0, n_alt_den_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            retrieval_unc[list(retrieval.keys())[index]].append(val)
                            index += 1
                    iuvs_dict['occultation' + str(occ_num)]['retrieval_sys_unc'] = retrieval_sys_unc

                elif obs_mode == "CORONA_LORES_HIGH":
                    line = f.readline()
                    n_alt_bins = int(line[19:len(line) - 1].strip())
                    header['n_alt_bins'] = float(n_alt_bins)

                    iuvs_dict['corona_lores_high'] = {}
                    iuvs_dict['corona_lores_high'].update(header)

                    f.readline()

                    # Read the Half int
                    line = f.readline()
                    half_int_dist_labels = line[19:len(line) - 1].strip().split()
                    half_int_dist = collections.OrderedDict((x, []) for x in half_int_dist_labels)
                    half_int_dist_unc = collections.OrderedDict((x, []) for x in half_int_dist_labels)
                    line = f.readline()
                    vals = line[26:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        half_int_dist[list(half_int_dist.keys())[index]].append(val)
                        index += 1
                    line = f.readline()
                    vals = line[26:len(line) - 1].strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        half_int_dist_unc[list(half_int_dist_unc.keys())[index]].append(val)
                        index += 1

                    iuvs_dict['corona_lores_high']['half_int_dist'] = half_int_dist
                    iuvs_dict['corona_lores_high']['half_int_dist_unc'] = half_int_dist_unc

                    # Blank space
                    f.readline()
                    f.readline()

                    # Read in the density
                    line = f.readline()
                    density_labels = line.strip().split()
                    density = collections.OrderedDict((x, []) for x in density_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            density[list(density.keys())[index]].append(val)
                            index += 1

                    iuvs_dict['corona_lores_high']['density'] = density

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density systematic uncertainty
                    density_sys_unc = collections.OrderedDict((x, []) for x in density_labels)
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        density_sys_unc[list(density.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict['corona_lores_high']['density_sys_unc'] = density_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the density uncertainty
                    density_unc = collections.OrderedDict((x, []) for x in density_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            density_unc[list(density.keys())[index]].append(val)
                            index += 1

                    iuvs_dict['corona_lores_high']['density_unc'] = density_unc

                    f.readline()
                    f.readline()

                    line = f.readline()
                    radiance_labels = line.strip().split()
                    if "Cameron" in radiance_labels:
                        radiance_labels.remove('Cameron')
                    radiance = collections.OrderedDict((x, []) for x in radiance_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            radiance[list(radiance.keys())[index]].append(val)
                            index += 1

                    iuvs_dict['corona_lores_high']['radiance'] = radiance

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance systematic uncertainty
                    radiance_sys_unc = collections.OrderedDict((x, []) for x in radiance_labels)
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        radiance_sys_unc[list(radiance.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict['corona_lores_high']['radiance_sys_unc'] = radiance_sys_unc

                    # Not needed lines
                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance uncertainty
                    radiance_unc = collections.OrderedDict((x, []) for x in radiance_labels)
                    for i in range(0, n_alt_bins):
                        line = f.readline()
                        vals = line.strip().split()
                        index = 0
                        for val in vals:
                            if val == '-9.9999990E+09':
                                val = float('nan')
                            else:
                                val = float(val)
                            radiance_unc[list(radiance.keys())[index]].append(val)
                            index += 1

                    iuvs_dict['corona_lores_high']['radiance_unc'] = radiance_unc

                elif obs_mode == 'APOAPSE':

                    f.readline()
                    maps = {}
                    for j in range(0, 17):
                        var = f.readline().strip()
                        line = f.readline()
                        lons = line.strip().split()
                        lons = [float(x) for x in lons]
                        lats = []
                        data = []
                        for k in range(0, 45):
                            line = f.readline().strip().split()
                            lats.append(float(line[0]))
                            line_data = line[1:]
                            line_data = [float(x) if x != '-9.9999990E+09' else float('nan') for x in line_data]
                            data.append(line_data)

                        maps[var] = data
                        f.readline()

                    maps['latitude'] = lats
                    maps['longitude'] = lons

                    iuvs_dict['apoapse'] = {}
                    iuvs_dict['apoapse'].update(header)
                    iuvs_dict['apoapse'].update(maps)

                    f.readline()
                    f.readline()
                    f.readline()

                    # Read in the radiance systematic uncertainty
                    line = f.readline()
                    radiance_labels = line.strip().split()
                    radiance_sys_unc = collections.OrderedDict((x, []) for x in radiance_labels)
                    line = f.readline()
                    vals = line.strip().split()
                    index = 0
                    for val in vals:
                        if val == '-9.9999990E+09':
                            val = float('nan')
                        else:
                            val = float(val)
                        radiance_sys_unc[list(radiance.keys())[index + 1]].append(val)
                        index += 1

                    iuvs_dict['apoapse']['radiance_sys_unc'] = radiance_sys_unc

            line = f.readline()

    return iuvs_dict


param_dict = {'Electron Density': 'ELECTRON_DENSITY',
              'Electron Density Quality Min': 'ELECTRON_DENSITY_QUAL_MIN',
              'Electron Density Quality Max': 'ELECTRON_DENSITY_QUAL_MAX',
              'Electron Temperature': 'ELECTRON_TEMPERATURE',
              'Electron Temperature Quality Min': 'ELECTRON_TEMPERATURE_QUAL_MIN',
              'Electron Temperature Quality Max': 'ELECTRON_TEMPERATURE_QUAL_MAX',
              'Spacecraft Potential': 'SPACECRAFT_POTENTIAL',
              'Spacecraft Potential Quality Min': 'SPACECRAFT_POTENTIAL_QUAL_MIN',
              'Spacecraft Potential Quality Max': 'SPACECRAFT_POTENTIAL_QUAL_MAX',
              'E-field Power 2-100 Hz': 'EWAVE_LOW_FREQ',
              'E-field 2-100 Hz Quality': 'EWAVE_LOW_FREQ_QUAL_QUAL',
              'E-field Power 100-800 Hz': 'EWAVE_MID_FREQ',
              'E-field 100-800 Hz Quality': 'EWAVE_MID_FREQ_QUAL_QUAL',
              'E-field Power 0.8-1.0 Mhz': 'EWAVE_HIGH_FREQ',
              'E-field 0.8-1.0 Mhz Quality': 'EWAVE_HIGH_FREQ_QUAL_QUAL',
              'EUV Irradiance 0.1-7.0 nm': 'IRRADIANCE_LOW',
              'Irradiance 0.1-7.0 nm Quality': 'IRRADIANCE_LOW_QUAL',
              'EUV Irradiance 17-22 nm': 'IRRADIANCE_MID',
              'Irradiance 17-22 nm Quality': 'IRRADIANCE_MID_QUAL',
              'EUV Irradiance Lyman-alpha': 'IRRADIANCE_LYMAN',
              'Irradiance Lyman-alpha Quality': 'IRRADIANCE_LYMAN_QUAL',
              'Solar Wind Electron Density': 'SOLAR_WIND_ELECTRON_DENSITY',
              'Solar Wind E- Density Quality': 'SOLAR_WIND_ELECTRON_DENSITY_QUAL',
              'Solar Wind Electron Temperature': 'SOLAR_WIND_ELECTRON_TEMPERATURE',
              'Solar Wind E- Temperature Quality': 'SOLAR_WIND_ELECTRON_TEMPERATURE_QUAL',
              'Flux, e- Parallel (5-100 ev)': 'ELECTRON_PARALLEL_FLUX_LOW',
              'Flux, e- Parallel (5-100 ev) Quality': 'ELECTRON_PARALLEL_FLUX_LOW_QUAL',
              'Flux, e- Parallel (100-500 ev)': 'ELECTRON_PARALLEL_FLUX_MID',
              'Flux, e- Parallel (100-500 ev) Quality': 'ELECTRON_PARALLEL_FLUX_MID_QUAL',
              'Flux, e- Parallel (500-1000 ev)': 'ELECTRON_PARALLEL_FLUX_HIGH',
              'Flux, e- Parallel (500-1000 ev) Quality': 'ELECTRON_PARALLEL_FLUX_HIGH_QUAL',
              'Flux, e- Anti-par (5-100 ev)': 'ELECTRON_ANTI_PARALLEL_FLUX_LOW',
              'Flux, e- Anti-par (5-100 ev) Quality': 'ELECTRON_ANTI_PARALLEL_FLUX_LOW_QUAL',
              'Flux, e- Anti-par (100-500 ev)': 'ELECTRON_ANTI_PARALLEL_FLUX_MID',
              'Flux, e- Anti-par (100-500 ev) Quality': 'ELECTRON_ANTI_PARALLEL_FLUX_MID_QUAL',
              'Flux, e- Anti-par (500-1000 ev)': 'ELECTRON_ANTI_PARALLEL_FLUX_HIGH',
              'Flux, e- Anti-par (500-1000 ev) Quality': 'ELECTRON_ANTI_PARALLEL_FLUX_HIGH_QUAL',
              'Electron eflux Parallel (5-100 ev)': 'ELECTRON_PARALLEL_FLUX_LOW',
              'Electron eflux Parallel (5-100 ev) Quality': 'ELECTRON_PARALLEL_FLUX_LOW_QUAL',
              'Electron eflux Parallel (100-500 ev)': 'ELECTRON_PARALLEL_FLUX_MID',
              'Electron eflux Parallel (100-500 ev) Quality': 'ELECTRON_PARALLEL_FLUX_MID_QUAL',
              'Electron eflux Parallel (500-1000 ev)': 'ELECTRON_PARALLEL_FLUX_HIGH',
              'Electron eflux Parallel (500-1000 ev) Quality': 'ELECTRON_PARALLEL_FLUX_HIGH_QUAL',
              'Electron eflux Anti-par (5-100 ev)': 'ELECTRON_ANTI_PARALLEL_FLUX_LOW',
              'Electron eflux Anti-par (5-100 ev) Quality': 'ELECTRON_ANTI_PARALLEL_FLUX_LOW_QUAL',
              'Electron eflux Anti-par (100-500 ev)': 'ELECTRON_ANTI_PARALLEL_FLUX_MID',
              'Electron eflux Anti-par (100-500 ev) Quality': 'ELECTRON_ANTI_PARALLEL_FLUX_MID_QUAL',
              'Electron eflux Anti-par (500-1000 ev)': 'ELECTRON_ANTI_PARALLEL_FLUX_HIGH',
              'Electron eflux Anti-par (500-1000 ev) Quality': 'ELECTRON_ANTI_PARALLEL_FLUX_HIGH_QUAL',
              'Electron Spectrum Shape': 'ELECTRON_SPECTRUM_SHAPE_PARAMETER',
              'Spectrum Shape Quality': 'ELECTRON_SPECTRUM_SHAPE_PARAMETER_QUAL',
              'H+ Density': 'HPLUS_DENSITY',
              'H+ Density Quality': 'HPLUS_DENSITY_QUAL',
              'H+ Flow Velocity MSO X': 'HPLUS_FLOW_VELOCITY_MSO_X',
              'H+ Flow MSO X Quality': 'HPLUS_FLOW_VELOCITY_MSO_X_QUAL',
              'H+ Flow Velocity MSO Y': 'HPLUS_FLOW_VELOCITY_MSO_Y',
              'H+ Flow MSO Y Quality': 'HPLUS_FLOW_VELOCITY_MSO_Y_QUAL',
              'H+ Flow Velocity MSO Z': 'HPLUS_FLOW_VELOCITY_MSO_Z',
              'H+ Flow MSO Z Quality': 'HPLUS_FLOW_VELOCITY_MSO_Z_QUAL',
              'H+ Temperature': 'HPLUS_TEMPERATURE',
              'H+ Temperature Quality': 'HPLUS_TEMPERATURE_QUAL',
              'Solar Wind Dynamic Pressure': 'SOLAR_WIND_DYNAMIC_PRESSURE',
              'Solar Wind Pressure Quality': 'SOLAR_WIND_DYNAMIC_PRESSURE_QUAL',
              'STATIC Quality Flag': 'STATIC_QUALITY_FLAG',
              'O+ Density': 'OPLUS_DENSITY',
              'O+ Density Quality': 'OPLUS_DENSITY_QUAL',
              'O2+ Density': 'O2PLUS_DENSITY',
              'O2+ Density Quality': 'O2PLUS_DENSITY_QUAL',
              'O+ Temperature': 'OPLUS_TEMPERATURE',
              'O+ Temperature Quality': 'OPLUS_TEMPERATURE_QUAL',
              'O2+ Temperature': 'O2PLUS_TEMPERATURE',
              'O2+ Temperature Quality': 'O2PLUS_TEMPERATURE_QUAL',
              'O2+ Flow Velocity MAVEN_APP X': 'O2PLUS_FLOW_VELOCITY_MAVEN_APP_X',
              'O2+ Flow MAVEN_APP X Quality': 'O2PLUS_FLOW_VELOCITY_MAVEN_APP_X_QUAL',
              'O2+ Flow Velocity MAVEN_APP Y': 'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Y',
              'O2+ Flow MAVEN_APP Y Quality': 'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Y_QUAL',
              'O2+ Flow Velocity MAVEN_APP Z': 'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Z',
              'O2+ Flow MAVEN_APP Z Quality': 'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Z_QUAL',
              'O2+ Flow Velocity MSO X': 'O2PLUS_FLOW_VELOCITY_MSO_X',
              'O2+ Flow MSO X Quality': 'O2PLUS_FLOW_VELOCITY_MSO_X_QUAL',
              'O2+ Flow Velocity MSO Y': 'O2PLUS_FLOW_VELOCITY_MSO_Y',
              'O2+ Flow MSO Y Quality': 'O2PLUS_FLOW_VELOCITY_MSO_Y_QUAL',
              'O2+ Flow Velocity MSO Z': 'O2PLUS_FLOW_VELOCITY_MSO_Z',
              'O2+ Flow MSO Z Quality': 'O2PLUS_FLOW_VELOCITY_MSO_Z_QUAL',
              'H+ Omni Flux': 'HPLUS_OMNI_DIRECTIONAL_FLUX',
              'H+ Energy': 'HPLUS_CHARACTERISTIC_ENERGY',
              'H+ Energy Quality': 'HPLUS_CHARACTERISTIC_ENERGY_QUAL',
              'He++ Omni Flux': 'HEPLUS_OMNI_DIRECTIONAL_FLUX',
              'He++ Energy': 'HEPLUS_CHARACTERISTIC_ENERGY',
              'He++ Energy Quality': 'HEPLUS_CHARACTERISTIC_ENERGY_QUAL',
              'O+ Omni Flux': 'OPLUS_OMNI_DIRECTIONAL_FLUX',
              'O+ Energy': 'OPLUS_CHARACTERISTIC_ENERGY',
              'O+ Energy Quality': 'OPLUS_CHARACTERISTIC_ENERGY_QUAL',
              'O2+ Omni Flux': 'O2PLUS_OMNI_DIRECTIONAL_FLUX',
              'O2+ Energy': 'O2PLUS_CHARACTERISTIC_ENERGY',
              'O2+ Energy Quality': 'O2PLUS_CHARACTERISTIC_ENERGY_QUAL',
              'H+ Direction MSO X': 'HPLUS_CHARACTERISTIC_DIRECTION_MSO_X',
              'H+ Direction MSO Y': 'HPLUS_CHARACTERISTIC_DIRECTION_MSO_Y',
              'H+ Direction MSO Z': 'HPLUS_CHARACTERISTIC_DIRECTION_MSO_Z',
              'H+ Angular Width': 'HPLUS_CHARACTERISTIC_ANGULAR_WIDTH',
              'H+ Width Quality': 'HPLUS_CHARACTERISTIC_ANGULAR_WIDTH_QUAL',
              'Pickup Ion Direction MSO X': 'DOMINANT_PICKUP_ION_CHARACTERISTIC_DIRECTION_MSO_X',
              'Pickup Ion Direction MSO Y': 'DOMINANT_PICKUP_ION_CHARACTERISTIC_DIRECTION_MSO_Y',
              'Pickup Ion Direction MSO Z': 'DOMINANT_PICKUP_ION_CHARACTERISTIC_DIRECTION_MSO_Z',
              'Pickup Ion Angular Width': 'DOMINANT_PICKUP_ION_CHARACTERISTIC_ANGULAR_WIDTH',
              'Pickup Ion Width Quality': 'DOMINANT_PICKUP_ION_CHARACTERISTIC_ANGULAR_WIDTH_QUAL',
              'Ion Flux FOV 1 F': 'ION_ENERGY_FLUX__FOV_1_F',
              'Ion Flux FOV 1F Quality': 'ION_ENERGY_FLUX__FOV_1_F_QUAL',
              'Ion Flux FOV 1 R': 'ION_ENERGY_FLUX__FOV_1_R',
              'Ion Flux FOV 1R Quality': 'ION_ENERGY_FLUX__FOV_1_R_QUAL',
              'Ion Flux FOV 2 F': 'ION_ENERGY_FLUX__FOV_2_F',
              'Ion Flux FOV 2F Quality': 'ION_ENERGY_FLUX__FOV_2_F_QUAL',
              'Ion Flux FOV 2 R': 'ION_ENERGY_FLUX__FOV_2_R',
              'Ion Flux FOV 2R Quality': 'ION_ENERGY_FLUX__FOV_2_R_QUAL',
              'Electron Flux FOV 1 F': 'ELECTRON_ENERGY_FLUX___FOV_1_F',
              'Electron Flux FOV 1F Quality': 'ELECTRON_ENERGY_FLUX___FOV_1_F_QUAL',
              'Electron Flux FOV 1 R': 'ELECTRON_ENERGY_FLUX___FOV_1_R',
              'Electron Flux FOV 1R Quality': 'ELECTRON_ENERGY_FLUX___FOV_1_R_QUAL',
              'Electron Flux FOV 2 F': 'ELECTRON_ENERGY_FLUX___FOV_2_F',
              'Electron Flux FOV 2F Quality': 'ELECTRON_ENERGY_FLUX___FOV_2_F_QUAL',
              'Electron Flux FOV 2 R': 'ELECTRON_ENERGY_FLUX___FOV_2_R',
              'Electron Flux FOV 2R Quality': 'ELECTRON_ENERGY_FLUX___FOV_2_R_QUAL',
              'Look Direction 1-F MSO X': 'LOOK_DIRECTION_1_F_MSO_X',
              'Look Direction 1-F MSO Y': 'LOOK_DIRECTION_1_F_MSO_Y',
              'Look Direction 1-F MSO Z': 'LOOK_DIRECTION_1_F_MSO_Z',
              'Look Direction 1-R MSO X': 'LOOK_DIRECTION_1_R_MSO_X',
              'Look Direction 1-R MSO Y': 'LOOK_DIRECTION_1_R_MSO_Y',
              'Look Direction 1-R MSO Z': 'LOOK_DIRECTION_1_R_MSO_Z',
              'Look Direction 2-F MSO X': 'LOOK_DIRECTION_2_F_MSO_X',
              'Look Direction 2-F MSO Y': 'LOOK_DIRECTION_2_F_MSO_Y',
              'Look Direction 2-F MSO Z': 'LOOK_DIRECTION_2_F_MSO_Z',
              'Look Direction 2-R MSO X': 'LOOK_DIRECTION_2_R_MSO_X',
              'Look Direction 2-R MSO Y': 'LOOK_DIRECTION_2_R_MSO_Y',
              'Look Direction 2-R MSO Z': 'LOOK_DIRECTION_2_R_MSO_Z',
              'Magnetic Field MSO X': 'MSO_X',
              'Magnetic MSO X Quality': 'MSO_X_QUAL',
              'Magnetic Field MSO Y': 'MSO_Y',
              'Magnetic MSO Y Quality': 'MSO_Y_QUAL',
              'Magnetic Field MSO Z': 'MSO_Z',
              'Magnetic MSO Z Quality': 'MSO_Z_QUAL',
              'Magnetic Field GEO X': 'GEO_X',
              'Magnetic GEO X Quality': 'GEO_X_QUAL',
              'Magnetic Field GEO Y': 'GEO_Y',
              'Magnetic GEO Y Quality': 'GEO_Y_QUAL',
              'Magnetic Field GEO Z': 'GEO_Z',
              'Magnetic GEO Z Quality': 'GEO_Z_QUAL',
              'Magnetic Field RMS Dev': 'RMS_DEVIATION',
              'Magnetic RMS Quality': 'RMS_DEVIATION_QUAL',
              'Density He': 'HE_DENSITY',
              'Density He Precision': 'HE_DENSITY_PRECISION',
              'Density He Quality': 'HE_DENSITY_QUAL',
              'Density O': 'O_DENSITY',
              'Density O Precision': 'O_DENSITY_PRECISION',
              'Density O Quality': 'O_DENSITY_QUAL',
              'Density CO': 'CO_DENSITY',
              'Density CO Precision': 'CO_DENSITY_PRECISION',
              'Density CO Quality': 'CO_DENSITY_QUAL',
              'Density N2': 'N2_DENSITY',
              'Density N2 Precision': 'N2_DENSITY_PRECISION',
              'Density N2 Quality': 'N2_DENSITY_QUAL',
              'Density NO': 'NO_DENSITY',
              'Density NO Precision': 'NO_DENSITY_PRECISION',
              'Density NO Quality': 'NO_DENSITY_QUAL',
              'Density Ar': 'AR_DENSITY',
              'Density Ar Precision': 'AR_DENSITY_PRECISION',
              'Density Ar Quality': 'AR_DENSITY_QUAL',
              'Density CO2': 'CO2_DENSITY',
              'Density CO2 Precision': 'CO2_DENSITY_PRECISION',
              'Density CO2 Quality': 'CO2_DENSITY_QUAL',
              'Density 32+': 'O2PLUS_DENSITY',
              'Density 32+ Precision': 'O2PLUS_DENSITY_PRECISION',
              'Density 32+ Quality': 'O2PLUS_DENSITY_QUAL',
              'Density 44+': 'CO2PLUS_DENSITY',
              'Density 44+ Precision': 'CO2PLUS_DENSITY_PRECISION',
              'Density 44+ Quality': 'CO2PLUS_DENSITY_QUAL',
              'Density 30+': 'NOPLUS_DENSITY',
              'Density 30+ Precision': 'NOPLUS_DENSITY_PRECISION',
              'Density 30+ Quality': 'NOPLUS_DENSITY_QUAL',
              'Density 16+': 'OPLUS_DENSITY',
              'Density 16+ Precision': 'OPLUS_DENSITY_PRECISION',
              'Density 16+ Quality': 'OPLUS_DENSITY_QUAL',
              'Density 28+': 'CO2PLUS_N2PLUS_DENSITY',
              'Density 28+ Precision': 'CO2PLUS_N2PLUS_DENSITY_PRECISION',
              'Density 28+ Quality': 'CO2PLUS_N2PLUS_DENSITY_QUAL',
              'Density 12+': 'CPLUS_DENSITY',
              'Density 12+ Precision': 'CPLUS_DENSITY_PRECISION',
              'Density 12+ Quality': 'CPLUS_DENSITY_QUAL',
              'Density 17+': 'OHPLUS_DENSITY',
              'Density 17+ Precision': 'OHPLUS_DENSITY_PRECISION',
              'Density 17+ Quality': 'OHPLUS_DENSITY_QUAL',
              'Density 14+': 'NPLUS_DENSITY',
              'Density 14+ Precision': 'NPLUS_DENSITY_PRECISION',
              'Density 14+ Quality': 'NPLUS_DENSITY_QUAL',
              'APP Attitude GEO X': 'ATTITUDE_GEO_X',
              'APP Attitude GEO Y': 'ATTITUDE_GEO_Y',
              'APP Attitude GEO Z': 'ATTITUDE_GEO_Z',
              'APP Attitude MSO X': 'ATTITUDE_MSO_X',
              'APP Attitude MSO Y': 'ATTITUDE_MSO_Y',
              'APP Attitude MSO Z': 'ATTITUDE_MSO_Z',
              'Spacecraft GEO X': 'GEO_X',
              'Spacecraft GEO Y': 'GEO_Y',
              'Spacecraft GEO Z': 'GEO_Z',
              'Spacecraft MSO X': 'MSO_X',
              'Spacecraft MSO Y': 'MSO_Y',
              'Spacecraft MSO Z': 'MSO_Z',
              'Spacecraft GEO Longitude': 'SUB_SC_LONGITUDE',
              'Spacecraft GEO Latitude': 'SUB_SC_LATITUDE',
              'Spacecraft Solar Zenith Angle': 'SZA',
              'Spacecraft Local Time': 'LOCAL_TIME',
              'Spacecraft Altitude Aeroid': 'ALTITUDE',
              'Spacecraft Attitude GEO X': 'ATTITUDE_GEO_X',
              'Spacecraft Attitude GEO Y': 'ATTITUDE_GEO_Y',
              'Spacecraft Attitude GEO Z': 'ATTITUDE_GEO_Z',
              'Spacecraft Attitude MSO X': 'ATTITUDE_MSO_X',
              'Spacecraft Attitude MSO Y': 'ATTITUDE_MSO_Y',
              'Spacecraft Attitude MSO Z': 'ATTITUDE_MSO_Z',
              'Mars Season (Ls)': 'MARS_SEASON',
              'Mars-Sun Distance': 'MARS_SUN_DISTANCE',
              'Subsolar Point GEO Longitude': 'SUBSOLAR_POINT_GEO_LONGITUDE',
              'Subsolar Point GEO Latitude': 'SUBSOLAR_POINT_GEO_LATITUDE',
              'Sub-Mars Point on the Sun Longitude': 'SUBMARS_POINT_SOLAR_LONGITUDE',
              'Sub-Mars Point on the Sun Latitude': 'SUBMARS_POINT_SOLAR_LATITUDE',
              'Rot matrix MARS -> MSO Row 1, Col 1': 'T11',
              'Rot matrix MARS -> MSO Row 1, Col 2': 'T12',
              'Rot matrix MARS -> MSO Row 1, Col 3': 'T13',
              'Rot matrix MARS -> MSO Row 2, Col 1': 'T21',
              'Rot matrix MARS -> MSO Row 2, Col 2': 'T22',
              'Rot matrix MARS -> MSO Row 2, Col 3': 'T23',
              'Rot matrix MARS -> MSO Row 3, Col 1': 'T31',
              'Rot matrix MARS -> MSO Row 3, Col 2': 'T32',
              'Rot matrix MARS -> MSO Row 3, Col 3': 'T33',
              'Rot matrix SPCCRFT -> MSO Row 1, Col 1': 'SPACECRAFT_T11',
              'Rot matrix SPCCRFT -> MSO Row 1, Col 2': 'SPACECRAFT_T12',
              'Rot matrix SPCCRFT -> MSO Row 1, Col 3': 'SPACECRAFT_T13',
              'Rot matrix SPCCRFT -> MSO Row 2, Col 1': 'SPACECRAFT_T21',
              'Rot matrix SPCCRFT -> MSO Row 2, Col 2': 'SPACECRAFT_T22',
              'Rot matrix SPCCRFT -> MSO Row 2, Col 3': 'SPACECRAFT_T23',
              'Rot matrix SPCCRFT -> MSO Row 3, Col 1': 'SPACECRAFT_T31',
              'Rot matrix SPCCRFT -> MSO Row 3, Col 2': 'SPACECRAFT_T32',
              'Rot matrix SPCCRFT -> MSO Row 3, Col 3': 'SPACECRAFT_T33'}

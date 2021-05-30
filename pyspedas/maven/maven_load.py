from dateutil.parser import parse
import os

import pytplot
from .download_files_utilities import set_new_data_root_dir, get_root_data_dir, create_dir_if_needed
from .download_files_utilities import get_orbit_files, get_filenames, get_new_files, get_file_from_site
from .download_files_utilities import display_progress
from .file_regex import kp_regex, l2_regex
from .orbit_time import orbit_time
from .maven_kp_to_tplot import maven_kp_to_tplot

def maven_filenames(filenames=None,
                    instruments=None,
                    level='l2',
                    insitu=True,
                    iuvs=False,
                    start_date='2014-01-01',
                    end_date='2020-01-01',
                    update_prefs=False,
                    only_update_prefs=False,
                    local_dir=None):
    '''
    This function queries the MAVEN SDC API, and will return a list of files that match the inputs above.
    '''

    # Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        print("Orbit numbers specified, checking for updated orbit # file from naif.jpl.nasa.gov")
        get_orbit_files()
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day+1, hour=0, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

    # Update the preference directory
    if update_prefs or only_update_prefs:
        set_new_data_root_dir()
        if only_update_prefs:
            return

    # Check for public vs private access
    # Hard code in access as public for now
    public=True
    '''
    public = get_access()
    if not public:
        get_uname_and_password()
    '''
    # If no instruments are specified, default to the KP data set
    if instruments is None:
        instruments = ['kp']
        if insitu:
            level = 'insitu'
        if iuvs:
            level = 'iuvs'

    if level == 'kp':
        instruments = ['kp']
        if insitu:
            level = 'insitu'
        if iuvs:
            level = 'iuvs'

    # Set data download location
    if local_dir is None:
        mvn_root_data_dir = get_root_data_dir()
    else:
        mvn_root_data_dir = local_dir

    # Keep track of files to download
    maven_files = {}
    for instrument in instruments:
        # Build the query to the website
        query_args = []
        query_args.append("instrument=" + instrument)
        query_args.append("level=" + level)
        if filenames is not None:
            query_args.append("file=" + filenames)
        query_args.append("start_date=" + start_date)
        query_args.append("end_date=" + end_date)
        if level == 'iuvs':
            query_args.append("file_extension=tab")

        data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', instrument, level)
        
        query = '&'.join(query_args)
        
        s = get_filenames(query, public)

        if not s:
            print("No files found for {}.".format(instrument))
            maven_files[instrument] = []
            continue

        s = s.split(',')

        maven_files[instrument] = [s, data_dir, public]

    # Grab KP data too, there is a lot of good ancillary info in here
    if instruments != 'kp':
        instrument='kp'
        # Build the query to the website
        query_args = []
        query_args.append("instrument=kp")
        query_args.append("level=insitu")
        query_args.append("start_date=" + start_date)
        query_args.append("end_date=" + end_date)
        data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', 'kp', 'insitu')
        query = '&'.join(query_args)
        s = get_filenames(query, public)
        if not s:
            print("No files found for {}.".format(instrument))
            maven_files[instrument] = []
        else:
            s = s.split(',')
            maven_files[instrument] = [s, data_dir, public]

    return maven_files


def load_data(filenames=None,
              instruments=None,
              level='l2',
              type=None,
              insitu=True,
              iuvs=False,
              start_date='2014-01-01',
              end_date='2020-01-01',
              update_prefs=False,
              only_update_prefs=False,
              local_dir=None,
              list_files=False,
              new_files=True,
              exclude_orbit_file=False,
              download_only=False,
              varformat=None,
              varnames=[],
              prefix='',
              suffix='',
              get_support_data=False,
              auto_yes=False):
    """
    This function downloads MAVEN data loads it into tplot variables, if applicable.
    """

    if not isinstance(instruments, list) and instruments is not None:
        instruments = [instruments]

    if not isinstance(type, list) and type is not None:
        type = [type]

    if not isinstance(filenames, list) and filenames is not None:
        filenames = [filenames]

    # 1. Get a list of MAVEN files queries from the above seach parameters
    maven_files = maven_filenames(filenames, instruments, level, insitu, iuvs, start_date, end_date, update_prefs,
                                  only_update_prefs, local_dir)

    # If we are not asking for KP data, this flag ensures only ancillary data is loaded in from the KP files
    if level != 'kp':
        ancillary_only = True
    else:
        ancillary_only = False

    # Convert to list
    if not isinstance(type, list):
        type = [type]

    # Keep track of what files are downloaded
    files_to_load = []

    # Loop through all instruments, download files locally if needed
    for instr in maven_files.keys():
        bn_files_to_load = []
        if maven_files[instr]:
            s = maven_files[instr][0]
            data_dir = maven_files[instr][1]
            public = maven_files[instr][2]

            # Add to list of files to load
            for f in s:
                # Filter by type
                if type != [None] and instr != 'kp':
                    file_type_match = False
                    desc = l2_regex.match(f).group("description")
                    for t in type:
                        if t in desc:
                            file_type_match = True
                    if not file_type_match:
                        continue

                # Check if the files are KP data
                if instr == 'kp':
                    full_path = create_dir_if_needed(f, data_dir, 'insitu')
                else:
                    full_path = create_dir_if_needed(f, data_dir, level)
                bn_files_to_load.append(f)
                files_to_load.append(os.path.join(full_path, f))

            if list_files:
                for f in s:
                    print(f)
                return

            if new_files:
                if instr == 'kp':
                    s = get_new_files(bn_files_to_load, data_dir, instr, 'insitu')
                else:
                    s = get_new_files(bn_files_to_load, data_dir, instr, level)
            if len(s) == 0:
                continue
            print("Your request will download a total of: "+str(len(s))+" files for instrument "+str(instr))
            print('Would you like to proceed with the download? ')
            valid_response = False
            cancel = False
            if auto_yes:
                valid_response = True
            while not valid_response:
                response = (input('(y/n) >  '))
                if response == 'y' or response == 'Y':
                    valid_response = True
                    cancel = False
                elif response == 'n' or response == 'N':
                    print('Cancelled download. Returning...')
                    valid_response = True
                    cancel = True
                else:
                    print('Invalid input.  Please answer with y or n.')

            if cancel:
                continue

            i = 0
            display_progress(i, len(s))
            for f in s:
                i = i+1
                if instr == 'kp':
                    full_path = create_dir_if_needed(f, data_dir, 'insitu')
                else:
                    full_path = create_dir_if_needed(f, data_dir, level)
                get_file_from_site(f, public, full_path)
                display_progress(i, len(s))



    # 2. Load files into tplot

    if files_to_load:
        # Flatten out downloaded files from list of lists of filenames
        if isinstance(files_to_load[0], list):
            files_to_load = [item for sublist in files_to_load for item in sublist]

        # Only load in files into tplot if we actually downloaded CDF files
        cdf_files = [f for f in files_to_load if '.cdf' in f]
        sts_files = [f for f in files_to_load if '.sts' in f]
        kp_files = [f for f in files_to_load if '.tab' in f]

        loaded_tplot_vars = []
        if not download_only:

            for f in cdf_files:
                # Loop through CDF files
                desc = l2_regex.match(os.path.basename(f)).group("description")
                if desc != '' and suffix == '':
                    created_vars = pytplot.cdf_to_tplot(f, varformat=varformat, varnames=varnames, string_encoding='utf-8',
                                                                 get_support_data=get_support_data, prefix=prefix,
                                                                 suffix=desc, merge=True)
                else:
                    created_vars = pytplot.cdf_to_tplot(f, varformat=varformat, varnames=varnames, string_encoding='utf-8',
                                                                  get_support_data=get_support_data, prefix=prefix,
                                                                  suffix=suffix, merge=True)

                # Specifically for SWIA and SWEA data, make sure the plots have log axes and are spectrograms
                instr = l2_regex.match(os.path.basename(f)).group("instrument")
                if instr in ["swi", "swe"]:
                    pytplot.options(created_vars, 'spec', 1)
                loaded_tplot_vars.append(created_vars)

            for f in sts_files:
                # Loop through STS (Mag) files
                desc = l2_regex.match(os.path.basename(f)).group("description")
                if desc != '' and suffix == '':
                    loaded_tplot_vars.append(pytplot.sts_to_tplot(f, prefix=prefix,
                                                                      suffix=desc, merge=True))
                else:
                    loaded_tplot_vars.append(pytplot.sts_to_tplot(f, prefix=prefix,
                                                                  suffix=suffix, merge=True))

                # Remove the Decimal Day column, not really useful
                for tvar in loaded_tplot_vars:
                    if "DDAY_" in tvar:
                        pytplot.del_data(tvar)
                        del tvar

            # Flatten out the list and only grab the unique tplot variables
            flat_list = list(set([item for sublist in loaded_tplot_vars for item in sublist]))

            # Load in KP data specifically for all of the Ancillary data (position, attitude, Ls, etc)
            if kp_files != []:
                kp_data_loaded = maven_kp_to_tplot(filename=kp_files, ancillary_only=ancillary_only, instruments=instruments)

                # Link all created KP data to the ancillary KP data
                for tvar in kp_data_loaded:
                    pytplot.link(tvar, "mvn_kp::spacecraft::altitude", link_type='alt')
                    pytplot.link(tvar, "mvn_kp::spacecraft::mso_x", link_type='x')
                    pytplot.link(tvar, "mvn_kp::spacecraft::mso_y", link_type='y')
                    pytplot.link(tvar, "mvn_kp::spacecraft::mso_z", link_type='z')
                    pytplot.link(tvar, "mvn_kp::spacecraft::geo_x", link_type='geo_x')
                    pytplot.link(tvar, "mvn_kp::spacecraft::geo_y", link_type='geo_y')
                    pytplot.link(tvar, "mvn_kp::spacecraft::geo_z", link_type='geo_z')
                    pytplot.link(tvar, "mvn_kp::spacecraft::sub_sc_longitude", link_type='lon')
                    pytplot.link(tvar, "mvn_kp::spacecraft::sub_sc_latitude", link_type='lat')
                
            # Link all created tplot variables to the corresponding KP data
            for tvar in flat_list:
                pytplot.link(tvar, "mvn_kp::spacecraft::altitude", link_type='alt')
                pytplot.link(tvar, "mvn_kp::spacecraft::mso_x", link_type='x')
                pytplot.link(tvar, "mvn_kp::spacecraft::mso_y", link_type='y')
                pytplot.link(tvar, "mvn_kp::spacecraft::mso_z", link_type='z')
                pytplot.link(tvar, "mvn_kp::spacecraft::geo_x", link_type='geo_x')
                pytplot.link(tvar, "mvn_kp::spacecraft::geo_y", link_type='geo_y')
                pytplot.link(tvar, "mvn_kp::spacecraft::geo_z", link_type='geo_z')
                pytplot.link(tvar, "mvn_kp::spacecraft::sub_sc_longitude", link_type='lon')
                pytplot.link(tvar, "mvn_kp::spacecraft::sub_sc_latitude", link_type='lat')


            # Return list of unique KP data
            return flat_list

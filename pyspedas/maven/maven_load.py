#!/usr/bin/python
# -*- coding: utf-8 -*-

from dateutil.parser import parse
import os

import pytplot

from .download_files_utilities import *
from .orbit_time import orbit_time


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
    """
    This function identifies which MAVEN data to download.
    """

    # Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day+1, hour=0, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
    if update_prefs or only_update_prefs:
        set_new_data_root_dir()
        if only_update_prefs:
            return
    
    public = get_access()
    if not public:
        get_uname_and_password()

    if filenames is None:
        if insitu and iuvs:
            print("Can't request both INSITU and IUVS in one query.")
            return
        if not insitu and not iuvs:
            print("If not specifying filename(s) to download, Must specify either insitu=True or iuvs=True.")
            return
        
    if instruments is None:
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

    return maven_files


def load_data(filenames=None,
              instruments=None,
              level='l2',
              insitu=True,
              iuvs=False,
              start_date='2014-01-01',
              end_date='2020-01-01',
              update_prefs=False,
              only_update_prefs=False,
              local_dir=None,
              list_files=False,
              new_files=False,
              exclude_orbit_file=False,
              download_only=False,
              varformat=None,
              prefix='',
              suffix='',
              get_support_data=False):
    """
    This function downloads MAVEN data loads it into tplot variables, if applicable.
    """

    # 1. Download files

    maven_files = maven_filenames(filenames, instruments, level, insitu, iuvs, start_date, end_date, update_prefs,
                                  only_update_prefs, local_dir)

    # Keep track of what files are downloaded
    downloaded_files = []

    for instr in maven_files.keys():
        if maven_files[instr]:
            s = maven_files[instr][0]
            data_dir = maven_files[instr][1]
            public = maven_files[instr][2]
            if list_files:
                for f in s:
                    print(f)
                return

            if new_files:
                s = get_new_files(s, data_dir, instr, level)

            print("Your request will download a total of: "+str(len(s))+" files for instrument "+str(instr))
            print('Would you like to proceed with the download? ')
            valid_response = False
            cancel = False
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

            if not exclude_orbit_file:
                print("Before downloading data files, checking for updated orbit # file from naif.jpl.nasa.gov")
                print("")
                get_orbit_files()

            i = 0
            display_progress(i, len(s))
            for f in s:
                i = i+1
                full_path = create_dir_if_needed(f, data_dir, level)
                get_file_from_site(f, public, full_path)
                display_progress(i, len(s))

                downloaded_files.append(os.path.join(full_path, f))

    # 2. Load files into tplot

    if downloaded_files:
        # Flatten out downloaded files from list of lists of filenames
        if isinstance(downloaded_files[0], list):
            downloaded_files = [item for sublist in downloaded_files for item in sublist]

        # Only load in files into tplot if we actually downloaded CDF files
        cdf_files = [f for f in downloaded_files if '.cdf' in f]

        if not download_only:
            # Create tplot variables
            downloaded_tplot_vars = pytplot.cdf_to_tplot(cdf_files, varformat=varformat,
                                                         get_support_data=get_support_data, prefix=prefix,
                                                         suffix=suffix, merge=True)
            return downloaded_tplot_vars

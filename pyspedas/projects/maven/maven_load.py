import logging
from dateutil.parser import parse
import os
import time

import pytplot
from .download_files_utilities import (
    set_new_data_root_dir,
    get_root_data_dir,
    create_dir_if_needed,
    get_orbit_files,
    get_filenames,
    get_new_files,
    get_file_from_site,
    display_progress,
)
from .file_regex import maven_kp_l2_regex  # kp_regex, l2_regex
from .orbit_time import orbit_time
from .maven_kp_to_tplot import maven_kp_to_tplot

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def maven_filenames(
    filenames=None,
    instruments=None,
    level="l2",
    insitu=True,
    iuvs=False,
    start_date="2014-01-01",
    end_date="2014-01-02",
    update_prefs=False,
    only_update_prefs=False,
    local_dir=None,
    public=True,
):
    """
    This function queries the MAVEN SDC API, and will return a list of files that match the given parameters.

    Parameters
    ----------
    filenames : list of str, optional
        Predefined list of filenames. If provided, other parameters are ignored. Defaults to None.
    instruments : list of str, optional
        List of instrument names. Defaults to None.
    level : str, optional
        Data level. Defaults to 'l2'.
    insitu : bool, optional
        If True, insitu files will be used. Defaults to True.
    iuvs : bool, optional
        If True, iuvs files will be used. Defaults to False.
        When True, file_extension=tab is added to the query.
    start_date : str/int, optional
        Start date in 'YYYY-MM-DD' format, or the orbit number. Defaults to '2014-01-01'.
    end_date : str/int, optional
        End date in 'YYYY-MM-DD' format, or the orbit number. Defaults to '2014-01-02'.
    update_prefs : bool, optional
        If True, updates preferences. Defaults to False.
    only_update_prefs : bool, optional
        If True, only updates preferences and does not return filenames. Defaults to False.
    local_dir : str, optional
        Local directory to use. Defaults to None.
    public: bool, optional
        If False, try loading data from the non-public service


    Returns
    -------
    list of str
        List of MAVEN filenames.
    """

    # Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        logging.info(
            "Orbit numbers specified, checking for updated orbit # file from naif.jpl.nasa.gov"
        )
        get_orbit_files()
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day + 1, hour=0, minute=0, second=0)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

    # Update the preference directory
    if update_prefs or only_update_prefs:
        set_new_data_root_dir()
        if only_update_prefs:
            return

    # Check for public vs private access
    # Hard code in access as public for now
    # public = True
    """
    public = get_access()
    if not public:
        get_uname_and_password()
    """
    # If no instruments are specified, default to the KP data set
    if instruments is None:
        instruments = ["kp"]
        if insitu:
            level = "insitu"
        if iuvs:
            level = "iuvs"

    if level == "kp":
        instruments = ["kp"]
        if insitu:
            level = "insitu"
        if iuvs:
            level = "iuvs"

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
        if level == "iuvs":
            query_args.append("file_extension=tab")

        sep = "/" if is_fsspec_uri(mvn_root_data_dir) else os.path.sep
        data_dir = sep.join([
            mvn_root_data_dir, "maven", "data", "sci", instrument, level
        ])

        query = "&".join(query_args)

        logging.info("Querying for filenames: %s", query)
        s = get_filenames(query, public)

        if not s:
            logging.error("No files found for {}.".format(instrument))
            if instrument not in maven_files:
                maven_files[instrument] = []
            continue

        s = s.split(",")
        logging.info("Returned %d files",len(s))

        if instrument not in maven_files:
            maven_files[instrument] = [s, data_dir, public]
        else:
            maven_files[instrument].extend([s, data_dir, public])

    # Grab KP data too, there is a lot of good ancillary info in here
    if instruments != "kp":
        instrument = "kp"
        # Build the query to the website
        query_args = []
        query_args.append("instrument=kp")
        query_args.append("level=insitu")
        query_args.append("start_date=" + start_date)
        query_args.append("end_date=" + end_date)
        sep = "/" if is_fsspec_uri(mvn_root_data_dir) else os.path.sep
        data_dir = sep.join([
            mvn_root_data_dir, "maven", "data", "sci", "kp", "insitu"
        ])
        query = "&".join(query_args)
        s = get_filenames(query, public)
        if not s:
            logging.error("No files found for {}.".format(instrument))
            if instrument not in maven_files:
                maven_files[instrument] = []
        else:
            s = s.split(",")
            if instrument not in maven_files:
                maven_files[instrument] = [s, data_dir, public]
            else:
                maven_files[instrument].extend([s, data_dir, public])

    return maven_files


def maven_file_groups(files):
    """
    This function groups MAVEN files by their description.

    Parameters
    ----------
    files : list of str
        List of MAVEN filenames.

    Returns
    -------
    dict
        Dictionary of grouped files.
    """

    # Group files by their description
    result = {}
    if len(files) == 0:
        return result
    files.sort()

    kp_regex, l2_regex = maven_kp_l2_regex()
    for f in files:
        if is_fsspec_uri(f):
            protocol, path = f.split("://")
            fs = fsspec.filesystem(protocol)

            basename = f.rstrip("/").split("/")[-1]
        else:
            basename = os.path.basename(f)
        desc = l2_regex.match(basename).group("description")
        if desc not in result:
            result[desc] = []
        result[desc].append(f)

    for k in result.keys():
        result[k].sort()

    return result


def load_data(
    filenames=None,
    instruments=None,
    level="l2",
    type=None,
    insitu=True,
    iuvs=False,
    start_date="2014-01-01",
    end_date="2014-01-02",
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
    get_metadata=False,
    auto_yes=False,
    public=True,
):
    """
    This function downloads MAVEN data loads it into tplot variables, if applicable.

    Parameters
    ----------
    filenames : list of str, optional
        Predefined list of filenames. If provided, other parameters are ignored. Defaults to None.
    instruments : list of str, optional
        List of instrument names. Defaults to None.
        Accepted values are any combination of: sta, swi, swe, lpw, euv, ngi, iuv, mag, sep, rse
    level : str, optional
        Data level. Defaults to 'l2'. Currently unused, only l2 data can be loaded.
    type : str, optional
        Type of data to load. Defaults to None.

        The observation/file type of the instruments to load.  If None, all file types are loaded.
        Otherwise, a file will only be loaded into tplot if its descriptor matches one of the strings in this field.

        Accepted values are:
        =================== ====================================
        Instrument           Level 2 Observation Type/File Type
        =================== ====================================
        EUV                 bands
        LPW                 lpiv, lpnt, mrgscpot, we12, we12burstlf, we12bursthf, we12burstmf, wn, wspecact, wspecpas
        STATIC              2a, c0, c2, c4, c6, c8, ca, cc, cd, ce, cf, d0, d1, d4, d6, d7, d8, d9, da, db
        SEP                 s1-raw-svy-full, s1-cal-svy-full, s2-raw-svy-full, s2-cal-svy-full
        SWEA                arc3d, arcpad, svy3d, svypad, svyspec
        SWIA                coarsearc3d, coarsesvy3d, finearc3d, finesvy3d, onboardsvymom, onboardsvyspec
        MAG                 ss, pc, pl, ss1s, pc1s, pl1s
        =================== =====================================
    insitu : bool, optional
        If True, only insitu files will be used. Defaults to True.
    iuvs : bool, optional
        If True, iuvs files will be used. Defaults to False.
        When True, file_extension=tab is added to the query.
    start_date : str/int, optional
        Start date in 'YYYY-MM-DD' format, or the orbit number. Defaults to '2014-01-01'.
    end_date : str/int, optional
        End date in 'YYYY-MM-DD' format, or the orbit number. Defaults to '2014-01-02'.
    update_prefs : bool, optional
        If True, updates preferences. Defaults to False.
    only_update_prefs : bool, optional
        If True, only updates preferences and does not return data. Defaults to False.
    local_dir : str, optional
        Local directory to use. Defaults to None.
    list_files : bool, optional
        If True, lists files without loading data. Defaults to False.
    new_files : bool, optional
        If True, get new files. Defaults to True.
    exclude_orbit_file : bool, optional
        If True, will not download the latest orbit table. Defaults to False.
        Currently unused.
    download_only : bool, optional
        If True, only downloads files without loading data. Defaults to False.
    varformat : str, optional
        Variable format. Defaults to None.
        The file variable formats to load into tplot. Wildcard character
        "*" is accepted.  By default, all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load. Defaults to [].
    prefix : str, optional
        Prefix to append to variable names. Defaults to ''.
    suffix : str, optional
        Suffix to append to variable names.
        Defaults to ''.
        By default the part of the filename (plus the suffix) is appended to the variable name.
        If suffix='empty', no suffix is appended to the variable name (no part of the filename and no suffix).
    get_support_data : bool, optional
        If True, retrieves support data. Defaults to False.
    get_metadata : bool, optional
        If True, retrieves metadata. Defaults to False.
    auto_yes : bool, optional
        If True, automatically answers 'yes' to prompts. Defaults to False.
    public: bool, optional
    If false, try using the non-public interface


    Returns
    -------
    dict
        Dictionary of loaded data variables.
    """

    if not isinstance(instruments, list) and instruments is not None:
        instruments = [instruments]

    if not isinstance(type, list) and type is not None:
        type = [type]

    if not isinstance(filenames, list) and filenames is not None:
        filenames = [filenames]

    kp_regex, l2_regex = maven_kp_l2_regex()

    # 1. Get a list of MAVEN files queries from the above seach parameters
    maven_files = maven_filenames(
        filenames,
        instruments,
        level,
        insitu,
        iuvs,
        start_date,
        end_date,
        update_prefs,
        only_update_prefs,
        local_dir,
        public=public,
    )

    # If we are not asking for KP data, this flag ensures only ancillary data is loaded in from the KP files
    if level != "kp":
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
        # There might be more than one set of files to load for this instrument (e.g. kp with iuvs)
        maven_file_list = maven_files[instr]
        while len(maven_file_list) > 0:
            s = maven_file_list[0]
            data_dir = maven_file_list[1]
            public = maven_file_list[2]
            # Strip off these three entries, in case there's more to process next iteration
            maven_file_list = maven_file_list[3:]

            # Add to list of files to load
            for f in s:
                # Filter by type
                if type != [None] and instr != "kp":
                    file_type_match = False
                    desc = l2_regex.match(f).group("description")
                    for t in type:
                        # kluge for STATIC, jmm, 2024-07-24, otherwise type='d1' results in ca,d0,d1,d4 loading
                        if instr == "sta":
                            if t + "-" in desc:
                                file_type_match = True
                        else:
                            if t in desc:
                                file_type_match = True
                    if not file_type_match:
                        continue

                # Check if the files are KP data
                try:
                    if instr == "kp":
                        full_path = create_dir_if_needed(f, data_dir, "insitu")
                    else:
                        full_path = create_dir_if_needed(f, data_dir, level)
                    bn_files_to_load.append(f)
                    sep = "/" if is_fsspec_uri(full_path) else os.path.sep
                    files_to_load.append(sep.join([full_path, f]))
                except Exception as e:
                    # todo: better handling of rse .tab files
                    # rse files are .tab files (TAB delimited text files) that currently cannot be loaded into tplot
                    # for now, we need to skip these files
                    logging.error("Cannot handle file: " + f)
                    continue

            if list_files:
                for f in s:
                    logging.info(f)
                return

            if new_files:
                if instr == "kp":
                    s = get_new_files(bn_files_to_load, data_dir, instr, "insitu")
                else:
                    s = get_new_files(bn_files_to_load, data_dir, instr, level)
            if len(s) == 0:
                continue
            logging.info(
                "Your request will download a total of: "
                + str(len(s))
                + " files for instrument "
                + str(instr)
            )
            logging.info("Files: ")
            logging.info(s)
            logging.info("Would you like to proceed with the download? ")
            valid_response = False
            cancel = False
            if auto_yes:
                valid_response = True
                logging.info("- Auto yes")
            while not valid_response:
                response = input("(y/n) >  ")
                if response == "y" or response == "Y":
                    valid_response = True
                    cancel = False
                elif response == "n" or response == "N":
                    logging.error("Cancelled download. Returning...")
                    valid_response = True
                    cancel = True
                else:
                    logging.error("Invalid input.  Please answer with y or n.")

            if cancel:
                continue

            i = 0
            display_progress(i, len(s))
            for f in s:
                logging.info("File:" + str(f))
                i = i + 1
                if instr == "kp":
                    full_path = create_dir_if_needed(f, data_dir, "insitu")
                else:
                    full_path = create_dir_if_needed(f, data_dir, level)
                get_file_from_site(f, public, full_path)
                time.sleep(10.0)
                display_progress(i, len(s))

    # 2. Load files into tplot

    if files_to_load:
        # Flatten out downloaded files from list of lists of filenames
        if isinstance(files_to_load[0], list):
            files_to_load = [item for sublist in files_to_load for item in sublist]

        # Only load in files into tplot if we actually downloaded CDF files
        cdf_files = [f for f in files_to_load if ".cdf" in f]
        sts_files = [f for f in files_to_load if ".sts" in f]
        kp_files = [f for f in files_to_load if ".tab" in f]

        loaded_tplot_vars = []
        if not download_only:

            # Load in CDF files
            if len(cdf_files) > 0:
                cdf_dict = maven_file_groups(cdf_files)
                for desc in cdf_dict.keys():
                    if suffix == "empty":
                        # In this case, no suffix is appended to the variable name
                        suf = ""
                    else:
                        # The description (part of the filename) is appended to the variable name
                        suf = desc + suffix
                    created_vars = pytplot.cdf_to_tplot(
                        cdf_dict[desc],
                        varformat=varformat,
                        varnames=varnames,
                        string_encoding="utf-8",
                        get_support_data=get_support_data,
                        prefix=prefix,
                        suffix=suf,
                        get_metadata=get_metadata,
                    )
                    # Specifically for SWIA and SWEA data, make sure the plots have log axes and are spectrograms
                    if is_fsspec_uri(cdf_dict[desc][0]):
                        protocol, path = cdf_dict[desc][0].split("://")
                        fs = fsspec.filesystem(protocol)

                        basename = cdf_dict[desc][0].rstrip("/").split("/")[-1]
                    else:
                        basename = os.path.basename(cdf_dict[desc][0])
                    instr = l2_regex.match(basename).group(
                        "instrument"
                    )
                    if instr in ["swi", "swe"]:
                        pytplot.options(created_vars, "spec", 1)
                    loaded_tplot_vars.append(created_vars)

            # Load in STS files
            if len(sts_files) > 0:
                sts_dict = maven_file_groups(sts_files)
                for desc in sts_dict.keys():
                    if suffix == "empty":
                        # In this case, no suffix is appended to the variable name
                        suf = ""
                    else:
                        # The description (part of the filename) is appended to the variable name
                        suf = desc + suffix
                    try:
                        created_vars = pytplot.sts_to_tplot(
                            sts_dict[desc],
                            prefix=prefix,
                            suffix=suf,
                        )
                    except FileNotFoundError:
                        logging.error("PyTplot Error: STS importer is not URI capable.")
                        logging.error("\tSkipping file as PyTplot cannot use this type of filesystem.")
                        continue
                    loaded_tplot_vars.append(created_vars)

                # Remove the Decimal Day column, not really useful
                for tvar in loaded_tplot_vars:
                    if "DDAY_" in tvar:
                        pytplot.del_data(tvar)
                        del tvar

            # Flatten out the list and only grab the unique tplot variables
            flat_list = list(
                set([item for sublist in loaded_tplot_vars for item in sublist])
            )

            # Load in KP data specifically for all of the Ancillary data (position, attitude, Ls, etc)
            if kp_files != []:
                kp_data_loaded = maven_kp_to_tplot(
                    filename=kp_files,
                    ancillary_only=ancillary_only,
                    instruments=instruments,
                )

                logging.info("Kp data loaded:")
                logging.info(kp_data_loaded)
                # Link all created KP data to the ancillary KP data
                for tvar in kp_data_loaded:
                    pytplot.link(tvar, "mvn_kp::spacecraft::altitude", link_type="alt")
                    pytplot.link(tvar, "mvn_kp::spacecraft::mso_x", link_type="x")
                    pytplot.link(tvar, "mvn_kp::spacecraft::mso_y", link_type="y")
                    pytplot.link(tvar, "mvn_kp::spacecraft::mso_z", link_type="z")
                    pytplot.link(tvar, "mvn_kp::spacecraft::geo_x", link_type="geo_x")
                    pytplot.link(tvar, "mvn_kp::spacecraft::geo_y", link_type="geo_y")
                    pytplot.link(tvar, "mvn_kp::spacecraft::geo_z", link_type="geo_z")
                    pytplot.link(
                        tvar, "mvn_kp::spacecraft::sub_sc_longitude", link_type="lon"
                    )
                    pytplot.link(
                        tvar, "mvn_kp::spacecraft::sub_sc_latitude", link_type="lat"
                    )

            # Link all created tplot variables to the corresponding KP data
            for tvar in flat_list:
                pytplot.link(tvar, "mvn_kp::spacecraft::altitude", link_type="alt")
                pytplot.link(tvar, "mvn_kp::spacecraft::mso_x", link_type="x")
                pytplot.link(tvar, "mvn_kp::spacecraft::mso_y", link_type="y")
                pytplot.link(tvar, "mvn_kp::spacecraft::mso_z", link_type="z")
                pytplot.link(tvar, "mvn_kp::spacecraft::geo_x", link_type="geo_x")
                pytplot.link(tvar, "mvn_kp::spacecraft::geo_y", link_type="geo_y")
                pytplot.link(tvar, "mvn_kp::spacecraft::geo_z", link_type="geo_z")
                pytplot.link(
                    tvar, "mvn_kp::spacecraft::sub_sc_longitude", link_type="lon"
                )
                pytplot.link(
                    tvar, "mvn_kp::spacecraft::sub_sc_latitude", link_type="lat"
                )

            logging.info("Maven data list:")
            logging.info(flat_list)

            # Return list of unique KP data
            return flat_list

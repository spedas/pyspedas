import logging
from .file_regex import maven_kp_l2_regex
from .config import CONFIG

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def get_filenames(query, public):
    """
    Retrieves file names based on the given query.

    Args:
        query (str): The query string used to filter the file names.
        public (bool): Flag indicating whether to use the public URL or private URL.

    Returns:
        str: The file names retrieved as a string.

    Raises:
        urllib.error.URLError: If there is an error in accessing the URL.
    """

    import urllib

    public_url = (
        "https://lasp.colorado.edu/maven/sdc/public/files/api/v1/search/science/fn_metadata/file_names"
        + "?"
        + query
    )
    private_url = (
        "https://lasp.colorado.edu/maven/sdc/service/files/api/v1/search/science/fn_metadata/file_names"
        + "?"
        + query
    )
    if not public:
        uname = CONFIG["maven_username"]
        pword = CONFIG["maven_password"]
        username = uname
        password = pword
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, private_url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        logging.info("get_filenames() making request to private URL: %s", private_url)
        page = urllib.request.urlopen(private_url)
        logging.info("get_filenames() finished request to private URL: %s", private_url)

    else:
        logging.info("get_filenames() making request to public URL: %s", public_url)
        page = urllib.request.urlopen(public_url)
        logging.info("get_filenames() finished request to public URL: %s", public_url)

    return page.read().decode("utf-8")


def get_file_from_site(filename, public, data_dir):
    """
    Downloads a file from a website and saves it to the specified directory.

    Args:
        filename (str): The name of the file to download.
        public (bool): Indicates whether the file is public or private.
        data_dir (str): The directory where the file should be saved.

    Returns:
        None
    """
    import os
    import urllib

    public_url = (
        "https://lasp.colorado.edu/maven/sdc/public/files/api/v1/search/science/fn_metadata/download"
        + "?file="
        + filename
    )
    private_url = (
        "https://lasp.colorado.edu/maven/sdc/service/files/api/v1/search/science/fn_metadata/download"
        + "?file="
        + filename
    )

    if not public:
        uname = CONFIG["maven_username"]
        pword = CONFIG["maven_password"]
        username = uname
        password = pword
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, private_url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        logging.debug("get_file_from_site making request to private url: %s", private_url)
        page = urllib.request.urlopen(private_url)
        logging.debug("get_file_from_site finished request to private url: %s", private_url)
    else:
        logging.debug("get_file_from_site making request to public url: %s", public_url)
        page = urllib.request.urlopen(public_url)
        logging.debug("get_file_from_site finished request to public url: %s", public_url)

    # Cloud Awareness: write page contents to URI
    if is_fsspec_uri(data_dir):
        protocol, path = data_dir.split("://")
        fs = fsspec.filesystem(protocol)

        fo = fs.open("/".join([data_dir, filename]), "wb")
    else:
        fo = open(os.path.join(data_dir, filename), "wb")

    with fo as code:
        code.write(page.read())

    return


def get_orbit_files():
    """
    Downloads MAVEN orbit files from the NASA NAIF website and saves them locally.

    Returns:
        None
    """
    import os
    import urllib
    import re

    orbit_files_url = "http://naif.jpl.nasa.gov/pub/naif/MAVEN/kernels/spk/"
    pattern = r">maven_orb_rec(\.orb|.{17}\.orb)<"
    logging.info("get_orbit_files() making request to URL %s", orbit_files_url)
    page = urllib.request.urlopen(orbit_files_url)
    logging.info("get_orbit_files() finished request to URL %s", orbit_files_url)
    page_string = str(page.read())
    toolkit_path = CONFIG["local_data_dir"]

    # Cloud Awareness: operate on fsspec filesystem instead of os
    if is_fsspec_uri(toolkit_path):
        protocol, path = toolkit_path.split("://")
        fs = fsspec.filesystem(protocol)

        orbit_files_path = "/".join([toolkit_path, "orbitfiles"])
        fs.mkdirs(orbit_files_path)
    else:
        orbit_files_path = os.path.join(toolkit_path, "orbitfiles")

        if not os.path.exists(toolkit_path):
            os.mkdir(toolkit_path)

        if not os.path.exists(orbit_files_path):
            os.mkdir(orbit_files_path)

    for matching_pattern in re.findall(pattern, page_string):
        filename = "maven_orb_rec" + matching_pattern
        logging.info("get_orbit_files() making request to URL %s", orbit_files_url + filename)
        o_file = urllib.request.urlopen(orbit_files_url + filename)
        logging.info("get_orbit_files() finished request to URL %s", orbit_files_url + filename)

        if is_fsspec_uri(toolkit_path):
            ifn = "/".join([orbit_files_path, filename])
            logging.info("reading fsspec file %s",ifn)
            fo = fs.open(ifn, "wb")
        else:
            ifn = os.path.join(orbit_files_path, filename)
            logging.info("reading plain file %s",ifn)
            fo = open(ifn, "wb")
        with fo as code:
            content=o_file.read()
            logging.info("writing %d bytes into file %s",len(content), ifn)
            code.write(content)

    merge_orbit_files()

    return


def merge_orbit_files():
    """
    Merge MAVEN orbit files into a single file.

    This function searches for MAVEN orbit files in the 'orbitfiles' directory and merges them into a single file
    named 'merged_maven_orbits.orb' in the same directory. The files are sorted based on their dates before merging.

    Returns:
        None
    """
    import os
    import re

    toolkit_path = CONFIG["local_data_dir"]

    # Cloud Awareness: traverse fsspec-like filesystem instead of os
    if is_fsspec_uri(toolkit_path):
        protocol, path = toolkit_path.split("://")
        fs = fsspec.filesystem(protocol)

        orbit_files_path = "/".join([toolkit_path, "orbitfiles"])
        fl = fs.listdir(orbit_files_path, detail=False)
        fl = [f.rstrip("/").split("/")[-1] for f in fl]
        output_filename = "/".join([orbit_files_path, "merged_maven_orbits.orb"])
        fo = fs.open(output_filename, "w")
    else:
        orbit_files_path = os.path.join(toolkit_path, "orbitfiles")

        fl = os.listdir(orbit_files_path)
        output_filename = os.path.join(orbit_files_path,"merged_maven_orbits.orb")
        fo = open(output_filename, "w")

    pattern = "maven_orb_rec(_|)(|.{6})(|_.{9}).orb"
    orb_dates = []
    orb_files = []
    for f in fl:
        x = re.match(pattern, f)
        if x is not None:
            orb_file = os.path.join(orbit_files_path, f) if not is_fsspec_uri(toolkit_path) else "/".join([orbit_files_path, f])
            orb_files.append(orb_file)
            if x.group(2) != "":
                orb_dates.append(x.group(2))
            else:
                orb_dates.append("999999")

    sorted_files = [x for (y, x) in sorted(zip(orb_dates, orb_files))]

    with fo as code:
        skip_2_lines = False
        for o_file in sorted_files:
            logging.info("merge_orbit_files processing file %s", o_file)
            if is_fsspec_uri(toolkit_path):
                # assumes fsspec filesystem triggered above
                fo_file = fs.open(o_file)
            else:
                fo_file = open(o_file)
            with fo_file as f:
                if skip_2_lines:
                    f.readline()
                    f.readline()
                skip_2_lines = True
                content=f.read()
                logging.info("writing %d bytes to output file %s",len(content),output_filename)
                if type(content) is bytes:
                    code.write(str(content))
                else:
                    code.write(content)

    return


def get_access():
    """
    Check the access status from the access.txt file.

    Returns:
        bool: True if access is granted, False otherwise.
    """
    import os

    toolkit_path = os.path.dirname(__file__)
    with open(os.path.join(toolkit_path, "access.txt"), "r") as f:
        f.readline()
        s = f.readline().rstrip()
        s = s.split(" ")
        if s[1] == "1":
            return False
        else:
            return True


def get_root_data_dir():
    """
    Returns the preferred data download location for the pyspedas project.

    Raises:
        NameError: If "local_data_dir" is not found in config.py.

    Returns:
        str: The preferred data download location.
    """
    from .config import CONFIG

    # Get preferred data download location for pyspedas project
    if "local_data_dir" in CONFIG:
        return CONFIG["local_data_dir"]
    else:
        raise NameError("local_data_dir is not found in config.py")


def create_pref_file(toolkit_path, download_path):
    """
    Create a preferences file for the Maven toolkit.

    Args:
        toolkit_path (str): The path to the Maven toolkit.
        download_path (str): The path to the data download directory.

    Returns:
        None
    """
    import os

    # Put data download path into preferences file
    with open(os.path.join(toolkit_path, "mvn_toolkit_prefs.txt"), "w") as f:
        f.write("'; IDL Toolkit Data Preferences File'\n")
        f.write("mvn_root_data_dir: " + download_path)

    return


def set_new_data_root_dir():
    """
    Sets the new data root directory for the pyspedas project.

    This function prompts the user to enter a directory preference and validates
    if the specified path exists. If the path does not exist, the user is prompted
    to enter a new path until a valid path is provided. The function then sets the
    location of the mvn_toolkit_prefs file to the specified download path.

    Parameters:
        None

    Returns:
        None
    """
    import os

    # Get new preferred data download location for pyspedas project
    valid_path = input("Enter directory preference: ")

    # Cloud Awareness: had to rework for ensuring URI exists
    exists = False
    while not exists:
        if is_fsspec_uri(valid_path):
            if not "://" in valid_path:
                valid_path = input("Specified path does not exist. Enter new path: ")
            else:
                protocol, path = valid_path.split("://")
                fs = fsspec.filesystem(protocol)

                if fs.exists(valid_path):
                    exists = True
                else:
                    valid_path = input("Specified path does not exist. Enter new path: ")
        else:
            if os.path.exists(valid_path):
                exists = True
            else:
                valid_path = input("Specified path does not exist. Enter new path: ")
    download_path = valid_path
    logging.warning("Location of the mvn_toolkit_prefs file set to " + download_path)

    # Also edit the mvn_toolkit_prefs file to reflect the new data download location
    toolkit_path = CONFIG["local_data_dir"]
    create_pref_file(toolkit_path, download_path)


def get_new_files(files_on_site, data_dir, instrument, level):
    """
    Get the new files that are present on the site but not on the local hard drive.

    Parameters:
        files_on_site (list): List of files available on the site.
        data_dir (str): Path to the local data directory.
        instrument (str): Instrument name.
        level (str): Data level.

    Returns:
        list: List of new files that are present on the site but not on the local hard drive.
    """
    import os
    import re

    fos = files_on_site
    files_on_hd = []

    # Cloud Awareness: traverse fsspec filesystem
    if is_fsspec_uri(data_dir):
        protocol, path = data_dir.split("://")
        fs = fsspec.filesystem(protocol)

        walk = fs.walk(data_dir)
    else:
        walk = os.walk(data_dir)

    for dir, _, files in walk:
        for f in files:
            if re.match("mvn_" + instrument + "_" + level + "_*", f):
                files_on_hd.append(f)

    x = set(files_on_hd).intersection(files_on_site)
    for matched_file in x:
        fos.remove(matched_file)

    return fos


def create_dir_if_needed(f, data_dir, level):
    """
    Create a directory if it does not already exist based on the year and month extracted from the file name.

    Parameters:
        f (str): The file name.
        data_dir (str): The base directory where the new directory will be created.
        level (str): The level of the file ("insitu" or "sci").

    Returns:
        str: The full path of the created directory.
    """
    import os

    if level == "insitu":
        year, month, _ = get_year_month_day_from_kp_file(f)
    else:
        year, month, _ = get_year_month_day_from_sci_file(f)

    # Cloud Awareness: operate upon fsspec-like filesystem
    if is_fsspec_uri(data_dir):
        protocol, path = data_dir.split("://")
        fs = fsspec.filesystem(protocol)

        full_path = "/".join([data_dir, year, month])
        fs.mkdirs(full_path)
        return full_path

    if not os.path.exists(os.path.join(data_dir, year, month)):
        os.makedirs(os.path.join(data_dir, year, month))

    full_path = os.path.join(data_dir, year, month)

    return full_path


def get_year_month_day_from_kp_file(f):
    """
    Extracts the year, month, and day from a given file name.

    Args:
        f (str): The file name.

    Returns:
        tuple: A tuple containing the year, month, and day extracted from the file name.
    """
    date_string = f.split("_")[3]
    year = date_string[0:4]
    month = date_string[4:6]
    day = date_string[6:8]

    return year, month, day


def get_year_month_day_from_sci_file(f):
    """
    Extracts the year, month, and day from a given scientific file name.

    Parameters:
        f (str): The scientific file name.

    Returns:
        tuple: A tuple containing the year, month, and day extracted from the file name.
    """
    kp_regex, l2_regex = maven_kp_l2_regex()
    m = l2_regex.match(f)
    if m is None:
        logging.error('l2_regex match failed for filename %s', f)
    year = m.group("year")
    month = m.group("month")
    day = m.group("day")

    return year, month, day


def display_progress(x, y):
    """
    Display the progress of a task as a visual bar.

    Parameters:
    x (int): The current progress value.
    y (int): The total value representing the completion of the task.

    Returns:
    None
    """
    num_stars = int(round(float(x) / y * 70))
    logging.warning(
        "||"
        + "*" * num_stars
        + "-" * (70 - num_stars)
        + "||"
        + " ( "
        + str(round(100 * float(x) / y))
        + "% )"
    )
    return


def get_uname_and_password():
    """
    Prompts the user to enter their username and password to access the team website.

    Returns:
        None
    """
    import getpass

    uname = input("Enter user name to access the team website: ")
    pword = getpass.getpass("Enter your password: ")

    CONFIG["maven_username"] = uname
    CONFIG["maven_password"] = pword
    return

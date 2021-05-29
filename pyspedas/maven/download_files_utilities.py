
"""
File:
    download_file_utilities.py

Description:
    Functions used by maven_load.
"""

uname = ''
pword = ''
from .file_regex import kp_regex, l2_regex

def get_filenames(query, public):
    import urllib

    public_url = 'https://lasp.colorado.edu/maven/sdc/public/files/api/v1/search/science/fn_metadata/file_names' + \
                 '?' + query
    private_url = 'https://lasp.colorado.edu/maven/sdc/service/files/api/v1/search/science/fn_metadata/file_names' + \
                  '?' + query
    if not public:
        username = uname
        password = pword
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, private_url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        page = urllib.request.urlopen(private_url)
    else:
        page = urllib.request.urlopen(public_url)

    return page.read().decode("utf-8")


def get_file_from_site(filename, public, data_dir):
    import os
    import urllib

    public_url = 'https://lasp.colorado.edu/maven/sdc/public/files/api/v1/search/science/fn_metadata/download' + '?file=' + filename
    private_url = 'https://lasp.colorado.edu/maven/sdc/service/files/api/v1/search/science/fn_metadata/download' + '?file=' + filename

    if not public:
        username = uname
        password = pword
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, private_url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        page = urllib.request.urlopen(private_url)
    else:
        page = urllib.request.urlopen(public_url)

    with open(os.path.join(data_dir, filename), "wb") as code:
        code.write(page.read())

    return


def get_orbit_files():
    import os
    import urllib
    import re

    orbit_files_url = "http://naif.jpl.nasa.gov/pub/naif/MAVEN/kernels/spk/"
    pattern = 'maven_orb_rec(\.orb|.{17}\.orb)'
    page = urllib.request.urlopen(orbit_files_url)
    page_string = str(page.read())
    full_path = os.path.realpath(__file__)
    toolkit_path = os.path.dirname(full_path)

    orbit_files_path = os.path.join(toolkit_path, "orbitfiles")

    if not os.path.exists(orbit_files_path):
        os.mkdir(orbit_files_path)

    for matching_pattern in re.findall(pattern, page_string):
        filename = "maven_orb_rec" + matching_pattern
        o_file = urllib.request.urlopen(orbit_files_url + filename)
        with open(os.path.join(orbit_files_path, filename), "wb") as code:
            code.write(o_file.read())

    merge_orbit_files()

    return


def merge_orbit_files():
    import os
    import re

    full_path = os.path.realpath(__file__)
    toolkit_path = os.path.dirname(full_path)
    orbit_files_path = os.path.join(toolkit_path, "orbitfiles")
    pattern = 'maven_orb_rec(_|)(|.{6})(|_.{9}).orb'
    orb_dates = []
    orb_files = []
    for f in os.listdir(orbit_files_path):
        x = re.match(pattern, f)
        if x is not None:
            orb_files.append(os.path.join(orbit_files_path, f))
            if x.group(2) != '':
                orb_dates.append(x.group(2))
            else:
                orb_dates.append('999999')

    sorted_files = [x for (y, x) in sorted(zip(orb_dates, orb_files))]

    with open(os.path.join(toolkit_path, 'maven_orb_rec.orb'), "w") as code:
        skip_2_lines = False
        for o_file in sorted_files:
            with open(o_file) as f:
                if skip_2_lines:
                    f.readline()
                    f.readline()
                skip_2_lines = True
                code.write(f.read())

    return


def get_access():
    import os
    toolkit_path = os.path.dirname(__file__)
    with open(os.path.join(toolkit_path, 'access.txt'), 'r') as f:
        f.readline()
        s = f.readline().rstrip()
        s = s.split(' ')
        if s[1] == '1':
            return False
        else:
            return True


def get_root_data_dir():
    from .config import CONFIG
    # Get preferred data download location for pyspedas project
    if 'local_data_dir' in CONFIG:
        return CONFIG['local_data_dir']
    else:
        raise NameError('local_data_dir is not found in config.py')


def create_pref_file(toolkit_path, download_path):
    import os

    # Put data download path into preferences file
    with open(os.path.join(toolkit_path, 'mvn_toolkit_prefs.txt'), 'w') as f:
        f.write("'; IDL Toolkit Data Preferences File'\n")
        f.write('mvn_root_data_dir: ' + download_path)

    return


def set_new_data_root_dir():
    import os

    # Get new preferred data download location for pyspedas project
    valid_path = input("Enter directory preference: ")
    while not os.path.exists(valid_path):
        valid_path = input("Specified path does not exist. Enter new path: ")
    download_path = valid_path
    print("Location of the mvn_toolkit_prefs file set to " + download_path)

    # Also edit the mvn_toolkit_prefs file to reflect the new data download location
    full_path = os.path.realpath(__file__)
    toolkit_path = os.path.dirname(full_path)
    create_pref_file(toolkit_path, download_path)


def get_new_files(files_on_site, data_dir, instrument, level):
    import os
    import re

    fos = files_on_site
    files_on_hd = []
    for (dir, _, files) in os.walk(data_dir):
        for f in files:
            if re.match('mvn_' + instrument + '_' + level + '_*', f):
                files_on_hd.append(f)

    x = set(files_on_hd).intersection(files_on_site)
    for matched_file in x:
        fos.remove(matched_file)

    return fos


def create_dir_if_needed(f, data_dir, level):
    import os

    if level == 'insitu':
        year, month, _ = get_year_month_day_from_kp_file(f)
    else:
        year, month, _ = get_year_month_day_from_sci_file(f)

    if not os.path.exists(os.path.join(data_dir, year, month)):
        os.makedirs(os.path.join(data_dir, year, month))

    full_path = os.path.join(data_dir, year, month)

    return full_path


def get_year_month_day_from_kp_file(f):
    date_string = f.split('_')[3]
    year = date_string[0:4]
    month = date_string[4:6]
    day = date_string[6:8]

    return year, month, day


def get_year_month_day_from_sci_file(f):

    m = l2_regex.match(f)
    year = m.group('year')
    month = m.group('month')
    day = m.group('day')

    return year, month, day


def display_progress(x, y):
    num_stars = int(round(float(x) / y * 70))
    print("||" + "*" * num_stars + "-" * (70 - num_stars) + "||" + " ( " + str(round(100 * float(x) / y)) + "% )")
    return


def get_uname_and_password():
    global uname
    global pword
    import getpass

    uname = input("Enter user name to access the team website: ")
    pword = getpass.getpass("Enter your password: ")
    return

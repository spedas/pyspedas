import re


def mms_file_filter(files, latest_version=False, major_version=False, min_version=None, version=None):
    """
    This function filters a list of MMS data files based on CDF version
    
    Parameters:
        version: str
            Specify a specific CDF version # to return (e.g., cdf_version='4.3.0')

        min_version: str
            Specify a minimum CDF version # to return

        latest_version: bool
            Only return the latest CDF version in the requested time interval

        major_version: bool
            Only return the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval

    Returns:
        List of filtered files
    """
    
    if not isinstance(files, list): files = [files]

    # allow the user to specify partial version #s
    if min_version is not None:
        n_declms = len(min_version.split('.'))
        if n_declms == 1:
            min_version = min_version + '.0.0'
        elif n_declms == 2:
            min_version = min_version + '.0'
    elif version is not None:
        n_declms = len(version.split('.'))
        if n_declms == 1:
            version = version + '.0.0'
        elif n_declms == 2:
            version = version + '.0'

    out_files = []
    file_versions = []
    max_major_version = 0
    max_version = 0

    # find all of the version #s, including the max major version and max total version
    for file in files:
        version_found = re.search(r'v([0-9]+)\.([0-9]+)\.([0-9]+)\.cdf$', file)
        if version_found:
            file_version = version_found.groups()
            # vX.Y.Z
            version_X = int(file_version[0])
            version_Y = int(file_version[1])
            version_Z = int(file_version[2])
            file_versions.append((version_X, version_Y, version_Z, file))
            if version_X > max_major_version:
                max_major_version = version_X
            if max_version == 0:
                max_version = (version_X, version_Y, version_Z)
            else:
                if (version_X > max_version[0]) or (version_X == max_version[0] and version_Y > max_version[1]) or (version_X == max_version[0] and version_Y == max_version[1] and version_Z > max_version[2]):
                    max_version = (version_X, version_Y, version_Z)
        else:
            continue

    for file_ver in file_versions:
        if min_version is not None: # MINIMUM file version
            min_version_num = [int(v) for v in min_version.split('.')]
            if (file_ver[0] > min_version_num[0]) or (file_ver[0] == min_version_num[0] and file_ver[1] > min_version_num[1]) or (file_ver[0] == min_version_num[0] and file_ver[1] == min_version_num[1] and file_ver[2] >= min_version_num[2]):
                out_files.append(file_ver[3])
        elif version is not None: # EXACT file version
            exact_version_num = [int(v) for v in version.split('.')]
            if file_ver[0] == exact_version_num[0] and file_ver[1] == exact_version_num[1] and file_ver[2] == exact_version_num[2]:
                out_files.append(file_ver[3])
        elif latest_version is not False: # LATEST (full) version, i.e., latest X.Y.Z
            if file_ver[0] == max_version[0] and file_ver[1] == max_version[1] and file_ver[2] == max_version[2]:
                out_files.append(file_ver[3])
        elif major_version is not False: # LATEST MAJOR version, i.e., latest X in vX.Y.Z
            if file_ver[0] >= max_major_version:
                out_files.append(file_ver[3])
        else:
            out_files.append(file_ver[3])

    return out_files

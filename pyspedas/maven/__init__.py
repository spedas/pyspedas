"""
This module contains routines for loading MAVEN data.
"""

from .maven_load import load_data


def maven_load(filenames=None,
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
               new_files=True,
               exclude_orbit_file=False,
               download_only=False,
               varformat=None,
               prefix='',
               suffix='',
               get_support_data=False):
    """
    Main function for downloading MAVEN data and loading it into tplot variables (if applicable).

    Parameters:
        filenames: str/list of str ['yyyy-mm-dd']
            List of dates to be downloaded (eg. ['2015-12-31']).
        instruments: str/list of str
            Instruments from which you want to download data.
        list_files: bool (True/False0
            If true, lists the files instead of downloading them.
        level: str
            Data level to download.
        insitu: bool (True/False)
            If true, specifies only insitu files.
        iuvs: bool (True/False)
            If true,
        new_files: bool (True/False)
            Checks downloaded files and only downloads those that haven't already been downloaded.
        start_date: str
            String that is the start date for downloading data (YYYY-MM-DD)
        end_date: str
            String that is the end date for downloading data (YYYY-MM-DD)
        update_prefs: bool (True/False)
            If true, updates where you want to store data locally
        only_update_prefs: bool (True/False)
            If true, *only* updates where to store dat alocally, doesn't download files.
        exclude_orbit_file: bool (True/False)
            If true, won't download the latest orbit tables.
        local_dir: str
            If indicated, specifies where to download files for a specific implementation of this function.
        download_only: bool (True/False)
            If True then files are downloaded only,
            if False then CDF files are also loaded into pytplot using cdf_to_tplot.
        varformat : str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.
        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".
    """
    tvars = load_data(filenames=filenames, instruments=instruments, level=level, insitu=insitu, iuvs=iuvs,
                      start_date=start_date, end_date=end_date, update_prefs=update_prefs,
                      only_update_prefs=only_update_prefs, local_dir=local_dir, list_files=list_files,
                      new_files=new_files, exclude_orbit_file=exclude_orbit_file, download_only=download_only,
                      varformat=varformat, prefix=prefix, suffix=suffix, get_support_data=get_support_data)
    return tvars

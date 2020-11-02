"""
This module contains routines for loading MAVEN data.
"""

from .maven_load import load_data


def maven_load(filenames=None,
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
    Main function for downloading MAVEN data and loading it into tplot variables (if CDF or STS data type).
    This function will also load in MAVEN KP data for position information, and read those into tplot as well

    Parameters:
        filenames: str/list of str ['yyyy-mm-dd']
            List of files to load
        instruments: str/list of str
            Instruments from which you want to download data.
            Accepted values are any combination of: sta, swi, swe, lpw, euv, ngi, iuv, mag, sep, rse
        type: str/list of str
            The observation/file type of the instruments to load.  If None, all file types are loaded.
            Otherwise, a file will only be loaded into tplot if its descriptor matches one of the strings in this field.
            See the instrument SIS for more detail on types.
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
        level: str
            Currently unused, defaults to using Level 2 data
        list_files: bool (True/False0
            If true, lists the files instead of downloading them.
        insitu: bool (True/False)
            If true, specifies only insitu files.
        iuvs: bool (True/False)
            If true,
        new_files: bool (True/False)
            Checks downloaded files and only downloads those that haven't already been downloaded.
        start_date: str
            String that is the start date for downloading data (YYYY-MM-DD), or the orbit number
        end_date: str
            String that is the end date for downloading data (YYYY-MM-DD), or the orbit number
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
        auto_yes : bool
            If this is True, there will be no prompt asking if you'd like to download files.
    """
    tvars = load_data(filenames=filenames, instruments=instruments, level=level, type=type, insitu=insitu, iuvs=iuvs,
                      start_date=start_date, end_date=end_date, update_prefs=update_prefs,
                      only_update_prefs=only_update_prefs, local_dir=local_dir, list_files=list_files,
                      new_files=new_files, exclude_orbit_file=exclude_orbit_file, download_only=download_only,
                      varformat=varformat, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                      auto_yes=auto_yes, varnames=varnames)
    return tvars

def kp(trange=['2016-01-01', '2016-01-02'], datatype=None, varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, insitu=True, iuvs=False, varnames=[]):
    return maven_load(start_date=trange[0], end_date=trange[1], type=datatype, level='kp', varformat=varformat, varnames=varnames, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, insitu=insitu, iuvs=iuvs)

def mag(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='ss', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='mag', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def sta(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='2a', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='sta', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def swea(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='svyspec', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='swe', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def swia(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='onboardsvyspec', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='swi', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def sep(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='s2-cal-svy-full', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='sep', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def rse(trange=['2016-01-01', '2016-01-02'], level='l2', datatype=None, varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='rse', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def lpw(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='lpiv', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='lpw', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def euv(trange=['2016-01-01', '2016-01-02'], level='l2', datatype='bands', varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='euv', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def iuv(trange=['2016-01-01', '2016-01-02'], level='l2', datatype=None, varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='iuv', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)

def ngi(trange=['2016-01-01', '2016-01-02'], level='l2', datatype=None, varformat=None, get_support_data=False, 
        auto_yes=True, downloadonly=False, varnames=[]):
    return maven_load(instruments='ngi', start_date=trange[0], end_date=trange[1], type=datatype, level=level, varformat=varformat, 
        get_support_data=get_support_data, auto_yes=auto_yes, download_only=downloadonly, varnames=varnames)




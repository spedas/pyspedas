from functools import update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial
from .load import load
from pyspedas.utilities.datasets import find_datasets


# Define partial wrappers for other load routines, fixing the instrument parameter
# 'better_partial' works better with PyCharm autocompletion than functools.partial
# update_wrapper() is necessary for help() to show info for the wrapped function,
# rather than the partial() object.

dcf = better_partial(load, instrument="dcf")
update_wrapper(dcf, load)
dcf.__doc__ = """
    Load FAST dcf data into tplot variables.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ["1996-12-01", "1996-12-02"].
    instrument : str, optional
        Type of instrument.
        Values can be: 'dcf', 'acf', 'esa', 'teams'.

        .. note::
           For this function, the `instrument` parameter is preset to `'dcf'` and should not be set manually.

    datatype : str, optional
        Data type to load. Depends on the instrument.
        For 'esa' valid options are: 'eeb', 'ees', 'ieb', 'ies'.
        For all other insturments, this keyword is ignored.
        Default is ''.
    level : str, optional
        Data level to load. Depends on the instrument.
        For 'dcf' and 'teams' valid options are: 'l2', 'k0'.
        For all other instruments, this keyword is ignored.
        Default is 'l2'.
    prefix : str, optional
        The tplot variable names will be given this prefix.
        Default is ''.
        In all cases a suitable prefix will be given depending on the instrument.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is no suffix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        Default is False; only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
        Default is False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
        Default is False.
    no_update : bool, optional
        If set, only load data from your local cache.
        Default is False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Default is False.
    force_download : bool, optional
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list of str/dictionary
        List of tplot variables created.
        If downloadonly is set to True, returns a list of the downloaded files.
        If notplot is set to True, returns a dictionary of the data loaded.

    """


acf = better_partial(load, instrument="acf")
update_wrapper(acf, load)
acf.__doc__ = """
    Load FAST acf data into tplot variables.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ["1996-12-01", "1996-12-02"].
    instrument : str, optional
        Type of instrument.
        Values can be: 'dcf', 'acf', 'esa', 'teams'.

        .. note::
           For this function, the `instrument` parameter is preset to `'acf'` and should not be set manually.

    datatype : str, optional
        Data type to load. Depends on the instrument.
        For 'esa' valid options are: 'eeb', 'ees', 'ieb', 'ies'.
        For all other insturments, this keyword is ignored.
        Default is ''.
    level : str, optional
        Data level to load. Depends on the instrument.
        For 'dcf' and 'teams' valid options are: 'l2', 'k0'.
        For all other instruments, this keyword is ignored.
        Default is 'l2'.
    prefix : str, optional
        The tplot variable names will be given this prefix.
        Default is ''.
        In all cases a suitable prefix will be given depending on the instrument.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is no suffix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        Default is False; only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
        Default is False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
        Default is False.
    no_update : bool, optional
        If set, only load data from your local cache.
        Default is False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Default is False.
    force_download : bool, optional
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list of str/dictionary
        List of tplot variables created.
        If downloadonly is set to True, returns a list of the downloaded files.
        If notplot is set to True, returns a dictionary of the data loaded.

    """


esa = better_partial(load, instrument="esa")
update_wrapper(esa, load)
esa.__doc__ = """
    Load FAST esa data into tplot variables.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ["1996-12-01", "1996-12-02"].
    instrument : str, optional
        Type of instrument.
        Values can be: 'dcf', 'acf', 'esa', 'teams'.

        .. note::
           For this function, the `instrument` parameter is preset to `'esa'` and should not be set manually.

    datatype : str, optional
        Data type to load. Depends on the instrument.
        For 'esa' valid options are: 'eeb', 'ees', 'ieb', 'ies'.
        For all other insturments, this keyword is ignored.
        Default is ''.
    level : str, optional
        Data level to load. Depends on the instrument.
        For 'dcf' and 'teams' valid options are: 'l2', 'k0'.
        For all other instruments, this keyword is ignored.
        Default is 'l2'.
    prefix : str, optional
        The tplot variable names will be given this prefix.
        Default is ''.
        In all cases a suitable prefix will be given depending on the instrument.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is no suffix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        Default is False; only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
        Default is False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
        Default is False.
    no_update : bool, optional
        If set, only load data from your local cache.
        Default is False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Default is False.
    force_download : bool, optional
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list of str/dictionary
        List of tplot variables created.
        If downloadonly is set to True, returns a list of the downloaded files.
        If notplot is set to True, returns a dictionary of the data loaded.

    """


teams = better_partial(load, instrument="teams")
update_wrapper(teams, load)
teams.__doc__ = """
    Load FAST teams data into tplot variables.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ["1996-12-01", "1996-12-02"].
    instrument : str, optional
        Type of instrument.
        Values can be: 'dcf', 'acf', 'esa', 'teams'.

        .. note::
           For this function, the `instrument` parameter is preset to `'teams'` and should not be set manually.

    datatype : str, optional
        Data type to load. Depends on the instrument.
        For 'esa' valid options are: 'eeb', 'ees', 'ieb', 'ies'.
        For all other insturments, this keyword is ignored.
        Default is ''.
    level : str, optional
        Data level to load. Depends on the instrument.
        For 'dcf' and 'teams' valid options are: 'l2', 'k0'.
        For all other instruments, this keyword is ignored.
        Default is 'l2'.
    prefix : str, optional
        The tplot variable names will be given this prefix.
        Default is ''.
        In all cases a suitable prefix will be given depending on the instrument.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is no suffix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data" will be loaded into tplot.
        Default is False; only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
        Default is False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
        Default is False.
    no_update : bool, optional
        If set, only load data from your local cache.
        Default is False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Default is False.
    force_download : bool, optional
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list of str/dictionary
        List of tplot variables created.
        If downloadonly is set to True, returns a list of the downloaded files.
        If notplot is set to True, returns a dictionary of the data loaded.

    """


datasets = better_partial(find_datasets, mission="FAST", label=True)
update_wrapper(datasets, find_datasets)

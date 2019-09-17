# -*- coding: utf-8 -*-
"""
File:
    load_data.py

Description:
    Main function for loading data.

Example:
    pyspedas.load_data('themis', '2015-12-31', ['tha'], '*', 'l2', False)

Parameters:
    mission: str
        The name of the mission (eg. 'themis').
    dates: str/list of str ['yyyy-mm-dd']
        List of dates to be downloaded (eg. ['2015-12-31']).
    probes: str/list of str
        Probes for missions with multiple probes (eg. ['tha', 'thb']),
        wildcard ('*') for all probes.
    instruments: str/list of str
        List of instruments (eg. ['fft']), wildcard ('*') for all instruments.
    level: str
        Usually, either 'l2' or 'l1', depends on mission.
    other: str
        Other mission specific parameters.
    downloadonly: bool (True/False)
        If True then CDF files are downloaded only,
        if False then they are also loaded into pytplot using cdf_to_tplot.
    varformat : str
        The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
    get_support_data: bool
        Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".
    prefix: str
        The tplot variable names will be given this prefix.
        By default, no prefix is added.
    suffix: str
        The tplot variable names will be given this suffix.
        By default, no suffix is added.
"""


def load_data(mission, dates, probes, instruments, level, other=None,
              downloadonly=False, varformat=None, get_support_data=False,
              prefix='', suffix=''):
    """Loads data from mission cdf files into pytplot"""

    if mission == 'themis':
        from pyspedas import themis_load
        themis_load(dates, probes, instruments, level, downloadonly, varformat,
                    get_support_data, prefix, suffix)
    elif mission == 'gmag':
        stations = probes
        group = other
        from pyspedas import gmag_load
        gmag_load(dates, stations, group, downloadonly, varformat,
                  get_support_data, prefix, suffix)
    elif mission == 'omni':
        from pyspedas import omni_load
        # level = 1min, 5min
        omni_load(dates, level, downloadonly, varformat, get_support_data,
                  prefix, suffix)
    else:
        print("Currently, only the THEMIS and OMNI missions are implemented.")

    print('Data loading finished.')

from pytplot import time_string, time_double
from pytplot import time_clip as tclip
from pyspedas.hapi_tools.hapi import hapi
from .config import CONFIG

def load(trange=['2017-03-27/06:00', '2017-03-27/08:00'], 
         probe='a',
         instrument='mag',
         datatype='', 
         level='l1b', 
         prefix='',
         suffix='',
         varnames=[],  # should be sent to hapi as parameters?
         time_clip=False,
         force_download=False):
    """
    Loads data from the Swarm mission.

    This function is not meant to be called directly; instead, see the wrappers such as:
        - pyspedas.projects.swarm.mag.

    Parameters
    ----------
    trange : list of str, default=['2017-03-27/06:00', '2017-03-27/08:00']
        Time range of interest [starttime, endtime] with the format 'YYYY-MM-DD' or 'YYYY-MM-DD/hh:mm:ss'.
    probe : str or list of str, default='a'
        Swarm spacecraft ID(s) ('a', 'b', and/or 'c').
    instrument : str, default='mag'
        The instrument from which to load data. For magnetometer data, use 'mag'.
    datatype : str, optional
        Specific data type to load, if applicable. For magnetometer data, options include 'hr' (high resolution) and 'lr' (low resolution).
    level : str, default='l1b'
        Data level; for magnetometer data. Options: 'l1b'.
    prefix : str, optional
        The tplot variable names will be given this prefix. By default, no prefix is added.
    suffix : str, optional
        The tplot variable names will be given this suffix. By default, no suffix is added.
    varnames : list of str, optional
        List of variable names to load as parameters. If not specified, all data variables are loaded.
    time_clip : bool, default=False
        Time clip the variables to exactly the range specified in the trange keyword.
    force_download : bool, default=False
        Swarm data is requested via HAPI. This parameter always ignored and reserved for compatibility.

    Returns
    -------
    out_vars : list of str
        List of tplot variable names created by the data loading process.

    Examples
    --------
    This function is not intended to be called directly.
    """


    server = CONFIG['remote_data_dir'] + 'hapi/'

    if not isinstance(probe, list):
        probe = [probe]

    tr = time_string(time_double(trange), fmt='%Y-%m-%dT%H:%M:%S')

    out_vars = []

    if prefix:
        prefix2 = prefix
    else:
        prefix2 = ''

    for this_probe in probe:
        prefix = prefix2 + 'swarm' + this_probe.lower() + '_'
        if instrument == 'mag':
            dataset = 'SW_OPER_MAG' + this_probe.upper() + '_' + datatype.upper() + '_' + level[1:].upper()
            tvars = hapi(trange=tr, 
                         server=server, 
                         dataset=dataset, 
                         parameters=varnames,
                         suffix=suffix,
                         prefix=prefix)

            if tvars is not None and len(tvars) != 0:
                out_vars.extend(tvars)

    if time_clip:
        for new_var in out_vars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return out_vars

from pytplot import tplot
import pyspedas
from .load import load

# This routine was originally in swarm/__init__.py.
def mag(trange=['2017-03-27/06:00', '2017-03-27/08:00'],
        probe='a',
        datatype='hr',
        level='l1b',
        prefix='',
        suffix='',
        varnames=[],
        time_clip=False,
        force_download=False):
    """
    Loads data from the Vector Field Magnetometer (VFM).

    Parameters
    ----------
    trange : list of str, default=['2017-03-27/06:00', '2017-03-27/08:00']
        Time range of interest [starttime, endtime] with the format
        'YYYY-MM-DD' or 'YYYY-MM-DD/hh:mm:ss'.
    probe : str or list of str, default='a'
        Swarm spacecraft ID ('a', 'b', and/or 'c').
    datatype : str, default='hr'
        Data type; valid options: 'hr' (high resolution), 'lr' (low resolution).
    level : str, default='l1b'
        Data level; options: 'l1b'.
    prefix : str, optional
        The tplot variable names will be given this prefix. By default, no prefix is added.
    suffix : str, optional
        The tplot variable names will be given this suffix. By default, no suffix is added.
    varnames : list of str, optional
        List of variable names to load. If not specified, all data variables are loaded.
    time_clip : bool, default=False
        Time clip the variables to exactly the range specified in the trange keyword.
    force_download : bool, default=False
        Swarm data is requested via HAPI. This parameter always ignored and reserved for compatibility.

    Returns
    -------
    out_vars : list of str
        List of tplot variables created.

    Examples
    --------
    To load and plot Magnetometer (MAG) data from the Swarm mission for probe 'c' over a specific time range, you can use the following commands:

    >>> import pyspedas
    >>> from pyspedas import tplot

    # Load MAG data for probe 'c'
    >>> mag_vars = pyspedas.projects.swarm.mag(probe='c', trange=['2017-03-27/06:00', '2017-03-27/08:00'], datatype='hr')

    # Plot the loaded MAG data
    >>> tplot('swarmc_B_VFM')
    """

    return load(instrument='mag', trange=trange, probe=probe, level=level, datatype=datatype, prefix=prefix, suffix=suffix, varnames=varnames, time_clip=time_clip, force_download=force_download)

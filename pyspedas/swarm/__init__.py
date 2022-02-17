
from .load import load

def mag(trange=['2017-03-27/06:00', '2017-03-27/08:00'],
        probe='a',
        datatype='hr',
        level='l1b', 
        suffix='', 
        varnames=[],
        time_clip=False):
    """
    This function loads data from the Vector Field Magnetometer (VFM)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Swarm spacecraft ID ('a', 'b' and/or 'c')

        datatype: str
            Data type; Valid options:
                'hr', 'lr'

        level: str
            Data level; options: 'l1b'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='mag', trange=trange, probe=probe, level=level, datatype=datatype, suffix=suffix, varnames=varnames, time_clip=time_clip)

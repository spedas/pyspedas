from pytplot import options
from .load import load


def mag(trange=['2020-06-01', '2020-06-02'],
        datatype='rtn-normal', 
        level='l2', 
        suffix='', 
        prefix='', 
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False):
    """
    This function loads data from the Magnetometer (MAG)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:
              'rtn-normal': RTN Coordinates in Normal Mode
              'rtn-normal-1-minute': Same as above, but at 1-min resolution
              'rtn-burst': RTN Coordinates in Burst Mode
              'srf-normal': Spacecraft Reference Frame in Normal Mode
              'srf-burst': Spacecraft Reference Frame in Burst Mode 

        level: str
            Data level (default: l2)

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no prefix is added.
            Default: ''
        
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """

    if prefix is None:
        prefix = ''
    
    if suffix is None:
        suffix = ''
        
    mag_vars = load(instrument='mag', trange=trange, level=level, datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)
    
    if mag_vars is None or notplot or downloadonly:
        return mag_vars

    if datatype[-5:] == 'burst':
        ytitle = 'SOLO MAG \\ burst'
    elif datatype[-6:] == 'minute':
        ytitle = 'SOLO MAG \\ 1-min'
    else:
        ytitle = 'SOLO MAG'

    if prefix+'B_SRF'+suffix in mag_vars:
        options(prefix+'B_SRF'+suffix, 'legend_names', ['Bx (SRF)', 'By (SRF)', 'Bz (SRF)'])
        options(prefix+'B_SRF'+suffix, 'ytitle', ytitle)

    if prefix+'B_RTN'+suffix in mag_vars:
        options(prefix+'B_RTN'+suffix, 'legend_names', ['Br (RTN)', 'Bt (RTN)', 'Bn (RTN)'])
        options(prefix+'B_RTN'+suffix, 'ytitle', ytitle)

    return mag_vars



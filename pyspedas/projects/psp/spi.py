
from .load import load

# This routine was originally in psp/__init__.py.  If you need to see the history of this routine before
# it was moved to its own file, please check the history for __init__.py.

# Loading
def spi(trange=['2018-11-5', '2018-11-6'], 
        datatype='sf00_l3_mom', 
        level='l3',
        suffix='',  
        prefix='',
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        username=None,
        password=None,
        last_version=False,
        force_download=False,
    ):
    """
    This function loads Parker Solar Probe SWEAP/SPAN-i data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options Include:
                'sf00_l3_mom': Moments of the Proton distribution function (RTN)
                'sf0a_l3_mom': Moments of the Alpha distribution function (RTN)
                'sf00_l3_mom_inst': Moments of the Proton distribution function (Instrument Frame)
                'sf0a_l3_mom_inst': Moments of the Alpha distribution function (Instrument Frame)

        suffix: str
            The tplot variable names will be given this suffix. By default,
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

        username: str
            Username to use for authentication.
            
            If passed, attempt to download data from the SWEAP Instrument Team server
            instead of the fully public server at SPDF.
            Provides access to unpublished files.

        password: str
            Password to use for authentication

        last_version: bool
            If True, only download the highest-numbered file version
        
        force_download: bool
            If True, downloads the file even if a newer version exists locally. 
            Default: False.

    Returns
    ----------
        List of tplot variables created.

    """
    if datatype in ['sf00_l3_mom','sf0a_l3_mom','sf00_l3_mom_inst','sf0a_l3_mom_inst']:
        datatype = 'spi_' + datatype
        level = 'l3'
        print("Using LEVEL=L3")

    return load(instrument='spi', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, prefix=prefix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, 
        username=username, password=password,last_version=last_version, force_download=force_download
        )


from .gmag_isee_fluxgate import gmag_isee_fluxgate

from typing import List, Union, Optional, Dict, Any

def gmag_stel_fluxgate(
    trange: List[str] = ['2020-08-01', '2020-08-02'],
    suffix: str = '',
    site: Union[str, List[str]] = 'all',
    datatype: Union[str, List[str]] = 'all',
    get_support_data: bool = False,
    varformat: Optional[str] = None,
    varnames: List[str] = [],
    downloadonly: bool = False,
    notplot: bool = False,
    no_update: bool = False,
    uname: Optional[str] = None,
    passwd: Optional[str] = None,
    time_clip: bool = False,
    ror: bool = True,
    force_download: bool = False,
) -> Union[Dict, None, List[Union[str, Any]]]:
    """
    Load data from STEL Fluxgate Magnetometers (wrapper for gmag_isee_fluxgate)

    Parameters
    ----------
    trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2020-08-01', '2020-08-02']

    suffix: str
            The tplot variable names will be given this suffix.  Default: ''

    site: str or list of str
            The site or list of sites to load.
            Valid values: 'msr', 'rik', 'kag', 'ktb', 'lcl', 'mdm', 'tew', 'all'
            Default: ['all']

    datatype: str or list of str
            The data types to load. Valid values: '64hz', '1sec', '1min', '1h', 'all'
            Default: 'all'

    get_support_data: bool
            If true, data with an attribute "VAR_TYPE" with a value of "support_data"
            or 'data' will be loaded into tplot. Default: False

    varformat: str
            The CDF file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables will be loaded).

    varnames: list of str
            List of variable names to load. Default: [] (all variables will be loaded)

    downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables. Default: False

    notplot: bool
            Return the data in hash tables instead of creating tplot variables. Default: False

    no_update: bool
            If set, only load data from your local cache. Default: False

    uname: str
            User name.  Default: None

    passwd: str
            Password. Default: None

    time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword. Default: False

    ror: bool
            If set, print PI info and rules of the road. Default: True

    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------

    Examples
    ________
    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> fluxgate_vars=pyspedas.projects.erg.gmag_stel_fluxgate(trange=['2020-08-01','2020-08-02'], site='all')
    >>> tplot('isee_fluxgate_mag_ktb_1min_hdz')


    """

    return gmag_isee_fluxgate(
        trange=trange,
        suffix=suffix,
        site=site,
        datatype=datatype,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        downloadonly=downloadonly,
        notplot=notplot,
        no_update=no_update,
        uname=uname,
        passwd=passwd,
        time_clip=time_clip,
        ror=ror,
        force_download=force_download,
    )

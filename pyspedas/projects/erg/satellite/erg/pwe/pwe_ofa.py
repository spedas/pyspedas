from pytplot import options, ylim, zlim, get_data

from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def pwe_ofa(
    trange: List[str] = ['2017-04-01', '2017-04-02'],
    datatype: str = 'spec',
    level: str = 'l2',
    suffix: str = '',
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
) -> List[str]:
    """
    This function loads data from the PWE experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-04-01', '2017-04-02']

        datatype: str
            Data type; Valid 'l2' options: 'complex', 'matrix', 'spec'. Valid 'l3' options: 'property'
            Default: 'spec'

        level: str
            Data level; Valid options: 'l2', 'l3'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix. Default: None

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded. Default: [] (all variables loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: True

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

        ror: bool
            If set, print PI info and rules of the road
            Default: True

        uname: str
            User name. Default: None

        passwd: str
            Password. Default: None

        force_download: bool
            Download file even if local version is more recent than server version
            Default: False

    Returns
    -------
        List of tplot variables created.

    Examples
    --------
    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> pwe_ofa_vars = pyspedas.projects.erg.pwe_ofa(trange=['2017-03-27', '2017-03-28'])
    >>> tplot('erg_pwe_ofa_l2_spec_E_spectra_132')

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600. * 24
    prefix = 'erg_pwe_ofa_'+level+'_'+datatype+'_'

    pathformat = 'satellite/erg/pwe/ofa/'+level+'/'+datatype + \
        '/%Y/%m/erg_pwe_ofa_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'

    loaded_data = load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                       varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, force_download=force_download)

    if (len(loaded_data) > 0) and ror:

        try:
            gatt = get_gatt_ror(downloadonly, loaded_data)

            # --- print PI info and rules of the road

            print(' ')
            print(' ')
            print(
                '**************************************************************************')
            print(gatt["LOGICAL_SOURCE_DESCRIPTION"])
            print('')
            print('Information about ERG PWE OFA')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: ", gatt["PI_AFFILIATION"])
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                'RoR of PWE/OFA: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Pwe/Ofa')
            print('')
            print('Contact: erg_pwe_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    # set spectrogram plot option
    options(prefix+'E_spectra_132'+suffix,  'Spec', 1)
    options(prefix+'B_spectra_132'+suffix,  'Spec', 1)

    # set y axis to logscale
    options(prefix+'E_spectra_132'+suffix,  'ylog', 1)
    options(prefix+'B_spectra_132'+suffix,  'ylog', 1)

    if prefix+'E_spectra_132'+suffix in loaded_data:
        # set ylim
        ylim(prefix+'E_spectra_132'+suffix, 32e-3, 20.)
        # set zlim
        zlim(prefix+'E_spectra_132'+suffix, 1e-9, 1e-2)

    if prefix+'B_spectra_132'+suffix in loaded_data:
        # set ylim
        ylim(prefix+'B_spectra_132'+suffix, 32e-3, 20.)
        # set zlim
        zlim(prefix+'B_spectra_132'+suffix, 1e-4, 1e2)

    # set ytitle
    options(prefix+'E_spectra_132'+suffix,  'ytitle', 'ERG PWE/OFA-SPEC (E)')
    options(prefix+'B_spectra_132'+suffix,  'ytitle', 'ERG PWE/OFA-SPEC (B)')

    # set ysubtitle
    options(prefix+'E_spectra_132'+suffix,  'ysubtitle', 'frequency [kHz]')
    options(prefix+'B_spectra_132'+suffix,  'ysubtitle', 'frequency [kHz]')

    # set ztitle
    options(prefix+'E_spectra_132'+suffix,  'ztitle', 'mV^2/m^2/Hz')
    options(prefix+'B_spectra_132'+suffix,  'ztitle', 'pT^2/Hz')

    # set z axis to logscale
    options(prefix+'E_spectra_132'+suffix,  'zlog', 1)
    options(prefix+'B_spectra_132'+suffix,  'zlog', 1)

    # change colormap option
    options(prefix+'E_spectra_132'+suffix,  'Colormap', 'jet')
    options(prefix+'B_spectra_132'+suffix,  'Colormap', 'jet')

    return loaded_data

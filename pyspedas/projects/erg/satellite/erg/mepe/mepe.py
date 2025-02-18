
from pytplot import options, ylim, get_data

from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def mepe(
    trange: List[str] = ['2017-03-27', '2017-03-28'],
    datatype: str = 'omniflux',
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
    This function loads data from the MEP-e experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Dafault: ['2017-03-27', '2017-03-28']
            '
        datatype: str
            Data type; Valid 'l2' options: '3dflux', 'omniflux'  Valid 'l3' options: '3dflux', 'pa'
            Default: 'omniflux'

        level: str
            Data level; Valid options: 'l2', 'l3'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  Default: None

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded.  Default: [] (all variables loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables. Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables.
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword.
            Default: False

        ror: bool
            If set, print PI info and rules of the road.
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
    >>> mepe_vars = pyspedas.projects.erg.mepe(trange=['2017-03-27', '2017-03-28'])
    >>> tplot('erg_mepe_l2_omniflux_FEDO')

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    if level == 'l3':
        datatype = '3dflux'

    file_res = 3600. * 24
    prefix = 'erg_mepe_'+level + '_' + datatype + '_'
    pathformat = 'satellite/erg/mepe/'+level+'/'+datatype + \
        '/%Y/%m/erg_mepe_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'

    loaded_data = load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                       varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, force_download=force_download)

    if (len(loaded_data) > 0) and ror:

        try:
            gatt = get_gatt_ror(downloadonly, loaded_data)

            # --- print PI info and rules of the road

            print(' ')
            print(
                '**************************************************************************')
            print(gatt["LOGICAL_SOURCE_DESCRIPTION"])
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: ", gatt["PI_AFFILIATION"])
            print('')
            print('- The rules of the road (RoR) common to the ERG project:')
            print(
                '      https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                '- RoR for MEP-e data:  https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Mepe')
            print('')
            print('Contact: erg_mep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if datatype == 'omniflux':
        # set spectrogram plot option
        options(prefix + 'FEDO' + suffix, 'Spec', 1)
        # set y axis to logscale
        options(prefix + 'FEDO' + suffix, 'ylog', 1)
        # set ytitle
        options(prefix + 'FEDO' + suffix, 'ytitle', 'ERG\nMEP-e\nFEDO\nEnergy')
        # set ysubtitle
        options(prefix + 'FEDO' + suffix, 'ysubtitle', '[keV]')
        # set ylim
        ylim(prefix + 'FEDO' + suffix, 6., 100.)
        # set z axis to logscale
        options(prefix + 'FEDO' + suffix, 'zlog', 1)
        # set ztitle
        options(prefix + 'FEDO' + suffix, 'ztitle', '[/s-cm^{2}-sr-keV]')
        # change colormap option
        options(prefix + 'FEDO' + suffix, 'Colormap', 'jet')
    elif (datatype == '3dflux') and (level == 'l2'):
        # set spectrogram plot option
        options(prefix + 'FEDU' + suffix, 'Spec', 1)
        options(prefix + 'FEDU_n' + suffix, 'Spec', 1)
        options(prefix + 'FEEDU' + suffix, 'Spec', 1)
        options(prefix + 'count_raw' + suffix, 'Spec', 1)

        # set y axis to logscale
        options(prefix + 'FEDU' + suffix, 'ylog', 1)
        options(prefix + 'FEDU_n' + suffix, 'ylog', 1)
        options(prefix + 'FEEDU' + suffix, 'ylog', 1)
        options(prefix + 'count_raw' + suffix, 'ylog', 1)

        # set ysubtitle
        options(prefix + 'FEDU' + suffix, 'ysubtitle', '[keV]')
        options(prefix + 'FEDU_n' + suffix, 'ysubtitle', '[keV]')
        options(prefix + 'count_raw' + suffix, 'ysubtitle', '[keV]')

        # set ylim
        ylim(prefix + 'FEDU' + suffix, 6., 100.)
        ylim(prefix + 'FEDU_n' + suffix, 6., 100.)
        ylim(prefix + 'count_raw' + suffix, 6., 100.)

        # set z axis to logscale
        options(prefix + 'FEDU' + suffix, 'zlog', 1)
        options(prefix + 'FEDU_n' + suffix, 'zlog', 1)
        options(prefix + 'FEEDU' + suffix, 'zlog', 1)
        options(prefix + 'count_raw' + suffix, 'zlog', 1)

        # set ztitle
        options(prefix + 'FEDU' + suffix, 'ztitle', '[/s-cm^{2}-sr-keV]')
        options(prefix + 'FEDU_n' + suffix, 'ztitle', '[/s-cm^{2}-sr-keV]')

        # change colormap option
        options(prefix + 'FEDU' + suffix, 'Colormap', 'jet')
        options(prefix + 'FEDU_n' + suffix, 'Colormap', 'jet')
        options(prefix + 'FEEDU' + suffix, 'Colormap', 'jet')
        options(prefix + 'count_raw' + suffix, 'Colormap', 'jet')

    return loaded_data

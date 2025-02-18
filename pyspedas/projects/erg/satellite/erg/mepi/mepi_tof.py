from pytplot import options, ylim, get_data

from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def mepi_tof(
    trange: List[str] = ['2017-03-27', '2017-03-28'],
    datatype: str = 'flux',
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
    This function loads data from the MEP-i experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-03-27', '2017-03-28']

        datatype: str
            Data type; Valid options: 'flux'
            Default: 'flux'

        level: str
            Data level; Valid options: 'l2'
            Defauls: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: None

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
            Default: None (all variables loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded.  Default: [] (all variables loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables. Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache.
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword.
            Default: False

        ror: bool
            If set, print PI info and rules of the road.
            Default: True

        uname: str
            User name.  Default: None

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
    >>> mepi_tof_vars = pyspedas.projects.erg.mepi_tof(trange=['2017-03-27', '2017-03-28'])

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600. * 24
    prefix = 'erg_mepi_'+level+'_tof'+datatype+'_'

    pathformat = 'satellite/erg/mepi/'+level+'/tof/%Y/%m/erg_mepi_' + \
        level+'_tof'+datatype+'_%Y%m%d_v??_??.cdf'

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
            print("Affiliation: ",gatt["PI_AFFILIATION"])
            print('')
            print('- The rules of the road (RoR) common to the ERG project:')
            print(
                '      https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                '- RoR for MEP-i data: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Mepi')
            print('')
            print('Contact: erg_mep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if 'flux' in datatype:
        original_suffix_list = ['FPDU', 'FHE2DU', 'FHEDU', 'FOPPDU', 'FODU', 'FO2PDU',
                                'count_raw_P', 'count_raw_HE2', 'count_raw_HE', 'count_raw_OPP', 'count_raw_O', 'count_raw_O2P']
        tplot_names_list = []
        for i in range(len(original_suffix_list)):
            tplot_names_list.append(prefix + original_suffix_list[i] + suffix)
            if tplot_names_list[i] in loaded_data:
                ylim(tplot_names_list[i], 4, 190)

        # set spectrogram plot option
        options(tplot_names_list, 'Spec', 1)

        # set y axis to logscale
        options(tplot_names_list, 'ylog', 1)

        # set ysubtitle
        options(tplot_names_list, 'ysubtitle', '[keV/q]')

        # set ztitle
        options(tplot_names_list[:6], 'ztitle', '[/s-cm^{2}-sr-keV/q]')
        options(tplot_names_list[6:], 'ztitle', '[cnt/smpl]')

        # set z axis to logscale
        options(tplot_names_list, 'zlog', 1)

    elif 'raw' in datatype:

        # set spectrogram plot option
        options(loaded_data, 'Spec', 1)

        # set z axis to logscale
        options(loaded_data, 'zlog', 1)

    return loaded_data

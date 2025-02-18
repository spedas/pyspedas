import numpy as np
from pytplot import clip, options, store_data, ylim, zlim, get_data

from ..load import load
from ..get_gatt_ror import get_gatt_ror

from typing import List, Optional

def xep(
    trange: List[str] = ['2017-06-01', '2017-06-02'],
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
    This function loads data from the XEP-e experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-06-01', '2017-06-02']

        datatype: str
            Data type; Valid options: 'omniflux', '2dflux'
            Default: 'omniflux'

        level: str
            Data level; Valid options: 'l2'
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
    >>> xep_vars = pyspedas.projects.erg.xep(trange=['2017-03-27', '2017-03-28'])
    >>> tplot('erg_xep_l2_FEDO_SSD')

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    if (datatype == 'omniflux') or (datatype == '2dflux'):
        # to avoid failure of creation Tplot variables (at store_data.py) of xep
        notplot = True
    file_res = 3600. * 24
    prefix = 'erg_xep_'+level+'_'
    pathformat = 'satellite/erg/xep/'+level+'/'+datatype + \
        '/%Y/%m/erg_xep_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'
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
            print('Information about ERG XEP')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: ",gatt["PI_AFFILIATION"])
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print('RoR of XEP: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Xep')
            print('')
            print('Contact: erg_xep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if isinstance(loaded_data, dict):

        if datatype == 'omniflux':
            tplot_variables = []

            if prefix + 'FEDO_SSD' + suffix in loaded_data:
                v_vars_min = loaded_data[prefix + 'FEDO_SSD' + suffix]['v'][0]
                v_vars_max = loaded_data[prefix + 'FEDO_SSD' + suffix]['v'][1]
                v_vars = np.sqrt(v_vars_min * v_vars_max)  # Geometric mean

                store_data(prefix + 'FEDO_SSD' + suffix, data={'x': loaded_data[prefix + 'FEDO_SSD' + suffix]['x'],
                                                               'y': loaded_data[prefix + 'FEDO_SSD' + suffix]['y'],
                                                               'v': v_vars},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDO_SSD' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDO_SSD' + suffix)

                if prefix + 'FEDO_SSD' + suffix in tplot_variables:
                    # remove minus valuse of y array
                    clip(prefix + 'FEDO_SSD' + suffix, 0., 5000.)
                # set spectrogram plot option
                options(prefix + 'FEDO_SSD' + suffix, 'Spec', 1)
                # set y axis to logscale
                options(prefix + 'FEDO_SSD' + suffix, 'ylog', 1)
                # set yrange
                options(prefix + 'FEDO_SSD' + suffix,
                        'yrange', [4.0e+02, 4.5e+03])
                # set z axis to logscale
                options(prefix + 'FEDO_SSD' + suffix, 'zlog', 1)
                # set zrange
                options(prefix + 'FEDO_SSD' + suffix,
                        'zrange', [1.0e-01, 1.0e+3])
                # change colormap option
                options(prefix + 'FEDO_SSD' + suffix, 'Colormap', 'jet')

                # set ztitle
                options(prefix + 'FEDO_SSD' + suffix,
                        'ztitle', '[/cm^{2}-str-s-keV]')
                # set ytitle
                options(prefix + 'FEDO_SSD' + suffix,
                        'ytitle', 'XEP\nomniflux\nLv2\nEnergy')
                # set ysubtitle
                options(prefix + 'FEDO_SSD' + suffix, 'ysubtitle', '[keV]')

                ylim(prefix + 'FEDO_SSD' + suffix, 4.0e+02, 4.5e+03)
                zlim(prefix + 'FEDO_SSD' + suffix, 1.0e-01, 1.0e+3)

            return tplot_variables

        if datatype == '2dflux':
            tplot_variables = []

            if prefix + 'FEDU_SSD' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'FEDU_SSD' + suffix]:
                    v_keyname = 'v1'
                store_data(prefix + 'FEDU_SSD' + suffix,
                           data={'x': loaded_data[prefix + 'FEDU_SSD' + suffix]['x'],
                                 'y': loaded_data[prefix + 'FEDU_SSD' + suffix]['y'],
                                 'v1': np.sqrt(loaded_data[prefix + 'FEDU_SSD' + suffix][v_keyname][:9, 0]
                                               * loaded_data[prefix + 'FEDU_SSD' + suffix][v_keyname][:9, 1]),  # Geometric mean of 'v'
                                 'v2': [i for i in range(16)]},  # [0, 1, 2, .., 15]
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_SSD' + suffix]['CDF']})

                tplot_variables.append(prefix + 'FEDU_SSD' + suffix)

                if prefix + 'FEDU_SSD' + suffix in tplot_variables:
                    clip(prefix + 'FEDU_SSD' + suffix, -1.0e+10, 1.0e+10)

                return tplot_variables

    return loaded_data

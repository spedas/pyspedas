
import numpy as np
from pytplot import clip, get_data, options, store_data, ylim, zlim

from pytplot import time_double


from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def lepe(
    trange: List[str] = ['2017-04-04', '2017-04-05'],
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
    version: Optional[str] = None,
    only_fedu: bool = False,
    et_diagram: bool = False,
    force_download: bool = False,
) -> List[str]:
    """
    This function loads data from the LEP-e experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-04-04','2017-04-05']

        datatype: str
            Data type; Valid 'l1' options: None
            Valid 'l2' options: 'omniflux', '3dflux', '3dflux_finech'
            Valid 'l3' options: 'pa'
            Default: 'omniflux'

        level: str
            Data level; Valid options: 'l1','l2','l3'   Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  Default: None

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables are loaded)

        varnames: list of str
            List of variable names to load
            Default: [] (all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables. Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables. Default: False

        no_update: bool
            If set, only load data from your local cache. Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword. Default: False

        ror: bool
            If set, print PI info and rules of the road. Default: True

        version: str
            Set this value to specify the version of cdf files (such as "v02_02")
            Default: None

        only_fedu: bool
            If set, not make erg_lepe_l3_pa_enech ??(??:01,01,..32)_FEDU Tplot Variables
            Default: False

        et_diagram: bool
            If set, make erg_lepe_l3_pa_pabin ??(??:01,01,..16)_FEDU Tplot Variables
            Default: False

        uname: str
            User name.  Default: None

        passwd: str
            Password.  Default: None

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
    >>> lepe_vars = pyspedas.projects.erg.lepe(trange=['2017-03-27', '2017-03-28'])
    >>> tplot('erg_lepe_l2_omniflux_FEDO')


    """

    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    if level == 'l3':
        datatype = 'pa'

    if ((level == 'l2') and (datatype == 'omniflux')) or \
        ((level == 'l2') and (datatype == '3dflux')) or \
            (level == 'l3'):
        # to avoid failure of creation plot variables (at store_data.py) of lepe
        notplot = True

    file_res = 3600. * 24
    prefix = 'erg_lepe_'+level+'_' + datatype + '_'
    pathformat = 'satellite/erg/lepe/'+level+'/'+datatype + \
        '/%Y/%m/erg_lepe_'+level+'_'+datatype+'_%Y%m%d_'

    if version is None:
        pathformat += 'v??_??.cdf'
    else:
        pathformat += version + '.cdf'

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
            print('Information about ERG LEPe')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: ",gatt["PI_AFFILIATION"])
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            if level == 'l2':
                print(
                    'RoR of LEPe L2: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Lepe')
            if level == 'l3':
                print(
                    'RoR of LEPe L3: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Lepe')
                print(
                    'RoR of MGF L2: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Mgf')
            print('')
            print('Contact: erg_lepe_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if (isinstance(loaded_data, dict)) and (len(loaded_data) > 0):
        if (level == 'l2') and (datatype == 'omniflux'):
            tplot_variables = []
            v_keyname = 'v'
            if v_keyname not in loaded_data[prefix + 'FEDO' + suffix]:
                v_keyname = 'v1'
            v_array = (loaded_data[prefix + 'FEDO' + suffix][v_keyname][:, 0, :] +
                       loaded_data[prefix + 'FEDO' + suffix][v_keyname][:, 1, :]) / 2.
            # change minus values to NaN
            v_array = np.where(v_array < 0., np.nan, v_array)
            all_nan_v_indices_array = np.where(
                np.all(np.isnan(v_array), axis=1))[0]
            store_data(prefix + 'FEDO' + suffix,
                       data={'x': np.delete(loaded_data[prefix + 'FEDO' + suffix]['x'], all_nan_v_indices_array, axis=0),
                             'y': np.delete(loaded_data[prefix + 'FEDO' + suffix]['y'], all_nan_v_indices_array, axis=0),
                             'v': np.delete(v_array, all_nan_v_indices_array, 0)},
                       attr_dict={'CDF':loaded_data[prefix + 'FEDO' + suffix]['CDF']})
            tplot_variables.append(prefix + 'FEDO' + suffix)

            # set spectrogram plot option
            options(prefix + 'FEDO' + suffix, 'Spec', 1)
            # change minus values to NaN in y array
            clip(prefix + 'FEDO' + suffix, 0.,
                 np.nanmax(loaded_data[prefix + 'FEDO' + suffix]['y']))

            # set y axis to logscale
            options(prefix + 'FEDO' + suffix, 'ylog', 1)

            # set ylim
            ylim(prefix + 'FEDO' + suffix, 19, 21*1e3)

            # set ytitle
            options(prefix + 'FEDO' + suffix, 'ytitle',
                    'ERG\nLEP-e\nFEDO\nEnergy')

            # set ysubtitle
            options(prefix + 'FEDO' + suffix, 'ysubtitle', '[eV]')

            # set z axis to logscale
            options(prefix + 'FEDO' + suffix, 'zlog', 1)

            # set zlim
            zlim(prefix + 'FEDO' + suffix,  1, 1e6)

            # set ztitle
            options(prefix + 'FEDO' + suffix, 'ztitle',  '[/cm^{2}-str-s-eV]')

            # change colormap option
            options(prefix + 'FEDO' + suffix, 'Colormap', 'jet')

            return tplot_variables

        if (level == 'l2') and (datatype == '3dflux'):
            tplot_variables = []
            other_variables_dict = {}
            if prefix + 'FEDU' + suffix in loaded_data:
                trange_double = np.array(time_double(trange))
                trange_dt64 = (trange_double*1.0e6).astype('datetime64[us]')
                time_array = np.array(loaded_data[prefix + 'FEDU' + suffix]['x'])
                inside_indices_array = np.argwhere( (trange_dt64[0] < time_array)
                             & (trange_dt64[1] > time_array))
                inside_indices_list = inside_indices_array[:, 0].tolist()
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'FEDU' + suffix]:
                    v_keyname = 'v1'
                store_data(prefix + 'FEDU' + suffix,
                           data={'x': time_array[inside_indices_list],
                                 'y': loaded_data[prefix + 'FEDU' + suffix]['y'][inside_indices_list],
                                 'v1': (loaded_data[prefix + 'FEDU' + suffix][v_keyname][inside_indices_list][:, 0, :]
                                        + loaded_data[prefix + 'FEDU' + suffix][v_keyname][inside_indices_list][:, 1, :]) / 2.,  # arithmetic mean
                                 'v2': ['01', '02', '03', '04', '05', 'A', 'B', '18', '19', '20', '21', '22'],
                                 'v3': [i for i in range(16)]},
                       attr_dict={'CDF':loaded_data[prefix + 'FEDU' + suffix]['CDF']})

                tplot_variables.append(prefix + 'FEDU' + suffix)

                options(prefix + 'FEDU' + suffix, 'spec', 1)
                ylim(prefix + 'FEDU' + suffix, 19, 21*1e3)
                zlim(prefix + 'FEDU' + suffix, 1, 1e6)
                options(prefix + 'FEDU' + suffix, 'zlog', 1)
                options(prefix + 'FEDU' + suffix, 'ylog', 1)
                options(prefix + 'FEDU' + suffix, 'ysubtitle', '[eV]')

            if prefix + 'Count_Rate' + suffix in loaded_data:
                other_variables_dict[prefix + 'Count_Rate' +
                                     suffix] = loaded_data[prefix + 'Count_Rate' + suffix]
            if prefix + 'Count_Rate_BG' + suffix in loaded_data:
                other_variables_dict[prefix + 'Count_Rate_BG' +
                                     suffix] = loaded_data[prefix + 'Count_Rate_BG' + suffix]

                tplot_variables.append(other_variables_dict)

                return tplot_variables

        if level == 'l3':
            tplot_variables = []

            if prefix + 'FEDU' + suffix in loaded_data:
                store_data(prefix + 'FEDU' + suffix,
                           data={'x': loaded_data[prefix + 'FEDU' + suffix]['x'],
                                 'y': loaded_data[prefix + 'FEDU' + suffix]['y'],
                                 'v1': (loaded_data[prefix + 'FEDU' + suffix]['v1'][:, 0, :]
                                        + loaded_data[prefix + 'FEDU' + suffix]['v1'][:, 1, :]) / 2.,  # arithmetic mean
                                 'v2': loaded_data[prefix + 'FEDU' + suffix]['v2']},
                       attr_dict={'CDF':loaded_data[prefix + 'FEDU' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU' + suffix)

                options(prefix + 'FEDU' + suffix, 'spec', 1)
                if prefix + 'FEDU' + suffix in tplot_variables:
                    clip(prefix + 'FEDU' + suffix, 0,
                         np.nanmax(loaded_data[prefix + 'FEDU' + suffix]['y']))
                ylim(prefix + 'FEDU' + suffix, 19, 21*1e3)
                zlim(prefix + 'FEDU' + suffix, 1, 1e6)
                options(prefix + 'FEDU' + suffix, 'zlog', 1)
                options(prefix + 'FEDU' + suffix, 'ylog', 1)
                options(prefix + 'FEDU' + suffix, 'ysubtitle', '[eV]')

                FEDU_get_data = get_data(prefix + 'FEDU' + suffix)
                FEDU_CDF_data = loaded_data[prefix + 'FEDU' + suffix]['CDF']

                if not only_fedu:

                    ytitle_eV_array = np.round(
                        np.nan_to_num(FEDU_get_data[2][0, :]), 2)
                    # processing for erg_lepe_l3_pa_enech_??(??:01,01,..32)_FEDU
                    for i in range(FEDU_get_data[1].shape[1]):
                        tplot_name = prefix + 'enech_' + \
                            str(i + 1).zfill(2) + '_FEDU' + suffix
                        store_data(tplot_name, data={'x': FEDU_get_data[0],
                                                     'y': FEDU_get_data[1][:, i, :],
                                                     'v': FEDU_get_data[3]},
                                    attr_dict={'CDF':FEDU_CDF_data})
                        options(tplot_name, 'spec', 1)
                        ylim(tplot_name, 0, 180)
                        zlim(tplot_name, 1, 1e6)
                        options(tplot_name, 'ytitle', 'ERG LEP-e\n' +
                                str(ytitle_eV_array[i]) + ' eV\nPitch angle')
                        tplot_variables.append(tplot_name)

                    options(tplot_variables[1:], 'zlog', 1)
                    options(tplot_variables[1:], 'ysubtitle', '[deg]')
                    options(tplot_variables[1:], 'yrange', [0, 180])
                    options(tplot_variables[1:], 'colormap', 'jet')
                    options(tplot_variables[1:],
                            'ztitle', '[/s-cm^{2}-sr-keV/q]')

                if et_diagram:
                    ytitle_deg_array = np.round(
                        np.nan_to_num(FEDU_get_data[3]), 3)
                    all_nan_v_indices_array = np.where(
                        np.all(np.isnan(FEDU_get_data[2]), axis=1))[0]
                    x_all_nan_deleted_array = np.delete(
                        FEDU_get_data[0], all_nan_v_indices_array, axis=0)
                    y_all_nan_deleted_array = np.delete(
                        FEDU_get_data[1], all_nan_v_indices_array, axis=0)
                    v_all_nan_deleted_array = np.delete(
                        FEDU_get_data[2], all_nan_v_indices_array, axis=0)
                    # processing for erg_lepe_l3_pa_pabin_??(??:01,01,..16)_FEDU
                    for i in range(FEDU_get_data[1].shape[2]):
                        tplot_name = prefix + 'pabin_' + \
                            str(i + 1).zfill(2) + '_FEDU' + suffix
                        store_data(tplot_name, data={'x': x_all_nan_deleted_array,
                                                     'y': y_all_nan_deleted_array[:, :, i],
                                                     'v': v_all_nan_deleted_array},
                                    attr_dict={'CDF':FEDU_CDF_data})
                        options(tplot_name, 'spec', 1)
                        ylim(tplot_name,  19, 21*1e3)
                        zlim(tplot_name, 1, 1e6)
                        options(tplot_name, 'ytitle', 'ERG LEP-e\n' +
                                str(ytitle_deg_array[i]) + ' deg\nEnergy')
                        tplot_variables.append(tplot_name)

                    options(
                        tplot_variables[-FEDU_get_data[1].shape[2]:], 'ysubtitle', '[eV]')
                    options(
                        tplot_variables[-FEDU_get_data[1].shape[2]:], 'zlog', 1)
                    options(
                        tplot_variables[-FEDU_get_data[1].shape[2]:], 'ylog', 1)
                    options(
                        tplot_variables[-FEDU_get_data[1].shape[2]:], 'colormap', 'jet')
                    options(
                        tplot_variables[-FEDU_get_data[1].shape[2]:], 'ztitle', '[/s-cm^{2}-sr-eV]')

                return tplot_variables

    return loaded_data

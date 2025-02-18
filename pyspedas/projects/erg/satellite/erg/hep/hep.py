import numpy as np
from pytplot import clip, options, store_data, ylim, zlim, get_data

from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def hep(
    trange: List[str] = ['2017-03-27', '2017-03-28'],
    datatype: str = 'omniflux',
    level: str = 'l2',
    suffix: str = '',
    get_support_data: bool = True,
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
    force_download: bool = False,
) -> List[str]:
    """
    This function loads data from the HEP experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-03-27', '2017-03-28']

        datatype: str
            Data type; Valid 'l2' options: 'omniflux', '3dflux'   Valid 'l3' options: 'pa'

        level: str
            Data level; Valid options: 'l2','l3'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  Default: ''

        get_support_data: bool
            If true, data with an attribute "VAR_TYPE" with a value of "support_data"
            or 'data' will be loaded into tplot. Default: True

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

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword. Default: False

        ror: bool
            If set, print PI info and rules of the road. Default: True

        version: str
            Set this value to specify the version of cdf files (such as "v01_02", "v01_03", ...)
            Default: None

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
    >>> hep_vars = pyspedas.projects.erg.hep(trange=['2017-03-27', '2017-03-28'])
    >>> tplot('erg_hep_l2_FEDO_L')


    """

    file_res = 3600. * 24
    prefix = 'erg_hep_'+level+'_'

    if level == 'l2':
        pathformat = 'satellite/erg/hep/'+level+'/'+datatype + \
            '/%Y/%m/erg_hep_'+level+'_'+datatype + '_%Y%m%d_'
        if version is None:
            pathformat += 'v??_??.cdf'
        else:
            pathformat += version + '.cdf'
    if level == 'l3':
        pathformat = 'satellite/erg/hep/'+level + \
            '/pa/%Y/%m/erg_hep_'+level+'_pa_%Y%m%d_'
        if version is None:
            pathformat += 'v??_??.cdf'
        else:
            pathformat += version + '.cdf'

    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    if ((level == 'l2') and (datatype == 'omniflux')) or (datatype == '3dflux') or (level == 'l3'):
        # to avoid failure of creation plot variables (at store_data.py) of hep
        notplot = True

    loaded_data = load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                       varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, version=version, force_download=force_download)

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
                '       https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                '- RoR for HEP data: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Hep')
            if level == 'l3':
                print(
                    '- RoR for MGF data: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Mgf')
            print('')
            print('Contact: erg_hep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if isinstance(loaded_data, dict):

        if (level == 'l2') and (datatype == 'omniflux'):
            tplot_variables = []
            if prefix + 'FEDO_L' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'FEDO_L' + suffix]:
                    v_keyname = 'v1'

                v_vars_min = loaded_data[prefix + 'FEDO_L' + suffix][v_keyname][0]
                v_vars_max = loaded_data[prefix + 'FEDO_L' + suffix][v_keyname][1]
                # log average of energy bins
                v_vars = np.power(
                    10., (np.log10(v_vars_min) + np.log10(v_vars_max)) / 2.)
                store_data(prefix + 'FEDO_L' + suffix, data={'x': loaded_data[prefix + 'FEDO_L' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDO_L' + suffix]['y'],
                                                             'v': v_vars},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDO_L' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDO_L' + suffix)

            if prefix + 'FEDO_H' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'FEDO_H' + suffix]:
                    v_keyname = 'v1'

                v_vars_min = loaded_data[prefix + 'FEDO_H' + suffix][v_keyname][0]
                v_vars_max = loaded_data[prefix + 'FEDO_H' + suffix][v_keyname][1]
                # log average of energy bins
                v_vars = np.power(
                    10., (np.log10(v_vars_min) + np.log10(v_vars_max)) / 2.)
                store_data(prefix + 'FEDO_H' + suffix, data={'x': loaded_data[prefix + 'FEDO_H' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDO_H' + suffix]['y'],
                                                             'v': v_vars},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDO_H' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDO_H' + suffix)

            # remove minus valuse of y array
            if prefix + 'FEDO_L' + suffix in tplot_variables:
                clip(prefix + 'FEDO_L' + suffix, 0., 1.0e+10)
            if prefix + 'FEDO_H' + suffix in tplot_variables:
                clip(prefix + 'FEDO_H' + suffix, 0., 1.0e+10)

            # set spectrogram plot option
            options(prefix + 'FEDO_L' + suffix, 'Spec', 1)
            options(prefix + 'FEDO_H' + suffix, 'Spec', 1)

            # set y axis to logscale
            options(prefix + 'FEDO_L' + suffix, 'ylog', 1)
            options(prefix + 'FEDO_H' + suffix, 'ylog', 1)

            # set yrange
            options(prefix + 'FEDO_L' + suffix, 'yrange', [3.0e+01, 2.0e+03])
            options(prefix + 'FEDO_H' + suffix, 'yrange', [7.0e+01, 2.0e+03])

            # set ytitle
            options(prefix + 'FEDO_L' + suffix, 'ytitle',
                    'HEP-L\nomniflux\nLv2\nEnergy')
            options(prefix + 'FEDO_H' + suffix, 'ytitle',
                    'HEP-H\nomniflux\nLv2\nEnergy')

            # set ysubtitle
            options(prefix + 'FEDO_L' + suffix, 'ysubtitle', '[keV]')
            options(prefix + 'FEDO_H' + suffix, 'ysubtitle', '[keV]')

            # set ylim
            if prefix + 'FEDO_L' + suffix in tplot_variables:
                ylim(prefix + 'FEDO_L' + suffix, 30, 1800)
            if prefix + 'FEDO_H' + suffix in tplot_variables:
                ylim(prefix + 'FEDO_H' + suffix, 500, 2048)

            # set z axis to logscale
            options(prefix + 'FEDO_L' + suffix, 'zlog', 1)
            options(prefix + 'FEDO_H' + suffix, 'zlog', 1)

            # set zrange
            options(prefix + 'FEDO_L' + suffix, 'zrange', [1.0e-15, 1.0e+06])
            options(prefix + 'FEDO_H' + suffix, 'zrange', [1.0e-10, 1.0e+5])

            # set ztitle
            options(prefix + 'FEDO_L' + suffix,
                    'ztitle', '[/cm^{2}-str-s-keV]')
            options(prefix + 'FEDO_H' + suffix,
                    'ztitle', '[/cm^{2}-str-s-keV]')

            # set zlim
            if prefix + 'FEDO_L' + suffix in tplot_variables:
                zlim(prefix + 'FEDO_L' + suffix, 1e+0, 1e+5)
            if prefix + 'FEDO_H' + suffix in tplot_variables:
                zlim(prefix + 'FEDO_H' + suffix, 1e+0, 1e+5)

            # change colormap option
            options(prefix + 'FEDO_L' + suffix,  'Colormap', 'jet')
            options(prefix + 'FEDO_H' + suffix,  'Colormap', 'jet')

            return tplot_variables

        if (level == 'l2') and (datatype == '3dflux'):
            tplot_variables = []
            v2_array = [i for i in range(15)]

            if prefix + 'FEDU_L' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'FEDU_L' + suffix]:
                    v_keyname = 'v1'
                store_data(prefix + 'FEDU_L' + suffix, data={'x': loaded_data[prefix + 'FEDU_L' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDU_L' + suffix]['y'],
                                                             'v1': np.sqrt(loaded_data[prefix + 'FEDU_L' + suffix][v_keyname][0, :] *
                                                                           loaded_data[prefix + 'FEDU_L' + suffix][v_keyname][1, :]),  # geometric mean for 'v1'
                                                             'v2': v2_array},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_L' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU_L' + suffix)
                clip(prefix + 'FEDU_L' + suffix, -1.0e+10, 1.0e+10)

            if prefix + 'FEDU_H' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'FEDU_H' + suffix]:
                    v_keyname = 'v1'


                store_data(prefix + 'FEDU_H' + suffix, data={'x': loaded_data[prefix + 'FEDU_H' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDU_H' + suffix]['y'],
                                                             'v1': np.sqrt(loaded_data[prefix + 'FEDU_H' + suffix][v_keyname][0, :] *
                                                                           loaded_data[prefix + 'FEDU_H' + suffix][v_keyname][1, :]),  # geometric mean for 'v1'
                                                             'v2': v2_array},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_H' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU_H' + suffix)
                clip(prefix + 'FEDU_H' + suffix, -1.0e+10, 1.0e+10)

            if prefix + 'FEDU_L_Angle_sga' + suffix in loaded_data:
                
                store_data(prefix + 'FEDU_L_Angle_sga' + suffix, data={'x': loaded_data[prefix + 'FEDU_L_Angle_sga' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDU_L_Angle_sga' + suffix]['y']},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_L_Angle_sga' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU_L_Angle_sga' + suffix)

            if prefix + 'FEDU_H_Angle_sga' + suffix in loaded_data:
                
                store_data(prefix + 'FEDU_H_Angle_sga' + suffix, data={'x': loaded_data[prefix + 'FEDU_H_Angle_sga' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDU_H_Angle_sga' + suffix]['y']},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_H_Angle_sga' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU_H_Angle_sga' + suffix)

            if prefix + 'FEDU_L_Angle_gse' + suffix in loaded_data:
                
                store_data(prefix + 'FEDU_L_Angle_gse' + suffix, data={'x': loaded_data[prefix + 'FEDU_L_Angle_gse' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDU_L_Angle_gse' + suffix]['y']},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_L_Angle_gse' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU_L_Angle_gse' + suffix)

            if prefix + 'FEDU_H_Angle_gse' + suffix in loaded_data:
                
                store_data(prefix + 'FEDU_H_Angle_gse' + suffix, data={'x': loaded_data[prefix + 'FEDU_H_Angle_gse' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'FEDU_H_Angle_gse' + suffix]['y']},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_H_Angle_gse' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDU_H_Angle_gse' + suffix)

            if prefix + 'sctno_L' + suffix in loaded_data:
                
                store_data(prefix + 'sctno_L' + suffix, data={'x': loaded_data[prefix + 'sctno_L' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'sctno_L' + suffix]['y']},
                           attr_dict={'CDF':loaded_data[prefix + 'sctno_L' + suffix]['CDF']})
                tplot_variables.append(prefix + 'sctno_L' + suffix)

            if prefix + 'sctno_H' + suffix in loaded_data:
                
                store_data(prefix + 'sctno_H' + suffix, data={'x': loaded_data[prefix + 'sctno_H' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'sctno_H' + suffix]['y']},
                           attr_dict={'CDF':loaded_data[prefix + 'sctno_H' + suffix]['CDF']})
                tplot_variables.append(prefix + 'sctno_H' + suffix)

            if prefix + 'rawcnt_H' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'rawcnt_H' + suffix]:
                    v_keyname = 'v1'

    
                store_data(prefix + 'rawcnt_H' + suffix, data={'x': loaded_data[prefix + 'rawcnt_H' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'rawcnt_H' + suffix]['y'],
                                                             'v1': np.sqrt(loaded_data[prefix + 'rawcnt_H' + suffix][v_keyname][0, :] *
                                                                           loaded_data[prefix + 'rawcnt_H' + suffix][v_keyname][1, :]),  # geometric mean for 'v1'
                                                             'v2': [i for i in range(15)]},
                           attr_dict={'CDF':loaded_data[prefix + 'rawcnt_H' + suffix]['CDF']})
                tplot_variables.append(prefix + 'rawcnt_H' + suffix)

            if prefix + 'rawcnt_L' + suffix in loaded_data:
                v_keyname = 'v'
                if v_keyname not in loaded_data[prefix + 'rawcnt_L' + suffix]:
                    v_keyname = 'v1'

                store_data(prefix + 'rawcnt_L' + suffix, data={'x': loaded_data[prefix + 'rawcnt_L' + suffix]['x'],
                                                             'y': loaded_data[prefix + 'rawcnt_L' + suffix]['y'],
                                                             'v1': np.sqrt(loaded_data[prefix + 'rawcnt_L' + suffix][v_keyname][0, :] *
                                                                           loaded_data[prefix + 'rawcnt_L' + suffix][v_keyname][1, :]),  # geometric mean for 'v1'
                                                             'v2': [i for i in range(15)]},
                           attr_dict={'CDF':loaded_data[prefix + 'rawcnt_L' + suffix]['CDF']})
                tplot_variables.append(prefix + 'rawcnt_L' + suffix)

            return tplot_variables

        if level == 'l3':  # implementation for level = 'l3'

            tplot_variables = []

            if prefix + 'FEDU_L' + suffix in loaded_data:

                L_energy_array_ave = np.sqrt(loaded_data[prefix + 'FEDU_L' + suffix]['v1'][0, :] *
                                             loaded_data[prefix + 'FEDU_L' + suffix]['v1'][1, :])  # geometric mean for 'v1'

                # get energy [keV] array for ytitle options
                L_energy_array = np.trunc(L_energy_array_ave).astype(int)
                non_negative_y_array = np.where(
                    loaded_data[prefix + 'FEDU_L' + suffix]['y'] < 0., np.nan, loaded_data[prefix + 'FEDU_L' + suffix]['y'])
                store_data(prefix + 'FEDU_L' + suffix, data={'x': loaded_data[prefix + 'FEDU_L' + suffix]['x'],
                                                             'y': non_negative_y_array,
                                                             'v1': L_energy_array_ave,
                                                             'v2': loaded_data[prefix + 'FEDU_L' + suffix]['v2']},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_L' + suffix]['CDF']})

                options(prefix + 'FEDU_L' + suffix, 'spec', 1)
                # set ylim
                ylim(prefix + 'FEDU_L' + suffix, 0, 180)
                # set zlim
                zlim(prefix + 'FEDU_L' + suffix, 1e+2, 1e+6)

                tplot_variables.append(prefix + 'FEDU_L' + suffix)

                # make Tplot Variables of erg_hep_l3_FEDU_L_paspec_ene?? (??: 00, 01, 02, ..., 15)
                for i in range(loaded_data[prefix + 'FEDU_L' + suffix]['y'].shape[1]):
                    tplot_name = prefix + 'FEDU_L_paspec_ene' + \
                        str(i).zfill(2) + suffix
                    store_data(tplot_name, data={'x': loaded_data[prefix + 'FEDU_L' + suffix]['x'],
                                                 'y': non_negative_y_array[:, i, :],
                                                 'v': loaded_data[prefix + 'FEDU_L' + suffix]['v2']},
                               attr_dict={'CDF':loaded_data[prefix + 'FEDU_L' + suffix]['CDF']})

                    options(tplot_name, 'spec', 1)
                    # set ylim
                    ylim(tplot_name, 0, 180)
                    # set zlim
                    zlim(tplot_name, 1e+2, 1e+6)
                    # set ytitle
                    options(
                        tplot_name, 'ytitle', f'HEP-L\nEne{str(i).zfill(2)}\n{L_energy_array[i]} keV')

                    tplot_variables.append(tplot_name)

            if prefix + 'FEDU_H' + suffix in loaded_data:

                H_energy_array_ave = np.sqrt(loaded_data[prefix + 'FEDU_H' + suffix]['v1'][0, :] *
                                             loaded_data[prefix + 'FEDU_H' + suffix]['v1'][1, :])  # geometric mean for 'v1'

                # get energy [keV] array for ytitle options
                H_energy_array = np.trunc(H_energy_array_ave).astype(int)
                non_negative_y_array = np.where(
                    loaded_data[prefix + 'FEDU_H' + suffix]['y'] < 0., np.nan, loaded_data[prefix + 'FEDU_H' + suffix]['y'])
                store_data(prefix + 'FEDU_H' + suffix, data={'x': loaded_data[prefix + 'FEDU_H' + suffix]['x'],
                                                             'y': non_negative_y_array,
                                                             'v1': H_energy_array_ave,
                                                             'v2': loaded_data[prefix + 'FEDU_H' + suffix]['v2']},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_H' + suffix]['CDF']})

                options(prefix + 'FEDU_H' + suffix, 'spec', 1)
                # set ylim
                ylim(prefix + 'FEDU_H' + suffix, 0, 180)
                # set zlim
                zlim(prefix + 'FEDU_H' + suffix, 1e+1, 1e+4)

                tplot_variables.append(prefix + 'FEDU_H' + suffix)

                # make Tplot Variables of erg_hep_l3_FEDU_H_paspec_ene?? (??: 00, 01, 02, ..., 10)
                for i in range(loaded_data[prefix + 'FEDU_H' + suffix]['y'].shape[1]):
                    tplot_name = prefix + 'FEDU_H_paspec_ene' + \
                        str(i).zfill(2) + suffix
                    store_data(tplot_name, data={'x': loaded_data[prefix + 'FEDU_H' + suffix]['x'],
                                                 'y': non_negative_y_array[:, i, :],
                                                 'v': loaded_data[prefix + 'FEDU_H' + suffix]['v2']},
                               attr_dict={'CDF':loaded_data[prefix + 'FEDU_H' + suffix]['CDF']})

                    options(tplot_name, 'spec', 1)
                    # set ylim
                    ylim(tplot_name, 0, 180)
                    # set zlim
                    zlim(tplot_name, 1e+1, 1e+4)
                    # set ytitle
                    options(
                        tplot_name, 'ytitle', f'HEP-H\nEne{str(i).zfill(2)}\n{H_energy_array[i]} keV')

                    tplot_variables.append(tplot_name)

            # set z axis to logscale
            options(tplot_variables, 'zlog', 1)
            # change colormap option
            options(tplot_variables, 'colormap', 'jet')
            # set ysubtitle
            options(tplot_variables, 'ysubtitle', 'PA [deg]')
            # set ztitle
            options(tplot_variables, 'ztitle', '[/keV/cm^{2}/sr/s]')

            return tplot_variables

    return loaded_data



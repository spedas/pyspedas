
import numpy as np
from pytplot import clip, get_data, options, store_data, ylim, zlim
from pyspedas import tcopy

from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def lepi(
    trange: List[str] = ['2017-07-01', '2017-07-02'],
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
    force_download: bool = False,
) -> List[str]:
    """
    This function loads data from the LEP-i experiment from the Arase mission

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2017-07-01', '2017-07-02']

        datatype: str
            Data type; Valid 'l2' options: '3dflux', 'omniflux'  Valid 'l3' options: 'pa'
            Default: 'omniflux'

        level: str
            Data level; Valid options: 'l2','l3'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool
            If Trye, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded. Default: [] (all data loaded)

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
            Default: False

        version: str
            Set this value to specify the version of cdf files (such as "v03_00")
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
    >>> lepi_vars = pyspedas.projects.erg.lepi(trange=['2017-04-09', '2017-04-10'])
    >>> tplot('erg_lepi_l2_omniflux_FODO')

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    if level == 'l3':
        datatype = 'pa'

    file_res = 3600. * 24
    prefix = 'erg_lepi_'+level+'_' + datatype + '_'

    pathformat = 'satellite/erg/lepi/'+level+'/'+datatype + \
        '/%Y/%m/erg_lepi_'+level+'_'+datatype+'_%Y%m%d_'
    if version is None:
        pathformat += 'v??_??.cdf'
    else:
        pathformat += version + '.cdf'

    loaded_data = load(pathformat=pathformat, trange=trange, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                       varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, force_download=force_download)

    flag_FPDO = False # In case it doesn't get set later

    if (len(loaded_data) > 0) and ror:
        try:
            gatt = get_gatt_ror(downloadonly, loaded_data)

            # --- print PI info and rules of the road

            print(' ')
            print(
                '**************************************************************************')
            print(gatt["LOGICAL_SOURCE_DESCRIPTION"])
            print('')
            print('Information about ERG LEPi')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: ", gatt["PI_AFFILIATION"])
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                'RoR of LEPi L2: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Lepi')
            print(
                'RoR of ERG/LEPi: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Lepi#Rules_of_the_Road')
            print('')
            print('Contact: erg_lepi_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if (datatype == 'omniflux') and (level == 'l2'):
        tplot_variables = []

        if prefix + 'FPDO' + suffix in loaded_data:
            store_data(prefix + 'FPDO' + suffix,
                       newname=prefix + 'FPDO_raw' + suffix)
            loaded_data.append(prefix + 'FPDO_raw' + suffix)
            get_data_vars = get_data(prefix + 'FPDO_raw' + suffix)
            flag_FPDO = store_data(prefix + 'FPDO' + suffix, data={'x': get_data_vars[0],
                                                                   'y': get_data_vars[1][:, :-2],
                                                                   'v': get_data_vars[2][:-2]})
            tplot_variables.append(prefix + 'FPDO' + suffix)

        if prefix + 'FHEDO' + suffix in loaded_data:
            store_data(prefix + 'FHEDO' + suffix,
                       newname=prefix + 'FHEDO_raw' + suffix)
            loaded_data.append(prefix + 'FHEDO_raw' + suffix)
            get_data_vars = get_data(prefix + 'FHEDO_raw' + suffix)
            store_data(prefix + 'FHEDO' + suffix, data={'x': get_data_vars[0],
                                                        'y': get_data_vars[1][:, :-2],
                                                        'v': get_data_vars[2][:-2]})
            tplot_variables.append(prefix + 'FHEDO' + suffix)

        if prefix + 'FODO' + suffix in loaded_data:
            store_data(prefix + 'FODO' + suffix,
                       newname=prefix + 'FODO_raw' + suffix)
            loaded_data.append(prefix + 'FODO_raw' + suffix)
            get_data_vars = get_data(prefix + 'FODO_raw' + suffix)
            store_data(prefix + 'FODO' + suffix, data={'x': get_data_vars[0],
                                                       'y': get_data_vars[1][:, :-2],
                                                       'v': get_data_vars[2][:-2]})
            tplot_variables.append(prefix + 'FODO' + suffix)

        # remove minus valuse of y array
        if flag_FPDO:
            clip(prefix + 'FPDO' + suffix, 0., 2.e+16)

        # set ytitle
        options(tplot_variables, 'ytitle', 'LEPi\nomniflux\nLv2\nEnergy')

        # set ysubtitle
        options(tplot_variables, 'ysubtitle', '[keV/q]')

        # set spectrogram plot option
        options(tplot_variables, 'Spec', 1)

        # set y axis to logscale
        options(tplot_variables, 'ylog', 1)

        for i in range(len(tplot_variables)):
            # set ylim
            ylim(tplot_variables[i], 0.01, 25.0)
            # set zlim
            zlim(tplot_variables[i], 1e+1, 1e+9)

        # set ztitle
        options(tplot_variables, 'ztitle', '[/cm^2-str-s-keV]')

        # set z axis to logscale
        options(tplot_variables, 'zlog', 1)

        # change colormap option
        options(tplot_variables, 'Colormap', 'jet')

    elif (datatype == '3dflux') and (level == 'l2') and (not notplot):
        vns_fidu = [ 'FPDU',  'FPDU_sub', 'FHEDU', 'FHEDU_sub', 'FODU', 'FODU_sub'] 
        vns_fiedu = [ 'FPEDU', 'FPEDU_sub', 'FHEEDU', 'FHEEDU_sub', 'FOEDU', 'FOEDU_sub']
        vns_cnt = ['FPDU_COUNT_RAW','FPDU_COUNT_RAW_sub', 'FHEDU_COUNT_RAW','FHEDU_COUNT_RAW_sub', 'FODU_COUNT_RAW', 'FODU_COUNT_RAW_sub']
        vns_list = vns_fidu + vns_fiedu + vns_cnt

        v2_array_for_not_sub = np.arange(8)
        v2_array_for_sub = np.arange(7) + 8
        v3_array = np.arange(16)
        
        for vns_pattarn in vns_list:
            t_plot_name = prefix + vns_pattarn + suffix
            if t_plot_name in loaded_data:
                tcopy(t_plot_name, t_plot_name + '_raw')
                get_data_vars_temporal = get_data(t_plot_name)
                meta_data_in = get_data(t_plot_name, metadata=True)
                if 'sub' in t_plot_name:
                    store_data(t_plot_name,data={'x':get_data_vars_temporal[0],
                                                'y':get_data_vars_temporal[1][:,0:30,:,:],
                                                'v1':get_data_vars_temporal[2][0:30],
                                                'v2':v2_array_for_sub,
                                                'v3':v3_array},
                            attr_dict=meta_data_in)
                else:
                    store_data(t_plot_name,data={'x':get_data_vars_temporal[0],
                                                'y':get_data_vars_temporal[1][:,0:30,:,:],
                                                'v1':get_data_vars_temporal[2][0:30],
                                                'v2':v2_array_for_not_sub,
                                                'v3':v3_array},
                            attr_dict=meta_data_in)
                ylim(t_plot_name,  0.01, 30.)
                options(t_plot_name, 'ylog', 1)
                options(t_plot_name, 'zlog', 1)
        
        """comment out in order to match the result of part_product of IDL.
        if prefix + 'FPDU' + suffix in loaded_data:
            clip(prefix + 'FPDU' + suffix, -1.0e+10, 1.0e+10)
        if prefix + 'FHEDU' + suffix in loaded_data:
            clip(prefix + 'FHEDU' + suffix, -1.0e+10, 1.0e+10)
        if prefix + 'FODU' + suffix in loaded_data:
            clip(prefix + 'FODU' + suffix, -1.0e+10, 1.0e+10)"""

    elif level == 'l3':
        tplot_variables = []

        if prefix + 'FPDU' + suffix in loaded_data:
            tplot_variables.append(prefix + 'FPDU' + suffix)
            get_data_vars = get_data(prefix + 'FPDU' + suffix)
            ylim(prefix + 'FPDU' + suffix, 0, 180)
            zlim(prefix + 'FPDU' + suffix, 1e2, 1e5)
            options(prefix + 'FPDU' + suffix, 'spec', 1)
            ytitle_keV_array = np.round(np.nan_to_num(get_data_vars[2]), 2)
            for i in range(get_data_vars[1].shape[1]):
                tplot_name = prefix + 'pabin_' + \
                    str(i).zfill(2) + '_FPDU' + suffix
                store_data(tplot_name, data={'x': get_data_vars[0],
                                             'y': get_data_vars[1][:, i, :],
                                             'v': get_data_vars[3]})
                options(tplot_name, 'spec', 1)
                ylim(tplot_name, 0, 180)
                zlim(tplot_name, 1e2, 1e5)
                options(tplot_name, 'ytitle', 'ERG LEP-i P\n' +
                        str(ytitle_keV_array[i]) + ' keV\nPitch angle')
                tplot_variables.append(tplot_name)

            loaded_data += tplot_variables[1:]

        tplot_variables_length = len(tplot_variables)

        if prefix + 'FHEDU' + suffix in loaded_data:
            tplot_variables.append(prefix + 'FHEDU' + suffix)
            get_data_vars = get_data(prefix + 'FHEDU' + suffix)
            options(prefix + 'FHEDU' + suffix, 'spec', 1)
            ylim(prefix + 'FHEDU' + suffix, 0, 180)
            zlim(prefix + 'FHEDU' + suffix, 1e2, 1e5)
            ytitle_keV_array = np.round(np.nan_to_num(get_data_vars[2]), 2)
            for i in range(get_data_vars[1].shape[1]):
                tplot_name = prefix + 'pabin_' + \
                    str(i).zfill(2) + '_FHEDU' + suffix
                store_data(tplot_name, data={'x': get_data_vars[0],
                                             'y': get_data_vars[1][:, i, :],
                                             'v': get_data_vars[3]})
                options(tplot_name, 'spec', 1)
                ylim(tplot_name, 0, 180)
                zlim(tplot_name, 1e2, 1e5)
                options(tplot_name, 'ytitle', 'ERG LEP-i P\n' +
                        str(ytitle_keV_array[i]) + ' keV\nPitch angle')
                tplot_variables.append(tplot_name)

            loaded_data += tplot_variables[tplot_variables_length + 1:]

        tplot_variables_length = len(tplot_variables)

        if prefix + 'FODU' + suffix in loaded_data:
            tplot_variables.append(prefix + 'FODU' + suffix)
            get_data_vars = get_data(prefix + 'FODU' + suffix)
            options(prefix + 'FODU' + suffix, 'spec', 1)
            ylim(prefix + 'FODU' + suffix, 0, 180)
            zlim(prefix + 'FODU' + suffix, 1e2, 1e5)
            ytitle_keV_array = np.round(np.nan_to_num(get_data_vars[2]), 2)
            for i in range(get_data_vars[1].shape[1]):
                tplot_name = prefix + 'pabin_' + \
                    str(i).zfill(2) + '_FODU' + suffix
                store_data(tplot_name, data={'x': get_data_vars[0],
                                             'y': get_data_vars[1][:, i, :],
                                             'v': get_data_vars[3]})
                options(tplot_name, 'spec', 1)
                ylim(tplot_name, 0, 180)
                zlim(tplot_name, 1e2, 1e5)
                options(tplot_name, 'ytitle', 'ERG LEP-i P\n' +
                        str(ytitle_keV_array[i]) + ' keV\nPitch angle')
                tplot_variables.append(tplot_name)

            loaded_data += tplot_variables[tplot_variables_length + 1:]

        options(tplot_variables, 'zlog', 1)
        options(tplot_variables, 'ysubtitle', 'PA [deg]')
        options(tplot_variables, 'colormap', 'jet')
        options(tplot_variables, 'ztitle', '[/s-cm^{2}-sr-keV/q]')

    return loaded_data

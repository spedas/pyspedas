import numpy as np
from pytplot import tnames
from pytplot import time_float
from pytplot import clip, get_data, options, store_data, ylim, zlim

from ..load import load
from ..get_gatt_ror import get_gatt_ror


from typing import List, Optional

def pwe_wfc(
    trange: List[str] = ['2017-04-01/12:00:00', '2017-04-01/13:00:00'],
    datatype: str = 'waveform',
    mode: str = '65khz',
    level: str = 'l2',
    suffix: str = '',
    coord: str = 'sgi',
    component: str = 'all',
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
            Default: ['2017-04-01/12:00:00','2017-04-01/13:00:00']

        datatype: str
            Data type; Valid 'l2' options: 'waveform', 'spec'
            Default: 'waveform'

        level: str
            Data level; Valid options: 'l2'
            Default: 'l2'

        coord: str
            Coordinate system to load. Valid options: 'dsi', 'sgi'
            Default: 'sgi'

        mode: str
            Mode of data to load. Valid options: '65khz', 'wp65khz'
            Default: '65khz'

        component: str
            Data components to load.  Valid options: 'all', 'e', 'b'
            Default: 'all'

        suffix: str
            The tplot variable names will be given this suffix. Default: None

        get_support_data: bool
            If Trye, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  Default: False

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  Default: None (all variables loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded. Default: [] (all variables loaded)

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
    >>> pwe_wfc_vars = pyspedas.projects.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'])
    >>> tplot('erg_pwe_wfc_l2_e_65khz_Ex_waveform')

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600.

    if level == 'l2':
        prefix = 'erg_pwe_wfc_'+level+'_' + mode + '_'

    loaded_data = []
    if level == 'l2':
        if datatype == 'waveform':
            tplot_name_list = []
            if component == 'all':
                component_list = ['e', 'b']
            elif (component == 'e') or (component == 'b'):
                component_list = [component]
            for com in component_list:
                prefix = 'erg_pwe_wfc_' + level + '_' + com + '_' + mode + '_'
                pathformat = 'satellite/erg/pwe/wfc/'+level+'/'+datatype+'/%Y/%m/erg_pwe_wfc_' + \
                    level+'_'+com+'_'+datatype+'_'+mode+'_'+coord+'_%Y%m%d%H_v??_??.cdf'
                loaded_data.extend(load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                                   varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, force_download=force_download))
                if com == 'e':
                    tplot_name_list += [prefix +
                                        'Ex_waveform', prefix + 'Ey_waveform']
                elif com == 'b':
                    tplot_name_list += [prefix + 'Bx_waveform',
                                        prefix + 'By_waveform', prefix + 'Bz_waveform']
        elif datatype == 'spec':
            prefix_list = []
            component_suffix_list = []
            if component == 'all':
                component_list = ['e', 'b']
            elif (component == 'e') or (component == 'b'):
                component_list = [component]
            for com in component_list:
                prefix = 'erg_pwe_wfc_' + level + '_' + com + '_' + mode + '_'
                pathformat = 'satellite/erg/pwe/wfc/'+level+'/'+datatype+'/%Y/%m/erg_pwe_wfc_' + \
                    level+'_'+com+'_'+datatype+'_'+mode+'_%Y%m%d%H_v??_??.cdf'
                loaded_data.extend(load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                                   varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, force_download=force_download))
                prefix_list.append(prefix)
                component_suffix_list.append(com.upper() + '_spectra')

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
            print('Information about ERG PWE WFC')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: "+str(gatt["PI_AFFILIATION"]))
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                'RoR of PWE/WFC: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Pwe/Wfc')
            print('')
            print('Contact: erg_pwe_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if datatype == 'spec':
        trange_in_float = time_float(trange)
        for i in range(len(prefix_list)):
            t_plot_name = prefix_list[i] + component_suffix_list[i]
            options(t_plot_name, 'spec', 1)
            options(t_plot_name, 'colormap', 'jet')
            options(t_plot_name, 'ylog', 1)
            options(t_plot_name, 'zlog', 1)
            options(t_plot_name, 'ysubtitle', '[Hz]')
            ylim(t_plot_name, 32., 2e4)
            if 'E_spectra' in component_suffix_list[i]:
                zlim(t_plot_name, 1e-9, 1e-2)
                options(t_plot_name, 'ztitle', '[mV^2/m^2/Hz]')
                options(t_plot_name, 'ytitle', 'E\nspectra')
            elif 'B_spectra' in component_suffix_list[i]:
                zlim(t_plot_name, 1e-4, 1e2)
                options(t_plot_name, 'ztitle', '[pT^2/Hz]')
                options(t_plot_name, 'ytitle', 'B\nspectra')

            get_data_vars = get_data(t_plot_name)
            time_array = get_data_vars[0]
            if time_array[0] <= trange_in_float[0]:
                t_ge_indices = np.where(time_array <= trange_in_float[0])
                t_min_index = t_ge_indices[0][-1]
            else:
                t_min_index = 0
            if trange_in_float[1] <= time_array[-1]:
                t_le_indices = np.where(trange_in_float[1] <= time_array)
                t_max_index = t_le_indices[0][0]
            else:
                t_max_index = -1
            if t_min_index == t_max_index:
                t_max_index = + 1
            if (t_min_index != 0) or (t_max_index != -1):
                meta_data = get_data(t_plot_name, metadata=True)
                store_data(t_plot_name, newname=t_plot_name +
                           '_all_loaded_time_range')
                store_data(t_plot_name, data={'x': time_array[t_min_index:t_max_index],
                                              'y': get_data_vars[1][t_min_index:t_max_index],
                                              'v': get_data_vars[2]},
                           attr_dict=meta_data)
                options(t_plot_name, 'zlog', 1)
                if 'E_spectra' in t_plot_name:
                    zlim(t_plot_name,  1e-9, 1e-2)
                elif 'B_spectra' in t_plot_name:
                    zlim(t_plot_name,  1e-4, 1e2)

    if datatype == 'waveform':
        trange_in_float = time_float(trange)
        yn = ''
        all_time_range_flag = False
        if trange_in_float[1] - trange_in_float[0] <= 0.:
            yn = input('Invalid time range. Use full time range ?:[y/n] ')
            if yn == 'y':
                all_time_range_flag = True
                t_min_index = 0
                t_max_index = -1
            else:
                return
        for t_plot_name in tplot_name_list:
            get_data_vars = get_data(t_plot_name)
            dl_in = get_data(t_plot_name, metadata=True)
            time_array = get_data_vars[0]
            if not all_time_range_flag:
                if time_array[0] <= trange_in_float[0]:
                    t_ge_indices = np.where(time_array <= trange_in_float[0])
                    t_min_index = t_ge_indices[0][-1]
                else:
                    t_min_index = 0
                if trange_in_float[1] <= time_array[-1]:
                    t_le_indices = np.where(trange_in_float[1] <= time_array)
                    t_max_index = t_le_indices[0][0]
                else:
                    t_max_index = -1
                if t_min_index == t_max_index:
                    t_max_index = + 1
            data = np.where(get_data_vars[1] <= -1e+30, np.nan, get_data_vars[1])
            dt = get_data_vars[2]
            ndt = dt.size
            ndata = (t_max_index - t_min_index) * ndt
            time_new = (np.tile(
                time_array[t_min_index:t_max_index], (ndt, 1)).T + dt * 1e-3).reshape(ndata)
            data_new = data[t_min_index:t_max_index].reshape(ndata)
            store_data(t_plot_name, data={
                       'x': time_new, 'y': data_new}, attr_dict=dl_in)
            options(t_plot_name, 'ytitle', '\n'.join(t_plot_name.split('_')))
            # ylim settings because pytplot.timespan() doesn't affect in ylim.
            # May be it will be no need in future.
            if not all_time_range_flag:
                if time_new[0] <= trange_in_float[0]:
                    t_min_index = np.where(
                        (time_new <= trange_in_float[0]))[0][-1]
                else:
                    t_min_index = 0
                if trange_in_float[1] <= time_new[-1]:
                    t_max_index = np.where(
                        trange_in_float[1] <= time_new)[0][0]
                else:
                    t_max_index = -1
            ylim_min = np.nanmin(data_new[t_min_index:t_max_index])
            ylim_max = np.nanmax(data_new[t_min_index:t_max_index])
            ylim(t_plot_name, ylim_min, ylim_max)

    return loaded_data

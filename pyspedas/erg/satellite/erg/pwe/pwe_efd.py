import cdflib
import numpy as np
from pyspedas import tnames
from pyspedas.utilities.time_double import time_float
from pytplot import get_data, options, store_data, ylim, zlim

from ..load import load


def pwe_efd(trange=['2017-04-01', '2017-04-02'],
            datatype='E_spin',
            level='l2',
            suffix='',
            coord='dsi',
            get_support_data=False,
            varformat=None,
            varnames=[],
            downloadonly=False,
            notplot=False,
            no_update=False,
            uname=None,
            passwd=None,
            time_clip=False,
            ror=True):
    """
    This function loads data from the PWE experiment from the Arase mission

    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        level: str
            Data level; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

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

        ror: bool
            If set, print PI info and rules of the road

    Returns:
        List of tplot variables created.

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True
    file_res = 3600. * 24
    prefix = 'erg_pwe_efd_'+level+'_'

    if ('64' in datatype) or ('256' in datatype):
        if '64' in datatype:
            mode = '64Hz'
        elif '256' in datatype:
            mode = '256Hz'
        md = 'E'+mode
        pathformat = 'satellite/erg/pwe/efd/'+level+'/'+md + \
            '/%Y/%m/erg_pwe_efd_'+level+'_'+md+'_'+coord+'_%Y%m%d_v??_??.cdf'
        prefix += md + '_' + coord + '_'
        if coord == 'wpt':
            component = ['Eu_waveform', 'Ev_waveform']
        elif coord == 'dsi':
            component = ['Ex_waveform', 'Ey_waveform',
                         'Eu_offset'+'_'+mode, 'Ev_offset'+'_'+mode]

    else:
        pathformat = 'satellite/erg/pwe/efd/'+level+'/'+datatype + \
            '/%Y/%m/erg_pwe_efd_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'
        prefix += datatype + '_'
        if 'spin' in datatype:
            component = ['Eu', 'Ev', 'Eu1', 'Ev1', 'Eu2', 'Ev2']
            labels = ['Ex', 'Ey']
        if datatype == 'pot':
            component = ['Vu1', 'Vu2', 'Vv1', 'Vv2']
        if datatype == 'pot8Hz':
            component = ['Vu1_waveform_8Hz', 'Vu2_waveform_8Hz',
                         'Vv1_waveform_8Hz', 'Vv2_waveform_8Hz']

    loaded_data = load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                       varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd)

    if (len(loaded_data) > 0) and ror:

        try:
            if isinstance(loaded_data, list):
                if downloadonly:
                    cdf_file = cdflib.CDF(loaded_data[-1])
                    gatt = cdf_file.globalattsget()
                else:
                    gatt = get_data(loaded_data[-1], metadata=True)['CDF']['GATT']
            elif isinstance(loaded_data, dict):
                gatt = loaded_data[list(loaded_data.keys())[-1]]['CDF']['GATT']

            # --- print PI info and rules of the road

            print(' ')
            print(' ')
            print(
                '**************************************************************************')
            print(gatt["LOGICAL_SOURCE_DESCRIPTION"])
            print('')
            print('Information about ERG PWE EFD')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: "+gatt["PI_AFFILIATION"])
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                'RoR of PWE/EFD: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Pwe/Efd')
            print('')
            print('Contact: erg_pwe_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    time_min_max = time_float(trange)
    if 'spin' in datatype:
        for elem in component:
            t_plot_name = prefix + elem + '_dsi'
            options(t_plot_name, 'ytitle', elem + ' vector in DSI')
            options(t_plot_name, 'legend_names', labels)
            # ylim settings because pytplot.timespan() doesn't affect in ylim.
            # May be it will be no need in future.
            get_data_vars = get_data(t_plot_name)
            if get_data_vars[0][0] < time_min_max[0]:
                min_time_index = np.where(
                    (get_data_vars[0] <= time_min_max[0]))[0][-1]
            else:
                min_time_index = 0
            if time_min_max[1] < get_data_vars[0][-1]:
                max_time_index = np.where(
                    time_min_max[1] <= get_data_vars[0])[0][0]
            else:
                max_time_index = -1
            ylim_min = np.nanmin(
                get_data_vars[1][min_time_index:max_time_index])
            ylim_max = np.nanmax(
                get_data_vars[1][min_time_index:max_time_index])
            ylim(t_plot_name, ylim_min, ylim_max)

    if ('64' in datatype) or ('256' in datatype) or (datatype == 'pot8Hz'):
        for elem in component:
            t_plot_name = prefix+elem
            get_data_vars = get_data(t_plot_name)
            dl_in = get_data(t_plot_name, metadata=True)
            time1 = get_data_vars[0]
            data = np.where(get_data_vars[1] <= -
                            1e+30, np.nan, get_data_vars[1])
            dt = get_data_vars[2]
            ndt = dt.size
            ndata = data.size
            time_new = (np.tile(time1, (ndt, 1)).T + dt * 1e-3).reshape(ndata)
            data_new = data.reshape(ndata)
            store_data(t_plot_name, data={
                       'x': time_new, 'y': data_new}, attr_dict=dl_in)
            options(t_plot_name, 'ytitle', '\n'.join(t_plot_name.split('_')))
            # ylim settings because pytplot.timespan() doesn't affect in ylim.
            # May be it will be no need in future.
            if time_new[0] < time_min_max[0]:
                min_time_index = np.where((time_new <= time_min_max[0]))[0][-1]
            else:
                min_time_index = 0
            if time_min_max[1] < time_new[-1]:
                max_time_index = np.where(time_min_max[1] <= time_new)[0][0]
            else:
                max_time_index = -1
            ylim_min = np.nanmin(data_new[min_time_index:max_time_index])
            ylim_max = np.nanmax(data_new[min_time_index:max_time_index])
            ylim(t_plot_name, ylim_min, ylim_max)

    if datatype == 'pot':
        for elem in component:
            t_plot_name = prefix+elem
            options(t_plot_name, 'ytitle', elem+' potential')

    if datatype == 'spec':
        options(tnames(prefix + '*spectra*'), 'spec', 1)
        options(tnames(prefix + '*spectra*'), 'colormap', 'jet')
        options(tnames(prefix + '*spectra*'), 'zlog', 1)
        ylim(prefix + 'spectra', 0, 100)
        zlim(prefix + 'spectra', 1e-6, 1e-2)
        options(tnames(prefix + '*spectra*'), 'ysubtitle', '[Hz]')
        options(tnames(prefix + '*spectra*'), 'ztitle', '[mV^2/m^2/Hz]')
        for t_plot_name in (tnames(prefix + '*spectra*')):
            options(t_plot_name, 'ytitle', '\n'.join(t_plot_name.split('_')))

    return loaded_data

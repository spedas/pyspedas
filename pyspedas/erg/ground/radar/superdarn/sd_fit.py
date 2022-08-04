import cdflib
import fnmatch

import numpy as np

from copy import deepcopy
from pytplot import get_data, store_data, options, clip, ylim, zlim
from pyspedas import tnames

from ....satellite.erg.load import load

from .get_sphcntr import get_sphcntr

"""
;Internal routine to get the table of the pixel
;centers from the table of the pixel corners.
"""
def get_pixel_cntr(tbl_array):
    dim_tuple = tbl_array.shape
    rgmax = dim_tuple[0] - 1
    azmax = dim_tuple[1] - 1
    cnttbl = np.zeros(shape=(rgmax, azmax, 2))
    for i in range(rgmax):
        for j in range(azmax):
            axis_0_indices_array = np.repeat(np.array([[i, i + 1, i + 1, i]]).T,4,1).T.reshape(16)
            axis_1_indices_array = np.array([j] * 8 + [j + 1] * 8)
            lonarr=tbl_array[tuple([axis_0_indices_array, axis_1_indices_array, 0])].reshape(4,4)
            latarr=tbl_array[tuple([axis_0_indices_array, axis_1_indices_array, 1])].reshape(4,4)
            pos_array = get_sphcntr(latarr, lonarr)
            cnttbl[i, j, 1] = pos_array[0]
            cnttbl[i, j, 0] = pos_array[1]
    return cnttbl

def sd_fit(
    trange=['2018-10-18/00:00:00','2018-10-18/02:00:00'],
    suffix='',
    site='all',
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    uname=None,
    passwd=None,
    time_clip=False,
    ror=True,
    compact=False
):

    valid_sites = [ 'ade', 'adw', 'bks', 'bpk', 'cly', 'cve', 'cvw', 'dce', 'fhe',
    'fhw', 'fir', 'gbr', 'hal', 'han', 'hok', 'hkw', 'inv', 'kap', 'ker', 'kod',
    'ksr', 'mcm', 'pgr', 'pyk', 'rkn', 'san', 'sas', 'sps', 'sto', 'sye',
    'sys', 'tig', 'unw', 'wal', 'zho', 'lyr' ]



    if isinstance(site, str):
        site_code = site.lower()
        site_code = site_code.split(' ')
    elif isinstance(site, list):
        site_code = []
        for i in range(len(site)):
            site_code.append(site[i].lower())
    if 'all' in site_code:
        site_code = valid_sites
    site_code = list(set(site_code).intersection(valid_sites))

    if notplot:
        loaded_data = {}
    else:
        loaded_data = []
    
    for site_input in site_code:

        prefix = 'sd_' + site_input + '_'
        file_res = 3600. * 24.
        pathformat = 'ground/radar/sd/fitacf/'+site_input\
                        +'/%Y/sd_fitacf_l2_'+site_input+'_%Y%m%d*.cdf'

        loaded_data_temp = load(pathformat=pathformat, file_res=file_res, trange=trange, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                    varformat=varformat, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd)
        if notplot:
            loaded_data.update(loaded_data_temp)
        else:
            loaded_data += loaded_data_temp
        if (len(loaded_data_temp) > 0) and ror:
            try:
                if isinstance(loaded_data_temp, list):
                    if downloadonly:
                        cdf_file = cdflib.CDF(loaded_data_temp[-1])
                        gatt = cdf_file.globalattsget()
                    else:
                        gatt = get_data(loaded_data_temp[-1], metadata=True)['CDF']['GATT']
                elif isinstance(loaded_data_temp, dict):
                    gatt = loaded_data_temp[list(loaded_data_temp.keys())[-1]]['CDF']['GATT']
                print('############## RULES OF THE ROAD ################')
                print(gatt["Rules_of_use"])
                print('############## RULES OF THE ROAD ################')
            except:
                print('printing PI info and rules of the road was failed')


        if (not downloadonly) and (not notplot) and (len(loaded_data_temp) > 0):

            t_plot_name_list = tnames([prefix + 'pwr*', prefix + 'spec*', prefix + 'vlos*'])
            t_plot_name_list = list(set(t_plot_name_list).intersection(loaded_data))
            for t_plot_name in t_plot_name_list:
                clip(t_plot_name, -9000, 9000)
            
            t_plot_name_list = tnames([prefix + 'elev*'])
            t_plot_name_list = list(set(t_plot_name_list).intersection(loaded_data))
            if len(t_plot_name_list) > 5:
                for t_plot_name in t_plot_name_list:
                    clip(t_plot_name, -9000, 9000)

            azim_no_name_list = list(set(tnames(prefix + '*azim_no_?' + suffix)).intersection(loaded_data))
            number_string_list = []
            for azim_no_name in azim_no_name_list:
                number_string_list.append(azim_no_name.split('_')[4][0])

            for number_string in number_string_list:

                site_input_upper = site_input.upper()
                #  ;Set labels for some tplot variables
                options(prefix + 'pwr_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'pwr_' + number_string + suffix, 'ztitle', 'Backscatter power [dB]')
                options(prefix + 'pwr_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'pwr_err_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'pwr_err_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'pwr_err_' + number_string + suffix, 'ztitle', 'power err [dB]')
                options(prefix + 'spec_width_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'spec_width_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'spec_width_' + number_string + suffix, 'ztitle', 'Spec. width [m/s]')
                options(prefix + 'spec_width_err_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'spec_width_err_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'spec_width_err_' + number_string + suffix, 'ztitle', 'Spec. width err [m/s]')

                if not prefix+'vlos_' + number_string + suffix in loaded_data:
                    vlos_notplot_dictionary = load(pathformat=pathformat, file_res=file_res, trange=trange, prefix=prefix,suffix=suffix, get_support_data=get_support_data,
                            varformat='vlos_' + number_string, downloadonly=downloadonly, notplot=True, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd)
                    vlos_tplot_name = prefix+'vlos_' + number_string + suffix
                    if len(vlos_notplot_dictionary) > 0:
                        store_data(vlos_tplot_name,
                                data={'x':vlos_notplot_dictionary[vlos_tplot_name]['x'],
                                    'y':vlos_notplot_dictionary[vlos_tplot_name]['y'],
                                    'v1':vlos_notplot_dictionary[vlos_tplot_name]['v'],
                                    'v2':np.arange(vlos_notplot_dictionary[vlos_tplot_name]['y'].shape[2])},
                                attr_dict={'CDF':vlos_notplot_dictionary[vlos_tplot_name]['CDF']})

                        clip(vlos_tplot_name, -9000, 9000)
                        options(vlos_tplot_name, 'spec', 1)
                        loaded_data.append(vlos_tplot_name)
                options(prefix + 'vlos_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'vlos_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'vlos_' + number_string + suffix, 'ztitle', 'Doppler velocity [m/s]')

                options(prefix + 'vlos_err_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'vlos_err_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'vlos_err_' + number_string + suffix, 'ztitle', 'Vlos err [m/s]')
                if prefix + 'elev_angle_' + number_string + suffix in loaded_data:  # need to get_support_data=True
                    options(prefix + 'elev_angle_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                    options(prefix + 'elev_angle_' + number_string + suffix, 'ysubtitle', '[range gate]')
                    options(prefix + 'elev_angle_' + number_string + suffix, 'ztitle', 'Elev. angle [deg]')
                options(prefix + 'echo_flag_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'echo_flag_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'echo_flag_' + number_string + suffix, 'ztitle', '1: iono. echo')
                options(prefix + 'quality_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'quality_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'quality_' + number_string + suffix, 'ztitle', 'quality')
                options(prefix + 'quality_flag_' + number_string + suffix, 'ytitle', site_input_upper+'\nall beams')
                options(prefix + 'quality_flag_' + number_string + suffix, 'ysubtitle', '[range gate]')
                options(prefix + 'quality_flag_' + number_string + suffix, 'ztitle', 'quality flg')

                #;Split vlos_? tplot variable into 3 components
                get_data_vlos = get_data(prefix + 'vlos_' + number_string + suffix)
                if get_data_vlos is not None:
                    if get_data_vlos[1].ndim >= 3:
                        get_metadata_vlos = get_data(prefix + 'vlos_' + number_string + suffix, metadata=True)
                        store_data(prefix + 'vnorth_' + number_string + suffix,
                                    data={'x':get_data_vlos[0],
                                        'y':get_data_vlos[1][:, :, 0],
                                        'v':get_data_vlos[2]},
                                    attr_dict=get_metadata_vlos)
                        options(prefix + 'vnorth_' + number_string + suffix, 'ztitle', 'LOS V Northward [m/s]')
                        loaded_data.append(prefix + 'vnorth_' + number_string + suffix)
                        if get_data_vlos[1].shape[2] >= 1:
                            store_data(prefix + 'veast_' + number_string + suffix,
                                        data={'x':get_data_vlos[0],
                                            'y':get_data_vlos[1][:, :, 1],
                                            'v':get_data_vlos[2]},
                                        attr_dict=get_metadata_vlos)
                            options(prefix + 'veast_' + number_string + suffix, 'ztitle', 'LOS V Eastward [m/s]')
                            loaded_data.append(prefix + 'veast_' + number_string + suffix)
                            if get_data_vlos[1].shape[2] >= 2:
                                store_data(prefix + 'vlos_' + number_string + suffix,
                                            data={'x':get_data_vlos[0],
                                                'y':get_data_vlos[1][:, :, 2],
                                                'v':get_data_vlos[2]},
                                            attr_dict=get_metadata_vlos)
                                options(prefix + 'vlos_' + number_string + suffix, 'ztitle', 'LOS Doppler vel. [m/s]')

                    #;Combine iono. echo and ground echo for vlos
                    v_var_names = ['vlos_','vnorth_','veast_']
                    flag_data = get_data(prefix + 'echo_flag_' + number_string + suffix)
                    for v_var in v_var_names:
                        v_var_data = get_data(prefix + v_var + number_string + suffix)
                        if v_var_data is not None:
                            v_var_metadata = get_data(prefix + v_var + number_string + suffix, metadata=True)
                            g_data_y = np.where(flag_data[1] == 1., np.nan, v_var_data[1])
                            v_var_data_y = np.where(flag_data[1] != 1., np.nan, v_var_data[1])
                            max_rg = np.nanmax(v_var_data[2]) + 1
                            store_data(prefix + v_var + 'iscat_' + number_string + suffix,
                                    data={'x':v_var_data[0],
                                        'y':v_var_data_y,
                                        'v':v_var_data[2]},
                                    attr_dict=v_var_metadata)
                            options(prefix + v_var + 'iscat_' + number_string + suffix, 'ytitle', ' ')
                            options(prefix + v_var + 'iscat_' + number_string + suffix, 'ysubtitle', ' ')
                            options(prefix + v_var + 'iscat_' + number_string + suffix, 'ztitle', ' ')
                            options(prefix + v_var + 'iscat_' + number_string + suffix, 'spec', 1)
                            loaded_data.append(prefix + v_var + 'iscat_' + number_string + suffix)
                            metadata_for_gscat = deepcopy(v_var_metadata)
                            metadata_for_gscat['plot_options']['extras']['fill_color'] = 5  #options like, 'fill_color:5' in IDL, have not implemented.
                            store_data(prefix + v_var + 'gscat_' + number_string + suffix,
                                    data={'x':v_var_data[0],
                                        'y':g_data_y,
                                        'v':v_var_data[2]},
                                    attr_dict=metadata_for_gscat)
                            options(prefix + v_var + 'gscat_' + number_string + suffix, 'ytitle', ' ')
                            options(prefix + v_var + 'gscat_' + number_string + suffix, 'ysubtitle', ' ')
                            options(prefix + v_var + 'gscat_' + number_string + suffix, 'ztitle', ' ')
                            options(prefix + v_var + 'gscat_' + number_string + suffix, 'spec', 1)
                            loaded_data.append(prefix + v_var + 'gscat_' + number_string + suffix)
                            store_data(prefix + v_var + 'bothscat_' + number_string + suffix,
                                    data=[prefix + v_var + 'iscat_' + number_string + suffix,
                                        prefix + v_var + 'gscat_' + number_string + suffix])
                            options(prefix + v_var + 'bothscat_' + number_string + suffix, 'yrange', [0,max_rg])
                            loaded_data.append(prefix + v_var + 'bothscat_' + number_string + suffix)
                            """
                            Currently, '*iscat_*' and '*bothscat_*' are almost same plot outputs.
                            Because, options like, 'fill_color:5' of IDL for '*gscat_*' have not implemented.
                            """

                #;Set the z range explicitly for some tplot variables
                zlim(prefix + 'pwr_' + number_string + suffix, 0., 30.)
                zlim(prefix + 'pwr_err_' + number_string + suffix, 0., 30.)
                zlim(prefix + 'spec_width_' + number_string + suffix, 0., 200.)
                zlim(prefix + 'spec_width_err_' + number_string + suffix, 0., 300.)
                
                # zlim for '*vlos_*scat_*'
                t_names_raw = tnames(prefix + 'vlos_*scat_' + number_string + suffix)
                t_names_remove_space = [t_name.split(' ')[0] for t_name in t_names_raw]
                t_plot_name_list = list(set(t_names_remove_space).intersection(loaded_data))
                for t_plot_name in t_plot_name_list:
                    zlim(t_plot_name, -400., 400.)
                
                # zlim for '*vnorth_*scat_*'
                t_names_raw = tnames(prefix + 'vnorth_*scat_' + number_string + suffix)
                t_names_remove_space = [t_name.split(' ')[0] for t_name in t_names_raw]
                t_plot_name_list = list(set(t_names_remove_space).intersection(loaded_data))
                for t_plot_name in t_plot_name_list:
                    zlim(t_plot_name, -400., 400.)
                
                # zlim for '*veast_*scat_*'
                t_names_raw = tnames(prefix + 'veast_*scat_' + number_string + suffix)
                t_names_remove_space = [t_name.split(' ')[0] for t_name in t_names_raw]
                t_plot_name_list = list(set(t_names_remove_space).intersection(loaded_data))
                for t_plot_name in t_plot_name_list:
                    zlim(t_plot_name, -400., 400.)
                
                zlim(prefix + 'vlos_err_' + number_string + suffix, 0., 300.)

                # ;Fill values --> NaN
                get_data_vars_pwr = get_data(prefix + 'pwr_' + number_string + suffix)
                if get_data_vars_pwr is not None:
                    pwr_y = deepcopy(get_data_vars_pwr[1])
                    indices_array_tuple = np.where(np.isfinite(pwr_y) == False)
                    var_name_list = ['echo_flag_', 'quality_', 'quality_flag_']
                    for var_name in var_name_list:
                        t_plot_name = prefix + var_name + number_string + suffix
                        get_data_vars = get_data(t_plot_name)
                        get_metadata_vars = get_data(t_plot_name, metadata=True)
                        if get_data_vars is not None:
                            val_array = deepcopy(get_data_vars[1].astype(np.float64))
                            val_array[indices_array_tuple] = np.nan
                            store_data(t_plot_name, data={'x':get_data_vars[0],
                                                        'y':val_array,
                                                        'v':get_data_vars[2]},
                                    attr_dict=get_metadata_vars)

                #;Reassign scan numbers for the combined data
                if (prefix + 'scanstartflag_' + number_string + suffix in loaded_data)\
                   and (prefix + 'scanno_' + number_string + suffix in loaded_data):  # need to get_support_data=True
                    t_plot_name = prefix + 'scanstartflag_' + number_string + suffix
                    scanstartflag_data = get_data(t_plot_name)
                    if scanstartflag_data is not None:
                        scflg = abs(scanstartflag_data[1])
                        try:
                            scno = np.full(shape=scflg.shape, fill_value=-1, dtype=np.int64)
                        except:
                            scno = np.full(shape=scflg.shape, fill_value=-1, dtype=np.int32)
                        scno_t = 0
                        scno[0] = scno_t
                        gt_1_indices_array = np.where(scflg > 0)[0]
                        for i in range(gt_1_indices_array.size - 1):
                            scno[gt_1_indices_array[i]:gt_1_indices_array[i+1]] = i
                        scno[gt_1_indices_array[i+1]:] = i + 1
                        t_plot_name = prefix + 'scanno_' + number_string + suffix
                        get_data_var_scanno = get_data(t_plot_name)
                        if get_data_var_scanno is not None:
                            get_metadata_var_scanno = get_data(t_plot_name, metadata=True)
                            store_data(t_plot_name, data={'x':get_data_var_scanno[0],
                                                          'y':scno},
                                                    attr_dict=get_metadata_var_scanno)

            """
            ;Load the position table(s) ;;;;;;;;;;;;;;;;;;
            ;Currently supports SD fitacf CDFs containing up to 4 pos. tables.
            """
            tbllist = ['tbl_0', 'tbl_1' , 'tbl_2', 'tbl_3', 'tbl_4',
            'tbl_5', 'tbl_6' , 'tbl_7', 'tbl_8', 'tbl_9' ]
            timelist = ['time_0','time_1','time_2','time_3', 'time_4',
            'time_5','time_6','time_7','time_8','time_9']

            get_metadata_vars = get_data(loaded_data[-1], metadata=True)
            if get_metadata_vars is not None:
                datfiles = deepcopy(get_metadata_vars['CDF']['FILENAME'])
                position_tbl_dictionary = {}
                for i in range(10):
                    position_tbl_dictionary[str(i)] = {
                        'time_input':[],
                        'tbl_input':[],
                        'cnttbl_input':[]
                    }
                if len(datfiles) > 0:
                    for file_name in datfiles:
                        cdf_file = cdflib.CDF(file_name)
                        cdf_info = cdf_file.cdf_info()
                        all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']
                        timevn = fnmatch.filter(all_cdf_variables, 'Epoch_?')
                        ptblvn = fnmatch.filter(all_cdf_variables, 'position_tbl_?')
                        timevn.sort()
                        ptblvn.sort()
                        for j in range(len(ptblvn)):
                            tv_name = timevn[j]
                            stblno = tv_name.split('_')[-1]
                            pv_name = ptblvn[j]
                            time_array = cdf_file.varget(tv_name)
                            tbl_array = cdf_file.varget(pv_name)
                            cnttbl = get_pixel_cntr(tbl_array)
                            position_tbl_dictionary[stblno]['time_input'] += [time_array[0], time_array[-1]]
                            dim_tuple = tbl_array.shape
                            tbl2_array = tbl_array.reshape(1, dim_tuple[0], dim_tuple[1], dim_tuple[2])
                            cnttbl2_array = cnttbl.reshape(1, dim_tuple[0] - 1, dim_tuple[1] - 1, dim_tuple[2])
                            if len(position_tbl_dictionary[stblno]['tbl_input']) == 0:
                                position_tbl_dictionary[stblno]['tbl_input'] = np.concatenate(
                                                                                [tbl2_array,tbl2_array],
                                                                                axis=0)
                            else:
                                position_tbl_dictionary[stblno]['tbl_input'] = np.concatenate([position_tbl_dictionary[stblno]['tbl_input']
                                                                                            ,tbl2_array,tbl2_array],axis=0)
                            if len(position_tbl_dictionary[stblno]['cnttbl_input']) == 0:
                                position_tbl_dictionary[stblno]['cnttbl_input'] = np.concatenate([cnttbl2_array,cnttbl2_array],axis=0)
                            else:
                                position_tbl_dictionary[stblno]['cnttbl_input'] = np.concatenate([position_tbl_dictionary[stblno]['cnttbl_input']
                                                                                            ,cnttbl2_array,cnttbl2_array],axis=0)
    
                    for t_plot_suffix_number in position_tbl_dictionary.keys():
                        if len(position_tbl_dictionary[t_plot_suffix_number]['time_input']) >= 2:
                            input_tplot_time_array= np.array(position_tbl_dictionary[t_plot_suffix_number]['time_input'])\
                                                    / 1000. - 719528. * 24.* 3600.
                            t_plot_name = prefix + 'position_tbl_' + t_plot_suffix_number + suffix
                            store_data(t_plot_name, data={'x':input_tplot_time_array,
                                            'y':position_tbl_dictionary[t_plot_suffix_number]['tbl_input']})
                            loaded_data.append(t_plot_name)
                            t_plot_name = prefix + 'positioncnt_tbl_' + t_plot_suffix_number + suffix
                            store_data(t_plot_name, data={'x':input_tplot_time_array,
                                            'y':position_tbl_dictionary[t_plot_suffix_number]['cnttbl_input']})
                            loaded_data.append(t_plot_name)


    if compact:  #;Leave only minimal set of the variables if compact=True.
        search_var_list = ['*cpid*', '*channel*', '*int_time*', '*azim_no*', '*pwr_err*', '*spec_width_err*',
                            '*vlos_err*', '*elev_angle*', '*elev_angle_err*', '*phi0*', '*phi0_err*', 
                            '*echo_flag*', '*quality*', '*quality_flag*', '*scanno*', '*scanstartflag*',
                            '*lagfr*', '*smsep*', '*nrang_max*', '*tfreq*', '*noise*', '*num_ave*', '*txpl*',
                            '*vnorth*', '*veast*', '*vlos_bothscat*', '*vlos_iscat*', '*vlos_gscat*',
                            '*vnorth_iscat*', '*vnorth_gscat*', '*vnorth_bothscat*', '*veast_iscat*',
                            '*veast_gscat*', '*veast_bothscat*', '*position_tbl*', '*positioncnt_tbl*']
        delete_tplot_name_list = list(set(tnames(search_var_list)).intersection(loaded_data))
        if len(delete_tplot_name_list) > 0:
            store_data(delete_tplot_name_list, delete=True)
            loaded_data = list(set(loaded_data).difference(delete_tplot_name_list))


    return loaded_data

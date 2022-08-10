import cdflib
import numpy as np

from pytplot import get_data, store_data, options, clip, ylim

from ...satellite.erg.load import load


def gmag_magdas_1sec(
    trange=['2010-11-20/00:00:00','2010-11-21/00:00:00'],
    suffix='',
    site='all',
    datatype='1sec',
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    uname=None,
    passwd=None,
    time_clip=False,
    ror=True
):

    site_code_all = ['ama', 'asb', 'daw', 'her', 'hln', 'hob',
                     'kuj', 'laq', 'mcq', 'mgd', 'mlb', 'mut',
                     'onw', 'ptk', 'wad', 'yap']
    tres_all=['1sec']
    if isinstance(datatype, str):
        datatype = datatype.lower()
        datatype = datatype.split(' ')
    elif isinstance(datatype, list):
        for i in range(len(datatype)):
            datatype[i] = datatype[i].lower()

    if 'all' in datatype:
        datatype=tres_all
    datatype = list(set(datatype).intersection(tres_all))
    if len(datatype) < 1:
        return

    if '1s' in datatype:
        index = np.where(np.array(datatype) == '1s')[0][0]
        datatype[index] = '1sec'
    
    if isinstance(site, str):
        site_code = site.lower()
        site_code = site_code.split(' ')
    elif isinstance(site, list):
        site_code = []
        for i in range(len(site)):
            site_code.append(site[i].lower())
    if 'all' in site_code:
        site_code = site_code_all
    site_code = list(set(site_code).intersection(site_code_all))

    prefix = 'magdas_'
    if notplot:
        loaded_data = {}
    else:
        loaded_data = []
    for site_input in site_code:
        for data_type_in in datatype:
            fres = data_type_in

            file_res = 3600. * 24
            pathformat = 'ground/geomag/magdas/'+fres+'/'+site_input\
                            +'/%Y/magdas_'+fres+'_'+site_input+'_%Y%m%d_v??.cdf'
            
            loaded_data_temp = load(pathformat=pathformat, file_res=file_res, trange=trange, datatype=datatype, prefix=prefix, suffix='_'+site_input+suffix, get_support_data=get_support_data,
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
                    print('**************************************************************************')
                    print(gatt["Logical_source_description"])
                    print('')
                    print(f'Information about {gatt["Station_code"]}')
                    print(f'PI and Host PI(s): {gatt["PI_name"]}')
                    print('')
                    print('Affiliations: ')
                    print(gatt["PI_affiliation"])
                    print('')
                    print('Rules of the Road for MAGDAS Data Use:')
                    for gatt_text in gatt["TEXT"]:
                        print(gatt_text)
                    print(f'{gatt["LINK_TEXT"]} {gatt["HTTP_LINK"]}')
                    print('**************************************************************************')
                except:
                    print('printing PI info and rules of the road was failed')
                
            if (not downloadonly) and (not notplot):
                current_tplot_name = prefix+'hdz_'+fres+'_' + site_input+suffix
                if current_tplot_name in loaded_data:
                    #;--- Rename *** HDZ
                    new_tplot_name = prefix+'mag_'+site_input+'_'+fres+'_hdz'+suffix
                    store_data(current_tplot_name, newname=new_tplot_name)
                    loaded_data.remove(current_tplot_name)
                    loaded_data.append(new_tplot_name)
                    #;--- Missing data -1.e+31 --> NaN
                    clip(new_tplot_name, -7e+4, 7e+4)
                    get_data_vars = get_data(new_tplot_name)
                    ylim(new_tplot_name, -np.nanmax(abs(get_data_vars[1])) * 1.1, np.nanmax(abs(get_data_vars[1])) * 1.1)
                    #;--- Labels
                    options(new_tplot_name, 'legend_names', ['H','D','Z'])
                    options(new_tplot_name, 'Color', ['b', 'g', 'r'])
                    options(new_tplot_name, 'ytitle', '\n'.join(new_tplot_name.split('_')))
                
                current_tplot_name = prefix+'f_'+fres+'_' + site_input+suffix
                if current_tplot_name in loaded_data:
                    #; --- Rename *** F
                    new_tplot_name = prefix+'mag_'+site_input+'_'+fres+'_f'+suffix
                    store_data(current_tplot_name, newname=new_tplot_name)
                    loaded_data.remove(current_tplot_name)
                    loaded_data.append(new_tplot_name)
                    #;--- Missing data -1.e+31 --> NaN
                    clip(new_tplot_name, -7e+4, 7e+4)
                    get_data_vars = get_data(new_tplot_name)
                    ylim(new_tplot_name, -np.nanmax(abs(get_data_vars[1])) * 1.1, np.nanmax(abs(get_data_vars[1])) * 1.1)
                    #;--- Labels
                    options(new_tplot_name, 'legend_names', ['F'])
                    options(new_tplot_name, 'ytitle', '\n'.join(new_tplot_name.split('_')))

    return loaded_data

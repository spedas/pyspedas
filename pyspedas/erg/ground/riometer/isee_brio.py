import cdflib
import numpy as np

from copy import deepcopy
from pytplot import get_data, store_data, options, clip, ylim

from ...satellite.erg.load import load


def isee_brio(
    trange=['2020-08-01', '2020-08-02'],
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
    ror=True
):

    #;----- datatype -----;
    datatype='64hz'
    instr='brio'
    freq='30'
    
    site_code_all = ['ath', 'kap', 'gak', 'hus', 'zgn', 'ist']
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

    prefix = 'iseetmp_'
    if notplot:
        loaded_data = {}
    else:
        loaded_data = []
    for site_input in site_code:
        fres = datatype
        file_res = 3600. * 24
        pathformat = 'ground/riometer/'+site_input\
                        +'/%Y/isee_'+fres+'_'+instr+freq+'_'+site_input+'_%Y%m%d_v??.cdf'
        
        loaded_data_temp = load(pathformat=pathformat, file_res=file_res, trange=trange, datatype=datatype, prefix=prefix, suffix='_' + site_input +suffix, get_support_data=get_support_data,
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
                print(f'PI {gatt["PI_name"]}')
                print('')
                print(f'Affiliations: {gatt["PI_affiliation"]}')
                print('')
                print('Rules of the Road for ISEE Riometer Data:')
                print('')
                print(gatt["TEXT"])
                print({gatt["LINK_TEXT"]})
                print('**************************************************************************')
            except:
                print('printing PI info and rules of the road was failed')
            
        if (not downloadonly) and (not notplot):
            if len(loaded_data_temp) > 0:
                file_name = get_data(loaded_data_temp[-1], metadata=True)['CDF']['FILENAME']
                if isinstance(file_name, list):
                    file_name = file_name[0]
                cdf_file = cdflib.CDF(file_name)
                cdf_info = cdf_file.cdf_info()
                all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']
                for t_plot_name in loaded_data_temp:
                    get_data_vars = get_data(t_plot_name)
                    if get_data_vars is None:
                        store_data(t_plot_name, delete=True)
                    else:
                        t_plot_name_split =t_plot_name.split('_')
                        if len(t_plot_name_split) > 2:
                            #;----- Find param -----;
                            param = t_plot_name_split[1]
                            if param in ['cna', 'qdc', 'raw']:
                                #;----- Rename tplot variables -----;
                                new_tplot_name = 'isee_brio'+freq+'_'+site_input+'_'+fres+'_'+param + suffix
                                store_data(t_plot_name, newname=new_tplot_name)
                                loaded_data.remove(t_plot_name)
                                loaded_data.append(new_tplot_name)
                                #;----- Missing data -1.e+31 --> NaN -----;
                                clip(new_tplot_name, -1e+5, 1e+5)
                                get_data_vars = get_data(new_tplot_name)
                                if param in all_cdf_variables:
                                    var_atts = cdf_file.varattsget(param)
                                    if "FILLVAL" in var_atts:  #removing "FILLVAL", like 999.9000 or 0.0.
                                                            #removing process of cdf_to_tplot.py may be not working well.
                                        var_properties = cdf_file.varinq(param)
                                        if ((var_properties['Data_Type_Description'] ==
                                                'CDF_FLOAT') or
                                                (var_properties['Data_Type_Description'] ==
                                                'CDF_REAL4') or
                                                (var_properties['Data_Type_Description'] ==
                                                'CDF_DOUBLE') or
                                                (var_properties['Data_Type_Description'] ==
                                                'CDF_REAL8')):
                                            if isinstance(var_atts["FILLVAL"], str):
                                                fill_value = float(var_atts["FILLVAL"])
                                            else:
                                                fill_value = deepcopy(var_atts["FILLVAL"])
                                            new_y = np.where(get_data_vars[1] == fill_value,
                                                            np.nan, get_data_vars[1])
                                            get_metadata_vars = get_data(new_tplot_name, metadata=True)
                                            store_data(new_tplot_name, data={'x':get_data_vars[0],
                                                                                'y':new_y},
                                                        attr_dict=get_metadata_vars)
                                            ylim(new_tplot_name, np.nanmin(new_y), np.nanmax(new_y))
                                    else:
                                        ylim(new_tplot_name, np.nanmin(get_data_vars[1]), np.nanmax(get_data_vars[1]))
                                #;----- Set options -----;
                                options(new_tplot_name, 'ytitle', site_input.upper())
                                if param == 'cna':
                                    options(new_tplot_name, 'ysubtitle', '[dB]')
                                    options(new_tplot_name, 'legend_names', ['CNA'])
                                elif param == 'qdc':
                                    options(new_tplot_name, 'ysubtitle', '[V]')
                                    options(new_tplot_name, 'legend_names', ['QDC'])
                                elif param == 'raw':
                                    options(new_tplot_name, 'ysubtitle', '[V]')
                                    options(new_tplot_name, 'legend_names', ['Raw data'])

    return loaded_data

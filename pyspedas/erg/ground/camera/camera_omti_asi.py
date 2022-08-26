import cdflib
import numpy as np

from pytplot import get_data, store_data, options, clip, ylim

from ...satellite.erg.load import load


def camera_omti_asi(
    trange=['2020-08-01', '2020-08-02'],
    suffix='',
    site='all',
    wavelength=[5577],
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

    site_code_all = ['abu', 'ath', 'drw', 'eur', 'gak', 'hlk',
                     'hus', 'isg', 'ist', 'ith', 'kap', 'ktb',
                     'mgd', 'nai', 'nyr', 'ptk', 'rik', 'rsb',
                     'sgk', 'sta', 'syo', 'trs', 'yng']

    if isinstance(wavelength, str):
        wavelengthc = wavelength.split(' ')
    elif isinstance(wavelength, int):
        wavelengthc = [str(wavelength)]
    elif isinstance(wavelength, list):
        wavelengthc = []
        for i in range(len(wavelength)):
            wavelengthc.append(str(wavelength[i]))

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

    
    if notplot:
        loaded_data = {}
    else:
        loaded_data = []
    for site_input in site_code:
        for wavelength_in in wavelengthc:
            prefix = 'omti_asi_'+site_input+'_'+wavelength_in+'_'
            file_res = 3600.
            pathformat = 'ground/camera/omti/asi/'+site_input\
                            +'/%Y/%m/%d/omti_asi_c??_'+site_input+'_'+wavelength_in+'_%Y%m%d%H_v??.cdf'

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
                    print('**************************************************************************')
                    print(gatt["Logical_source_description"])
                    print('')
                    print(f'Information about {gatt["Station_code"]}')
                    print(f'PI: {gatt["PI_name"]}')
                    print('')
                    print(f'Affiliations: {gatt["PI_affiliation"]}')
                    print('')
                    print('Rules of the Road for OMTI ASI Data Use:')
                    for gatt_text in gatt["TEXT"]:
                        print(gatt_text)
                    print(f'{gatt["LINK_TEXT"]}')
                    print('**************************************************************************')
                except:
                    print('printing PI info and rules of the road was failed')
                
            if (not downloadonly) and (not notplot):
                current_tplot_name = prefix+'cloud' + suffix
                if current_tplot_name in loaded_data:
                    get_data_vars = get_data(current_tplot_name)
                    if get_data_vars is None:
                        store_data(current_tplot_name, delete=True)
                    else:
                        new_tplot_name = 'omti_asi_'+site_input+'_cloud'+suffix
                        store_data(current_tplot_name, newname=new_tplot_name)
                        loaded_data.remove(current_tplot_name)
                        if new_tplot_name not in loaded_data:
                            loaded_data.append(new_tplot_name)
                        #;--- Missing data -1.e+31 --> NaN
                        clip(new_tplot_name, -1, 9)
                    
                current_tplot_name = prefix+'image_raw' + suffix
                if current_tplot_name in loaded_data:
                    get_data_vars = get_data(current_tplot_name)
                    if get_data_vars is None:
                        store_data(current_tplot_name, delete=True)
                    else:
                        #;--- Missing data -1.e+31 --> NaN
                        clip(current_tplot_name, -1e+6, 1e+6)
                        get_data_vars = get_data(current_tplot_name)
                        """
                        Transpose y element of the image data.
                        In order to not to make an Upside down, left and right upside down,
                        for saving figure, by PIL library.
                        """
                        image_y_transpose = get_data_vars[1].transpose(0, 2, 1)
                        """
                        Try to get 'Data_Type_Description' from CDF file.
                        In order to adjust the data type of y element into original one.
                        (After clip, data type of y element may become float.)
                        This may be need for saving figure correctly.
                        """
                        file_name = get_data(current_tplot_name,
                                            metadata=True)['CDF']['FILENAME']
                        if isinstance(file_name, list):
                            if len(file_name) > 0:
                                file_name = file_name[0]
                        cdf_file = cdflib.CDF(file_name)
                        cdf_info = cdf_file.cdf_info()
                        all_cdf_variables = cdf_info['rVariables'] + cdf_info['zVariables']
                        if 'image_raw' in all_cdf_variables:
                            var_string = 'image_raw'
                            var_properties = cdf_file.varinq(var_string)
                            if 'Data_Type_Description' in var_properties:
                                original_datatype_string = var_properties['Data_Type_Description']
                                if original_datatype_string == 'CDF_INT4':
                                    image_y_transpose = image_y_transpose.astype(np.int32)
                                elif original_datatype_string == 'CDF_UINT1':
                                    image_y_transpose = image_y_transpose.astype(np.uint8)
                                elif original_datatype_string == 'CDF_UINT2':
                                    image_y_transpose = image_y_transpose.astype(np.uint16)
                                elif original_datatype_string == 'CDF_UINT4':
                                    image_y_transpose = image_y_transpose.astype(np.uint32)

                        get_metadata_vars = get_data(current_tplot_name, metadata=True)
                        store_data(current_tplot_name,
                                   data={'x':get_data_vars[0],
                                         'y':image_y_transpose},
                                   attr_dict=get_metadata_vars)

    return loaded_data

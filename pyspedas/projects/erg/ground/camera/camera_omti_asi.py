import cdflib
import numpy as np

from pytplot import get_data, store_data, options, clip, ylim

from ...satellite.erg.load import load
from ...satellite.erg.get_gatt_ror import get_gatt_ror

from typing import List, Union, Optional

def camera_omti_asi(
    trange: List[str] = ['2020-08-01', '2020-08-02'],
    suffix: str = '',
    site: Union[str, List[str]] = 'all',
    wavelength: Union[int, List[int], str, List[str]] = [5577],
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
    Load data from OMTI all sky imagers

    Parameters
    ----------
    trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2020-08-01', '2020-08-02']

    suffix: str
            The tplot variable names will be given this suffix.  Default: ''

    site: str or list of str
            The site or list of sites to load.
            Valid values: 'abu', 'ath', 'drw', 'eur', 'gak', 'hlk', 'hus', 'isg',
            'ist', 'ith', 'kap', 'ktb','mgd', 'nai', 'nyr', 'ptk', 'rik', 'rsb',
            'sgk', 'sta', 'syo', 'trs', 'yng', 'all'
            Default: 'all'

    wavelength: str, int, list of str, or list of int
            Valid values: [5577, 5725, 6300, 7200, 7774]
            Default: [5577]

    get_support_data: bool
            If true, data with an attribute "VAR_TYPE" with a value of "support_data"
            or 'data' will be loaded into tplot. Default: False

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

    uname: str
            User name.  Default: None

    passwd: str
            Password. Default: None

    time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword. Default: False

    ror: bool
            If set, print PI info and rules of the road. Default: True

    force_download: bool
        Download file even if local version is more recent than server version
        Default: False

    Returns
    -------
    None

    Examples
    ________

    >>> import pyspedas
    >>> omti_vars=pyspedas.projects.erg.camera_omti_asi(site='ath', trange=['2020-01-20','2020-01-21'])
    >>> print(omti_vars)

    """
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

    new_cdflib = False
    if cdflib.__version__ > "0.4.9":
        new_cdflib = True
    else:
        new_cdflib = False

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
                            varformat=varformat, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd, force_download=force_download)
            
            if notplot:
                loaded_data.update(loaded_data_temp)
            else:
                loaded_data += loaded_data_temp
            if (len(loaded_data_temp) > 0) and ror:
                try:
                    gatt = get_gatt_ror(downloadonly, loaded_data)
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

                        if new_cdflib:
                            all_cdf_variables = cdf_info.rVariables + cdf_info.zVariables
                        else:
                            all_cdf_variables = cdf_info["rVariables"] + cdf_info["zVariables"]

                        if 'image_raw' in all_cdf_variables:
                            var_string = 'image_raw'
                            var_properties = cdf_file.varinq(var_string)
                            if new_cdflib:
                                original_datatype_string = var_properties.Data_Type_Description
                            else:
                                original_datatype_string = var_properties["Data_Type_Description"]
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

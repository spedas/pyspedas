import numpy as np

from pytplot import get_data, store_data, options, clip, ylim

from ...satellite.erg.load import load
from ...satellite.erg.get_gatt_ror import get_gatt_ror

from typing import List, Union, Optional, Dict, Any

def gmag_isee_fluxgate(
    trange: List[str] = ['2020-08-01', '2020-08-02'],
    suffix: str = '',
    site: Union[str, List[str]] = 'all',
    datatype: Union[str, List[str]] = 'all',
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
    force_download=False,
) -> Union[Dict, None, List[Union[str, Any]]]:
    """
    Load data from ISEE Fluxgate Magnetometers

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
            Valid values: 'msr', 'rik', 'kag', 'ktb', 'lcl', 'mdm', 'tew', 'all'
            Default: ['all']

    datatype: str or list of str
            The data types to load. Valid values: '64hz', '1sec', '1min', '1h', 'all'
            Default: 'all'

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

    Examples
    ________

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> fluxgate_vars=pyspedas.projects.erg.gmag_isee_fluxgate(trange=['2020-08-01','2020-08-02'], site='all')
    >>> tplot('isee_fluxgate_mag_ktb_1min_hdz')

    """
    site_code_all = ['msr', 'rik', 'kag', 'ktb', 'lcl', 'mdm', 'tew']
    tres_all=['64hz', '1sec', '1min', '1h']
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

    if '64' in datatype:
        index = np.where(np.array(datatype) == '64')[0][0]
        datatype[index] = '64hz'
    elif  '1s' in datatype:
        index = np.where(np.array(datatype) == '1s')[0][0]
        datatype[index] = '1sec'
    elif  '1m' in datatype:
        index = np.where(np.array(datatype) == '1m')[0][0]
        datatype[index] = '1min'
    elif  '1hr' in datatype:
        index = np.where(np.array(datatype) == '1hr')[0][0]
        datatype[index] = '1h'

    
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

    prefix = 'isee_fluxgate_'
    if notplot:
        loaded_data = {}
    else:
        loaded_data = []
    for site_input in site_code:
        for data_type_in in datatype:
            fres = data_type_in
            if fres == '64hz':
                file_res = 3600.
                pathformat = 'ground/geomag/isee/fluxgate/'+fres+'/'+site_input\
                                +'/%Y/%m/isee_fluxgate_'+fres+'_'+site_input+'_%Y%m%d%H_v??.cdf'
            if fres == '1h':
                fres = '1min'
            if (fres == '1sec') or (fres == '1min'):
                file_res = 3600. * 24
                pathformat = 'ground/geomag/isee/fluxgate/'+fres+'/'+site_input\
                                +'/%Y/isee_fluxgate_'+fres+'_'+site_input+'_%Y%m%d_v??.cdf'
            
            loaded_data_temp = load(pathformat=pathformat, file_res=file_res, trange=trange, datatype=datatype, prefix=prefix, suffix='_'+site_input+suffix, get_support_data=get_support_data,
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
                    print('PI and Host PI(s):')
                    print(gatt["PI_name"])
                    print('')
                    print('Affiliations: ')
                    print(gatt["PI_affiliation"])
                    print('')
                    print('Rules of the Road for ISEE Fluxgate Data Use:')
                    for gatt_text in gatt["TEXT"]:
                        print(gatt_text)
                    print(f'{gatt["LINK_TEXT"]} {gatt["HTTP_LINK"]}')
                    print('**************************************************************************')
                except:
                    print('printing PI info and rules of the road was failed')
                
            if (not downloadonly) and (not notplot):
                if fres == '1min':
                    fres_list = ['1min', '1h']
                else:
                    fres_list = [fres]
                for fres_in in fres_list:
                    current_tplot_name = prefix+'hdz_'+fres_in+'_' + site_input+suffix
                    if current_tplot_name in loaded_data:
                        get_data_vars = get_data(current_tplot_name)
                        if get_data_vars is None:
                            store_data(current_tplot_name, delete=True)
                        else:
                            new_tplot_name = prefix+'mag_'+site_input+'_'+fres_in+'_hdz'+suffix
                            store_data(current_tplot_name, newname=new_tplot_name)
                            loaded_data.remove(current_tplot_name)
                            loaded_data.append(new_tplot_name)
                            clip(new_tplot_name, -1e+4, 1e+4)
                            get_data_vars = get_data(new_tplot_name)
                            ylim(new_tplot_name, np.nanmin(get_data_vars[1]), np.nanmax(get_data_vars[1]))
                            options(new_tplot_name, 'legend_names', ['H','D','Z'])
                            options(new_tplot_name, 'Color', ['b', 'g', 'r'])
                            options(new_tplot_name, 'ytitle', '\n'.join(new_tplot_name.split('_')))


    return loaded_data

import cdflib
import numpy as np

from pyspedas import tnames
from pytplot import get_data, store_data, options, clip, ylim, zlim

from ...satellite.erg.load import load


def isee_vlf(
    trange=['2017-03-30/12:00:00', '2017-03-30/15:00:00'],
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
    cal_gain=False
):

    site_code_all = ['ath', 'gak', 'hus', 'ist', 'kap', 'mam', 'nai']

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
        prefix='isee_vlf_'+site_input+'_'
        file_res = 3600.
        pathformat = 'ground/vlf/'+site_input\
                        +'/%Y/%m/isee_vlf_'+site_input+'_%Y%m%d%H_v??.cdf'

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
                        cdf_file = cdflib.CDF(loaded_data_temp[0])
                        gatt = cdf_file.globalattsget()
                    else:
                        gatt = get_data(loaded_data_temp[0], metadata=True)['CDF']['GATT']
                elif isinstance(loaded_data_temp, dict):
                    gatt = loaded_data_temp[list(loaded_data_temp.keys())[0]]['CDF']['GATT']
                print('**************************************************************************')
                print(gatt["Logical_source_description"])
                print('')
                print(f'Information about {gatt["Station_code"]}')
                print(f'PI {gatt["PI_name"]}')
                print('')
                print(f'Affiliations: {gatt["PI_affiliation"]}')
                print('')
                print('Rules of the Road for ISEE VLF Data Use:')
                print('')
                for gatt_text in gatt["TEXT"]:
                    print(gatt_text)
                print({gatt["LINK_TEXT"]})
                print('**************************************************************************')
            except:
                print('printing PI info and rules of the road was failed')
            
        if (not downloadonly) and (not notplot):
            t_plot_name_list = list(set(tnames([prefix+'ch1'+suffix, 
                                    prefix+'ch2'+suffix])).intersection(loaded_data))
            options(t_plot_name_list, 'zlog', 1)
            options(t_plot_name_list, 'ytitle', 'Frequency [Hz]')
            options(t_plot_name_list, 'ysubtitle','')
            if not cal_gain:
                options(t_plot_name_list, 'ztitle', 'V^2/Hz')
            else:
                print('Calibrating the gain of VLF antenna system...')
                file_name = get_data(t_plot_name_list[0], metadata=True)['CDF']['FILENAME']
                if isinstance(file_name, list):
                    file_name = file_name[0]
                cdf_file = cdflib.CDF(file_name)
                
                ffreq=cdf_file.varget('freq_vlf')
                gain_ch1=cdf_file.varget('amplitude_cal_vlf_ch1')
                gain_ch2=cdf_file.varget('amplitude_cal_vlf_ch2')

                gain_ch1_mod = np.interp(ffreq, gain_ch1[0], gain_ch1[1]) * 1.e-9
                gain_ch2_mod = np.interp(ffreq, gain_ch2[0], gain_ch2[1]) * 1.e-9

                t_plot_name = prefix+'ch1' + suffix
                tmp1 = get_data(t_plot_name)
                if tmp1 is not None:
                    tmp1_metadata = get_data(t_plot_name, metadata=True)
                    tmp1_y = tmp1[1] / gain_ch1_mod/gain_ch1_mod
                    store_data(t_plot_name,
                                data={'x':tmp1[0],
                                      'y':tmp1_y,
                                      'v':tmp1[2]},
                                attr_dict=tmp1_metadata)

                t_plot_name = prefix+'ch2' + suffix
                tmp2 = get_data(t_plot_name)
                if tmp2 is not None:
                    tmp2_metadata = get_data(t_plot_name, metadata=True)
                    tmp2_y = tmp1[1] / gain_ch2_mod/gain_ch2_mod
                    store_data(t_plot_name,
                                data={'x':tmp2[0],
                                      'y':tmp2_y,
                                      'v':tmp2[2]},
                                attr_dict=tmp2_metadata)

                options(t_plot_name_list, 'ztitle', 'nT^2/Hz')



    return loaded_data

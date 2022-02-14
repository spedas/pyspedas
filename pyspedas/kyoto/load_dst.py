
import requests
from pyspedas import time_double
from pyspedas import time_clip as tclip
from pyspedas.utilities.dailynames import dailynames
from pytplot import store_data, options

def dst(trange=None, time_clip=True, remote_data_dir='http://wdc.kugi.kyoto-u.ac.jp/', suffix=''):
    """
    Loads Dst data from the Kyoto servers. 

    Parameters
    -----------
        trange: list of str
            Time range to load

        time_clip: bool
            If set, time the data to the requested trange

        remote_data_dir: str
            Remote data server at Kyoto

        suffix: str
            Suffix to append to the output variable's name

    Acknowledgment
    ----------------
        The DST data are provided by the World Data Center for Geomagnetism, Kyoto, and
        are not for redistribution (http://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
        the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus
        [RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to
        make the Dst index available.
    
    Returns
    --------
        Name of the tplot variable created.
    """

    if trange is None:
        print('trange keyword required to download data.')
        return

    file_names = dailynames(file_format='%Y%m/index.html', trange=trange)

    if file_names is None:
        print('No files found for this trange.')
        return
        
    times = []
    data = []
    datatype = ''

    # Final files
    for filename in file_names:
        html_text = requests.get(remote_data_dir + 'dst_final/' + filename).text
        file_times, file_data = parse_html(html_text, year=filename[:4], month=filename[4:6])
        times.extend(file_times)
        data.extend(file_data)
        if len(file_times) != 0:
            datatype = 'Final'

    # Provisional files
    for filename in file_names:
        html_text = requests.get(remote_data_dir + 'dst_provisional/' + filename).text
        file_times, file_data = parse_html(html_text, year=filename[:4], month=filename[4:6])
        times.extend(file_times)
        data.extend(file_data)
        if len(file_times) != 0:
            datatype = 'Provisional'

    # Real Time files
    for filename in file_names:
        html_text = requests.get(remote_data_dir + 'dst_realtime/' + filename).text
        file_times, file_data = parse_html(html_text, year=filename[:4], month=filename[4:6])
        times.extend(file_times)
        data.extend(file_data)
        if len(file_times) != 0:
            datatype = 'Real Time'

    if len(times) == 0:
        print('No data found.')
        return

    store_data('kyoto_dst'+suffix, data={'x': times, 'y': data})

    if time_clip:
        tclip('kyoto_dst'+suffix, trange[0], trange[1], suffix='')

    options('kyoto_dst'+suffix, 'ytitle', 'Dst (' + datatype + ')')

    print('**************************************************************************************')
    print('The DST data are provided by the World Data Center for Geomagnetism, Kyoto, and')
    print(' are not for redistribution (http://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank')
    print(' the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus')
    print(' [RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to')
    print(' make the Dst index available.')
    print('**************************************************************************************')

    return 'kyoto_dst'+suffix

def parse_html(html_text, year=None, month=None):
    times = []
    data = []
    # remove all of the HTML before the table
    html_data = html_text[html_text.find('Hourly Equatorial Dst Values'):]
    # remove all of the HTML after the table
    html_data = html_data[:html_data.find('<!-- vvvvv S yyyymm_part3.html vvvvv -->')]
    html_lines = html_data.split('\n')
    data_strs = html_lines[5:]
    # loop over days
    for day_str in data_strs:
        # the first element of hourly_data is the day, the rest are the hourly Dst values
        hourly_data = day_str.split()
        if len(hourly_data[1:]) != 24:
            continue
        for idx, dst_value in enumerate(hourly_data[1:]):
            times.append(time_double(year + '-' + month + '-' + hourly_data[0] + '/' + str(idx) + ':30'))
            data.append(float(dst_value))

    return (times, data)

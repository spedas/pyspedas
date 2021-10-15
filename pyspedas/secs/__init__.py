"""
@Author: Xin Cao, Xiangning Chu, University of Colorado Boulder
This version: For Machine Learning purpose, unlike store the data as Py-tplot variables,
this function is designed to read EICS or SECS data, and return it as a pandas dataframe.
"""

from .load import load
import numpy as np
import pandas as pd
import time
from pyspedas.utilities.time_double import time_double
import logging


def data(trange=['2012-11-05/00:00:00', '2012-11-06/00:00:00'], resolution=10, dtype='EICS', no_download = False, downloadonly = False, out_type = 'np'):
    """
    This function loads SECS/EICS data

    Parameters
    ----------
        trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        resolution: the resolution of the data in seconds, the default is 10s.

        dtype: str
            Data type; valid options: 'EICS' or 'SECS'

        no_download: bool
            Set this flag not to duplicately download the data files.

        downloadonly: bool
            Set this flag only download the data but not read.

        out_type: str
            Set the type of the return/output to be
            'df' (pandas dataframe), 'np' (numpy array) or 'dc' (dictionary).
    Returns
    ----------
        list of str of downloaded filenames (if downloadonly == True)
        or
        the data which is read from the downloaded files..
    """
    return load(trange = trange, resolution=resolution, dtype = dtype, no_download = no_download, downloadonly = downloadonly, out_type = out_type)


def read_data_files(out_files = None, dtype = None, out_type = 'np'):
    """
    Read data on a daily basis with a 10-secs or other resolution
    :param out_files: the string list of the downloaded data files' path.
    :param out_type: the return type: 'np': numpy array; 'df': pandas dataframe; 'dc': dictionary
    :param dtype: the data which will be read ('EICS' or 'SECS')
    :return: a numpy nd-array acrossing one or multiple days.
    """
    file_names_arr_Dir = out_files
    start_time = time.time()
    # Reading the data at each time stamp (per resolution secs) on one specific date.

    # input the data into one pd data frame. (four columns)
    if out_type == 'df':
        if dtype == 'EICS':
            colnames = ['latitude', 'longitude', 'Jx', 'Jy']
        if dtype == 'SECS':
            colnames = ['latitude', 'longitude', 'J']
        data_all = []
        for idx, file in enumerate(file_names_arr_Dir):
            df = pd.read_csv(file, header=None, sep='\s+', skiprows=0, names=colnames)
            df['datetime'] = file[-19:-4]
            data_all.append(df)
        output = pd.concat(data_all, axis=0, ignore_index=True)
    elif out_type == 'np':
        latitude = []
        longitude = []
        date_time = []
        if dtype == 'EICS':
            Jx = []
            Jy = []
            for file in file_names_arr_Dir:
                di = np.loadtxt(file)
                num_row = np.shape(di)[0]
                latitude.append(di[:, 0])
                longitude.append(di[:, 1])
                Jx.append(di[:, 2])
                Jy.append(di[:, 3])
                date_time.append(file[-19:-4])
            latitude = np.vstack(latitude)
            longitude = np.vstack(longitude)
            Jx = np.vstack(Jx)
            Jy = np.vstack(Jy)
            date_time = np.array(date_time)
            date_time = time_double(date_time)
            data_all = {'time': date_time, 'latitude': latitude, 'longitude': longitude, 'Jx': Jx, 'Jy': Jy}


        if dtype == 'SECS':
            J = []
            for file in file_names_arr_Dir:
                di = np.loadtxt(file)
                num_row = np.shape(di)[0]
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                J.extend(di[:, 2])
                date_time.extend(np.full((num_row, 1), file[-19:-4]))
            num_row2 = len(latitude)
            data_all = np.array([latitude, longitude, J, date_time])
            data_all = data_all.reshape([4, num_row2])
            data_all = np.transpose(data_all)

        output = data_all
    elif out_type == 'dc':
        data_dict = {}
        latitude = []
        longitude = []
        Jx = []
        Jy = []
        J = []
        for file in file_names_arr_Dir:
            di = np.loadtxt(file)
            if dtype == 'EICS':
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                Jx.extend(di[:, 2])
                Jy.extend(di[:, 3])
            if dtype == 'SECS':
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                J.extend(di[:, 2])
        data_dict['latitude'] = latitude
        data_dict['longitude'] = longitude
        if dtype == 'EICS':
            data_dict['Jx'] = Jx
            data_dict['Jy'] = Jy
        if dtype == 'SECS':
            data_dict['J'] = J
        output = data_dict
    else:
        raise TypeError("%r are invalid keyword arguments" % out_type)
    logging.info('running time of output ' + out_type + ": --- %s seconds ---" % (time.time() - start_time))

    return output


def data_selecttime(data = None, dtime = None):
    Data_Days = data
    tp = dtime
    datetime_tp = tp[0:4] + tp[5:7] + tp[8:10] + '_' + tp[11:13] + tp[14:16] + tp[17:19]
    Data_Days_time = Data_Days.loc[Data_Days['datetime'] == datetime_tp]
    return Data_Days_time

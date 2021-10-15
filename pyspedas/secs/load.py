"""
@Author : Xin Cao, Xiangning Chu, Sep. 2021.
@University of Colorado Boulder
"""
import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip

from .config import CONFIG
import zipfile
import pyspedas
import logging

def load(trange = None, resolution=10, dtype = 'EICS', no_download = False, downloadonly = False, out_type = 'np'):
    """
    This function loads SECS/EICS data; this function is not meant
    to be called directly; instead, see the wrapper:
        pyspedas.secs.data

    """

    if dtype == 'EICS' or dtype == 'SECS':
        pathformat_prefix = dtype + '/%Y/%m/'
        pathformat_zip = pathformat_prefix + dtype + '%Y%m%d.zip'
        pathformat_unzipped = pathformat_prefix + '%d/' + dtype + '%Y%m%d_%H%M%S.dat'

    else:
        raise TypeError("%r are invalid keyword arguments" % dtype)

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat_zip, trange=trange)

    out_files = []

    files_zip = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'],
                     local_path=CONFIG['local_data_dir'], no_download=no_download)


    if files_zip is not None:
        for rf_zip in files_zip:
            foldername_unzipped = rf_zip[0:-16] + rf_zip[-6:-4]
            if not os.path.isdir(foldername_unzipped):
                logging.info('Start unzipping: '+ rf_zip + '  ------')
                with zipfile.ZipFile(rf_zip, 'r') as zip_ref:
                    zip_ref.extractall(rf_zip[0:-16])
            else:
                logging.info('Unzipped folder: ' + foldername_unzipped + ' existed, skip unzipping  ------')

    if files_zip is not None:
        for file in files_zip:
            out_files.append(file)

    out_files = sorted(out_files)
    #print('out_files: ', out_files)

    if downloadonly:
        return out_files

    remote_names_unzipped = dailynames(file_format=pathformat_unzipped, trange=trange, res=resolution)
    #print('remote_names_res: ', remote_names_res)
    out_files_unzipped = [CONFIG['local_data_dir'] + rf_res for rf_res in remote_names_unzipped]
    #print('out_files_unzipped: ', out_files_unzipped)
    data_vars = pyspedas.secs.read_data_files(out_files=out_files_unzipped, dtype = dtype, out_type = out_type)


    return data_vars #tvars





"""
@Author : Xin Cao, Xiangning Chu, Sep. 2021.
@University of Colorado Boulder
"""
import os
import numpy as np
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip

from .config import CONFIG
import zipfile
import pyspedas
import logging
import shutil
import gzip

def load(trange = None, resolution=10, dtype = None, no_download = False, downloadonly = False, out_type = 'np', save_pickle = False):
    """
    This function loads SECS/EICS data; this function is not meant
    to be called directly; instead, see the wrapper:
        pyspedas.secs.data

    """

    if dtype == 'EICS' or dtype == 'SECS':
        pathformat_prefix = dtype + '/%Y/%m/'
        pathformat_zip = pathformat_prefix + dtype + '%Y%m%d.zip'
        pathformat_gz = pathformat_prefix + dtype + '%Y%m%d.zip.gz' # only 2007!
        pathformat_unzipped = pathformat_prefix + '%d/' + dtype + '%Y%m%d_%H%M%S.dat'

    else:
        raise TypeError("%r are invalid keyword arguments" % dtype)

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat_zip, trange=trange)
    remote_names_gz = dailynames(file_format=pathformat_gz, trange=trange)
    remote_names_gz = [s for s in remote_names_gz if s[-15:-11] == '2007']

    out_files = []
    out_files_zip = []

    files_zip = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'],
                     local_path=CONFIG['local_data_dir'], no_download=no_download)
    files_gz = download(remote_file=remote_names_gz, remote_path=CONFIG['remote_data_dir'],
                         local_path=CONFIG['local_data_dir'], no_download=no_download)
    files_zip = files_zip + files_gz

    if files_zip is not None:
        for rf_zip_zero in files_zip:
            if rf_zip_zero.endswith('.gz'):
                rf_zip = rf_zip_zero[0:-3]
                # unzip .gz file to .zip file
                with gzip.open(rf_zip_zero, 'rb') as f_in:
                    with open(rf_zip, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            elif rf_zip_zero.endswith('.zip'):
                rf_zip = rf_zip_zero
            else:
                rf_zip = rf_zip_zero
            out_files_zip.append(rf_zip)
            #print('Start for unzipping process ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            foldername_unzipped = rf_zip[0:-19] + rf_zip[-8:-6] + '/' + rf_zip[-6:-4]
            #print('foldername_unzipped-------: ', foldername_unzipped)
            ### add??????
            if not os.path.isdir(foldername_unzipped):
                logging.info('Start unzipping: '+ rf_zip + '  ------')
                with zipfile.ZipFile(rf_zip, 'r') as zip_ref:
                    zip_ref.extractall(rf_zip[0:-16])
                if not os.path.isdir(foldername_unzipped):
                    # for the case of unzipping directly without the %d folder made.
                    # make %d folder
                    os.makedirs(foldername_unzipped)
                    # move .dat files
                    sourcepath = rf_zip[0:-16]
                    sourcefiles = os.listdir(sourcepath)
                    destinationpath = foldername_unzipped
                    logging.info('start to move files: --------------')
                    for file in sourcefiles:
                        if rf_zip[-16:-4] in file and file.endswith('.dat'):
                            shutil.move(os.path.join(sourcepath, file), os.path.join(destinationpath, file))

            else:
                logging.info('Unzipped folder: ' + foldername_unzipped + ' existed, skip unzipping  ------')

    if files_zip is not None:
        for file in files_zip:
            out_files.append(file)
    out_files = sorted(out_files)

    if out_files_zip is not None:
        out_files_zip = list(set(out_files_zip))
        out_files_zip = sorted(out_files_zip)


    if downloadonly:
        return out_files_zip #out_files

    remote_names_unzipped = dailynames(file_format=pathformat_unzipped, trange=trange, res=resolution)
    """
    files_unzipped = download(remote_file=remote_names_unzipped, remote_path=CONFIG['remote_data_dir'],
                         local_path=CONFIG['local_data_dir'], no_download=True)
    """
    remote_names_unzipped_existed = [rnud for rnud in remote_names_unzipped for ofz in out_files_zip if ofz[-16:-4] in rnud]
    remote_names_unzipped = remote_names_unzipped_existed
    out_files_unzipped = [CONFIG['local_data_dir'] + rf_res for rf_res in remote_names_unzipped]
    out_files_unzipped = sorted(out_files_unzipped)

    if out_files_unzipped == []:
        data_vars = []
    else:
        data_vars = pyspedas.secs.read_data_files(out_files=out_files_unzipped, dtype = dtype, out_type = out_type, save_pickle = save_pickle)
        #print('data_vars: ', data_vars, np.shape(data_vars))


    return data_vars #tvars





"""
@Author: Xin Cao, Xiangning Chu, University of Colorado Boulder
@Created in Sep. 2021.

In this config.py file, the following environment variables need to be defined in advance.
@LOCAL_SECS_DATA_DIR: the local path where the SECS/EICS data will be downloaded and stored.
@PLOTS_SECS_DIR: the local path where the vector and contour plots of SECS/EICS data will be saved.
"""

import os
CONFIG ={'local_data_dir': '',
         'remote_data_dir': 'http://vmo.igpp.ucla.edu/data1/SECS/'}

# override local data directory with environment variables
if os.environ.get('LOCAL_SECS_DATA_DIR'):
    CONFIG['local_data_dir']  = os.environ['LOCAL_SECS_DATA_DIR'] # self-defined, e.g. '/Users/cao/Documents/Data_N_Res/data_local'

if os.environ.get('PLOTS_SECS_DIR'):
    CONFIG['plots_dir']  = os.environ['PLOTS_SECS_DIR'] # self-defined, e.g. '/Users/cao/Documents/Data_N_Res/plots'

if os.environ.get('CONDA_PREFIX'):
    env_name = os.environ['CONDA_PREFIX']
    os.environ['PROJ_LIB'] = env_name + '/share/proj'

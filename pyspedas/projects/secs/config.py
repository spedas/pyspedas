"""
@Author: Xin Cao, Xiangning Chu, University of Colorado Boulder
@Created in Sep. 2021.

In this config.py file, the following environment variables need to be defined in advance.
@LOCAL_SECS_DATA_DIR: the local path where the SECS/EICS data will be downloaded and stored.
@PLOTS_SECS_DIR: the local path where the vector and contour plots of SECS/EICS data will be saved.
"""

import os

CONFIG = {
    "local_data_dir": "secs_data/",
    "plots_dir": "secs_plots/",
    "remote_data_dir": "http://vmo.igpp.ucla.edu/data1/SECS/",
    "remote_data_dir_spdf": "https://spdf.gsfc.nasa.gov/pub/data/aaa_special-purpose-datasets/spherical-elementary-and-equivalent-ionospheric-currents-weygand/",
}

# override local data directory with environment variables
if os.environ.get("LOCAL_SECS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ[
        "LOCAL_SECS_DATA_DIR"
    ]  # self-defined, e.g. '/Users/cao/Documents/Data_N_Res/data_local'
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "secs"])

if os.environ.get("PLOTS_SECS_DIR"):
    CONFIG["plots_dir"] = os.environ[
        "PLOTS_SECS_DIR"
    ]  # self-defined, e.g. '/Users/cao/Documents/Data_N_Res/plots'
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["plots_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "secs_plots"])

if os.environ.get("CONDA_PREFIX"):
    env_name = os.environ["CONDA_PREFIX"]
    os.environ["PROJ_LIB"] = env_name + "/share/proj"

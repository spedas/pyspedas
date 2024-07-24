from .load import load
import numpy as np
import pandas as pd
from pytplot import store_data, options
from pytplot import time_double
from pyspedas.cotrans.xyz_to_polar import xyz_to_polar


def load_csv_file(filenames, cols=None):
    """
    Loads a list of CSV/txt files into pandas data frames
    """
    if not isinstance(filenames, list):
        filenames = [filenames]
    df = pd.concat((pd.read_csv(f, header=0, sep=r'\s+', dtype=str, names=cols) for f in filenames), ignore_index=True)
    return df

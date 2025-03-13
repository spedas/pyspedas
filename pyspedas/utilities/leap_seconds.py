import os
import datetime
import pandas as pd
import numpy as np
from pyspedas.utilities.download import download
from pytplot import time_double


def load_leap_table(reload=False):
    """
        Loads the leap second table for converting TAI to unix times

    Parameters
    -----------
        reload: bool
            Re-load the leap second table, even if it exists locally.

            This shouldn't be needed until at least 2035:
                https://www.scientificamerican.com/article/the-leap-seconds-time-is-up-world-votes-to-stop-pausing-clocks/

    Returns
    ---------
        dict
            A dictionary containing 'dates' with array of Julian dates corresponding to the leap seconds in the 'leaps' array

    """
    if os.environ.get('CDF_LEAPSECONDSTABLE') is not None:
        table_file = os.environ.get('CDF_LEAPSECONDSTABLE')
    elif os.environ.get('SPEDAS_DATA_DIR') is not None:
        table_file = os.path.join(os.environ.get('SPEDAS_DATA_DIR'), 'CDFLeapSeconds.txt')
    else:
        table_file = os.path.join('data', 'CDFLeapSeconds.txt')

    table_dir = os.path.dirname(table_file)

    if reload or not os.path.exists(table_file):
        downloaded = download(remote_path='https://cdf.gsfc.nasa.gov/html/',
                              remote_file='CDFLeapSeconds.txt',
                              local_path=table_dir)

    cols = ['Year', 'Month', 'Day', 'LS', 'Drift1','Drift2']
    table = pd.read_csv(table_file,
                        sep=r'\s+',
                        dtype=str,
                        names=cols,
                        comment=';',
                        skipinitialspace=True,
                        index_col=False)

    leap_dates = table['Year'].to_numpy() + '-' + table['Month'].to_numpy() + '-' + table['Day'].to_numpy()
    leap_dates = time_double(leap_dates)
    juls = np.array(leap_dates)/86400.0 + datetime.date(1970, 1, 1).toordinal() + 1721424.5

    return {'leaps': np.float64(table['LS'].to_numpy()),
            'juls': juls}

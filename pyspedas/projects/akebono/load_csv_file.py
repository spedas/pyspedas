import pandas as pd

# This routine was originally in akebono/__init__.py.  If you need to see the history of this routine before
# it was moved to its own file, please check the history for __init__.py.

def load_csv_file(filenames, cols=None, gz=False):
    """
    Loads a list of CSV/txt files into pandas data frames
    """
    if not isinstance(filenames, list):
        filenames = [filenames]
    if gz:
        df = pd.concat((pd.read_csv(f, header=0, sep=r'\s+', dtype=str, names=cols, compression='gzip') for f in filenames), ignore_index=True)
    else:
        df = pd.concat((pd.read_csv(f, header=0, sep=r'\s+', dtype=str, names=cols) for f in filenames), ignore_index=True)
    return df

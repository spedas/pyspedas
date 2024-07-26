from pyspedas.utilities.datasets import find_datasets

# This routine was moved out of __init__.py.  Please see that file for previous revision history.

def datasets(instrument=None, label=True):
    return find_datasets(mission='TWINS', instrument=instrument, label=label)

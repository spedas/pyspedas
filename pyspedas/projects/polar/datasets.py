from pyspedas.utilities.datasets import find_datasets

# This routine was originally in polar/__init__.py.  If you need to see the history of this routine before
# it was moved to its own file, please check the history for __init__.py.

def datasets(instrument=None, label=True):
    return find_datasets(mission='Polar', instrument=instrument, label=label)

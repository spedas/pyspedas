from .load import load
from pytplot import options
from pyspedas.utilities.datasets import find_datasets

# This routine was originally in ace/__init__.py, until being moved to its own file.
# Please refer to __init__.py if you need to see the revision history before it was moved.

def datasets(instrument=None, label=True):
    return find_datasets(mission='ACE', instrument=instrument, label=label)

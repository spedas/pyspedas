from .load import load
from pytplot import options
from pyspedas.utilities.datasets import find_datasets


def datasets(instrument=None, label=True):
    return find_datasets(mission='ACE', instrument=instrument, label=label)

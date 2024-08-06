from .load import load
from pyspedas.utilities.datasets import find_datasets


def datasets(instrument=None, label=True):
    return find_datasets(mission='Wind', instrument=instrument, label=label)

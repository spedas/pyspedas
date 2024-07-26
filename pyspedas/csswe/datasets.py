from pyspedas.utilities.datasets import find_datasets


def datasets(instrument=None, label=True):
    out = find_datasets(mission='Smallsats/Cubesats', instrument='csswe', label=label)
    return out

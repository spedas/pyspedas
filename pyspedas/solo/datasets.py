from pyspedas.utilities.datasets import find_datasets


def datasets(instrument=None, label=True):
    return find_datasets(mission='Solar Orbiter', instrument=instrument, label=label)

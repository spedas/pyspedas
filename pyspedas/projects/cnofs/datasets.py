from pyspedas.utilities.datasets import find_datasets

# Refer to __init__.py for revision history before load routines split out into separate files

def datasets(instrument=None, label=True):
    return find_datasets(mission='CNOFS', instrument=instrument, label=label)
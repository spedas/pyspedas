from pyspedas.utilities.datasets import find_datasets

# Refer to __init__.py for revision history before the function definitions were split out

def datasets(instrument=None, label=True):
    out = find_datasets(mission='Smallsats/Cubesats', instrument='csswe', label=label)
    return out

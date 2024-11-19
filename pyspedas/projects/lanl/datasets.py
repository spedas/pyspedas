from pyspedas import find_datasets

# This routine was originally in lanl/__init__.py.
def datasets(instrument=None, label=True):
    return find_datasets(mission="LANL", instrument=instrument, label=label)

from pyspedas import find_datasets

# This routine was originally in poes/__init__.py.
def datasets(instrument=None, label=True):
    return find_datasets(mission='POES', instrument='sem2', label=label)

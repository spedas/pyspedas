from .load import load
from functools import update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial
from pyspedas.utilities.datasets import find_datasets


# Define partial wrappers for other load routines, fixing the instrument parameter
# 'better_partial' works better with PyCharm autocompletion than functools.partial
# update_wrapper() is necessary for help() to show info for the wrapped function,
# rather than the partial() object.

mag = better_partial(load, instrument="mag")
update_wrapper(mag, load)
nacs = better_partial(load, instrument="nacs")
update_wrapper(nacs, load)
rpa = better_partial(load, instrument="rpa")
update_wrapper(rpa, load)
fpi = better_partial(load, instrument="fpi")
update_wrapper(fpi, load)
idm = better_partial(load, instrument="idm")
update_wrapper(idm, load)
wats = better_partial(load, instrument="wats")
update_wrapper(wats, load)
vefi = better_partial(load, instrument="vefi")
update_wrapper(vefi, load)
lang = better_partial(load, instrument="lang")
update_wrapper(lang, load)
datasets = better_partial(find_datasets, mission="Dynamics Explorer", label=True)
update_wrapper(datasets, find_datasets)

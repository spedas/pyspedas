from functools import update_wrapper
from .load import load
from pyspedas.utilities.datasets import find_datasets
from pyspedas.utilities.pyspedas_functools import better_partial


# Define partial wrappers for other load routines, fixing the instrument parameter
# 'better_partial' works better with PyCharm autocompletion than functools.partial
# update_wrapper() is necessary for help() to show info for the wrapped function,
# rather than the partial() object.

mag = better_partial(load, instrument="mag")
update_wrapper(mag, load)
fc = better_partial(load, instrument="fc")
update_wrapper(fc, load)
orb = better_partial(load, instrument="orb")
update_wrapper(orb, load)
att = better_partial(load, instrument="att")
update_wrapper(att, load)
all = better_partial(load, instrument="all")
update_wrapper(all, load)

datasets = better_partial(find_datasets, mission="DSCOVR", label=True)
update_wrapper(datasets, find_datasets)

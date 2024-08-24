from functools import update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial
from .load import load
from pyspedas.utilities.datasets import find_datasets


# Define partial wrappers for other load routines, fixing the instrument parameter
# 'better_partial' works better with PyCharm autocompletion than functools.partial
# update_wrapper() is necessary for help() to show info for the wrapped function,
# rather than the partial() object.

dcf = better_partial(load, instrument="dcf")
update_wrapper(dcf, load)
acf = better_partial(load, instrument="acf")
update_wrapper(acf, load)
esa = better_partial(load, instrument="esa")
update_wrapper(esa, load)
teams = better_partial(load, instrument="teams")
update_wrapper(teams, load)

datasets = better_partial(find_datasets, mission="FAST", label=True)
update_wrapper(datasets, find_datasets)

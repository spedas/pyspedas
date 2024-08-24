from functools import update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial
from .load import load
from pyspedas.utilities.datasets import find_datasets


# Define partial wrappers for other load routines, fixing the instrument parameter
# 'better_partial' works better with PyCharm autocompletion than functools.partial
# update_wrapper() is necessary for help() to show info for the wrapped function,
# rather than the partial() object.

mam = better_partial(load, instrument="mam")
update_wrapper(mam, load)
edi = better_partial(load, instrument="edi")
update_wrapper(edi, load)
epi = better_partial(load, instrument="epi")
update_wrapper(epi, load)
ici = better_partial(load, instrument="ici")
update_wrapper(ici, load)
pcd = better_partial(load, instrument="pcd")
update_wrapper(pcd, load)
sfd = better_partial(load, instrument="sfd")
update_wrapper(sfd, load)

datasets = better_partial(find_datasets, mission="Equator-S", label=True)
update_wrapper(datasets, find_datasets)

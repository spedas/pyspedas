"""DMSP space physics data loaders."""
from functools import update_wrapper

from pyspedas.utilities.pyspedas_functools import better_partial
from pyspedas.utilities.datasets import find_datasets
from .load import load

ssj = better_partial(load, instrument='ssj')
update_wrapper(ssj, load)
ssies = better_partial(load, instrument='ssies')
update_wrapper(ssies, load)
ssm = better_partial(load, instrument='ssm')
update_wrapper(ssm, load)
datasets = better_partial(find_datasets, mission='DMSP', label=True)
update_wrapper(datasets, find_datasets)

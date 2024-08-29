from functools import partial
from .load import load
from pyspedas.utilities.datasets import find_datasets

# Define another name for load
data = load

# retrieve datasets from the ACE mission with a focus on OMNI instrument data
datasets = partial(find_datasets, mission="ACE", instrument="OMNI")

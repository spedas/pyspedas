# Example of getting MTH5 datasets availability

from pyspedas.mth5.utilities import datasets

# Getting a dictionary of valid datasets for a given time range
valid_dataset = datasets(trange=["2015-06-22", "2015-06-23"])

# List of all the networks
nets = valid_dataset.keys()
print("Networks: ", nets)

# List of all the stations for a given network
net = list(nets)[0]
print("Stations: ", valid_dataset[net].keys())

# Getting data availability for a given network and station in 2015
res = datasets(trange=["2015-01-01", "2016-01-01"], network="4P", station="TNU48")
print("Data availability", res)


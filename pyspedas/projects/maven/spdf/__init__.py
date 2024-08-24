from functools import partial
from .load import load

# Alias for load function with instrument parameter set
mag = partial(load, instrument="mag")
swea = partial(load, instrument="swea")
swia = partial(load, instrument="swia")
static = partial(load, instrument="static")
sep = partial(load, instrument="sep")
kp = partial(load, instrument="kp")

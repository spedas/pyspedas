from .load import load, loadr
from .load_orbit import load_orbit
from functools import partial

# Define an alias to the load function
orbit = load_orbit
fgm = partial(load, instrument="fgm")
eps = partial(load, instrument="eps")
epead = partial(load, instrument="epead")
maged = partial(load, instrument="maged")
magpd = partial(load, instrument="magpd")
hepad = partial(load, instrument="hepad")
xrs = partial(load, instrument="xrs")
euvs = partial(load, instrument="euvs")
mag = partial(load, instrument="mag")
mpsh = partial(load, instrument="mpsh")
sgps = partial(load, instrument="sgps")

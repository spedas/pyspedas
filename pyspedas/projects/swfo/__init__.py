"""NOAA SWFO / SOLAR-1 in situ data loaders."""
from functools import update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial
from .load import load

mag = better_partial(load, instrument="mag")
swips = better_partial(load, instrument="swips")
stis = better_partial(load, instrument="stis")
for wrapper in (mag, swips, stis):
    update_wrapper(wrapper, load)

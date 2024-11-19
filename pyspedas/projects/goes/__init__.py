from .load import load, loadr
from .load_orbit import load_orbit
from functools import partial, update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial

# Define alias to the load function
orbit = load_orbit

# Define partial wrappers for other load routines, fixing the instrument parameter
# 'better_partial' works better with PyCharm autocompletion than functools.partial
# update_wrapper() is necessary for help() to show info for the wrapped function,
# rather than the partial() object.

fgm = better_partial(load, instrument="fgm")
update_wrapper(fgm, load)
eps = better_partial(load, instrument="eps")
update_wrapper(eps, load)
epead = better_partial(load, instrument="epead")
update_wrapper(epead,load)
maged = better_partial(load, instrument="maged")
update_wrapper(maged,load)
magpd = better_partial(load, instrument="magpd")
update_wrapper(magpd, load)
hepad = better_partial(load, instrument="hepad")
update_wrapper(hepad, load)
xrs = better_partial(load, instrument="xrs")
update_wrapper(xrs, load)
euvs = better_partial(load, instrument="euvs")
update_wrapper(euvs, load)
mag = better_partial(load, instrument="mag")
update_wrapper(mag, load)
mpsh = better_partial(load, instrument="mpsh")
update_wrapper(mpsh, load)
sgps = better_partial(load, instrument="sgps")
update_wrapper(sgps, load)

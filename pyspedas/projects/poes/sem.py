from functools import update_wrapper
from pyspedas.utilities.pyspedas_functools import better_partial
from .load import load

sem = better_partial(load, instrument="sem")
update_wrapper(sem, load)

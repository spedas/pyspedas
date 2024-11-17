from functools import partial
from typing import TypeVar

# Credit to Aidan Grant, from the comments of a Jetbrains open issue (linked below) regarding autocompletion
# of functions defined with functools.partial.  This seems to solve the issue with
# PyCharm not being able to autocomplete or show arguments for some of our load routines,
# e.g. from pyspedas.projects.goes

T = TypeVar('T')

def better_partial(func: T, *args, **kwargs) -> T:
    """
    Behaves the same as functools.partial, but works with idea's type hinting.
    @see https://youtrack.jetbrains.com/issue/PY-25698/No-proper-completion-or-parameter-info-for-partially-applied-parameters-of-functools.partial
    """
    return partial(func, *args, **kwargs)

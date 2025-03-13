"""
Displays location of source files, one line of documentation and the function name based on the request
"""

import importlib
import inspect
import itertools
import pkgutil
import sys
import io
from fnmatch import fnmatchcase

import pytplot
import pyspedas
import functools


def libs(function_name, package=None):
    """
    Search for a specified function by exact name, substring, or wildcard within a given package and its submodules.

    Parameters
    ----------
    function_name (str):
        The name or partial name of the function to search for. If "*" or "?" are found in the function name, a case-insensitive wildcard match is performed, otherwise
        function_name is treated as a substring to match.
        package (module, optional): The Python package in which to search for the function.
        Default is the pyspedas package. This should be a Python module object.

    Note
    ----

    All submodules of pyspedas and pytplot are imported during the search. The package option is
    simply narrows the search.
    The function specifically searches for functions, not classes or other objects.
    If multiple functions with the same name exist in different modules within the package, it will list them all.
    The function handles ImportError exceptions by printing an error message and
    continuing the search, except 'pytplot.QtPlotter'. pytplot.QtPlotter results in error during import and ignored

    Example
    -------

    >>> from pyspedas import libs
    >>> libs('fgm')
    >>> libs('fgm', package=pyspedas.projects.mms)

    """

    # Gate for no function_name
    if not function_name:
        return

    # Using separate functions for the wildcard and substring matching eliminates a test and branch in the inner loop

    def list_functions_substring(module, root, search_string, pacakge_obj):
        full_module_name = module.__name__
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and (search_string in name) and (pacakge_obj.__name__ in obj.__module__):
                full_name = full_module_name + '.' + name
                source_file = inspect.getsourcefile(obj)
                doc = inspect.getdoc(obj)
                first_line_of_doc = doc.split('\n')[0] if doc else "No documentation"
                print(f"Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n")
            elif isinstance(obj, functools.partial) and (search_string in name):
                original_func = obj.func
                full_name = full_module_name + '.' + name
                source_file = inspect.getsourcefile(original_func)
                doc = inspect.getdoc(original_func)
                first_line_of_doc = doc.split('\n')[0] if doc else "No documentation"
                print(f"Partial Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n")

    def list_functions_wildcard(module, root, wildcard_pattern, pacakge_obj):
        full_module_name = module.__name__
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and fnmatchcase(name.lower(), wildcard_pattern) and (pacakge_obj.__name__ in obj.__module__):
                full_name = full_module_name + '.' + name
                source_file = inspect.getsourcefile(obj)
                doc = inspect.getdoc(obj)
                first_line_of_doc = doc.split('\n')[0] if doc else "No documentation"
                print(f"Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n")
            elif isinstance(obj, functools.partial) and fnmatchcase(name.lower(), wildcard_pattern):
                original_func = obj.func
                full_name = full_module_name + '.' + name
                source_file = inspect.getsourcefile(original_func)
                doc = inspect.getdoc(original_func)
                first_line_of_doc = doc.split('\n')[0] if doc else "No documentation"
                print(f"Partial Function: {full_name}\nLocation: {source_file}\nDocumentation: {first_line_of_doc}\n")

    def traverse_modules(package, function_name, package_obj):
        # Add the module itself
        walk_packages_iterator = pkgutil.walk_packages(path=package.__path__, prefix=package.__name__ + '.')
        combined_iterator = itertools.chain(((None, package.__name__, True),), walk_packages_iterator)

        # Check for wildcard characters
        if '*' in function_name or '?' in function_name:
            wildcard=True
            # There is no 'fnmatchnocase', so lowercase the search pattern and function names before comparing
            # We'll add implicit leading and trailing '*', so any substring match will appear in the list
            wildcard_pattern = '*' + function_name.lower() + '*'
        else:
            wildcard=False
            wildcard_pattern=''

        for _, modname, ispkg in combined_iterator:
            if ispkg and 'qtplotter' not in modname.lower():
                # Save the current stdout so that we can restore it later
                original_stdout = sys.stdout

                # Redirect stdout to a dummy stream
                sys.stdout = io.StringIO()

                try:
                    module = importlib.import_module(modname)
                    if not package_obj:
                        package_obj = package

                    # Restore the original stdout
                    sys.stdout = original_stdout
                    if not wildcard:
                        list_functions_substring(module, package, function_name, package_obj)
                    else:
                        list_functions_wildcard(module, package, wildcard_pattern, package_obj)
                except ImportError as e:
                    # Restore the original stdout
                    sys.stdout = original_stdout
                    print(f"Error importing module {modname}: {e}")
                finally:
                    # Restore the original stdout
                    sys.stdout = original_stdout

    for module in [pyspedas, pytplot]:
        if not package or module.__name__ in package.__name__:
            traverse_modules(module, function_name, package)

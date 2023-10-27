from xarray_einstats import linalg
from pytplot import split_vec, join_vec

def _tvectot(tvar: str, new_name: str, join_component: bool):
    data = get_data(tvar, xarray=True)
    new_data = linalg.norm(data, dims="v_dim")
    store_data(new_name, new_data, xarray=True)
    
    if join_vec:
        join_vec(split_vec(tvar)+[new_name], new_name)
        options(new_name, 'legend_names', ['x', 'y', 'z', 'Magnitude'])
    else:
        options(new_name, 'legend_names', 'Magnitude')
    return new_name

def tvectot(tvars: str | list[str], newnames: str | list[str] = None, suffix="_mag", join_component=False) -> str | list[str]:
    """
    Computes the magnitude of a vector time series.

    Parameters
    ----------
    - tvars : Names of the tplot variables.
    - new_names: Names for the resultant magnitude tplot variables. If not provided, it appends the suffix to `tvars`.
    - suffix: The suffix to append to tensor_names to form new_names if new_names is not provided.
    - join_component: If True, the magnitude tplot variable is joined with the component tplot variables.

    Returns
    -------
    Names of the magnitude tplot variables.
    """
    tvars_type = type(tvars)
    if tvars_type == str:
        tvars = [tvars]
    if join_vec:
        suffix = "_tot"

    if newnames is None:
        newnames = [tvar + suffix for tvar in tvars]

    for tvar, newname in zip(tvars, newnames):
        _tvectot(tvar, newname, join_component)
    
    if tvars_type == str:
        return newnames[0]
    else:
        return newnames

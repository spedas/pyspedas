from .tplot_average import tplot_average


def slice2d_get_support(variable, trange, matrix=False):
    """

    """

    if variable is None:
        return

    if isinstance(variable, str):  # tplot variable
        return tplot_average(variable, trange)

    return variable

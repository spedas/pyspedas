from .tplot_average import tplot_average


def slice2d_get_support(variable, trange, matrix=False):
    """
    Retrieve user specified support data for spd_slice2d

    Input
    ------
        variable: str or float or ndarray
            Tplot variable or input data

        trange: list of float
            Time range to average over if the input is a tplot variable

    Parameters
    -----------
        matrix: ndarray
            Specifies that the input is a matrix

    Returns
    --------
        Output data (average over time range if the input is a tplot variable)
    """

    if variable is None:
        return

    if isinstance(variable, str):  # tplot variable
        return tplot_average(variable, trange)

    return variable


import logging
import pytplot
import numpy


def subtract_average(
        names,
        newname=None,
        new_names=None,
        suffix=None,
        overwrite=None,
        median=None
):
    """
    Subtracts the average or median from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    newname: str/list of str, optional
        List of new names for pytplot variables.
        Default: None. If not given, then a suffix is applied.
    new_names: str/list of str, optional (Deprecated)
        List of new names for pytplot variables.
        Default: None. If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply.
        Default: '-d'.
    overwrite: bool, optional
        If set, then pytplot variables are replaced.
        Default: None
    median: float, optional
        If it is 0 or not set, then it computes the mean.
        Otherwise, it computes the median.
        Default: None.

    Returns
    -------
    list of str
        List of new tplot variables created

    """

    # new_names is deprecated in favor of newname
    if new_names is not None:
        logging.info("subtract_average: The new_names parameter is deprecated. Please use newname instead.")
        newname = new_names

    old_names = pytplot.tnames(names)

    if len(old_names) < 1:
        logging.error('Subtract Average error: No pytplot names were provided.')
        return

    if suffix is None:
        if median:
            suffix = '-m'
        else:
            suffix = '-d'

    if overwrite is not None:
        n_names = old_names
    elif newname is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = newname

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    old_names = pytplot.tnames(names)

    for old_idx, old in enumerate(old_names):
        new = n_names[old_idx]

        if new != old:
            pytplot.tplot_copy(old, new)

        data = pytplot.data_quants[new].values
        dim = data.shape
        if median:
            if len(dim) == 1:
                data -= numpy.median(data, axis=0)
            else:
                for i in range(dim[1]):
                    data[:, i] -= numpy.median(data[:, i], axis=0)
            ptype = 'Median'
        else:
            if len(dim) == 1:
                data -= numpy.mean(data, axis=0)
            else:
                for i in range(dim[1]):
                    data[:, i] -= numpy.mean(data[:, i], axis=0)
            ptype = 'Mean'

        pytplot.data_quants[new].values = data

        logging.info('Subtract ' + ptype + ' was applied to: ' + new)

    return n_names

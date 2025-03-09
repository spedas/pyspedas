import logging
import pyspedas
import pytplot
import numpy as np


def yclip(
    names,
    ymin,
    ymax,
    flag=None,
    newname=None,
    new_names=None,
    suffix=None,
    overwrite=None,
):
    """
    Clip data and replace values with flag.

    Parameters
    ----------
    names : str or list of str
        List of tplot names.
        Allowed wildcards are ? for a single character, * from multiple characters.
    ymin : float
        Minimum value to clip.
    ymax : float
        Maximum value to clip.
    flag : float, optional
        Values outside (ymin, ymax) are replaced with this flag.
        Default is float('nan').
    newname : str or list of str, optional
        List of new names for tplot variables.
        If not given, then a suffix is applied.
    new_names : str or list of str, optional
        List of new names for tplot variables.
        If not given, then a suffix is applied.
        This parameter is deprecated.
    suffix : str, optional
        A suffix to apply. Default is '-clip'.
    overwrite : bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None
        This function works in-place and does not return a value, it creates a new tplot variable.

    Notes
    -----
    Similar to tclip.pro in IDL SPEDAS.
    This function clips y-axis data. To clip time-axis, use time_clip.

    Examples
    --------
        import numpy as np
        import pytplot
        import pyspedas

        # Create some data
        times = np.array(['2002-02-03T04:05:06', '2002-02-03T04:05:07', '2002-02-03T04:05:08'], dtype='datetime64')
        data = np.array([1.0, 2.0, 3.0])

        # Store the data in tplot 'variable1'
        pytplot.store_data('variable1', data={'x': times, 'y': data})

        # Clip the data between 1.5 and 2.5, replacing values outside this range with NaN
        pyspedas.yclip(names='variable1', ymin=1.5, ymax=2.5)

        # The clipped data is now stored in 'variable1-clip'
        clipped_data = pytplot.get_data('variable1-clip')
        print(clipped_data)
    """
    # new_names is deprecated in favor of newname
    if new_names is not None:
        logging.info(
            "yclip: The new_names parameter is deprecated. Please use newname instead."
        )
        newname = new_names

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        logging.error("yclip: No valid tplot names were provided.")
        return

    if suffix is None:
        suffix = "-clip"

    if flag is None:
        flag = np.nan

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

    for i, old in enumerate(old_names):
        new = n_names[i]

        data = pytplot.clip(old, ymin, ymax, new)

        logging.info("yclip was applied to: " + new)

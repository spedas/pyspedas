import numpy as np
import logging
from pyspedas.utilities.interpol import interpol


def interp_gap(x, y):
    """
    Replace NaNs with interpolated values for the y array.
    If there are any NaNs in the x array, no interpolation is performed.

    This function replaces NaN values in y with interpolated values based on x.
    For multidimensional y arrays, interpolation is performed on each column.

    Parameters
    ----------
    x : array_like
        Independent variable array (e.g., time). Must be 1-dimensional
        and finite.
    y : array_like
        Dependent variable array to interpolate. Can be 1D or 2D.

    Returns
    -------
    dict
        Dictionary containing:
            'y': Modified y array with NaNs replaced by interpolated values
            'index': Indices where interpolation was performed
            'count': Number of points that were interpolated

    Notes
    -----
    This function mirrors the behavior of the IDL procedure interp_gap.
    It uses the interpol function for the actual interpolation.

    Examples
    --------
    >>> import numpy as np
    >>> from pyspedas.utilities.interp_gap import interp_gap
    >>> x = np.array([1, 2, 3, 4, 5])
    >>> y = np.array([10, np.nan, 30, np.nan, 50])
    >>> result = interp_gap(x, y)
    >>> print(result['y'])  # [10, 20, 30, 40, 50]
    """

    # Convert inputs to numpy arrays
    x = np.asarray(x)
    y = np.asarray(y)

    # Check that x values are finite
    invalid_x = ~np.isfinite(x)
    if np.any(invalid_x):
        logging.error("Invalid x points")
        return {"y": y, "index": [-1], "count": 0}

    # Handle multidimensional case (operate per column and union indices)
    if y.ndim > 1:
        index = np.zeros(len(x), dtype=bool)
        y_modified = y.copy()

        for i in range(y.shape[1]):
            column = y[:, i].copy()
            result = interp_gap(x, column)
            y_modified[:, i] = result["y"]
            if result["count"] > 0:
                index[result["index"]] = True

        wb = np.where(index)[0]
        return {"y": y_modified, "index": wb, "count": len(wb)}

    # Handle 1D case
    ny = len(y)

    # Find NaN/infinite values in y
    wb = np.where(~np.isfinite(y))[0]
    count = len(wb)

    if count == 0:
        # No bad points
        return {"y": y, "index": np.array([]), "count": 0}

    logging.info("Found %d out of %d bad points", count, ny)

    # Find neighboring good points for interpolation
    wbp_candidates = np.concatenate([wb - 1, wb + 1])
    wbp_candidates = np.clip(wbp_candidates, 0, ny - 1)
    wbp = np.unique(wbp_candidates)

    # Keep only finite neighboring points in y
    finite_mask = np.isfinite(y[wbp])
    if not np.any(finite_mask):
        logging.info("All points bad, no interpolation done")
        return {"y": y, "index": wb, "count": count}

    wbp = wbp[finite_mask]
    xwbp = x[wbp]
    ywbp = y[wbp]

    # Extend with boundary points (flat extrapolation at edges)
    x_extended = np.concatenate(([x[0]], xwbp, [x[ny - 1]]))
    y_extended = np.concatenate(([ywbp[0]], ywbp, [ywbp[-1]]))

    # Interpolate at bad point locations
    try:
        yp = interpol(y_extended, x_extended, x[wb])
        y_result = y.copy()
        y_result[wb] = yp
        return {"y": y_result, "index": wb, "count": count}
    except (ValueError, IndexError) as e:
        logging.info("Interpolation failed: %s", str(e))
        return {"y": y, "index": wb, "count": count}

"""
This is a Python implementation of IDL's REBIN function.

https://www.nv5geospatialsoftware.com/docs/REBIN.html

It works for 1D, 2D, and 3D arrays.
"""

import numpy as np


def rebin1d(a, m, sample=False):
    """
    Resize an 1D array by interpolation or averaging.

    Parameters
    ----------
    array : array_like
        Input array to be resized.
    m : int
        New size for the output array.
    sample : bool, optional
        If True, use nearest-neighbor sampling (no interpolation/averaging).
        If False (default), use bilinear interpolation for expansion and averaging for compression.

    Returns
    -------
    ndarray
        Resized 1D array with the specified dimension.
        Type of array is the same as the input array.

    """
    a = np.asarray(a)
    if a.ndim != 1:
        raise ValueError("Input array must be 1D")

    if int(m) != m:
        raise ValueError("New size must be an integer")

    n = a.size  # Old size
    if n <= 0 or m <= 0:
        return np.array([])

    if m == 1:
        return np.array([np.mean(a)])

    if n == 1:
        return np.repeat(a, m)

    new_arr = np.zeros(m, dtype=a.dtype)  # keep the same dtype

    if m < n:
        # Downsample (Compression)
        if int(n / m) != n / m:
            raise ValueError("Compression to non-integer multiple is not supported")
        if sample:
            # Nearest neighbor sampling
            for i in range(m):
                p0 = int(i * n / m)
                if p0 >= n - 1:
                    # Repeat last value
                    new_arr[i] = a[n - 1]
                else:
                    new_arr[i] = a[p0]
        else:
            # Nearest neighbor averaging
            for i in range(m):
                new_arr[i] = np.mean(a[int(i * n / m) : int((i + 1) * n / m)])
    else:
        # Upsample (Expansion)
        if int(m / n) != m / n:
            raise ValueError("Expansion to non-integer multiple is not supported")
        if sample:
            # Nearest neighbor sampling
            for i in range(m):
                p0 = int(i * n / m)
                if p0 >= n - 1:
                    # Repeat last value
                    new_arr[i] = a[n - 1]
                else:
                    new_arr[i] = a[p0]
        else:
            # Bilinear interpolation
            for i in range(m):
                p = n * i / m
                if p >= n - 1:
                    # Repeat last value
                    new_arr[i] = a[n - 1]
                else:
                    p0 = int(p)
                    # To get the same results as in IDL when array a is integers:
                    # 1. Take the integer part only (not rounding), 3.667 -> 3
                    # 2. Perform the division last, so that we don't get 3.9997 which would become 3
                    new_arr[i] = a[p0] + (i * n - m * p0) * (a[p0 + 1] - a[p0]) / m

    return new_arr


def rebin(arr, new_dimensions, sample=False):
    """
    Resize an array by interpolation or averaging.

    Python implementation of IDL's REBIN function.

    Parameters
    ----------
    arr : array_like
        Input array to be resized.
    new_dimensions : int or tuple of ints
        New dimensions for the output array as a tuple of integers.
        For example, if new array is 2x3, pass (2, 3).
        New dimensions must be positive integers.
        Each dimension must be an integer multiple of the corresponding old dimension
            or the old dimension must be an integer multiple of the new dimension.
    sample : bool, optional
        If True, use nearest-neighbor sampling (no interpolation/averaging).
        If False (default), use bilinear interpolation for expansion and averaging for compression.

    Returns
    -------
    ndarray
        Resized array with the specified dimensions.
        If the input is array of int, the output will also be array of int.

    """
    arr = np.asarray(arr)
    old_shape = arr.shape
    if type(new_dimensions) is tuple:
        new_shape = new_dimensions
    else:
        new_shape = (new_dimensions,)

    # Validate dimensions
    if len(new_shape) != len(old_shape):
        raise ValueError(
            f"Number of dimensions must match: got {len(new_shape)}, expected {len(old_shape)}"
        )

    # Check if any dimension is zero or negative
    if any(d <= 0 for d in new_shape):
        raise ValueError("All dimensions must be positive")

    # Each new dimension has to be an integer multiple of the corresponding old dimension
    for old_dim, new_dim in zip(old_shape, new_shape):
        if old_dim < 1 or new_dim < 1 or (new_dim > old_dim and new_dim % old_dim != 0):
            raise ValueError(
                f"New dimension {new_dim} is not an integer multiple of old dimension {old_dim}"
            )
        elif new_dim < old_dim and old_dim % new_dim != 0:
            raise ValueError(
                f"Old dimension {old_dim} is not an integer multiple of new dimension {new_dim}"
            )

    # If shapes are the same, return a copy
    if new_shape == old_shape:
        return arr.copy()

    # Initialize new array, keep the same dtype
    new_arr = np.zeros(new_shape, dtype=arr.dtype)

    if len(new_shape) == 1:
        # One dimensional array
        m = new_shape[0]
        new_arr = rebin1d(arr, m, sample)

    elif len(new_shape) == 2:
        # Two dimensional array
        n1, n2 = old_shape
        m1, m2 = new_shape
        new_arr1 = np.zeros((m1, n2), dtype=arr.dtype)
        for i in range(n2):
            # Rebin each column
            new_arr1[:, i] = rebin1d(arr[:, i], m1, sample)

        new_arr = np.zeros((m1, m2), dtype=arr.dtype)
        for i in range(m1):
            # Rebin each row
            new_arr[i, :] = rebin1d(new_arr1[i, :], m2, sample)

    elif len(new_shape) == 3:
        # Three dimensional array
        n1, n2, n3 = old_shape
        m1, m2, m3 = new_shape

        # First rebin along dimension 0
        new_arr1 = np.zeros((m1, n2, n3), dtype=arr.dtype)
        for j in range(n2):
            for k in range(n3):
                new_arr1[:, j, k] = rebin1d(arr[:, j, k], m1, sample)

        # Then rebin along dimension 1
        new_arr2 = np.zeros((m1, m2, n3), dtype=arr.dtype)
        for i in range(m1):
            for k in range(n3):
                new_arr2[i, :, k] = rebin1d(new_arr1[i, :, k], m2, sample)

        # Finally rebin along dimension 2
        new_arr = np.zeros((m1, m2, m3), dtype=arr.dtype)
        for i in range(m1):
            for j in range(m2):
                new_arr[i, j, :] = rebin1d(new_arr2[i, j, :], m3, sample)

    else:
        raise ValueError("Only 1D, 2D, and 3D arrays are supported")

    return new_arr

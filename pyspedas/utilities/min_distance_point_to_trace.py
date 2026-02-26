import numpy as np

def strip_trailing_nan_rows(xyz: np.ndarray) -> np.ndarray:
    """
    Remove trailing rows that are all-NaN. If all rows are NaN, returns (0,3).
    """
    xyz = np.asarray(xyz, dtype=float)
    if xyz.ndim != 2 or xyz.shape[1] != 3:
        raise ValueError("Expected shape (N, 3).")

    all_nan = np.all(np.isnan(xyz), axis=1)
    if not np.any(all_nan):
        return xyz

    valid_idx = np.where(~all_nan)[0]
    if valid_idx.size == 0:
        return xyz[:0]  # empty
    return xyz[: valid_idx[-1] + 1]

def point_to_segments_dist(p: np.ndarray, A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Distance from point p (3,) to each segment A[i]->B[i].
    A, B: (S,3)
    Returns distances: (S,)
    """
    p = np.asarray(p, dtype=float)
    v = B - A                      # (S,3)
    w = p - A                      # (S,3)

    vv = np.einsum("ij,ij->i", v, v)  # (S,)
    # Avoid divide-by-zero for degenerate segments:
    vv_safe = np.where(vv == 0.0, 1.0, vv)

    t = np.einsum("ij,ij->i", w, v) / vv_safe  # (S,)
    t = np.clip(t, 0.0, 1.0)

    closest = A + t[:, None] * v   # (S,3)
    d = p - closest
    dist2 = np.einsum("ij,ij->i", d, d)

    # If vv==0, closest should be A; formula already gives that since v==0.
    return np.sqrt(dist2)

def directed_trace_distance(trace1: np.ndarray, trace2: np.ndarray) -> float:
    """
    For each point in trace1, compute distance to closest segment in trace2.
    Return the maximum of those distances.

    Returns NaN if trace1 has no valid points or trace2 has <2 valid points.
    """
    t1 = strip_trailing_nan_rows(trace1)
    t2 = strip_trailing_nan_rows(trace2)
    print(f"Directed trace distance, non-nan npoints {len(t1)} and {len(t2)}" )

    if len(t1) == 0 or len(t2) < 2:
        return np.nan

    A = t2[:-1]
    B = t2[1:]

    # (Optional robustness) drop segments that contain NaNs (shouldn't happen if only trailing)
    good = ~(np.any(np.isnan(A), axis=1) | np.any(np.isnan(B), axis=1))
    A, B = A[good], B[good]
    if len(A) == 0:
        return np.nan

    # For each point in t1, compute min distance to any segment, then take max.
    mins = []
    for p in t1:
        if np.any(np.isnan(p)):
            continue
        mins.append(point_to_segments_dist(p, A, B).min())

    if len(mins) == 0:
        return np.nan

    return float(np.max(mins))

def symmetric_trace_distance(trace1: np.ndarray, trace2: np.ndarray) -> float:
    d12 = directed_trace_distance(trace1, trace2)
    d21 = directed_trace_distance(trace2, trace1)
    if np.isnan(d12) and np.isnan(d21):
        return np.nan
    return float(np.nanmax([d12, d21]))

def directed_trace_distance_with_worst_point(trace1: np.ndarray, trace2: np.ndarray):
    """
    Returns (max_min_distance, worst_index, worst_point, worst_min_distance)
    """
    t1 = strip_trailing_nan_rows(trace1)
    t2 = strip_trailing_nan_rows(trace2)
    print ('number of points',len(t1), len(t2))

    if len(t1) == 0 or len(t2) < 2:
        return np.nan, None, None, np.nan

    A, B = t2[:-1], t2[1:]
    good = ~(np.any(np.isnan(A), axis=1) | np.any(np.isnan(B), axis=1))
    A, B = A[good], B[good]
    if len(A) == 0:
        return np.nan, None, None, np.nan

    worst_i = None
    worst_d = -np.inf

    for i, p in enumerate(t1):
        if np.any(np.isnan(p)):
            continue
        dmin = point_to_segments_dist(p, A, B).min()
        if dmin > worst_d:
            worst_d = dmin
            worst_i = i

    if worst_i is None:
        return np.nan, None, None, np.nan

    return float(worst_d), worst_i, t1[worst_i], float(worst_d)
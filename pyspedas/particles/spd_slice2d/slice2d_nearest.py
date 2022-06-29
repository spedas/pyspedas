import numpy as np


def slice2d_nearest(dists, time, samples):
    """
    Get a time range that encompasses a specified number of
    samples closest to a specified time.

    Input
    ------
        dists: list
            List containing distribution data structures

        time: float
            Unix time

        samples: int
            Number of samples to return

    Returns
    --------
        List containing [start time, end time] for the time range
    """
    start_times = np.zeros(len(dists))
    end_times = np.zeros(len(dists))

    for i, dist in enumerate(dists):
        start_times[i] = dist['start_time']
        end_times[i] = dist['end_time']

    # use center
    distance = np.abs((start_times + end_times)/2.0 - time)

    # get indices for N closest samples
    idx = np.argsort(distance)
    if samples > len(idx):
        n = len(idx)
    else:
        n = samples
    idx = idx[0:n]

    # full time range
    return [np.nanmin(start_times[idx]),
            np.nanmax(end_times[idx])]

from copy import deepcopy
import numpy as np

from .slice2d_intrange import slice2d_intrange
from .slice2d_get_sphere import slice2d_get_sphere
from .slice2d_checkbins import slice2d_checkbins
from .slice2d_collate import slice2d_collate
from .slice2d_get_ebounds import slice2d_get_ebounds


def slice2d_get_data(dists, trange=None, energy=False, erange=None):
    """

    """
    # Get indexes of data structures in requested time window
    times_idx = slice2d_intrange(dists, trange)

    if len(times_idx) == 0:
        print('No data in the time range')
        return

    weight = np.zeros(dists[0]['bins'][:, :, :].shape)
    data = np.zeros(dists[0]['data'][:, :, :].shape)
    out = None
    sphere = None
    last = None

    for time in times_idx:
        dist = dists[time]

        # if this sample's angle or energy bins or mass differ from last then
        # collate any aggregated data and continue
        if not slice2d_checkbins(dist, last):
            out = slice2d_collate(data, weight, sphere, previous_out=out)
            weight = np.zeros(dists[0]['bins'][:, :, :].shape)
            data = np.zeros(dists[0]['data'][:, :, :].shape)

        # copy current data for comparison in next iteration
        last = deepcopy(dist)

        # find active, valid bins
        bins = (dist['bins'] != 0)*1 & (np.isfinite(dist['data'])*1)

        # find bins within energy limits
        if erange is not None:
            n = dist['energy'].shape[0]
            energies = slice2d_get_ebounds(dist)
            ecenters = (energies[0:n-1, :, :]+energies[1:n, :, :])/2.0
            bins = bins & ((ecenters >= erange[0]) & (ecenters <= erange[1]))

        # Get data & bin boundaries
        # Coordinates will only be calculated/copied if the arrays are not 
        # in existence, otherwise this just copies the data and bins arrays.
        sphere = slice2d_get_sphere(dist, energy=energy)

        # sum of counts over current set of samples
        data = data + dist['data']

        # keep track of valid bins within range. this array will be used later
        # to average bins and discard any that are out of range or invalid
        weight = weight + bins

    # collate any remaining data
    out = slice2d_collate(data, weight, sphere, previous_out=out)

    return out

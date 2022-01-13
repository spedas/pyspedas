

import numpy as np

# use nansum from bottleneck if it's installed, otherwise use the numpy one
try:
    import bottleneck as bn
    nansum = bn.nansum
except ImportError:
    nansum = np.nansum

def mms_pgs_make_e_spec(data_in):

    data = data_in.copy()

    # zero inactive bins to ensure areas with no data are represented as NaN
    zero_bins = np.argwhere(data['bins'] == 0)
    if zero_bins.size != 0:
        for item in zero_bins:
            data['data'][item[0], item[1]] = 0.0

    # use the first energy table for now
    outtable = data['energy'][:, 0]
    outbins = np.zeros([len(data['data'][:, 0]), len(data['data'][0, :])])

    # rebin the data to the original energy table
    for ang_idx in range(0, len(data['data'][0, :])):
        etable = data['energy'][:, ang_idx]
        for binidx in range(0, len(outtable)):
            if data['data'][binidx, ang_idx] != 0.0:
                this_en = find_nearest_neighbor(outtable, [etable[binidx]])
                whereen = np.argwhere(outtable == this_en)
                outbins[whereen, ang_idx] += data['data'][binidx, ang_idx]

    if len(data['data'][0, :]) > 1:
        ave = nansum(outbins, axis=1)/nansum(data['bins'], axis=1)
    else:
        ave = outbins/data['bins']

    return (outtable, ave)


def find_nearest_neighbor(table, item):
    table = np.array(table)
    return min(table, key=lambda p: sum((p - item)**2))

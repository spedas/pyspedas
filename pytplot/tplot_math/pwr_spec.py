import numpy as np
import pytplot
from scipy import signal


# First pass at the power spectrum function.  This is still missing several features of the IDL power spectrum routine, such as
# bin, nohanning, notperhertz, and tm_sensativity.  The IDL routine is located in dpwrspc.pro.

# There is also the issue of this not quite having the same units as the plot I use as my reference.
# https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2015GL065366#grl53372-bib-0016
# Interestingly enough, the output is the same if units of seconds are used in the periodogram instead of Hertz.
# Perhaps they calculated it differently?



def pwr_spec(tvar, nbp=256, nsp=128, name=None):

    x = pytplot.data_quants[tvar].data.index.values
    y = pytplot.data_quants[tvar].data[0].values
    
    l = len(x)
    x_new = []
    f_new = []
    pxx_new = []
    shift_lsp = np.arange(0, l-1, nsp)
    for i in shift_lsp:

        x_n = x[i:i+nbp]
        y_n = y[i:i+nbp]
        if len(x_n) < nbp:
            continue

        median_diff_between_points = np.median(np.diff(x_n))

        w = signal.get_window("hanning", nbp)
        f,pxx = signal.periodogram(y_n, fs=(1/median_diff_between_points), window=w, detrend='linear')
        f = f[1:-1]
        pxx = pxx[1:-1]
        x_new.append((x_n[-1] + x_n[0]) / 2)
        f_new.append(f)
        pxx_new.append(pxx)

    if name is None:
        name = tvar + "_pwrspec"

    pytplot.store_data(name, data={'x': x_new, 'y': pxx_new, 'v': f_new})
    pytplot.options(name, 'spec', 1)
    pytplot.options(name, 'zlog', 1)
    pytplot.options(name, 'ylog', 1)

    return


from pytplot import get_data
from .tnames import tnames
from csv import writer

def tplot2ascii(names):
    tvars = tnames(names)
    for var in tvars:
        times, data = get_data(var)
        csvout = writer(open(var+'.txt', 'w'))
        for i, time in enumerate(times):
            csvout.writerow([time] + list(data[i]))
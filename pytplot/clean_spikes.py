# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
import pydivide
import scipy
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from astropy.convolution import convolve,Box1DKernel

insitu = pydivide.read('2017-06-19')
t = insitu['Time']
data = insitu['SPACECRAFT']['ALTITUDE']
pytplot.store_data('sgx',data = {'x':t, 'y':data})
 
N= len(pytplot.data_quants['sgx'].data.index)
x = pytplot.data_quants['sgx'].data.index
y = pytplot.data_quants['sgx'].data
print(N)
print(x)
print(y)
def fourier_smooth():
    N= len(pytplot.data_quants['sgx'].data.index)
    x = pytplot.data_quants['sgx'].data.index
    y = pytplot.data_quants['sgx'].data
    w = scipy.fftpack.rfft(y)
    f = scipy.fftpack.rfftfreq(N, x[1]-x[0])
    w2 = w.copy()
    y2 = scipy.fftpack.irfft(w2)
    t = plt.plot(x,y,'r')
    s = plt.plot(x,y2)
    plt.show([s,t])

def boxcar_smooth():
    N= len(pytplot.data_quants['sgx'].data.index)
    x = pytplot.data_quants['sgx'].data.index
    y = pytplot.data_quants['sgx'].data
    print((y.values))
    smoothed = convolve(y.values,Box1DKernel(4))
    s = plt.plot(x,smoothed)
    t = plt.plot(x,y,'r')
    plt.show([s,t])

boxcar_smooth()



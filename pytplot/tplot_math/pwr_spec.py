import numpy as np
import pytplot
import pydivide
from scipy import signal

insitu,iuvs = pydivide.read('2017-06-19','2017-06-20')
t = insitu['Time']
data = insitu['SPACECRAFT']['ALTITUDE']
pytplot.store_data('sgx',data = {'x':t, 'y':data})

def pwr_spec(tvar,nbp=256,nsp=128):
    x = pytplot.data_quants[tvar].data.index.values
    y = pytplot.data_quants[tvar].data.values
    
    l = len(x)
    shift_lsp = np.arange(0,l-1,nsp)
    #print(shift_lsp)
    #print(x[0:255])
    for i in shift_lsp-nsp:
        x_n = x[i:i+nsp-1]
        y_n = y[i:i+nsp-1]
    
        x_n = x_n - x_n[0]
        c = np.polyfit(x_n,y_n,1)
        #print(c[0]*x_n[0:nbp-1])
        y_trend = c[0]*x_n + c[1]
        y_n = y_n - y_trend
        print(y_n)
    
    w = signal.get_window("hanning",nbp)
    f,pxx = signal.periodogram(y[0:nbp], window = w, detrend = lambda x: x)
    
pwr_spec('sgx')
    
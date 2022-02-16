# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 14:24:48 2021

@author: kvidal
"""

from scipy import signal, special
import numpy as np

def time_domain_filter(data,time, freq_low, freq_high):
    """
    Modified for python from SPEDAS's function of the same name
    Purpose: band-pass filter of data, assuming constant dt between points
    Parameters:
        data: input nx3 array
        time: in seconds
        freq_low: low coutoff frequency in Hz
        freq_high: high cutoff frequency in Hz
    Returns: nx3 array of band-pass filtered data
    """
    dt = time[1]-time[0]
    nyquist = 1./(2.*dt)
    flow = freq_low/nyquist
    fhigh = freq_high/nyquist
    A = 120. # from Ergun's fa_fields_filter
    if flow == 0.0:
        f = fhigh
    else:
        f = flow
    nterms = int(5./f)
    if nterms > 5000.:
        nterms = 5000.
    out = digital_filter(flow,fhigh,A,nterms)
    new_series_x = signal.convolve(data[:,0],out,mode='same',method='direct')
    new_series_y = signal.convolve(data[:,1],out,mode='same',method='direct')
    new_series_z = signal.convolve(data[:,2],out,mode='same',method='direct')
    new_series =  np.transpose(np.vstack((new_series_x,new_series_y,new_series_z)))

    return new_series

def digital_filter(flow,fhigh,aGibbs,nterms):
    
    if fhigh < flow:
        fstop = float(1)
    else:
        fstop = float(0)
    
    # Computes Kaiser weights W(N,K) for digital filters
    # W = coef = returned array of Kaiser weights
    # N = value of N in W(N,K), ie number of terms
    # A = Size of gibbs phenomenon wiggles in -DB
    
    if aGibbs <= 21 :
        alpha = 0.
    elif (aGibbs >= 50) :
        alpha = 0.1102*(aGibbs-8.7)
    else:
        alpha = 0.5842*(aGibbs-21)**(0.4) + 0.07886*(aGibbs-21)
        
    arg = (np.arange(nterms)+1)/nterms
    coef = special.iv(0,alpha*np.sqrt(1.-arg**2))/special.iv(0,alpha)
    t = (np.arange(nterms)+1)*np.pi
    coef = coef*(np.sin(t*fhigh)-np.sin(t*flow))/t
    coef = np.concatenate((np.flip(coef), [fhigh - flow + fstop], coef))
    return coef

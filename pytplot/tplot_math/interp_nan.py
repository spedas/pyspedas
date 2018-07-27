# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#LINEAR INTERPOLATION
#interpolate over NaN data
def interp_nan(tvar1):
    tv1 = pytplot.data_quants[tvar1].data
    tv1 = tv1.astype(float)
    tv1 = tv1.interpolate(method='linear')
    tv1 = tv1.astype(object)
    return tv1
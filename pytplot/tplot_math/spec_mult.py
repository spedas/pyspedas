import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#SPEC BIN MULTIPLICATION
#multiply spec_bin values by tvar data, store in new_tvar
def spec_mult(tvar1,new_tvar='tvar_specmult'):
    dataframe = pytplot.data_quants[tvar1].data
    specframe = pytplot.data_quants[tvar1].spec_bins
    new_df = pd.DataFrame(dataframe.values*specframe.values, columns=dataframe.columns, index=dataframe.index)    
    pytplot.store_data(new_tvar,data={'x':new_df.index,'y':new_df.values})
    return new_tvar
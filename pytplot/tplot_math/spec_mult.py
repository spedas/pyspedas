import pytplot
import pandas as pd

#SPEC BIN MULTIPLICATION
#multiply spec_bin values by tvar data, store in new_tvar
def spec_mult(tvar1,new_tvar='tvar_specmult'):

    if new_tvar == 'tvar_specmult':
        new_tvar = tvar1+'_specmult'

    dataframe = pytplot.data_quants[tvar1].data
    specframe = pytplot.data_quants[tvar1].spec_bins
    new_df = pd.DataFrame(dataframe.values*specframe.values, columns=dataframe.columns, index=dataframe.index)    
    pytplot.store_data(new_tvar,data={'x': new_df.index,'y': new_df.values})
    return
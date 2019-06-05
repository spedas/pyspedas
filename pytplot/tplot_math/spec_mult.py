import pytplot
import pandas as pd

#SPEC BIN MULTIPLICATION
#multiply spec_bin values by tvar data, store in new_tvar
def spec_mult(tvar1,new_tvar=None):

    if new_tvar is None:
        new_tvar = tvar1+'_specmult'

    d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)
    dataframe = d.values
    specframe = s.values
    new_df = pd.DataFrame(dataframe.values*specframe.values, columns=dataframe.columns, index=dataframe.index)    
    pytplot.store_data(new_tvar,data={'x': new_df.index,'y': new_df.values})
    return
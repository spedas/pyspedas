import pyspedas
from pytplot import tplot, tplot_names
from pyspedas.themis.spacecraft.fields.fit import cal_fit

t = ['2008-03-15', '2008-03-16']
pyspedas.themis.fit(trange=t, probe='a', level='l1', get_support_data=True,
                    varnames=['tha_fit', 'tha_fit_code', 'tha_fit_npts'], time_clip=True)
cal_fit(probe='a')

tplot_names()
tplot(['tha_fit_bfit', 'tha_fit_efit'])
#tplot(['tha_fgs', 'tha_fgs_sigma', 'tha_fit_bfit', 'tha_fit_efit',
#       'tha_efs', 'tha_efs_sigma', 'tha_efs_0', 'tha_efs_dot0'])
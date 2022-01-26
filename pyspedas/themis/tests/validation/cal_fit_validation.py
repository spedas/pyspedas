import pyspedas
import pytplot
import numpy as np
from pyspedas.themis.spacecraft.fields.fit import cal_fit
from pyspedas.utilities.download import download
from pyspedas.themis.config import CONFIG

# Download tplot files
remote_server = 'https://spedas.org/'
remote_name ='testfiles/cal_fit.tplot'
calfile = download(remote_file=remote_name,
                   remote_path=remote_server,
                   local_path=CONFIG['local_data_dir'],
                   no_download=False)

remote_name ='testfiles/tha_efs_no_cal.tplot'
nocalfile = download(remote_file=remote_name,
                   remote_path=remote_server,
                   local_path=CONFIG['local_data_dir'],
                   no_download=False)

# Load validation variables
filename = calfile[0]
pytplot.tplot_restore(filename)
tha_fit_idl = pytplot.get_data('tha_fit')
tha_fgs_idl = pytplot.get_data('tha_fgs')
tha_fgs_sigma_idl = pytplot.get_data('tha_fgs_sigma')
tha_fit_bfit_idl = pytplot.get_data('tha_fit_bfit')
tha_fit_efit_idl = pytplot.get_data('tha_fit_efit')
tha_efs_idl = pytplot.get_data('tha_efs')
tha_efs_sigma_idl = pytplot.get_data('tha_efs_sigma')
tha_efs_0_idl = pytplot.get_data('tha_efs_0')
tha_efs_dot0_idl = pytplot.get_data('tha_efs_dot0')

pytplot.tplot_names()
pytplot.del_data('*')

filename = nocalfile[0]
pytplot.tplot_restore(filename)
tha_efs_idl_no_cal = pytplot.get_data('tha_efs')

pytplot.tplot_names()
pytplot.del_data('*')

t = ['2008-03-15', '2008-03-16']
pyspedas.themis.fit(trange=t, probe='a', level='l1', get_support_data=True,
                    varnames=['tha_fit', 'tha_fit_code', 'tha_fit_npts'], time_clip=True)
# cal_fit
cal_fit(probe='a')
tha_fit = pytplot.get_data('tha_fit')

tha_fgs = pytplot.get_data('tha_fgs')
tha_fgs_sigma = pytplot.get_data('tha_fgs_sigma')

tha_fit_bfit = pytplot.get_data('tha_fit_bfit')
tha_fit_efit = pytplot.get_data('tha_fit_efit')

tha_efs = pytplot.get_data('tha_efs')
tha_efs_sigma = pytplot.get_data('tha_efs_sigma')

tha_efs_0 = pytplot.get_data('tha_efs_0')
tha_efs_dot0 = pytplot.get_data('tha_efs_dot0')

# no_cal flag
cal_fit(probe='a', no_cal=True)
tha_efs_no_cal = pytplot.get_data('tha_efs')

# Comparison
diff_fgs = np.nanmedian(tha_fgs.y - tha_fgs_idl.y, axis=0, keepdims=True)
diff_sigma = np.nanmedian(tha_fgs_sigma.y - tha_fgs_sigma_idl.y,  axis=0, keepdims=True)
diff_bfit = np.nanmedian(tha_fit_bfit.y - tha_fit_bfit_idl.y,  axis=0, keepdims=True)
diff_efit = np.nanmedian(tha_fit_efit.y - tha_fit_efit_idl.y,  axis=0, keepdims=True)
diff_efs = np.nanmedian(tha_efs.y - tha_efs_idl.y,  axis=0, keepdims=True)
diff_efs_sigma = np.nanmedian(tha_efs_sigma.y - tha_efs_sigma_idl.y,  axis=0, keepdims=True)
diff_efs_no_cal = np.nanmedian(tha_efs_no_cal.y - tha_efs_idl_no_cal.y,  axis=0, keepdims=True)

diff_efs_0 = np.nanmedian(tha_efs_0.y - tha_efs_0_idl.y,  axis=0, keepdims=True)
diff_efs_dot0 = np.nanmedian(tha_efs_dot0.y - tha_efs_dot0_idl.y,  axis=0, keepdims=True)


print('fgs: ', diff_fgs)
print('fgs_sigma:', diff_sigma)

print('bfit:', diff_bfit)
print('efit:', diff_efit)

print('efs:', diff_efs)
print('efs_sigma:', diff_efs_sigma)

print('efs_0:', diff_efs_0)
print('efs_dot0:', diff_efs_dot0)

print('efs_no_cal:', diff_efs_no_cal)

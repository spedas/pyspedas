# secs module
### EICS and SECS data

pySPEDAS.secs module is to load and read EICS and SECS data. The vector field and contour maps are also implemented.
```python
import pyspedas
from pyspedas.secs.makeplots import make_plots
if __name__ == '__main__':
    dtype = 'EICS' # 'EICS or SECS'
    files_downloaded = pyspedas.secs.data(trange=['2012-04-05/02:15:35', '2012-04-06/02:15:35'], resolution=10,
                                          dtype=dtype, no_download=False, downloadonly = False, out_type = 'df')
    dtime = '2010-04-05/09:12:00'  # set one single data point when plotting.
    make_plots(dtype = dtype, dtime = dtime, vplot_sized = True, contour_den = 201, s_loc=False)

```
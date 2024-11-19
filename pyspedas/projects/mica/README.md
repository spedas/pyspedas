
## Magnetic Induction Coil Array (MICA)
The routines in this module can be used to load data from the Magnetic Induction Coil Array (MICA). 


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

```python
nal_vars = pyspedas.mica.load(site='NAL', trange=['2019-02-01','2019-02-02'])
print(nal_vars)
tplot('spectra_x_1Hz_NAL')
```


### Information

For more information, see:

https://themis.igpp.ucla.edu/events/Fall2019SWT/PDF/Hartinger_THEMIS_postAGU2019.pdf

https://slidetodoc.com/the-magnetic-induction-coil-array-mica-marc-lessard/

For data files, see:

http://mirl.unh.edu/ULF/cdf/
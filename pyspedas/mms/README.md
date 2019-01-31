
## Magnetospheric Multiscale (MMS) Mission
The routines in this folder can be used to load data from the Magnetospheric Multiscale (MMS) mission into pytplot variables. 

### Fluxgate Magnetometer (FGM) Example

```python
from pytplot import tplot
from pyspedas.mms import mms_load_fgm
mms_load_fgm(probe='1', trange=['2015-10-16', '2015-10-17'])
tplot('mms1_fgm_b_gsm_srvy_l2')
```

### Search-coil Magnetometer (SCM) Example

```python
from pytplot import tplot
from pyspedas.mms import mms_load_scm
mms_load_scm(probe='1', trange=['2015-10-16', '2015-10-17'])
tplot('mms1_scm_acb_gse_scsrvy_srvy_l2')
```

### Configuration
Configuration settings are set in the CONFIG hash table in the mms_config.py file. 

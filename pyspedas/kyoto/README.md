
## Kyoto Dst
The routines in this module can be used to load Dst data from the World Data Center for Geomagnetism, Kyoto, Japan

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Load the data

```python
dst_vars = pyspedas.kyoto.dst(trange=['2018-11-5', '2018-11-6'])

tplot('kyoto_dst')
```

### Acknowledgment
The DST data are provided by the World Data Center for Geomagnetism, Kyoto,  and
are not for redistribution (http://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
the geomagnetic observatories (Kakioka [JMA], Honolulu and San Juan [USGS], Hermanus
[RSA], Alibag [IIG]), NiCT, INTERMAGNET, and many others for their cooperation to
make the Dst index available.

## Kyoto Dst
The routines in this module can be used to load Dst data from the World Data Center for Geomagnetism, Kyoto, Japan.

Example page:
https://wdc.kugi.kyoto-u.ac.jp/dst_final/197407/index.html

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



## Kyoto AE Indices
The routines in this module can be used to load AE index data (AE, AL, AO, AU, AX) from the World Data Center for Geomagnetism, Kyoto, Japan.

Example page:
https://wdc.kugi.kyoto-u.ac.jp/ae_provisional/201210/ae121001.for.request


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Load the data

```python
ae_vars = pyspedas.kyoto.load_ae(trange=['2018-11-5', '2018-11-6'])

tplot(ae_vars)
```

### Acknowledgment
The provisional AE data are provided by the World Data Center for Geomagnetism, Kyoto,
and are not for redistribution (https://wdc.kugi.kyoto-u.ac.jp/). Furthermore, we thank
AE stations (Abisko [SGU, Sweden], Cape Chelyuskin [AARI, Russia], Tixi [IKFIA and
AARI, Russia], Pebek [AARI, Russia], Barrow, College [USGS, USA], Yellowknife,
Fort Churchill, Sanikiluaq (Poste-de-la-Baleine) [CGS, Canada], Narsarsuaq [DMI,
Denmark], and Leirvogur [U. Iceland, Iceland]) as well as the RapidMAG team for
their cooperations and efforts to operate these stations and to supply data for the provisional
AE index to the WDC, Kyoto. (Pebek is a new station at geographic latitude of 70.09N
and longitude of 170.93E, replacing the closed station Cape Wellen.)

## Swarm
The routines in this module can be used to load data from the Swarm mission. 

### Notes
- This plug-in is still EXPERIMENTAL, and provides access to the Swarm data available via the VirES(+HAPI) server at https://vires.services/hapi
- The VirES(+HAPI) server only serves the latest versions of the Swarm data; we suggest users document the date the data were accessed to track the version they're using for their analysis. Eventually, this plug-in will support tracking versions via the dataset's metadata, but we're not there yet. 
- A much more comprehensive interface to the Swarm data in Python, along with several example notebooks, is available at: https://swarm.magneticearth.org/

### Instruments
- Magnetometer (MAG)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.swarm.mag(probe='c', trange=['2017-03-27/06:00', '2017-03-27/08:00'], datatype='hr')

tplot('swarmc_B_VFM')
```


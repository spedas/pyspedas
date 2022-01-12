
## Magnetic Field Models
The routines in this module can be used to calculate Tsyganenko magnetic field models using Sheng Tian's `geopack` library (https://github.com/tsssss/geopack).

### IGRF model

```python
from pyspedas.geopack.tt89 import tt89

tt89('position_data', igrf_only=True)
```

### T89

```python
from pyspedas.geopack.tt89 import tt89

tt89('position_data')
```

### T96

```python
from pyspedas.geopack.tt96 import tt96

tt96('position_data', parmod=params)
```

### T01

```python
from pyspedas.geopack.tt01 import tt01

tt01('position_data', parmod=params)
```

### TS04

```python
from pyspedas.geopack.tts04 import tts04

tts04('position_data', parmod=params)
```




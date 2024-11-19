
## Electron Losses and Fields Investigation (ELFIN)
The routines in this module can be used to load data from the Electron Losses and Fields Investigation (ELFIN) mission. 

### Instruments
- Fluxgate Magnetometer (FGM)
- Energetic Particle Detector (EPD)
- Magneto Resistive Magnetometer-a (MRMa)
- Magneto Resistive Magnetometer-i (MRMi)
- State data (state)
- Engineering data (ENG)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
fgm_vars = pyspedas.elfin.fgm(trange=['2020-10-01', '2020-10-02'])

tplot('ela_fgs')
```


#### Energetic Particle Detector (EPD)

```python
epd_vars = pyspedas.elfin.epd(trange=['2020-11-01', '2020-11-02'])

tplot('ela_pef')
```


#### Magneto Resistive Magnetometer (MRMa)

```python
mrma_vars = pyspedas.elfin.mrma(trange=['2020-11-5', '2020-11-6'])

tplot('ela_mrma')
```


#### Magneto Resistive Magnetometer (MRMi)

```python
mrmi_vars = pyspedas.elfin.mrmi(trange=['2020-11-5', '2020-11-6'])

tplot('ela_mrmi')
```


#### State data (state)

```python
state_vars = pyspedas.elfin.state(trange=['2020-11-5/10:00', '2020-11-5/12:00'])

tplot('ela_pos_gei')
```


#### Engineering (ENG)

```python
eng_vars = pyspedas.elfin.eng(trange=['2020-11-5', '2020-11-6'])

tplot('ela_fc_idpu_temp')
```


    
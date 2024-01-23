## PySPEDAS Analysis Tools

The routines in this module can be used to perform various analysis tasks on spacecraft or ground data.

### Linear Gradient Estimation (lingradest)

This routine is used to estimate the gradients and other properties of the magnetic field, using positions and field measurements from four spacecraft in a roughly
tetrahedral formation (e.g. MMS or Cluster).

### Magnetic Null Finding via First Order Taylor Expansion (find_magnetic_nulls_fote)

This routine finds locations and toplogical properties of magnetic null points near a
tetrahedral formation of spacecraft (e.g. MMS or Cluster)

Example:
```python
import pyspedas
from pytplot import tplot

data = pyspedas.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-09-19/07:40', '2015-09-19/07:45'], data_rate='srvy', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
fields = ['mms'+prb+'_fgm_b_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
positions = ['mms'+prb+'_fgm_r_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
null_vars = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions, smooth_fields=True,smooth_npts=10,smooth_median=True)
tplot(null_vars)
```

### Magnetic Null Classification (classify_null_types)

This routine takes three complex values (eigenvalues of a Jacobian matrix) and uses
them to classify the corresponding magnetic null point (2-D types X or O, or 3-D types
A (radial), B (radial), A (spiral) or B (spiral)).

Example:
```python
import pyspedas

l1 = complex(-.25,0.0)
l2 = complex(-.25, 0.0)
l3 = complex(0.5,0.0)
lambdas = [l1,l2,l3]
tc = pyspedas.classify_null_type(lambdas)
# tc == 3, indicating a type A (radial) null
```

### Neutral Sheet Models (neutral_sheet)

This routine takes a list of times and positions, some additional model parameters, and
a model name, and computes the GSM-Z coordinate of the neutral sheet at those
times and positions, or optionally the difference along Z between the NS and the input position.

### Time Domain Filtering (time_domain_filter)

TBD

### Wave Polarization Analysis (twavpol)

This routine takes a variable containing field data (preferably in a minimum variance coordinate system), and some processing parameters, and calculates
several wave polarization properties of the input field versus time and frequency: wave power, degree of polarization, wave normal angle, helicity, ellipticity,

### Wavelet analysis (wavelet)

TBD


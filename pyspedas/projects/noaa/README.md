## Geomagnetic Indices

The following geomagnetic indices can be loaded into tplot variables:

["Kp", "ap", "Sol_Rot_Num", "Sol_Rot_Day", "Kp_Sum", "ap_Mean", "Cp", "C9", "Sunspot_Number", "F10.7", "Flux_Qualifier"]

For "Kp" and "ap", there is one data point for every 3 hours.
For all other variables, there is one data point per day.


### Example

To download the indices you can use:

```python
from pyspedas.noaa.noaa_load_kp import noaa_load_kp

trange = ["2017-03-23/00:00:00", "2017-04-23/23:59:59"]
vars = noaa_load_kp(trange=trange)
print(vars)
```


### NOAA and GFZ ftp sites

Data is downloaded either from the NOAA ftp site or the GFZ (Helmholtz Centre Potsdam) ftp site.

NOAA data is available from 1932 to March 2018.<br>
(ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP/, filenames: 1932, 1933, ..., 2018)

GFZ data is available from 1932 to present.<br>
(ftp.gfz-potsdam.de/pub/home/obs/kp-ap/wdc/yearly/, filenames: kp1932.wdc, kp1933.wdc, ..., kp2020.wdc)

A single file contains one year of data.<br>
A single line inside a file contains one day of data.

File names are different in the two ftp sites.<br>
Data format is a little different, the NOAA data has 72 characters per line,<br>
while the GFZ data has 62 characters per line (it is missing the last 3 columns).

Example of data from NOAA and from WDC:
```
1701012502 73337272323302017210 18 22 12  9  9 15  7  6 120.73---070.10
17 1 12502 73337272323302017210 18 22 12  9  9 15  7  6 120.73
```

IDL SPEDAS code loads empty variables for the three missing columns in the GFZ data, python pyspedas code skips these empty variables.


### FTP file data format

A description of the text file format can be found in the following file:
ftp://ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP/kp_ap.fmt

```
FORMAT FOR RECORDS OF SELECTED GEOMAGNETIC AND SOLAR ACTIVITY INDICES
-------------------------------------------------------------------------------
COLUMNS   FMT   DESCRIPTION
-------------------------------------------------------------------------------
 1- 2     I2    YEAR
 3- 4     I2    MONTH
 5- 6     I2    DAY

 7-10     I4    BARTELS SOLAR ROTATION NUMBER--a sequence of 27-day intervals
                  counted continuously from February 8, 1832.
11-12     I2    NUMBER OF DAY within the Bartels 27-day cycle.

13-14     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 0000 - 0300 UT.
15-16     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 0300 - 0600 UT.
17-18     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 0600 - 0900 UT.
19-20     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 0900 - 1200 UT.
21-22     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 1200 - 1500 UT.
23-24     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 1500 - 1800 UT.
25-26     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 1800 - 2100 UT.
27-28     I2    Kp or PLANETARY 3-HOUR RANGE INDEX for 2100 - 2400 UT.
29-31     I3    SUM of the eight Kp indices for the day expressed to the near-
                  est third of a unit.

32-34     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 0000 - 0300 UT.
35-37     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 0300 - 0600 UT.
38-40     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 0600 - 0900 UT.
41-43     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 0900 - 1200 UT.
44-46     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 1200 - 1500 UT.
47-49     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 1500 - 1800 UT.
50-52     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 1800 - 2100 UT.
53-55     I3    ap or PLANETARY EQUIVALENT AMPLITUDE for 2100 - 2400 UT.
56-58     I3    Ap or PLANETARY EQUIVALENT DAILY AMPLITUDE--the arithmetic mean
                  of the day's eight ap values.

59-61     F3.1  Cp or PLANETARY DAILY CHARACTER FIGURE--a qualitative estimate
                  of overall level of magnetic activity for the day determined
                  from the sum of the eight ap amplitudes.  Cp ranges, in steps
                  of one-tenth, from 0 (quiet) to 2.5 (highly disturbed).

62-62     I1    C9--a conversion of the 0-to-2.5 range of the Cp index to one
                  digit between 0 and 9.

63-65     I3    INTERNATIONAL SUNSPOT NUMBER.  Records contain the Zurich num-
                   ber through December 31, 1980, and the International Brus-
                   sels number thereafter.

66-70     F5.1  OTTAWA 10.7-CM SOLAR RADIO FLUX ADJUSTED TO 1 AU--measured at
                  1700 UT daily and expressed in units of 10 to the -22 Watts/
                  meter sq/hertz.  Observations began on February 14, 1947.
                  From that date through December 31, 1973, the fluxes given
                  here don't reflect the revisions Ottawa made in 1966. NOTE:
                  If a solar radio burst is in progress during the observation
                  the pre-noon or afternoon value is used (as indicated by a
                  flux qualifier value of 1 in column 71.

71-71     I1    FLUX QUALIFIER.  "0" indicates flux required no adjustment;
                  "1" indicates flux required adjustment for burst in progress
                  at time of measurement; "2" indicates a flux approximated by
                  either interpolation or extrapolation; and "3" indicates no
                  observation.
```


### GFZ HTTPS site

The .wdc files in GFZ are also available using HTTPS which is easier to use than ftp:

https://datapub.gfz-potsdam.de/download/10.5880.Kp.0001/Kp_definitive/


For the description of these files, see:

https://datapub.gfz-potsdam.de/download/10.5880.Kp.0001/kp_index_data_description_20210311.pdf


For more information, see:

https://www.gfz-potsdam.de/en/section/geomagnetism/data-products-services/geomagnetic-kp-index
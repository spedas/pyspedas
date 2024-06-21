Load Routines
====================================

This section describes the load routines for data sets that have direct support in PySPEDAS (as opposed to data sets
available via HAPI, CDAWeb, or other APIs).

Some key points that apply to most or all of these load routines:

* PySPEDAS maintains a cache of previously downloaded data.   The cache location to use is controlled by the SPEDAS_DATA_DIR environment variable.
  Many missions allow the user to set a data directory specific to that mission, overriding the global SPEDAS_DATA_DIR setting. For example,
  THM_DATA_DIR can be used to specify the local directory to use for the THEMIS mission.

* By default, PySPEDAS contacts the data server to get a list of filenames to fulfill the request,
  and compares the modification times on the server and locally cached files to determine
  whether the files need to be downloaded.

    * Specify **no_update=True** in the parameter list to bypass the data server, and only use
      locally cached files.  This is useful when internet services is slow or unavailable.

* The time range for data to be loaded is specified via the **trange** parameter, which should be a list ``[start_time end_time]``
  The start and end times can be specified as:

    * Strings, with somewhat flexible formatting:

        * "2007-03-23" (corresponds to time 00:00:00 on that date)
        * "2021-01-01/01:23:45.678"
    * Python or Numpy datetime objects
    * Numeric values corresponding to Unix timestamps (seconds since 1970-01-01/00:00:00)

    The start and end times should be supplied in the same format.

* For data sets supplied in CDF format, the following parameters may be supported:

  * **get_support_data**: If True, CDF variables with attributes identifying them as 'support data'
    will be loaded.  By default, only variables marked as 'data' would be loaded.

  * **varformat**: If supported by the load routine, the **varformat** parameter can be used to
    specify a wildcard pattern describing the CDF variable names to be loaded.

  * **varnames**: If supported by the load routine, **varnames** specifies a list of CDF variable names to be loaded.

* **prefix** and **suffix** parameters:  By default, tplot variable names of loaded data correspond to the variable names
  used in the data files. If supported by the load routine, these parameters can be used
  to modify the tplot variable names.  This is useful when the data files use generic names, like
  "Temperature" or "Pressure", which could conflict with similar variables from other data sets.

* Some data sets (e.g. MAVEN, MMS, THEMIS, etc) can be downloaded via their own servers, and
  are also archived at NASA's Space Physics Data Facility (SPDF).  If supported by the
  load routine, setting **spdf=True** will retrieve data from SPDF rather than the mission's
  default data server.   This is useful for cases where the mission's data server is offline
  or otherwise unavailable.

* **notplot**: Some load routines support setting **notplot=True** to return the data structures directly,
  rather than converting them to tplot variables and returning a variable list.

* **time_clip**: Some load routines support setting **time_clip=True** to ensure that only data in the specified trange
  will be returned.  By default, if the data is supplied in 1-day chunks, the entire file contents will be returned, even if
  the trange specifies less than a day.

* **downloadonly**: If supported, setting **downloadonly=True** downloads the data files, without
  converting them to tplot variables and loading them into Python.  This is useful if you intend to
  process the data files with some other tool, but PySPEDAS provides convenient access to the data.

* **probe**, **probes**, **site** and **sites** parameters: Some missions (for example, MMS, THEMIS, GOES, etc) provide data sets
  for multiple observatories.  The **probes** and **sites** parameters allow the user
  to select the observatories for which data should be loaded.  **probes** is generally used for
  space missions, while **sites** is used for ground-based data. (Check the documentation for the specific load routine to see if
  it uses the singular or plural forms.)


.. toctree::
   :maxdepth: 2

   ace
   akebono
   barrel
   cluster
   cnofs
   csswe
   de2
   dscovr
   elfin
   equator-s
   erg
   fast
   geotail
   geomagnetic_indices
   goes
   image
   kompsat
   kyoto
   lanl
   maven
   mica
   mms
   mth5
   noaa
   omni
   poes
   polar
   psp
   rbsp
   soho
   solo
   st5
   stereo
   swarm
   themis
   twins
   ulysses
   vires
   wind

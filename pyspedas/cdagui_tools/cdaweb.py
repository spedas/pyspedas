"""
Get information and download files from CDAWeb using cdasws.

For cdasws documentation, see:
    https://pypi.org/project/cdasws/
    https://cdaweb.gsfc.nasa.gov/WebServices/REST/py/cdasws/index.html

"""

import logging
import os
import re
from cdasws import CdasWs
from pytplot import cdf_to_tplot, netcdf_to_tplot, time_clip as tclip
from pyspedas.utilities.download import download
from pyspedas.cdagui_tools.config import CONFIG


class CDAWeb:
    """Get information and download files from CDAWeb using cdasws."""

    def __init__(self):
        """Initialize."""
        self.cdas = CdasWs(endpoint=CONFIG['cdas_endpoint'])

    def get_observatories(self):
        """Return a list of strings CDAWeb uses to designate missions or mission groups

        Examples
        --------

        >>> from pyspedas import CDAWeb
        >>> cdaweb_obj = CDAWeb()
        >>> obs_names = cdaweb_obj.get_observatories()
        """
        observatories = self.cdas.get_observatory_groups()
        onames = []
        for mission in observatories:
            mission_name = mission["Name"].strip()
            if len(mission_name) > 1 and mission_name != "(null)":
                onames.append(mission_name)
        return onames

    def get_instruments(self):
        """Return a list of strings CDAWeb uses to designate instrument or dataset types.

        Examples
        --------

        >>> from pyspedas import CDAWeb
        >>> cdaweb_obj = CDAWeb()
        >>> obs_names = cdaweb_obj.get_instruments()
        """
        instruments = self.cdas.get_instrument_types()
        inames = []
        for instrument in instruments:
            instr_name = instrument["Name"].strip()
            if len(instr_name) > 1 and instr_name != "(null)":
                inames.append(instr_name)
        return inames

    def clean_time_str(self, t):
        """Remove the time part from datetime variable."""
        t0 = re.sub("T.+Z", "", t)
        return t0

    def get_datasets(self, mission_list, instrument_list):
        """Return a list of datasets recognized by CDAWeb, given lists of missions and instruments.

        Parameters
        ----------
        mission_list: list of str
            List of mission names, as obtained from get_observatories()
        instrument_list: list of str
            List of instrument names, as obtained from get_instruments()

        Returns
        -------
        list of str
            A list of available datasets for the given missions and instruments.

        Examples
        --------

        >>> from pyspedas import CDAWeb
        >>> cdaweb_obj = CDAWeb()
        >>> dataset_list = cdaweb_obj.get_datasets(['ARTEMIS'],['Electric Fields (space)'])

        """
        thisdict = {"observatoryGroup": mission_list, "instrumentType": instrument_list}
        datasets = self.cdas.get_datasets(**thisdict)
        dnames = []
        for dataset in datasets:
            data_item = dataset["Id"].strip()
            if len(data_item) > 0 and data_item != "(null)":
                tinterval = dataset["TimeInterval"]
                t1 = tinterval["Start"].strip()
                t2 = tinterval["End"].strip()
                t1 = self.clean_time_str(t1)
                t2 = self.clean_time_str(t2)
                data_item += " (" + t1 + " to " + t2 + ")"
            dnames.append(data_item)
        return dnames

    def get_filenames(self, dataset_list, t0, t1):
        """Return a list of urls for a dataset between dates t0 and t1.

        Example: get_files(['THB_L2_FIT (2007-02-26 to 2020-01-17)'],
            '2010-01-01 00:00:00', '2010-01-10 00:00:00')

        Parameters
        ----------
        dataset_list: list of str
            A list of dataset names, as obtained from get_datasets()
        t0: str
            Start time for data to be retrieved
        t1: str
            End time for data to be retrieved

        Returns
        -------
        list of str
            A list of URLs for the given dataset and time range

        Examples
        --------

        >>> from pyspedas import CDAWeb
        >>> cdaweb_obj = CDAWeb()
        >>> urllist = cdaweb_obj.get_filenames(['THB_L2_FIT (2007-02-26 to 2020-01-17)'], '2010-01-01 00:00:00', '2010-01-10 00:00:00')
        """
        remote_url = []

        # Set times to cdas format
        t0 = t0.strip().replace(" ", "T", 1)
        if len(t0) == 10:
            t0 += "T00:00:01Z"
        elif len(t0) > 10:
            t0 += "Z"
        t1 = t1.strip().replace(" ", "T", 1)
        if len(t1) == 10:
            t1 += "T23:23:59Z"
        elif len(t1) > 10:
            t1 += "Z"

        # For each dataset, find the url of files
        for d in dataset_list:
            d0 = d.split(" ")
            if len(d0) > 0:
                status, result = self.cdas.get_data_file(d0[0], [], t0, t1)
                if status == 200 and (result is not None):
                    r = result.get("FileDescription")
                    if r is not None:
                        for f in r:
                            remote_url.append(f.get("Name"))
        return remote_url

    def cda_download(
        self,
        remote_files,
        local_dir=None,
        download_only=False,
        varformat=None,
        get_support_data=False,
        prefix="",
        suffix="",
        varnames=[],
        notplot=False,
        merge=False,
        trange=None,
        time_clip=False,
        force_download=False,
    ):
        """Download data files and (by default) load the data into tplot variables

        Parameters
        ----------
        remote_files : list of str
            List of remote file URLs, as obtained from function get_datasets().
        local_dir : str
            Local directory to save the data in.
        download_only : bool
            If True, download the data, but do not load it into tplot variables.
        varformat: str
            If set, specifies a pattern for which CDF or NetCDF variables to load.
        get_support_data: bool
            If True, load CDF variables marked as 'support_data'.
        prefix: str
            If set, prepend this string to the variable name when creating the tplot variables.
        suffix: str
            If set, append this string to the variable name when creating the tplot variables.
        varnames: list of str
            If set, specifies a list of variables to load from the data files.
        notplot: bool
            If True, return data directly as tplot data structures, rather than a list of tplot names.
        merge: bool
            If True, merge the data with existing tplot variables.
            If False (the default), overwrite existing tplot variables.
        trange: list of str
            If set, clip the time range of the data to these values.
        time_clip: bool
            If True, clip the time range of the data to the values in trange.
        force_download: bool
            If True, download the data even if it already exists locally.

        Returns
        -------
        tuple
            A tuple containing the number of files downloaded, the number of variables loaded, and a list of the tplot variables loaded.

        Examples
        --------
        >>> from pyspedas import CDAWeb
        >>> from pyspedas import tplot
        >>> cdaweb_obj = CDAWeb()
        >>> urllist = cdaweb_obj.get_filenames(['THB_L2_FIT (2007-02-26 to 2020-01-17)'], '2010-01-01 00:00:00', '2010-01-10 00:00:00')
        >>> result = cdaweb_obj.cda_download(urllist,local_dir="/tmp")
        >>> tplot('thb_fgs_gsm')
        """

        # Return quantities
        no_of_files = 0
        no_of_variables = 0
        loaded_vars = []

        # Set the local and remote directories
        remotehttp = CONFIG['remote_data_dir']
        if local_dir is None:
            local_dir = CONFIG["local_data_dir"]

        count = 0
        dcount = 0
        cdf_files = []
        netcdf_files = []
        all_files = []

        # Download the files
        for remotef in remote_files:
            f = remotef.strip().replace(remotehttp, "", 1)
            localf = os.path.normpath(local_dir + os.path.sep + f)
            localfiles = download(
                remote_file=remotef,
                local_file=localf,
                force_download=force_download,
            )
            if localfiles is None:
                continue
            for f in localfiles:
                if f is not None and len(f) > 0:
                    all_files.append(os.path.normpath(f))

        no_of_files = len(all_files)
        if no_of_files > 0:

            # Sort the file list
            all_files = list(set(all_files))
            all_files.sort()

            # Load the data into tplot variables
            if not download_only:
                # Separate cdf and netcdf files. All other files cannot be loaded into tplot.
                for f in all_files:
                    if f.endswith(".cdf"):
                        cdf_files.append(f)
                    elif f.endswith(".nc"):
                        netcdf_files.append(f)
                    else:
                        logging.warning("File type not supported: " + f)

                if len(cdf_files) > 0:
                    cdf_files.sort()
                    logging.info("Downloaded " + str(len(cdf_files)) + " CDF files.")
                    try:
                        cdf_vars = cdf_to_tplot(
                            cdf_files,
                            prefix=prefix,
                            suffix=suffix,
                            get_support_data=get_support_data,
                            varformat=varformat,
                            varnames=varnames,
                            notplot=notplot,
                            merge=merge,
                        )
                        if cdf_vars is not None:
                            loaded_vars.extend(cdf_vars)
                    except ValueError as err:
                        msg = "cdf_to_tplot could not load " + str(cdf_files)
                        msg += "\n\n"
                        msg += "Error from pytplot: " + str(err)
                        logging.error(msg)

                if len(netcdf_files) > 0:
                    netcdf_files.sort()
                    logging.info(
                        "Downloaded " + str(len(netcdf_files)) + " NetCDF files."
                    )
                    try:
                        netcdf_vars = netcdf_to_tplot(
                            netcdf_files,
                            prefix=prefix,
                            suffix=suffix,
                            merge=merge,
                        )
                        if netcdf_vars is not None:
                            loaded_vars.extend(netcdf_vars)
                    except ValueError as err:
                        msg = "netcdf_to_tplot could not load " + str(netcdf_files)
                        msg += "\n\n"
                        msg += "Error from pytplot: " + str(err)
                        logging.error(msg)

                loaded_vars = list(set(loaded_vars))
                no_of_variables = len(loaded_vars)
                logging.info("Number of tplot variables loaded:" + str(no_of_variables))

                if time_clip and trange is not None:
                    if trange[0] >= trange[1]:
                        logging.warning(
                            "trange values equal or out of order, no time clipping performed"
                        )
                    else:
                        tclip(
                            loaded_vars, trange[0], trange[1], suffix="", overwrite=True
                        )
                elif time_clip:
                    logging.warning("Warning: No trange specified for time_clip")

        return (no_of_files, no_of_variables, loaded_vars)

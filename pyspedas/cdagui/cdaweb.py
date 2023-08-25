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
from pytplot import cdf_to_tplot
from pyspedas.utilities.download import download


class CDAWeb():
    """Class for loading data from CDA web."""

    def __init__(self):
        """Initialize."""
        self.cdas = CdasWs()

    def get_observatories(self):
        """Return a list of missions."""
        observatories = self.cdas.get_observatory_groups()
        onames = []
        for mission in observatories:
            mission_name = mission["Name"].strip()
            if len(mission_name) > 1 and mission_name != "(null)":
                onames.append(mission_name)
        return onames

    def get_instruments(self):
        """Return a list of instrument types."""
        instruments = self.cdas.get_instrument_types()
        inames = []
        for instrument in instruments:
            instr_name = instrument['Name'].strip()
            if len(instr_name) > 1 and instr_name != "(null)":
                inames.append(instr_name)
        return inames

    def clean_time_str(self, t):
        """Remove the time part from datetime variable."""
        t0 = re.sub('T.+Z', '', t)
        return t0

    def get_datasets(self, mission_list, instrument_list):
        """Return a list of datasets given the missions and instruments.

        Example: get_datasets(['ARTEMIS'],['Electric Fields (space)'])
        """
        thisdict = {
            "observatoryGroup": mission_list,
            "instrumentType": instrument_list
        }
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
                data_item += " (" + t1 + ' to ' + t2 + ")"
            dnames.append(data_item)
        return dnames

    def get_filenames(self, dataset_list, t0, t1):
        """Return a list of urls for a dataset between dates t0 and t1.

        Example: get_files(['THB_L2_FIT (2007-02-26 to 2020-01-17)'],
            '2010-01-01 00:00:00', '2010-01-10 00:00:00')
        """
        remote_url = []

        # Set times to cdas format
        t0 = t0.strip().replace(' ', 'T', 1)
        if len(t0) == 10:
            t0 += "T00:00:01Z"
        elif len(t0) > 10:
            t0 += "Z"
        t1 = t1.strip().replace(' ', 'T', 1)
        if len(t1) == 10:
            t1 += "T23:23:59Z"
        elif len(t1) > 10:
            t1 += "Z"

        # For each dataset, find the url of files
        for d in dataset_list:
            d0 = d.split(' ')
            if (len(d0) > 0):
                status, result = self.cdas.get_data_file(d0[0], [], t0, t1)
                if (status == 200 and (result is not None)):
                    r = result.get('FileDescription')
                    for f in r:
                        remote_url.append(f.get('Name'))
        return remote_url

    def cda_download(self, remote_files, local_dir, download_only=False,
                     varformat=None, get_support_data=False, prefix='',
                     suffix='', varnames=[], notplot=False):
        """Download cdf files.

        Load cdf files into pytplot variables (optional).
        """
        result = []
        loaded_vars = []
        remotehttp = "https://cdaweb.gsfc.nasa.gov/sp_phys/data"
        count = 0
        dcount = 0
        for remotef in remote_files:
            tplot_loaded = 0
            f = remotef.strip().replace(remotehttp, '', 1)
            localf = local_dir + os.path.sep + f
            localfile = download(remote_file=remotef, local_file=localf)
            if localfile is None:
                continue
            localfile = localfile[0]  # download returns an array
            count += 1
            if localfile != '':
                dcount += 1
                if not download_only:
                    try:
                        cvars = cdf_to_tplot(localfile,
                                             suffix=suffix,
                                             get_support_data=get_support_data,
                                             varformat=varformat,
                                             varnames=varnames,
                                             notplot=notplot)
                        if cvars != [] and cvars is not None:
                            loaded_vars.extend(cvars)
                        tplot_loaded = 1
                    except ValueError as err:
                        msg = "cdf_to_tplot could not load " + localfile
                        msg += "\n\n"
                        msg += "Error from pytplot: " + str(err)
                        logging.error(msg)
                        tplot_loaded = 0
            else:
                logging.error(str(count) + '. There was a problem. Could not download \
                      file: ' + remotef)
                tplot_loaded = -1
                localfile = ''
            result.append([remotef, localfile, tplot_loaded])

        logging.info('Downloaded ' + str(dcount) + ' files.')
        if not download_only:
            loaded_vars = list(set(loaded_vars))
            logging.info('tplot variables:')
            for var in loaded_vars:
                logging.info(var)

        return result

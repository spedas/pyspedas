"""
Load data from the Cluster Science Archive.

This loading function uses the Cluster Science Archive:
    https://csa.esac.esa.int/
It is a web service, we create the query and the web service responds
with a CDF file which is packaged as tar.gz.

We download the tar.gz file directly, without using pyspedas.download().
"""
import logging
from pytplot import time_clip as tclip
from pytplot import time_string
from pytplot import time_double
from pytplot import cdf_to_tplot

import requests
import sys
import tarfile
import os
from pathlib import Path
from typing import List
from .config import CONFIG

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def cl_master_datatypes():
    """Return list of data types."""
    md = ['CE_WBD_WAVEFORM_CDF', 'CP_AUX_POSGSE_1M',
          'CP_CIS-CODIF_HS_H1_MOMENTS', 'CP_CIS-CODIF_HS_He1_MOMENTS',
          'CP_CIS-CODIF_HS_O1_MOMENTS', 'CP_CIS-CODIF_PAD_HS_H1_PF',
          'CP_CIS-CODIF_PAD_HS_He1_PF', 'CP_CIS-CODIF_PAD_HS_O1_PF',
          'CP_CIS-HIA_ONBOARD_MOMENTS', 'CP_CIS-HIA_PAD_HS_MAG_IONS_PF',
          'CP_EDI_AEDC', 'CP_EDI_MP', 'CP_EDI_SPIN', 'CP_EFW_L2_E3D_INERT',
          'CP_EFW_L2_P', 'CP_EFW_L2_V3D_INERT', 'CP_EFW_L3_E3D_INERT',
          'CP_EFW_L3_P', 'CP_EFW_L3_V3D_INERT', 'CP_FGM_5VPS', 'CP_FGM_FULL',
          'CP_FGM_SPIN', 'CP_PEA_MOMENTS', 'CP_PEA_PITCH_SPIN_DEFlux',
          'CP_PEA_PITCH_SPIN_DPFlux', 'CP_PEA_PITCH_SPIN_PSD', 'CP_RAP_ESPCT6',
          'CP_RAP_ESPCT6_R', 'CP_RAP_HSPCT', 'CP_RAP_HSPCT_R',
          'CP_RAP_ISPCT_CNO', 'CP_RAP_ISPCT_He', 'CP_STA_CS_HBR',
          'CP_STA_CS_NBR', 'CP_STA_CWF_GSE', 'CP_STA_CWF_HBR_ISR2',
          'CP_STA_CWF_NBR_ISR2', 'CP_STA_PSD', 'CP_WBD_WAVEFORM',
          'CP_WHI_ELECTRON_DENSITY', 'CP_WHI_NATURAL', 'JP_AUX_PMP', 'JP_AUX_PSE']
    return md


def cl_master_probes():
    """Return list of probe names."""
    mp = ['C1', 'C2', 'C3', 'C4']
    return mp


def cl_format_time(s):
    """Return a string formated for Cluster web services."""
    # Date format: YYYY-MM-DDThh:mm:ssZ
    r = time_string(time_double(s), "%Y-%m-%dT%H:%M:%SZ")
    return r


def load_csa(trange:List[str]=['2001-02-01', '2001-02-03'],
             probes:List[str]=['C1'],
             datatypes:List[str]=['CP_CIS-CODIF_HS_H1_MOMENTS'],
             downloadonly:bool=False,
             time_clip:bool=True,
             prefix:str='',
             suffix:str='',
             get_support_data:bool=False,
             varformat:str=None,
             varnames:List[str]=[],
             notplot:bool=False) -> List[str]:
    """Load data using the Cluster Science Data archive.

    Parameters
    ----------
        trange : list of str
            Time range [start, end].
            Default: ['2001-02-01', '2001-02-03']

        probes : list of str
            List of Cluster probes. Valid options: 'C1','C2','C3','C4', '*' to load all probes
            Default: ['C1']

        datatypes : list of str
            List of Cluster data types. Valid options::
              'CE_WBD_WAVEFORM_CDF', 'CP_AUX_POSGSE_1M',
              'CP_CIS-CODIF_HS_H1_MOMENTS', 'CP_CIS-CODIF_HS_He1_MOMENTS',
              'CP_CIS-CODIF_HS_O1_MOMENTS', 'CP_CIS-CODIF_PAD_HS_H1_PF',
              'CP_CIS-CODIF_PAD_HS_He1_PF', 'CP_CIS-CODIF_PAD_HS_O1_PF',
              'CP_CIS-HIA_ONBOARD_MOMENTS', 'CP_CIS-HIA_PAD_HS_MAG_IONS_PF',
              'CP_EDI_AEDC', 'CP_EDI_MP', 'CP_EDI_SPIN', 'CP_EFW_L2_E3D_INERT',
              'CP_EFW_L2_P', 'CP_EFW_L2_V3D_INERT', 'CP_EFW_L3_E3D_INERT',
              'CP_EFW_L3_P', 'CP_EFW_L3_V3D_INERT', 'CP_FGM_5VPS', 'CP_FGM_FULL',
              'CP_FGM_SPIN', 'CP_PEA_MOMENTS', 'CP_PEA_PITCH_SPIN_DEFlux',
              'CP_PEA_PITCH_SPIN_DPFlux', 'CP_PEA_PITCH_SPIN_PSD', 'CP_RAP_ESPCT6',
              'CP_RAP_ESPCT6_R', 'CP_RAP_HSPCT', 'CP_RAP_HSPCT_R',
              'CP_RAP_ISPCT_CNO', 'CP_RAP_ISPCT_He', 'CP_STA_CS_HBR',
              'CP_STA_CS_NBR', 'CP_STA_CWF_GSE', 'CP_STA_CWF_HBR_ISR2',
              'CP_STA_CWF_NBR_ISR2', 'CP_STA_PSD', 'CP_WBD_WAVEFORM',
              'CP_WHI_ELECTRON_DENSITY', 'CP_WHI_NATURAL', 'JP_AUX_PMP', 'JP_AUX_PSE'

            Default: ['CP_CIS-CODIF_HS_H1_MOMENTS']

        downloadonly: bool
            If true, do not use cdf_to_tplot.
            Default: False

        time_clip: bool
            If true, apply time clip to data.
            Default: False

        suffix: str
            The tplot variable names will be given this suffix.
            Default: ''

        get_support_data: bool
            If True, data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        varformat : str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (all variables will be loaded)

        varnames: str or list of str
            Load these variables only. If [] or ['*'], then load everything.
            Default: []

        notplot: bool
            If True, then data are returned in a hash table instead of
            being stored in tplot variables (useful for debugging, and
            access to multi-dimensional data products)
            Default: False

    Returns
    -------
        list of str
            List of tplot variables created (unless notplot keyword is used).

    Examples
    --------

    >>> import pyspedas
    >>> from pyspedas import tplot
    >>> fgm_vars = pyspedas.projects.cluster.load_csa(trange=['2008-11-01','2008-11-02'],datatypes=['CP_FGM_FULL'])
    >>> tplot(['B_vec_xyz_gse__C1_CP_FGM_FULL','B_mag__C1_CP_FGM_FULL'])
    """
    # Empty output in case of errors.
    tvars = []

    if prefix is None:
        prefix = ''
    if suffix is None:
        suffix = ''

    # Start and end dates
    start_date = cl_format_time(trange[0])
    end_date = cl_format_time(trange[1])

    # Delivery format
    delivery_format = 'CDF_ISTP'
    # Delivery interval
    delivery_interval = 'ALL'

    if not probes:
        return tvars

    if not datatypes:
        return tvars

    if not isinstance(probes, list):
        probes = [probes]

    if not isinstance(datatypes, list):
        datatypes = [datatypes]

    # TODO: Create a function that can resolve wildcards
    # similar to IDL spedas ssl_check_valid_name
    # my_datatypes=ssl_check_valid_name(uc_datatypes,master_datatypes)
    # my_probes=ssl_check_valid_name(uc_probes,master_probes)
    if probes[0] == '*':  # load all probes
        probes = cl_master_probes()

    # Construct the query string
    base_url = 'https://csa.esac.esa.int/csa-sl-tap/data?'
    query_string = ('retrieval_type=PRODUCT&START_DATE=' + start_date +
                    '&END_DATE=' + end_date +
                    '&DELIVERY_FORMAT=' + delivery_format +
                    '&DELIVERY_INTERVAL=' + delivery_interval +
                    '&NON_BROWSER')

    for p in probes:
        for d in datatypes:
            query_string += '&DATASET_ID=' + p + '_' + d

    # Encode the url urllib.parse.quote
    url = base_url + (query_string)

    local_path = CONFIG['local_data_dir'] # could be URI
    if is_fsspec_uri(local_path):
        local_protocol, lpath = local_path.split("://")
        local_fs = fsspec.filesystem(local_protocol, anon=False)

        out_gz = '/'.join([local_path, 'temp_cluster_file.tar.gz'])  # Temp file name
        fileobj = local_fs.open(out_gz, 'wb')
    else:
        Path(local_path).mkdir(parents=True, exist_ok=True)
        out_gz = os.path.join(local_path, 'temp_cluster_file.tar.gz')  # Temp file name
        fileobj = open(out_gz, 'wb')

    # Download the file.
    logging.info("Downloading Cluster data, please wait....")
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error("Download HTTP error: " + str(err))
        return tvars
    except requests.exceptions.RequestException as e:
        logging.error("Download error: " + str(e))
        return tvars
    logging.info("Download complete.")

    # Open the downloaded file.
    with fileobj as w:
        w.write(r.content)

    # Extract the tar archive.
    if is_fsspec_uri(out_gz):
        # Cloud-Awareness: Opens byte stream for tarfile package.
        bo = local_fs.open(out_gz, "rb")
        tar = tarfile.open(fileobj=bo)
    else:
        tar = tarfile.open(out_gz, "r:gz")
    f = tar.getnames()

    for member in tar.getmembers():
        if member.isfile():
            p = '/'.join([local_path, member.path])
            if is_fsspec_uri(p):
                membo = local_fs.open(p, "wb")
            else:
                os.makedirs(str(Path(p).parent), exist_ok=True)
                membo = open(p, "wb")

            # Python > 3.9 requirement from setup.py
            # note: data is written after file is read into memory
            # https://stackoverflow.com/a/62247729
            with tar.extractfile(member.path) as tarbo:
                membo.write(tarbo.read())

            membo.close()
    tar.close()
    # Remove the tar.gz file but keep the extracted.
    if is_fsspec_uri(out_gz):
        local_fs.delete(out_gz)
    else:
        os.remove(out_gz)

    # Get unique set of files.
    f_set = set(f)
    # File list with full path.
    sep = "/" if is_fsspec_uri(local_path) else os.path.sep
    out_files = [sep.join([local_path, s]) for s in list(f_set)]
    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    # Load data into tplot
    tvars = cdf_to_tplot(out_files,
                         prefix=prefix,
                         suffix=suffix,
                         get_support_data=get_support_data,
                         varformat=varformat,
                         varnames=varnames,
                         notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

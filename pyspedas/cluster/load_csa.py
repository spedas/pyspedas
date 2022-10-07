"""
Load data from the Cluster Science Archive.

This loading function uses the Cluster Science Archive:
    https://csa.esac.esa.int/
It is a web service, we create the query and the web service responts
with a CDF file which is packaged as tar.gz.

We download the tar.gr file directly, without using pyspedas.download().
"""
import logging
from pyspedas.analysis.time_clip import time_clip as tclip
from pyspedas.utilities.time_string import time_string
from pyspedas.utilities.time_double import time_double
from pytplot import cdf_to_tplot

import requests
import tarfile
import os
from pathlib import Path

from pyspedas.cluster.config import CONFIG


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
          'CP_WHI_ELECTRON_DENSITY', 'CP_WHI_NATURAL', 'JP_PMP', 'JP_PSE']
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


def load_csa(trange=['2001-02-01', '2001-02-03'],
             probes=['C1'],
             datatypes=['CP_CIS-CODIF_HS_H1_MOMENTS'],
             downloadonly=False,
             time_clip=True,
             suffix='',
             get_support_data=False,
             varformat=None,
             varnames=[],
             notplot=False):
    """Load data using the Cluster Science Data archive.

    Parameters:
        trange : list of str
            Time range [start, end].
        probes : list of str
            List of Cluster probes.
            Use ['*'] to load all. See cl_master_probes().
        datatypes : list of str
            List of Cluster data types.
            Use ['*'] to load all. See cl_master_datatypes().
        downloadonly: bool
            If true, do not use cdf_to_tplot.
        time_clip: bool
            If true, apply time clip to data.
        suffix: str (for pytplot)
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.
        get_support_data: bool (for pytplot)
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".
        varformat : str (for pytplot)
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.
        varnames: str or list of str (for pytplot)
            Load these variables only. If [] or ['*'], then load everything.
        notplot: bool (for pytplot)
            If True, then data are returned in a hash table instead of
            being stored in tplot variables (useful for debugging, and
            access to multi-dimensional data products)

    Returns:
        List of tplot variables created (unless notplot keyword is used).
    """
    # Empty output in case of errors.
    tvars = []

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

    local_path = CONFIG['local_data_dir']
    Path(local_path).mkdir(parents=True, exist_ok=True)
    out_gz = local_path + 'temp_cluster_file.tar.gz'  # Temp file name

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
    with open(out_gz, 'wb') as w:
        w.write(r.content)

    # Extract the tar archive.
    tar = tarfile.open(out_gz, "r:gz")
    f = tar.getnames()
    tar.extractall(path=local_path)
    tar.close()
    # Remove the tar.gz file but keep the extracted.
    os.remove(out_gz)

    # Get unique set of files.
    f_set = set(f)
    # File list with full path.
    out_files = [local_path+s for s in list(f_set)]
    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    # Load data into tplot
    tvars = cdf_to_tplot(out_files,
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

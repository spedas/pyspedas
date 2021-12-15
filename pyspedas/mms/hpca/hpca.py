
import numpy as np
import logging
import re
from pyspedas.mms.mms_load_data import mms_load_data
from pyspedas.mms.hpca.mms_hpca_set_metadata import mms_hpca_set_metadata
from pyspedas.mms.hpca.mms_get_hpca_info import mms_get_hpca_info
from pyspedas.mms.hpca.mms_hpca_energies import mms_hpca_energies
from pyspedas.mms.print_vars import print_vars
from pyspedas.mms.mms_config import CONFIG

from pytplot import get_data, store_data

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

@print_vars
def mms_load_hpca(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', 
    level='l2', datatype='moments', get_support_data=None, time_clip=False, no_update=False,
    varformat=None, varnames=[], suffix='', center_measurement=False, available=False, notplot=False, 
    latest_version=False, major_version=False, min_version=None, cdf_version=None, spdf=False,
    always_prompt=False):
    """
    This function loads HPCA data into tplot variables
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for HPCA include 'brst', 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            Valid datatypes for HPCA are 'moments' and 'ion'; the default is 'moments'

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        center_measurement: bool
            If True, the CDF epoch variables are time-shifted to the middle
            of the accumulation interval by their DELTA_PLUS_VAR and
            DELTA_MINUS_VAR variable attributes

        notplot: bool
            If True, then data are returned in a hash table instead of 
            being stored in tplot variables (useful for debugging, and
            access to multi-dimensional data products)

        available: bool
            If True, simply return the available data files (without downloading)
            for the requested paramters

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten

        cdf_version: str
            Specify a specific CDF version # to load (e.g., cdf_version='4.3.0')

        min_version: str
            Specify a minimum CDF version # to load

        latest_version: bool
            Only grab the latest CDF version in the requested time interval

        major_version: bool
            Only open the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidently save an incorrect password, or if your SDC password has changed

        spdf: bool
            If True, download the data from the SPDF instead of the SDC
            
    Returns:
        List of tplot variables created.

    """

    if level.lower() != 'l2':
        if varformat is None:
            if level.lower() != 'l1a':
                if datatype.lower() == 'ion':
                    varformat = '*'
                elif datatype.lower() == 'combined':
                    varformat = '*'
                elif datatype.lower() == 'rf_corr':
                    varformat = '*_RF_corrected'
                elif datatype.lower() == 'count_rate':
                    varformat = '*_count_rate'
                elif datatype.lower() == 'flux':
                    varformat = '*_flux'
                elif datatype.lower() == 'vel_dist':
                    varformat = '*_vel_dist_fn'
                elif datatype.lower() == 'bkgd_corr':
                    varformat = '*_bkgd_corrected'
                elif datatype.lower() == 'moments':
                    varformat = '*'
                else:
                    varformat = '*_RF_corrected'
                if varformat != None and varformat != '*':
                    datatype = 'ion'
                if level.lower() == 'sitl':
                    varformat = '*'
    else:
        if get_support_data is None:
            get_support_data = True

        if isinstance(datatype, str):
            if datatype not in ['ion', 'moments']:
                logging.warning("Unknown datatype: " + datatype + "for L2 HPCA data; expected 'ion' or 'moments', loading 'ion'")
                datatype = 'ion'

    tvars = mms_load_data(trange=trange, notplot=notplot, probe=probe, data_rate=data_rate, level=level, instrument='hpca',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, center_measurement=center_measurement, available=available, 
            latest_version=latest_version, major_version=major_version, min_version=min_version, cdf_version=cdf_version,
            spdf=spdf, always_prompt=always_prompt)
    
    if tvars is None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_hpca_set_metadata(probe=probe, suffix=suffix)

    if not isinstance(datatype, list):
        datatype = [datatype]
    if not isinstance(probe, list):
        probe = [probe]

    # Replace supplementary fields in 3D distribution variables with actual
    # values from supplementary tplot variables (theta).
    for dtype in datatype:
        if dtype == 'moments':
            continue

        for prb in probe:
            prb = str(prb)
            for tvar in tvars:
                df_var = re.search('^mms'+prb+'_hpca_[^_]+plus(_(phase_space_density|count_rate|flux)| ?)'+suffix+'$', tvar)
                if df_var:
                    df_data = get_data(tvar)
                    df_metadata = get_data(tvar, metadata=True)
                    theta_data = get_data('mms' + prb + '_hpca_centroid_elevation_angle' + suffix)

                    if theta_data is None:
                        info = mms_get_hpca_info()
                        theta = info['elevation']
                    else:
                        theta = theta_data

                    store_data(tvar, data={'x': df_data.times, 'y': df_data.y, 'v1': theta, 'v2': df_data.v2}, attr_dict=df_metadata)

                    # check if energy table contains all 0s
                    zerocheck = np.argwhere(df_data.v2 == 0.0)
                    if len(zerocheck) == 63:
                        #  energy table is all 0s, using hard coded table
                        energy_table = mms_hpca_energies()
                        logging.warning('Found energy table with all 0s: ' + tvar + '; using hard-coded energy table instead')
                        store_data(tvar, data={'x': df_data.times, 'y': df_data.y, 'v1': theta, 'v2': energy_table}, attr_dict=df_metadata)

    return tvars

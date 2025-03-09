"""
This function transforms MMS vector fields from GSM coordinates to LMN (boundary-normal) coordinates using the Shue et al., 1998 magnetopause model. The input and output tplot variables are specified by name_in and name_out, respectively. Additional optional parameters include specifying the input data coordinates (GSM or GSE), probe, and data rate. The function returns the name of the output variable containing the data in LMN coordinates.
"""

import numpy as np
import logging
from pytplot import get_data, store_data, options, get_coords
import pyspedas
from pyspedas.cotrans_tools.cotrans import cotrans
from pyspedas.cotrans_tools.gsm2lmn import gsm2lmn
from pyspedas import tinterpol, data_exists

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_cotrans_lmn(name_in, name_out, gsm=False, gse=False, probe=None, data_rate='srvy'):
    """
    Tranforms MMS vector fields from GSM coordinates to LMN (boundary-normal) coordinates
    using the Shue et al., 1998 magnetopause model

    Input
    ------
        name_in: str
            Name of the input tplot variable

        name_out: str
            Name of the output tplot variable

    Parameters
    -----------
        gsm: bool
            Flag to indicate the input data are in GSM coordinates

        gse: bool
            Flag to indicate the input data are in GSE coordinates; note: the input data 
            will be transformed to GSM prior to transforming to LMN

        probe: str
            Spacecraft probe #; if not specified, the routine attempts to extract from the 
            input variable name

        data_rate: str
            Data rate of the ephemeris support data to be loaded; default is 'srvy'

    Returns
    --------
        Name of the variable containing the data in LMN coordinates.

    """

    data_in = get_data(name_in)
    metadata_in = get_data(name_in, metadata=True)

    if data_in is None:
        logging.error('Error reading tplot variable: ' + name_in)
        return None

    data_in_coord = get_coords(name_in).lower()

    if data_in_coord != 'gse' and data_in_coord != 'gsm' and not gse and not gsm:
        logging.error('Please specify the coordinate system of the input data.')
        return

    # we'll need the probe if it's not specified via keyword
    if probe is None:
        sc_id = name_in.split('_')[0]

        if sc_id != '':
            probe = sc_id[-1]

        if probe not in ['1', '2', '3', '4']:
            logging.error('Error, probe not found; please specify the probe via the "probe" keyword.')
            return

    # load the spacecraft position data
    mec_vars = pyspedas.projects.mms.mec(trange=[min(data_in.times), max(data_in.times)], probe=probe, data_rate=data_rate)

    if mec_vars is None or len(mec_vars) == 0:
        logging.error('No MEC data found for probe %s and data rate %s; unable to transform to LMN.', probe, data_rate)
        return

    ephemeris_var = 'mms'+probe+'_mec_r_gsm'
    if not data_exists(ephemeris_var):
        logging.error('Ephemeris variable %s not found; unable to transform to LMN', ephemeris_var)
        return

    # interpolate the position data to the input data
    tinterp_vars = tinterpol(ephemeris_var, name_in, newname='mms'+probe+'_mec_r_gsm_interp')

    pos_data = get_data('mms'+probe+'_mec_r_gsm_interp')

    # we'll need the input data in GSM coordinates
    if data_in_coord != 'gsm':
        cotrans_out = cotrans(name_in, name_in + '_gsm', coord_out='gsm')
        data_in = get_data(name_in + '_gsm')
    
    swdata = solarwind_load([min(data_in.times), max(data_in.times)])

    logging.info('Transforming GSM -> LMN; this may take several minutes, depending on the size of the input.')
    Blmn = gsm2lmn(data_in.times, pos_data.y, data_in.y, swdata=swdata)

    saved = store_data(name_out, data={'x': data_in.times, 'y': Blmn}, attr_dict=metadata_in)

    if saved:
        options(name_out, 'legend_names', ['L', 'M', 'N'])
        return name_out
    else:
        logging.error('Problem creating tplot variable.')


def solarwind_load(trange, level='hro2', min5=False):
    """
    Loads solar wind data for use in the GSM to LMN transformation.

    Parameters
    ----------
        trange: list of float
            Time range of data to be loaded

        level: str
            Data level (default: hro2)

        min5: bool
            Flag indicating whether to load 1 minute or 5 minute data (default: 1 minute)

    Returns
    -------
        Numpy array of solar wind data with shape (N, 3), where N is the number of time points
        and the columns are the time, Bz GSM, and pressure.
    """

    if min5:
        datatype = '5min'
    else:
        datatype = '1min'
    omni_vars = pyspedas.projects.omni.data(trange=trange, level=level, datatype=datatype)
    bzgsm = get_data('BZ_GSM')
    dp = get_data('Pressure')
    return np.array([bzgsm.times, bzgsm.y, dp.y]).T

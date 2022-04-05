
import numpy as np
import logging
from pytplot import get_data, store_data, options
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans import cotrans
from pyspedas.cotrans.gsm2lmn import gsm2lmn
from pyspedas.mms import mec
from pyspedas import tinterpol, omni

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_cotrans_lmn(name_in, name_out, gsm=False, gse=False, probe=None, data_rate='srvy'):
    '''
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
            Data rate of the input data; default is 'srvy'

    Returns
    --------
        Name of the variable containing the data in LMN coordinates.

    '''

    data_in = get_data(name_in)
    metadata_in = get_data(name_in, metadata=True)

    if data_in is None:
        logging.error('Error reading tplot variable: ' + name_in)
        return None

    data_in_coord = cotrans_get_coord(name_in).lower()

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
    mec_vars = mec(trange=[min(data_in.times), max(data_in.times)], probe=probe, data_rate=data_rate)

    # interpolate the position data to the input data
    tinterp_vars = tinterpol('mms'+probe+'_mec_r_gsm', name_in, newname='mms'+probe+'_mec_r_gsm_interp')

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
    if min5:
        datatype = '5min'
    else:
        datatype = '1min'
    omni_vars = omni.data(trange=trange, level=level, datatype=datatype)
    bzgsm = get_data('BZ_GSM')
    dp = get_data('Pressure')
    return np.array([bzgsm.times, bzgsm.y, dp.y]).T

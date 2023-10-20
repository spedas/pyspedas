from .version import version
from pytplot import data_exists
from pytplot import tnames
from pytplot import time_string, time_datetime
from pytplot import time_float, time_double
from .utilities.tcopy import tcopy
from pytplot import tkm2re

from .analysis.avg_data import avg_data
from pytplot import clean_spikes
from .analysis.deriv_data import deriv_data
from .analysis.dpwrspc import dpwrspc
from pytplot import subtract_average
from pytplot import subtract_median
from pytplot import time_clip
from .analysis.tdeflag import tdeflag
from .analysis.tdpwrspc import tdpwrspc
from .analysis.tinterpol import tinterpol
from pytplot import tnormalize
from pytplot import tdotp
from pytplot import tcrossp
from pytplot import tsmooth
from .analysis.yclip import yclip
from .analysis.twavpol import twavpol
from pytplot import cdf_to_tplot

from .cotrans.cotrans import cotrans
from .cotrans.cotrans_get_coord import cotrans_get_coord
from .cotrans.cotrans_set_coord import cotrans_set_coord
from .cotrans.tvector_rotate import tvector_rotate
from .cotrans.cart2spc import cart2spc
from .cotrans.spc2cart import spc2cart
from .cotrans.sm2mlt import sm2mlt

from .mms import mms_load_mec, mms_load_fgm, mms_load_scm, mms_load_edi, \
    mms_load_edp, mms_load_eis, mms_load_feeps, \
    mms_load_hpca, mms_load_fpi, mms_load_aspoc, \
    mms_load_dsp, mms_load_fsm, mms_load_state
from .mms.feeps.mms_feeps_pad import mms_feeps_pad
from .mms.feeps.mms_feeps_gpd import mms_feeps_gpd
from .mms.eis.mms_eis_pad import mms_eis_pad
from .mms.hpca.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from .mms.hpca.mms_hpca_spin_sum import mms_hpca_spin_sum

from .maven import maven_load
from .sosmag.load import sosmag_load

from . import erg
from . import ulysses
from . import mica
from . import goes
from . import themis
from . import omni
from . import dscovr
from . import psp
from . import poes
from . import rbsp
from . import ace
from . import wind
from . import csswe
from . import cluster
from . import geotail
from . import twins
from . import stereo
from . import image
from . import polar
from . import fast
from . import equator_s
from . import solo
from . import secs
from . import kyoto
from . import swarm
from . import vires
from . import cnofs
from . import lanl
from . import st5
from . import de2
from . import akebono
from . import soho
from . import barrel
from . import elfin

# set up logging/console output
import logging
from os import environ

logging_level = environ.get('PYTPLOT_LOGGING_LEVEL')
logging_format = environ.get('PYTPLOT_LOGGING_FORMAT')
logging_date_fmt = environ.get('PYTPLOT_LOGGING_DATE_FORMAT')

if logging_format is None:
    logging_format = '%(asctime)s: %(message)s'

if logging_date_fmt is None:
    logging_date_fmt = '%d-%b-%y %H:%M:%S'

if logging_level is None:
    logging_level = logging.INFO
else:
    logging_level = logging_level.lower()
    if logging_level == 'debug':
        logging_level = logging.DEBUG
    elif logging_level == 'info':
        logging_level = logging.INFO
    elif logging_level == 'warn' or logging_level == 'warning':
        logging_level = logging.WARNING
    elif logging_level == 'error':
        logging_level = logging.ERROR
    elif logging_level == 'critical':
        logging_level = logging.CRITICAL

logging.captureWarnings(True)

# basicConfig here doesn't work if it has previously been called
logging.basicConfig(format=logging_format, datefmt=logging_date_fmt, level=logging_level)

# manually set the logger options from the defaults/environment variables
logger = logging.getLogger()
logger_handler = logger.handlers[0]  # should exist since basicConfig has been called
logger_fmt = logging.Formatter(logging_format, logging_date_fmt)
logger_handler.setFormatter(logger_fmt)
logger.setLevel(logging_level)

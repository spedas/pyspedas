# Import pyspedas tools into pyspedas namespace
# These are imported as a convenience for pyspedas users.  For internal pyspedas development, it is
# probably best to keep using the fully qualified module names.

from .analysis.avg_data import avg_data
from .analysis.deriv_data import deriv_data
from .analysis.dpwrspc import dpwrspc
from .analysis.tvectot import tvectot
from .analysis.tdeflag import tdeflag
from .analysis.tdpwrspc import tdpwrspc
from .analysis.tinterpol import tinterpol
from .analysis.yclip import yclip
from .analysis.twavpol import twavpol
from .cdagui.cdagui import cdagui
from .cotrans.cotrans import cotrans
from .cotrans.cotrans_get_coord import cotrans_get_coord
from .cotrans.cotrans_set_coord import cotrans_set_coord
from .cotrans.tvector_rotate import tvector_rotate
from .cotrans.cart2spc import cart2spc
from .cotrans.spc2cart import spc2cart
from .cotrans.sm2mlt import sm2mlt
from .cotrans.fac_matrix_make import fac_matrix_make
from .cotrans.gsm2lmn import gsm2lmn
from .cotrans.minvar import minvar
from .cotrans.minvar_matrix_make import minvar_matrix_make
from .cotrans.quaternions import qtom, qconj, qdotp, qmult, qnorm, qslerp, qcompose, qvalidate, qdecompose, mtoq
from .cotrans.tvector_rotate import tvector_rotate
from .cotrans.xyz_to_polar import xyz_to_polar
# Importing geopack causes IGRF coefficients to be loaded by the external geopack package, which may not be desired.
#from .geopack.get_tsy_params import get_tsy_params
#from .geopack.get_w_params import get_w
#from .geopack.kp2iopt import kp2iopt
#from .geopack.t01 import t01, tt01
#from .geopack.t89 import t89, tt89
#from .geopack.t96 import t96, tt96
#from .geopack.ts04 import tts04
from .hapi.hapi import hapi
from .utilities.spice.time_ephemeris import time_ephemeris
from .utilities.dailynames import dailynames
from .utilities.datasets import find_datasets
# Note: "download" and "download_file" might be problematic names to import, due to risk of conflict with other packages
from .utilities.download import download, download_file, check_downloaded_file
from .utilities.download_ftp import download_ftp
from .utilities.interpol import interpol
from .utilities.leap_seconds import load_leap_table
from .utilities.libs import libs
from .utilities.mpause_2 import mpause_2
from .utilities.mpause_t96 import mpause_t96
from .utilities.tcopy import tcopy
from .version import version


# Import pytplot tools into pyspedas namespace
# Note to developers: Do not use these imports for pyspedas internals, or it may cause
# circular dependencies.  Import directly from pytplot instead.

from pytplot import *

# Import routine names with mission prefixes into pyspedas namespace
from .mms import mms_load_mec, mms_load_fgm, mms_load_scm, mms_load_edi, \
    mms_load_edp, mms_load_eis, mms_load_feeps, \
    mms_load_hpca, mms_load_fpi, mms_load_aspoc, \
    mms_load_dsp, mms_load_fsm, mms_load_state, \
    mms_qcotrans, mms_cotrans_lmn, mms_cotrans_qrotate, mms_cotrans_qtransformer
from .mms.feeps.mms_feeps_pad import mms_feeps_pad
from .mms.feeps.mms_feeps_gpd import mms_feeps_gpd
from .mms.eis.mms_eis_pad import mms_eis_pad
from .mms.hpca.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from .mms.hpca.mms_hpca_spin_sum import mms_hpca_spin_sum
from .mms.mms_overview_plot import mms_overview_plot
from .mms.particles.mms_part_getspec import mms_part_getspec
from .mms.particles.mms_part_slice2d import mms_part_slice2d
from .maven import maven_load
from .sosmag.load import sosmag_load

# Make mission-specific namespaces available under pyspedas
from . import ace
from . import akebono
from . import barrel
from . import cluster
from . import cnofs
from . import csswe
from . import de2
from . import dscovr
from . import elfin
from . import equator_s
from . import erg
from . import fast
from . import geotail
from . import goes
from . import image
from . import kyoto
from . import lanl
from . import maven
from . import mica
from . import omni
from . import poes
from . import polar
from . import psp
from . import rbsp
from . import secs
from . import soho
from . import solo
from . import st5
from . import stereo
from . import swarm
from . import themis
from . import twins
from . import ulysses
from . import vires
from . import wind

# set up logging/console output
import logging
from os import environ

logging_level = environ.get('PYSPEDAS_LOGGING_LEVEL')
logging_format = environ.get('PYSPEDAS_LOGGING_FORMAT')
logging_date_fmt = environ.get('PYSPEDAS_LOGGING_DATE_FORMAT')

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

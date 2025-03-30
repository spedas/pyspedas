# Import pyspedas tools into pyspedas namespace
# These are imported as a convenience for pyspedas users.  For internal pyspedas development, it is
# probably best to keep using the fully qualified module names.

from .analysis.avg_data import avg_data
from .analysis.deriv_data import deriv_data
from .analysis.tvectot import tvectot
from .analysis.tinterpol import tinterpol
from .analysis.yclip import yclip
from .analysis.twavpol import twavpol
from .analysis.wavelet import wavelet
from .analysis.time_domain_filter import time_domain_filter
from .analysis.find_magnetic_nulls import find_magnetic_nulls_fote, classify_null_type
from .analysis.lingradest import lingradest
from .cdagui_tools.cdagui import cdagui
from .cdagui_tools.cdaweb import CDAWeb
from .cotrans_tools.cotrans import cotrans
from .cotrans_tools.cotrans_get_coord import cotrans_get_coord
from .cotrans_tools.cotrans_set_coord import cotrans_set_coord
from .cotrans_tools.tvector_rotate import tvector_rotate
from .cotrans_tools.cart2spc import cart2spc
from .cotrans_tools.spc2cart import spc2cart
from .cotrans_tools.sm2mlt import sm2mlt
from .cotrans_tools.fac_matrix_make import fac_matrix_make
from .cotrans_tools.gsm2lmn import gsm2lmn
from .cotrans_tools.lmn_matrix_make import lmn_matrix_make
from .cotrans_tools.minvar import minvar
from .cotrans_tools.minvar_matrix_make import minvar_matrix_make
from .cotrans_tools.quaternions import qtom, qconj, qdotp, qmult, qnorm, qslerp, qcompose, qvalidate, qdecompose, mtoq, qnormalize
from .cotrans_tools.tvector_rotate import tvector_rotate
from .cotrans_tools.xyz_to_polar import xyz_to_polar
# Importing geopack causes IGRF coefficients to be loaded by the external geopack package, which may not be desired.
#from .geopack.get_tsy_params import get_tsy_params
#from .geopack.get_w_params import get_w
#from .geopack.kp2iopt import kp2iopt
#from .geopack.t01 import t01, tt01
#from .geopack.t89 import t89, tt89
#from .geopack.t96 import t96, tt96
#from .geopack.ts04 import tts04
from .hapi_tools.hapi import hapi

from .particles.moments import moments_3d, spd_pgs_moments, spd_pgs_moments_tplot
from .particles.spd_part_products import spd_pgs_do_fac, spd_pgs_regrid
from .particles.spd_slice2d import slice1d_plot, slice2d, slice2d_plot
from .utilities.spice.time_ephemeris import time_ephemeris
from .utilities.dailynames import dailynames
from .utilities.datasets import find_datasets
# Note: "download" and "download_file" might be problematic names to import, due to risk of conflict with other packages
from .utilities.download import download, download_file, check_downloaded_file
from .utilities.download_ftp import download_ftp
from .utilities.find_ip_address import find_ip_address
from .utilities.interpol import interpol
from .utilities.leap_seconds import load_leap_table
from .utilities.libs import libs
from .utilities.mpause_2 import mpause_2
from .utilities.mpause_t96 import mpause_t96
from .utilities.tcopy import tcopy
from .utilities.is_gzip import is_gzip
from .version import version


# Import pytplot tools into pyspedas namespace
# Note to developers: Do not use these imports for pyspedas internals, or it may cause
# circular dependencies.  Import directly from pytplot instead.

from pytplot import *
from .projects.noaa.noaa_load_kp import noaa_load_kp
# omni must precede mms to avoid problems with circular imports
from .projects import omni

# Import routine names with mission prefixes into pyspedas namespace
from .projects.mms import mms_load_mec, mms_load_fgm, mms_load_scm, mms_load_edi, \
    mms_load_edp, mms_load_eis, mms_load_feeps, \
    mms_load_hpca, mms_load_fpi, mms_load_aspoc, \
    mms_load_dsp, mms_load_fsm, mms_load_state, \
    mms_qcotrans, mms_cotrans_lmn, mms_cotrans_qrotate, mms_cotrans_qtransformer
from .projects.mms.feeps_tools.mms_feeps_pad import mms_feeps_pad
from .projects.mms.feeps_tools.mms_feeps_gpd import mms_feeps_gpd
from .projects.mms.eis_tools.mms_eis_pad import mms_eis_pad
from .projects.mms.hpca_tools.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from .projects.mms.hpca_tools.mms_hpca_spin_sum import mms_hpca_spin_sum
from .projects.mms.plots.mms_overview_plot import mms_overview_plot
from .projects.mms.particles.mms_part_getspec import mms_part_getspec
from .projects.mms.particles.mms_part_slice2d import mms_part_slice2d


# The code below is needed for backward compatibility, so users can continue to do things
# like "from pyspedas.mms import mec" even after mms has been moved to the projects directory.

import sys
from importlib import import_module

# List of submodules we want to make available under the pyspedas namespace
submodules = ['ace', 'akebono', 'barrel', 'cluster', 'cnofs', 'csswe', 'de2', 'dscovr',
             'elfin', 'equator_s', 'erg', 'fast', 'geotail', 'goes', 'image', 'kompsat',
              'kyoto', 'lanl', 'maven', 'mica', 'mms', 'noaa', 'omni', 'poes', 'polar', 'psp',
              'rbsp', 'secs', 'soho', 'solo', 'st5', 'stereo', 'swarm', 'themis', 'themis.state_tools', 'twins',
              'ulysses'
              ]

for submodule in submodules:
    # Import the module from the new path
    full_module_path = f"pyspedas.projects.{submodule}"
    imported_module = import_module(full_module_path)

    # Add it to sys.modules under the old path
    sys.modules[f"pyspedas.{submodule}"] = imported_module

# This set of imports is still needed for backward compatibility, when using fully-qualified
# routine names in function calls, like "pyspedas.mms.mec()" rather than "pyspedas.projects.mms.mec()"

# Make mission-specific namespaces available under pyspedas
from .projects import ace
from .projects import akebono
from .projects import barrel
from .projects import cluster
from .projects import cnofs
from .projects import csswe
from .projects import de2
from .projects import dscovr
from .projects import elfin
from .projects import equator_s
from .projects import erg
from .projects import fast
from .projects import geotail
from .projects import goes
from .projects import image
from .projects import kompsat
# for backward compatibility
from .projects.kompsat.load import load as kompsat_load
from .projects import kyoto
from .projects import lanl
from .projects import maven
# for backward compatibility
from .projects.maven import maven_load
from .projects import mica
from .projects import mms
from .projects import noaa
from .projects import poes
from .projects import polar
from .projects import psp
from .projects import rbsp
from .projects import secs
from .projects import soho
from .projects import solo
from .projects import st5
from .projects import stereo
from .projects import swarm
from .projects import themis
from .projects import twins
from .projects import ulysses
from . import vires
from .projects import wind

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

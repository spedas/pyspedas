#Import pyspedas tools into pyspedas namespace
# These are imported as a convenience for pyspedas users.  For internal pyspedas development, it is
# probably best to keep using the fully qualified module names.

#from .pytplot import *

from .tplot_tools import get_y_range
from .tplot_tools import tplot_rename
from .tplot_tools import del_data
from .tplot_tools import store_data
from .tplot_tools import store
from .tplot_tools import get_data
from .tplot_tools import get
from .tplot_tools import str_to_float_fuzzy
from .tplot_tools import tplot_names
from .tplot_tools import wildcard_expand
from .tplot_tools import tplot_wildcard_expand
from .tplot_tools import tname_byindex
from .tplot_tools import tindex_byname
from .tplot_tools import options
from .tplot_tools import xlim
from .tplot_tools import ylim
from .tplot_tools import zlim
from .tplot_tools import tlimit
from .tplot_tools import tplot_save
from .tplot_tools import tnames
from .tplot_tools import convert_tplotxarray_to_pandas_dataframe
from .tplot_tools import tplot_restore
from .tplot_tools import is_pseudovariable
from .tplot_tools import count_traces
from .tplot_tools import get_timespan
from .tplot_tools import tplot_options
from .tplot_tools import tplot_rename
from .tplot_tools import tplot_copy
from .tplot_tools import replace_data
from .tplot_tools import replace_metadata
from .tplot_tools import get_ylimits
from .tplot_tools import rgb_color
from .tplot_tools import timebar
from .tplot_tools import databar
from .tplot_tools import del_data
from .tplot_tools import timespan
from .tplot_tools import timestamp
from .tplot_tools import time_float
from .tplot_tools import time_double
from .tplot_tools import time_float_one
from .tplot_tools import time_string_one
from .tplot_tools import time_string
from .tplot_tools import time_datetime
from .tplot_tools import sts_to_tplot
from .tplot_tools import set_coords
from .tplot_tools import get_coords
from .tplot_tools import set_units
from .tplot_tools import get_units
from .tplot_tools import data_exists
from .tplot_tools import link
from .tplot_tools import tres

from .tplot_tools import tinterp
from .tplot_tools import add_across
from .tplot_tools import add
from .tplot_tools import avg_res_data
from .tplot_tools import clip
from .tplot_tools import crop
from .tplot_tools import deflag
from .tplot_tools import degap
from .tplot_tools import derive
from .tplot_tools import divide
from .tplot_tools import interp_nan
from .tplot_tools import join_vec
from .tplot_tools import multiply
from .tplot_tools import spec_mult
from .tplot_tools import split_vec
from .tplot_tools import subtract
from .tplot_tools import pwr_spec
from .tplot_tools import clean_spikes
from .tplot_tools import tdotp
from .tplot_tools import tcrossp
from .tplot_tools import tnormalize
from .tplot_tools import subtract_median
from .tplot_tools import subtract_average
from .tplot_tools import smooth
from .tplot_tools import tsmooth
from .tplot_tools import time_clip
from .tplot_tools import tkm2re
from .tplot_tools import makegap
from .tplot_tools import tdeflag
from .tplot_tools import pwrspc
from .tplot_tools import tpwrspc
from .tplot_tools import dpwrspc
from .tplot_tools import tdpwrspc


from .tplot_tools import reduce_spec_dataset
from .tplot_tools import lineplot
from .tplot_tools import specplot
from .tplot_tools import specplot_make_1d_ybins
from .tplot_tools import get_var_label_ticks
from .tplot_tools import var_label_panel
from .tplot_tools import ctime
from .tplot_tools import highlight
from .tplot_tools import annotate
from .tplot_tools import tplot
from .tplot_tools import cdf_to_tplot
from .tplot_tools import netcdf_to_tplot
from .tplot_tools import tplot_ascii



from .analysis.avg_data import avg_data
from .analysis.deriv_data import deriv_data
from .analysis.tvectot import tvectot
from .analysis.tinterpol import tinterpol
from .analysis.yclip import yclip
from .analysis.twavpol import twavpol
from .analysis.wavelet import wavelet
from .analysis.wavelet98 import wavelet98
from .analysis.wave_signif import wave_signif
from .analysis.wav_data import wav_data
from .analysis.wavelet2 import wavelet2
from .analysis.time_domain_filter import time_domain_filter
from .analysis.find_magnetic_nulls import find_magnetic_nulls_fote, classify_null_type
from .analysis.lingradest import lingradest
from .cdagui_tools.cdagui import cdagui
from .cdagui_tools.cdaweb import CDAWeb
from .cotrans_tools.cotrans import cotrans
from .cotrans_tools.rotmat_get_coords import rotmat_get_coords
from .cotrans_tools.rotmat_set_coords import rotmat_set_coords
from .cotrans_tools.tvector_rotate import tvector_rotate
from .cotrans_tools.cart2spc import cart2spc
from .cotrans_tools.spc2cart import spc2cart
from .cotrans_tools.sphere_to_cart import sphere_to_cart
from .cotrans_tools.cart_to_sphere import cart_to_sphere
from .cotrans_tools.sm2mlt import sm2mlt
from .cotrans_tools.fac_matrix_make import fac_matrix_make
from .cotrans_tools.gsm2lmn import gsm2lmn
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
from .particles.spd_part_products import spd_pgs_do_fac, spd_pgs_regrid, spd_pgs_v_shift
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
from .utilities.xdegap import xdegap
from .version import version


from .projects.noaa.noaa_load_kp import noaa_load_kp
# omni must precede mms to avoid problems with circular imports
from .projects import omni
# lmn_matrix_make requires omni 
from .cotrans_tools.lmn_matrix_make import lmn_matrix_make
from .projects.kompsat.load import load as kompsat_load

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


from . import vires

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

# Now that logging is configured, check to see if pytplot is installed.  If so, advise the
# user that pytplot is now included with pyspedas, and that the external pytplot package can
# and should be removed.

try:
    import tplot_tools as old_pytplot
    # If we get here, the external package is installed.
    logging.info("You appear to have the external pytplot or pytplot-mpl-temp packages installed.")
    logging.info("PySPEDAS 2.0 and later now bundles the pytplot tools, and we recommend that you remove the external packages to avoid using obsolete code.")
    logging.info("To uninstall, run these commands in a terminal window (not a Python window!) in the environment you're using with PySPEDAS:")
    logging.info("pip uninstall pytplot")
    logging.info("pip uninstall pytplot-mpl-temp")
    logging.info("To update your own code for PySPEDAS 2.0 compatibility, please refer to our PySPEDAS 2.0 migration guide:")
    logging.info("https://pyspedas.readthedocs.io/en/latest/pyspedas_2_migration.html")
except ImportError:
    # Nothing to do here, external pytplot package not found
    pass

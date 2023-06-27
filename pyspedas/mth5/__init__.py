# Make sure that download folder exists
import os, pyspedas
from .config import CONFIG

if not os.path.exists(CONFIG['local_data_dir']):
    os.makedirs(CONFIG['local_data_dir'])

# Determine if MTH5 is in the scope
try:
    from mth5.clients.make_mth5 import FDSN
    from mth5.mth5 import MTH5
except ImportError:
    pyspedas.logging.error(f'MTH5 must be installed to use module {__name__}.')
    pyspedas.logging.error('Please install it using: pip install mth5')

# Remove imported
del os, pyspedas, CONFIG


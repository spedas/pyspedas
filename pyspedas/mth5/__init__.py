# Make sure that download folder exists
import os, pyspedas
from .config import CONFIG

if not os.path.exists(CONFIG['local_data_dir']):
    os.makedirs(CONFIG['local_data_dir'])

# Remove imported
del os, CONFIG

# Determine if MTH5 is in the scope
try:
    import mth5
    del mth5, pyspedas
except ImportError:
    pyspedas.logging.error(f'MTH5 must be installed to use module {__name__}.')
    pyspedas.logging.error('Please install it using: pip install mth5')
    raise

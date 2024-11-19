import os
import logging
import pyspedas
from pyspedas.mth5.config import CONFIG

# Make sure that download folder exists
if not os.path.exists(CONFIG['local_data_dir']):
    os.makedirs(CONFIG['local_data_dir'])

# Remove imported
del os, CONFIG

# Determine if MTH5 is in the scope
try:
    from mth5 import config as mth5_logger_config

except (ImportError, ModuleNotFoundError):
    logging.error(f'MTH5 must be installed to use module {__name__}.')
    logging.error("Please install it using: pip install mth5")
    raise

# # Synchronize mth5 logging output level with pyspedas logging output level
try:
    import loguru, pyspedas
    from mth5 import config as mth5_logger_config
    from pyspedas import logging_level
    from pyspedas.mth5.load_fdsn import _disable_loguru_warnings

    # This is how to disable all together
    # import warnings
    # warnings.filterwarnings('ignore')

    # TODO: terminate this code if handler logging_level is the same as in loguru

    mth5_logger_config['handlers'][0]['level'] = logging_level
    mth5_logger_config['handlers'][0]["filter"] = _disable_loguru_warnings
    mth5_logger_config['extra']['no_warning'] = False
    if loguru.logger._core.handlers:
        handler_id = next(iter(loguru.logger._core.handlers.keys()))
        loguru.logger.remove(handler_id)
        loguru.logger.configure(**mth5_logger_config)
        logging.debug('loguru synchronized with pyspedas logging')
except:
    logging.error('loguru synchronization error')
    pass
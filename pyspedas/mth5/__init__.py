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

# # Synchronize mth5 logging output level with pyspedas logging output level
try:
    import loguru, pyspedas
    from mth5 import config as mth5_logger_config
    from pyspedas import logging_level

    # TODO: terminate this code if handler logging_level is the same as in loguru

    mth5_logger_config['handlers'][0]['level'] = logging_level
    if loguru.logger._core.handlers:
        handler_id = next(iter(loguru.logger._core.handlers.keys()))
        loguru.logger.remove(handler_id)
        loguru.logger.configure(**mth5_logger_config)
        pyspedas.logging.info('loguru synchronized with pyspedas logging')
except:
    pyspedas.logging.error('loguru synchronization error')
    pass
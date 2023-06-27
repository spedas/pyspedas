# Make sure that download folder exists
import os
from .config import CONFIG

if not os.path.exists(CONFIG['local_data_dir']):
    os.makedirs(CONFIG['local_data_dir'])

# Remove imported
del os
del CONFIG
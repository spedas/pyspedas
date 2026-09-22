import os

CONFIG = {'no_download': False,
          'local_data_dir': 'elfin_data/',
          'remote_data_dir': 'https://data.elfin.ucla.edu/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "elfin")
apply_no_download_environment(CONFIG, "ELFIN_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'elfin/'])

if os.environ.get('ELFIN_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ELFIN_DATA_DIR']

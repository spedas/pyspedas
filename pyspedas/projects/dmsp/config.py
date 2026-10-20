"""DMSP archive and cache configuration."""
import os

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

CONFIG = {
    'local_data_dir': 'dmsp_data/',
    'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/dmsp/',
    'no_download': False,
}
apply_mission_preferences(CONFIG, 'dmsp')
apply_no_download_environment(CONFIG, 'DMSP_NO_DOWNLOAD')
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.path.join(os.environ['SPEDAS_DATA_DIR'], 'dmsp')
if os.environ.get('DMSP_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['DMSP_DATA_DIR']

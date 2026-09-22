import os

CONFIG = {'no_download': False,
          'local_data_dir': 'dscovr_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/dscovr/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "dscovr")
apply_no_download_environment(CONFIG, "DSC_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('DSC_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['DSC_DATA_DIR']
elif os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'dscovr'])

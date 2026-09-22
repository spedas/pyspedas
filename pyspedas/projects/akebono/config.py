import os

CONFIG = {'no_download': False,
          'local_data_dir': 'akebono_data/',
          'remote_data_dir': 'https://data.darts.isas.jaxa.jp/pub/akebono/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "akebono")
apply_no_download_environment(CONFIG, "AKEBONO_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'akebono'])

if os.environ.get('AKEBONO_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['AKEBONO_DATA_DIR']

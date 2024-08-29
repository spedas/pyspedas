import os

CONFIG = {'local_data_dir': 'pydata',
         #'local_data_dir': '/Users/eric/data/mms', # example of setting your local data directory on macOS
         #'local_data_dir': 'c:\users\eric\data\mms', # and Windows
          'mirror_data_dir': None, # e.g., '/Volumes/data_network/data/mms'
          'debug_mode': False,
          'download_only': False,
          'no_download': False}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'mms'])

if os.environ.get('MMS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['MMS_DATA_DIR']


if os.environ.get('MMS_MIRROR_DATA_DIR'):
    CONFIG['mirror_data_dir'] = os.environ['MMS_MIRROR_DATA_DIR']
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

CONFIG = {'local_data_dir': 'pydata',
         #'local_data_dir': '/Users/eric/data/mms', # example of setting your local data directory on macOS
         #'local_data_dir': 'c:\users\eric\data\mms', # and Windows
          'debug_mode': False,
          'download_only': True,
          'no_download': False}

# override local data directory with environment variables
if os.environ.get('ROOT_DATA_DIR'):
	CONFIG['local_data_dir'] = os.sep.join([os.environ['ROOT_DATA_DIR'], 'mms'])

if os.environ.get('MMS_DATA_DIR'):
	CONFIG['local_data_dir'] = os.environ['MMS_DATA_DIR']
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

CONFIG = {'local_data_dir': 'pydata',
          'debug_mode': False,
          'no_download': False}

# override local data directory with environment variables
if os.environ.get('ROOT_DATA_DIR'):
	CONFIG['local_data_dir'] = os.sep.join([os.environ['ROOT_DATA_DIR'], 'mms'])

if os.environ.get('MMS_DATA_DIR'):
	CONFIG['local_data_dir'] = os.environ['MMS_DATA_DIR']
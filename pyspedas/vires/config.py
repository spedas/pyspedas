import os
import logging
from viresclient import ClientConfig
import configparser

CONFIG = {
    'local_data_dir': 'vires_data/',
    'remote_data_dir': 'https://vires.services/ows',
    'access_token': ''
}

if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir']  = os.environ['SPEDAS_DATA_DIR'] # self-defined, e.g. '/Users/cao/Documents/Data_N_Res/data_local'

if os.environ.get('VIRES_DATA_DIR'):
    CONFIG['local_data_dir']  = os.environ['VIRES_DATA_DIR'] # self-defined, e.g. '/Users/cao/Documents/Data_N_Res/data_local'

if os.environ.get('VIRES_TOKEN'):
    CONFIG['access_token'] = os.environ['VIRES_TOKEN']
else:
    homedir = os.path.expanduser('~')
    token_file = os.path.join(homedir, '.viresclient.ini')

    # try to read from token file
    try:
        config = configparser.ConfigParser()
        config.read(token_file)
        access_token = config.get('https://vires.services/ows','token')
        CONFIG['access_token'] = access_token
    except FileNotFoundError:
        logging.warning('Unable to load VIRES access token from VIRES_TOKEN environment variable or token file %s.',
                        token_file)
        logging.warning(
            'Visit https://viresclient.readthedocs.io/en/latest/access_token.html to learn how to set up an account and generate an access token.')
    except configparser.NoSectionError:
        logging.warning('Unable to load VIRES access token from VIRES_TOKEN environment variable or token file %s.', token_file)
        logging.warning('Visit https://viresclient.readthedocs.io/en/latest/access_token.html to learn how to set up an account and generate an access token.')

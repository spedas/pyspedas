import os

CONFIG = {'local_data_dir': 'cluster_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/cluster/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'cluster'])

if os.environ.get('CLUSTER_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['CLUSTER_DATA_DIR']
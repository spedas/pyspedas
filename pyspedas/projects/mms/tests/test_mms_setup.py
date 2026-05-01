import os
import pickle

MMS_AUTH_U = os.getenv('MMS_AUTH_U')
MMS_AUTH_P = os.getenv('MMS_AUTH_P')
pickle.dump({'user': MMS_AUTH_U, 'passwd': MMS_AUTH_P}, open(os.sep.join([os.path.expanduser('~'), 'mms_auth_info.pkl']), 'wb'))

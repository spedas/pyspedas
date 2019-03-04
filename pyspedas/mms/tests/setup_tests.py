import os
import pickle

pickle.dump({'user': '', 'passwd': ''}, open(os.sep.join([os.path.expanduser('~'), 'mms_auth_info.pkl']), 'wb'))

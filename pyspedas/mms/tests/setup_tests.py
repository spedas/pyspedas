
import pickle

saved_auth = pickle.dump({'user': '', 'passwd': ''}, open(os.sep.join([os.path.expanduser('~'), 'mms_auth_info.pkl']), 'wb'))

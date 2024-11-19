from getpass import getpass
from scipy.io import readsav
import requests
import os
import pickle
import logging
import warnings


def mms_login_lasp(always_prompt=False, headers={}):
    """
    This function logs the user into the SDC and returns a tuple with: (requests.Session object, username)
    """
    homedir = os.path.expanduser('~')
    user_input_passwd = False
    saved_auth = None

    # try to read saved pickle
    try:
        auth_file = open(os.sep.join([homedir, 'mms_auth_info.pkl']), 'rb')
        saved_auth = pickle.load(auth_file)
        auth_file.close()
    except FileNotFoundError:
        pass

    # try to read the IDL sav file
    try:
        idl_auth_info = readsav(os.sep.join([homedir, 'mms_auth_info.sav']))
        saved_auth = {'user': idl_auth_info['auth_info'][0][0].decode("utf-8"),
                      'passwd': idl_auth_info['auth_info'][0][1].decode("utf-8")}
    except:
        pass

    if saved_auth is None or always_prompt == True:
        try:
            user = input('SDC username (blank for public access): ')
        except:
            logging.error('Error while reading SDC username/password; defaulting to public user...')
            user = ''

        if user != '': 
            passwd = getpass() 
        else: passwd = ''

        user_input_passwd = True
    else:
        user = saved_auth['user']
        passwd = saved_auth['passwd']

    session = requests.Session()

    if user != '':
        session.auth = (user, passwd)

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=ResourceWarning)
                testget = session.get('https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/download/science', verify=True, timeout=5, headers=headers)
        except:
            return session, None

        # check if the login failed
        if testget.status_code == 401:
            logging.error('Invalid password for user: ' + user + '; trying public access..')
            user = None

    # only save the user's user/passwd if login was successful
    if user_input_passwd and user is not None:
        saved_auth = pickle.dump({'user': user, 'passwd': passwd}, open(os.sep.join([homedir, 'mms_auth_info.pkl']), 'wb'))

    if user == '':
        user = None

    return session, user

from getpass import getpass
from scipy.io import readsav
import requests
import os
import pickle
import logging
import warnings


def mms_login_lasp(always_prompt=False, headers=None):
    """
    Log the user into the MMS Science Data Center (SDC).

    Returns a tuple with (requests.Session object, username).  If no
    credentials are available or credential validation fails, the returned
    username is ``None`` and the session is configured for public access.

    Saved credentials are read from ``~/mms_auth_info.pkl`` (PySPEDAS) or
    ``~/mms_auth_info.sav`` (IDL SPEDAS).  Delete those files to reset stale
    saved credentials before retrying with ``always_prompt=True``.
    """
    if headers is None:
        headers = {}

    homedir = os.path.expanduser("~")
    auth_info_path = os.sep.join([homedir, "mms_auth_info.pkl"])
    idl_auth_info_path = os.sep.join([homedir, "mms_auth_info.sav"])
    user_input_passwd = False
    saved_auth = None

    # try to read saved pickle
    try:
        with open(auth_info_path, "rb") as auth_file:
            saved_auth = pickle.load(auth_file)
    except FileNotFoundError:
        pass

    # try to read the IDL sav file
    try:
        idl_auth_info = readsav(idl_auth_info_path)
        saved_auth = {
            "user": idl_auth_info["auth_info"][0][0].decode("utf-8"),
            "passwd": idl_auth_info["auth_info"][0][1].decode("utf-8"),
        }
    except:
        pass

    if saved_auth is None or always_prompt:
        try:
            user = input("SDC username (blank for public access): ")
        except:
            logging.error(
                "Error while reading SDC username/password; defaulting to public user..."
            )
            user = ""

        if user != "":
            passwd = getpass()
        else:
            passwd = ""

        user_input_passwd = True
    else:
        try:
            user = saved_auth["user"] or ""
            passwd = saved_auth["passwd"] or ""
        except (KeyError, TypeError):
            logging.warning(
                "Ignoring invalid MMS SDC credentials in %s or %s; using public access. "
                "Delete the stale file and rerun with always_prompt=True to reset saved credentials.",
                auth_info_path,
                idl_auth_info_path,
            )
            user = ""
            passwd = ""

    session = requests.Session()

    if user != "":
        session.auth = (user, passwd)

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=ResourceWarning)
                testget = session.get(
                    "https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/download/science",
                    verify=True,
                    timeout=5,
                    headers=headers,
                )
        except Exception as exc:
            logging.warning(
                "Unable to verify MMS SDC credentials; using public access. "
                "If authentication keeps failing, delete saved credentials at %s "
                "and/or %s, then rerun with always_prompt=True. Error: %s",
                auth_info_path,
                idl_auth_info_path,
                exc,
            )
            session.auth = None
            return session, None

        # check if the login failed
        if testget.status_code == 401:
            logging.error(
                "Invalid MMS SDC password for user %s; using public access. "
                "If this came from saved credentials, delete %s and/or %s, "
                "then rerun with always_prompt=True.",
                user,
                auth_info_path,
                idl_auth_info_path,
            )
            session.auth = None
            user = None

    # only save the user's user/passwd if login was successful
    if user_input_passwd and user is not None:
        with open(auth_info_path, "wb") as auth_file:
            pickle.dump({"user": user, "passwd": passwd}, auth_file)

    if user == "":
        user = None

    return session, user

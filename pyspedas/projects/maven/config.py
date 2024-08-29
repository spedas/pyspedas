import os

CONFIG = {"local_data_dir": "maven_data/", "maven_username": "", "maven_password": ""}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "maven"])

if os.environ.get("MAVEN_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["MAVEN_DATA_DIR"]

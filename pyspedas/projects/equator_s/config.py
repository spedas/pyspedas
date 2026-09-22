import os

CONFIG = {
    "no_download": False,
    "local_data_dir": "equator-s_data/",
    "remote_data_dir": "https://spdf.gsfc.nasa.gov/pub/data/equator-s/",
}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "equator_s")
apply_no_download_environment(CONFIG, "EQUATORS_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get("EQUATORS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["EQUATORS_DATA_DIR"]
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "equator-s"])

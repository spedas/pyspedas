"""SWFO archive and cache configuration."""
import os
from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

CONFIG = {
    "local_data_dir": "swfo_data/",
    "remote_data_dir": "https://archive.data.noaa.gov/satellite-spaceweather/",
    "no_download": False,
}
apply_mission_preferences(CONFIG, "swfo")
apply_no_download_environment(CONFIG, "SWFO_NO_DOWNLOAD")
if os.environ.get("SWFO_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["SWFO_DATA_DIR"]
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.path.join(os.environ["SPEDAS_DATA_DIR"], "swfo")

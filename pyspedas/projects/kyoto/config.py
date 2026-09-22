import os

CONFIG = {
    "no_download": False,
    "remote_data_dir_ae": "https://wdc.kugi.kyoto-u.ac.jp/",
    "remote_data_dir_dst": "http://wdc.kugi.kyoto-u.ac.jp/",
    "local_data_dir": "pydata/geom_indices/kyoto/",
}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "kyoto")
apply_no_download_environment(CONFIG, "KYOTO_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join(
        [os.environ["SPEDAS_DATA_DIR"], "geom_indices/kyoto/"]
    )

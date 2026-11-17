import os

CONFIG = {
    "no_download": False,
    "local_data_dir": "goes_data/",
    "remote_data_dir": "https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/",  # original netCDF file format
    "remote_goes_r": "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/",  # GOES-R satellites (16 and later)
    "remote_goes_r_reprocessed": "https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/science/",  # Reprocessed data for GOES 8-15 in GOES-R format
}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "goes")
apply_no_download_environment(CONFIG, "GOES_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "goes"])

if os.environ.get("GOES_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["GOES_DATA_DIR"]

import os

CONFIG = {
    "local_data_dir": "geom_indices/",
    "gfz_remote_data_dir": "https://datapub.gfz-potsdam.de/download/10.5880.Kp.0001/Kp_definitive/",
    "noaa_remote_data_dir": "https://www.ngdc.noaa.gov/stp/space-weather/geomagnetic-data/INDICES/KP_AP/"
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join(
        [os.environ["SPEDAS_DATA_DIR"], "geom_indices"]
    )

if os.environ.get("KP_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["KP_DATA_DIR"]

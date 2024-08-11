import os

CONFIG = {
    "local_data_dir": "equator-s_data/",
    "remote_data_dir": "https://spdf.gsfc.nasa.gov/pub/data/equator-s/",
}

# override local data directory with environment variables
if os.environ.get("EQUATORS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["EQUATORS_DATA_DIR"]
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "equator-s"])

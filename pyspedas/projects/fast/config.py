import os

CONFIG = {
    "local_data_dir": "fast_data/",
    "remote_data_dir": "https://spdf.gsfc.nasa.gov/pub/data/fast/",
}

# override local data directory with environment variables
if os.environ.get("FAST_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["FAST_DATA_DIR"]
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "fast"])

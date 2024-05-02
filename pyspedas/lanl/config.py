import os

CONFIG = {
    "local_data_dir": "lanl_data/",
    "remote_data_dir": "https://spdf.gsfc.nasa.gov/pub/data/lanl/",
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "lanl"])

if os.environ.get("LANL_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["LANL_DATA_DIR"]

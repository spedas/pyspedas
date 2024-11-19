import os

CONFIG = {
    "local_data_dir": "poes_data/",
    "remote_data_dir": "https://spdf.gsfc.nasa.gov/pub/data/noaa/",
    "ncei_remote_data_dir": "https://www.ncei.noaa.gov/data/poes-metop-space-environment-monitor/access/l2/v01r00/cdf/",
}

# override local data directory with environment variables
if os.environ.get("POES_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["POES_DATA_DIR"]
elif os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "poes"])

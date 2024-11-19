import os

CONFIG = {
    "local_data_dir": "geom_indices/",
    "remote_data_dir": "http://themis.ssl.berkeley.edu/data/themis/",
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join(
        [os.environ["SPEDAS_DATA_DIR"], "geom_indices"]
    )

if os.environ.get("KP_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["KP_DATA_DIR"]

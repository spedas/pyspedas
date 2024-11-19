import os

CONFIG = {
    "remote_data_dir_ae": "https://wdc.kugi.kyoto-u.ac.jp/ae_provisional/",
    "remote_data_dir_dst": "http://wdc.kugi.kyoto-u.ac.jp/",
    "local_data_dir": "pydata/geom_indices/kyoto/",
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join(
        [os.environ["SPEDAS_DATA_DIR"], "geom_indices/kyoto/"]
    )

import os

CONFIG = {
    "local_data_dir": "maven/",
    "remote_data_dir": "https://spdf.gsfc.nasa.gov/pub/data/maven/",
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "maven"])

if os.environ.get("MAVEN_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["MAVEN_DATA_DIR"]

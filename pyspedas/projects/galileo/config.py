import os

datasets = [
    {
        "type": "ephemeris",
        "abrev": "jovicentric",
        "full_set": "Galileo/Ephemeris/Jovicentric",
        "description": "Galileo PWS Jupiter orbit parameters",
    },
    {
        "type": "mag",
        "abrev": "fce",
        "full_set": "Galileo/MAG/Fce",
        "description": "Galileo MAG - Cyclotron Electron Frequnecy",
    },
    {
        "type": "mag",
        "abrev": "magnitude",
        "full_set": "Galileo/MAG/Magnitude",
        "description": "Galileo MAG - B-Field Magnitude",
    },
]


CONFIG = {
    "local_data_dir": "galileo/",
    "remote_data_dir": "https://jupiter.physics.uiowa.edu/das/server",
    "datasets": datasets,
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "galileo"])

if os.environ.get("GALILEO_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["GALILEO_DATA_DIR"]

import os

datasets = [
    {
        "type": "ephemeris",
        "abrev": "europa",
        "full_set": "Juno/Ephemeris/EuropaCoRotational",
        "description": "Juno Europa Co-Rotational orbit",
    },
    {
        "type": "ephemeris",
        "abrev": "ganymede",
        "full_set": "Juno/Ephemeris/GanymedeCoRotational",
        "description": "Juno Ganymede Co-Rotational orbit",
    },
    {
        "type": "ephemeris",
        "abrev": "geocentric",
        "full_set": "Juno/Ephemeris/Geocentric",
        "description": "Juno Earth orbit parameters",
    },
    {
        "type": "ephemeris",
        "abrev": "heliocentric",
        "full_set": "Juno/Ephemeris/Heliocentric",
        "description": "Juno Solar orbit parameters",
    },
    {
        "type": "ephemeris",
        "abrev": "io",
        "full_set": "Juno/Ephemeris/IoCoRotational",
        "description": "Juno Io Co-Rotational orbit parameters",
    },
    {
        "type": "ephemeris",
        "abrev": "jse",
        "full_set": "Juno/Ephemeris/JSE_Attitude",
        "description": "Juno Jupiter Solar Ecliptic Pointing angles",
    },
    {
        "type": "ephemeris",
        "abrev": "jovicentric",
        "full_set": "Juno/Ephemeris/Jovicentric",
        "description": "Juno Jupiter orbit parameters",
    },
    {
        "type": "fgm",
        "abrev": "electron",
        "full_set": "Juno/FGM/ElectronCyclotron",
        "description": "Electron Cyclotron Resonance Frequency",
    },
    {
        "type": "fgm",
        "abrev": "mag",
        "full_set": "Juno/FGM/MagComponents",
        "description": "Quicklook Magnetic Field Compontents in Payload; Planetocentric or Sun State Coordinates.",
    },
    {
        "type": "fgm",
        "abrev": "magnitude",
        "full_set": "Juno/FGM/Magnitude",
        "description": "Magnetic Field Magnitude from payload coordinates data",
    },
]


CONFIG = {
    "local_data_dir": "juno/",
    "remote_data_dir": "https://jupiter.physics.uiowa.edu/das/server",
    "datasets": datasets,
}

# override local data directory with environment variables
if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["local_data_dir"] = os.sep.join([os.environ["SPEDAS_DATA_DIR"], "juno"])

if os.environ.get("JUNO_DATA_DIR"):
    CONFIG["local_data_dir"] = os.environ["JUNO_DATA_DIR"]

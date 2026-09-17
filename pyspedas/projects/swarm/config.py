
CONFIG = {'remote_data_dir': 'https://vires.services/'}

from pyspedas.preferences import apply_mission_preferences

apply_mission_preferences(CONFIG, "swarm")

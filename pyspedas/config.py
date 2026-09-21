"""Package-wide PySPEDAS defaults (separate from mission settings)."""

import os
from pathlib import Path

from .preferences import apply_pyspedas_preferences


CONFIG = {
    "plotting": {
        "global_display": True,
        "plot_directory": "pyspedas_plots",
    },
    "testing": {
        "output_dir": "_testing_output",
        "validation_dir": "https://github.com/spedas/test_data/raw/refs/heads/main/",
        "global_display": False,
    },
    "s3": {
        "use_anon_access": True,
    },
}

apply_pyspedas_preferences(CONFIG)

def _display_from_environment(name: str) -> bool:
    value = os.environ[name].strip().lower()
    if value not in {"true", "false", "1", "0", "yes", "no"}:
        raise ValueError(f"{name} must be true or false")
    return value in {"true", "1", "yes"}


if "PYSPEDAS_GLOBAL_DISPLAY" in os.environ:
    display = _display_from_environment("PYSPEDAS_GLOBAL_DISPLAY")
    CONFIG["plotting"]["global_display"] = display
    CONFIG["testing"]["global_display"] = display

if "PYSPEDAS_TEST_GLOBAL_DISPLAY" in os.environ:
    CONFIG["testing"]["global_display"] = _display_from_environment(
        "PYSPEDAS_TEST_GLOBAL_DISPLAY"
    )

if "PYSPEDAS_PLOT_DIRECTORY" in os.environ:
    CONFIG["plotting"]["plot_directory"] = os.environ["PYSPEDAS_PLOT_DIRECTORY"]

if os.environ.get("SPEDAS_DATA_DIR"):
    CONFIG["testing"]["output_dir"] = str(
        Path(os.environ["SPEDAS_DATA_DIR"]) / "_testing_output"
    )
if os.environ.get("PYSPEDAS_TESTING_DIR"):
    CONFIG["testing"]["output_dir"] = os.environ["PYSPEDAS_TESTING_DIR"]
if os.environ.get("PYSPEDAS_VALIDATION_DIR"):
    CONFIG["testing"]["validation_dir"] = os.environ["PYSPEDAS_VALIDATION_DIR"]

if os.environ.get("PYSPEDAS_S3_USE_ANON_ACCESS"):
    CONFIG["s3"]["use_anon_access"] = os.environ["PYSPEDAS_S3_USE_ANON_ACCESS"]

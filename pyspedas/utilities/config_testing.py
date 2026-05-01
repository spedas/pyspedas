"""Parameters for pyspedas testing files.

Specify local output directory for testing, and remote directory with SPEDAS validation files.
"""

import os

TESTING_CONFIG = {
    "local_testing_dir": "_testing_output",  # Testing output will be saved here
    "remote_validation_dir": "https://github.com/spedas/test_data/raw/refs/heads/main/",  # SPEDAS-pyspedas validation files can be found here
    "global_display": False,  # Whether to display plots during testing
}

# Override local output directory with environment variables, if there are any
if os.environ.get("SPEDAS_DATA_DIR"):
    TESTING_CONFIG["local_testing_dir"] = os.sep.join(
        [os.environ["SPEDAS_DATA_DIR"], "_testing_output"]
    )
# Override local output directory with a local path
# TESTING_CONFIG["local_testing_dir"] = os.path.expanduser("~/data/_testing_output")

if os.environ.get("PYSPEDAS_TESTING_DIR"):
    TESTING_CONFIG["local_testing_dir"] = os.environ["PYSPEDAS_TESTING_DIR"]

# Override remote validation directory with environment variables, if there are any
if os.environ.get("PYSPEDAS_VALIDATION_DIR"):
    TESTING_CONFIG["remote_validation_dir"] = os.environ["PYSPEDAS_VALIDATION_DIR"]

# Override remote validation directory with a local path for offline testing
# TESTING_CONFIG["remote_validation_dir"] = os.path.expanduser("~/work/GitHub/test_data")

# Override global display setting with environment variables, if there are any
if os.environ.get("PYSPEDAS_GLOBAL_DISPLAY"):
    TESTING_CONFIG["global_display"] = bool(os.environ["PYSPEDAS_GLOBAL_DISPLAY"])

# Override global display setting for testing
# TESTING_CONFIG["global_display"] = True


def test_data_download_file(validation_dir, sub_dir, file_name, output_dir):
    """
    Fetch a validation tplot file_name from the configured remote directory or from local directory.

    This function is used in unit tests to download validation data files needed for testing.

    Parameters
    ----------
    validation_dir : str
        Base URL or path that hosts validation data files.
        For example: "https://github.com/spedas/test_data/raw/refs/heads/main/"
    sub_dir : str
        Remote subdirectory that contains the desired sub_dir/file_name.
        For example: "analysis_tools"
    file_name : str
        Name of the file to download.
        For example: "wavelet_test.tplot"
    output_dir : str
        Local destination directory for downloaded files.
        For example: "/data/_testing_output"

    Returns
    -------
    str
        Full path to the downloaded validation file, or an empty string if the
        file could not be retrieved.
    """

    import os
    import logging
    from pyspedas.utilities.download import download

    filename = ""
    remote_file = os.path.join(sub_dir, file_name)
    # Download the file if it doesn't already exist locally
    local_file = os.path.join(validation_dir, remote_file)
    if not os.path.exists(local_file):
        datafile = download(
            remote_file=remote_file,
            remote_path=validation_dir,
            local_path=output_dir,
            no_download=False,
        )
    else:
        datafile = [local_file]  # File already exists locally

    if not datafile:
        # Skip tests
        logging.info("Cannot download data validation file. Filename: " + remote_file)
        return filename

    filename = datafile[0]

    return filename

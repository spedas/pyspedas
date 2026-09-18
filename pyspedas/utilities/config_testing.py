"""Parameters for pyspedas testing files.

Specify local output directory for testing, and remote directory with SPEDAS validation files.
"""

from pyspedas.config import CONFIG

# Compatibility for code importing the former test-only configuration. New tests
# should read CONFIG["testing"] directly.
TESTING_CONFIG = {
    "local_testing_dir": CONFIG["testing"]["output_dir"],
    "remote_validation_dir": CONFIG["testing"]["validation_dir"],
    "global_display": CONFIG["testing"]["global_display"],
}


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

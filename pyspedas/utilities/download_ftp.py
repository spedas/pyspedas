from ftplib import FTP
import os
import time
import logging


def download_ftp(
    ftp_server,
    remote_path,
    remote_file,
    local_path,
    local_file=None,
    username="anonymous",
    password="anonymous@",
    force_download=False,
):
    """
    Download a file from an FTP server.

    Parameters
    ----------
    ftp_server : str
        FTP server name or IP address.
    remote_path : str
        Path on the FTP server where the file is located.
    remote_file : str
        Name of the file to download.
    local_path : str
        Local directory to save the file.
    local_file : str, optional
        Name of the file to save locally. If not provided, the name of the remote file is used.
    username : str, optional
        Username for the FTP server. Default is 'anonymous'.
    password : str, optional
        Password for the FTP server. Default is 'anonymous@'.
    force_download : bool, optional
        Force the download even if the remote file is not newer than the local file. Default is False.

    Returns
    -------
    list
        A list containing the path of the downloaded file.

    Raises
    ------
    Exception
        If the remote file is not found on the FTP server.

    Examples
    --------
    >>> from pyspedas import download_ftp
    >>> ftp_site = "ftp.gfz-potsdam.de"
    >>> kp_dir = "/pub/home/obs/kp-ap/wdc/yearly/"
    >>> remote_file = "kp2012.wdc"
    >>> local_dir = "/tmp/"
    >>> files = download_ftp(ftp_site, kp_dir, remote_file, local_dir)
    >>> print(files)
    ['/tmp/kp2012.wdc']
    """
    return_files = []

    try:
        with FTP(ftp_server) as ftp:
            ftp.login(user=username, passwd=password)
            ftp.cwd(remote_path)  # Change to the directory containing the file

            if local_file is None:
                local_file = os.path.join(local_path, remote_file)

            # Check if remote file exists
            if remote_file not in ftp.nlst():
                msg = f"File '{remote_file}' was not found on the FTP server '{ftp_server}'"
                raise Exception(msg)

            # Get the modification time of the remote file
            response = ftp.sendcmd("MDTM " + remote_file)
            remote_mtime = time.mktime(time.strptime(response[4:], "%Y%m%d%H%M%S"))

            # Get the modification time of the local file
            local_mtime = (
                os.path.getmtime(local_file) if os.path.exists(local_file) else 0
            )

            # Get the directory name from the file path
            dir_name = os.path.dirname(local_file)

            # Create the directory if it doesn't exist
            os.makedirs(dir_name, exist_ok=True)

            # Download the file if the remote file has been changed or if force_download is True
            if force_download or remote_mtime > local_mtime:
                with open(local_file, "wb") as local_file_r:
                    ftp.retrbinary("RETR " + remote_file, local_file_r.write)
                logging.warning(
                    f"File '{remote_file}' downloaded successfully to '{local_file}'"
                )
            else:
                logging.warning(
                    f"File '{remote_file}' has not been modified since last download"
                )
        return_files.append(local_file)
    except Exception as e:
        logging.error(e)

    return return_files

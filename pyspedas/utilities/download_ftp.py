from ftplib import FTP
import os


def download_ftp(
    ftp_server,
    ftp_path,
    filename,
    local_dir,
    username="anonymous",
    password="anonymous@",
):
    """
    Download a file from an FTP server.

    Parameters:
        ftp_server (str):
            FTP server address.
        ftp_path (str):
            Path on the FTP server where the file is located.
        filename (str):
            Name of the file to download.
        local_dir (str):
            Local directory to save the file.
        username (str):
            Username for the FTP server. Default is 'anonymous'.
        password (str):
            Password for the FTP server. Default is 'anonymous@'.

    Returns:
        list of str:
            List of files downloaded.
    """
    return_files = []
    with FTP(ftp_server) as ftp:
        ftp.login(user=username, passwd=password)
        ftp.cwd(ftp_path)  # Change to the directory containing the file

        local_filename = os.path.join(local_dir, filename)
        with open(local_filename, "wb") as local_file:
            ftp.retrbinary("RETR " + filename, local_file.write)

        print(f"File '{filename}' downloaded successfully to '{local_dir}'")
        return_files.append(local_filename)

    return return_files

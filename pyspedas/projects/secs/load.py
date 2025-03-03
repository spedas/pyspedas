import os
import zipfile
import logging
import shutil
import gzip
from pathlib import Path
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from .read_data_files import read_data_files

from .config import CONFIG


def load(
    trange=["2012-11-05/00:00:00", "2012-11-06/00:00:00"],
    resolution=10,
    dtype=None,
    no_download=False,
    downloadonly=False,
    out_type="np",
    save_pickle=False,
    spdf=False,
    force_download=False,
):
    """
    This function downloads and reads SECS/EICS data.

    It does not return tplot variables, but rather the data itself.
    Usually, this data is used by makeplots.py to create contour plots.

    Parameters
    ----------
    trange : list of str
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD', 'YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss', 'YYYY-MM-DD/hh:mm:ss'].
        Default: ["2012-11-05/00:00:00", "2012-11-06/00:00:00"]
    resolution : int, optional
        Time resolution of the data in seconds.
        Default: 10
    dtype : str, optional
        Data type; Valid options: 'EICS', 'SECS'.
        Default: None
    no_download : bool, optional
        Only load data from the local cache.
        Default: False
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load data from them.
        If True, the function returns a list of the downloaded files.
        Default: False
    out_type : str, optional
        The return type: 'np' for numpy array, 'df' for pandas dataframe, 'dc' for dictionary.
        Default: 'np'
    save_pickle : bool, optional
        Whether to save the output as a pickle file.
        Default: False
    spdf : bool, optional
        If True, download data from SPDF instead of UCLA.
        Default: False
    force_download : bool, optional
        If True, re-download the data files.
        Default: False

    Returns
    -------
    Varies (list of str, np.ndarray, pd.DataFrame, or dict)

        If downloadonly is True, the function returns a list of the downloaded files.
        Otherwise, it returns the data read from the files in the specified format.
        If out_type is 'np', the data is a numpy array.
        If out_type is 'df', the data is a pandas dataframe.
        If out_type is 'dc', the data is a dictionary.

    Examples
    --------
    >>> import pyspedas
    >>> secs_vars = pyspedas.projects.secs.data(dtype='EICS', trange=['2018-02-01', '2018-02-02'], downloadonly=True)
    >>> print(secs_vars)
    >>> ['/Users/user/data/secs/EICS/2018/02/EICS20180201.zip']
    """

    if dtype is None:
        logging.error("No data type provided.")
        return None
    else:
        dtype = dtype.upper()

    if trange is None or len(trange) != 2 or trange[1] < trange[0]:
        logging.error("Invalid time range provided.")
        return None

    if not downloadonly:
        if out_type is None:
            logging.error("No out_type provided.")
            return None
        else:
            out_type = out_type.lower()
        if out_type not in ["np", "df", "dc"]:
            logging.error("Invalid out_type provided.")
            return None

    if dtype == "EICS" or dtype == "SECS":

        pathformat_prefix = dtype + "/%Y/%m/"
        pathformat_zip = pathformat_prefix + dtype + "%Y%m%d.zip"
        pathformat_gz = pathformat_prefix + dtype + "%Y%m%d.zip.gz"  # only 2007!
        pathformat_unzipped = pathformat_prefix + "%d/" + dtype + "%Y%m%d_%H%M%S.dat"
        remote_path = CONFIG["remote_data_dir"]

    else:
        logging.error("Invalid data type provided:" + str(dtype))
        return None

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat_zip, trange=trange)
    remote_names_gz = dailynames(file_format=pathformat_gz, trange=trange)
    remote_names_gz = [s for s in remote_names_gz if s[-15:-11] == "2007"]

    out_files = []
    out_files_zip = []

    if spdf:
        # Download files from SPDF
        remote_path_spdf = CONFIG["remote_data_dir_spdf"]
        # Paths at SPDF do not include the month
        # zip files at UCLA are inside a directory /year/month/
        # but the same files at SPDF are inside a directory /year/
        pathformat_prefix_spdf = dtype + "/%Y/"
        pathformat_zip_spdf = pathformat_prefix_spdf + dtype + "%Y%m%d.zip"
        remote_names_spdf = dailynames(file_format=pathformat_zip_spdf, trange=trange)
        local_dir_spdf = CONFIG["local_data_dir"]

        files_zip_spdf = download(
            remote_file=remote_names_spdf,
            remote_path=remote_path_spdf,
            local_path=local_dir_spdf,
            no_download=no_download,
            force_download=force_download,
        )
        # At this point, the zip files are downloaded but in a different dir than UCLA files.
        # We need to move them to a directory containing the month
        files_zip = []
        for f in files_zip_spdf:
            if os.path.exists(f):
                stem = Path(f).stem
                if len(stem) >= 10:
                    # Stem is similar to 'SECS20120301' or 'EICS20120301'
                    month = stem[8:10]
                    path = str(Path(f).parent)
                    new_path = os.path.join(path, month)
                    new_filename = os.path.join(new_path, os.path.basename(f))
                    if os.path.exists(new_filename):
                        os.remove(new_filename)
                    else:
                        os.makedirs(new_path)
                    new_filename = shutil.copy(f, new_path)
                    files_zip.append(new_filename)

        # SPDF does not contain any .gz files
        files_gz = []
    else:
        # Download files from UCLA
        files_zip = download(
            remote_file=remote_names,
            remote_path=remote_path,
            local_path=CONFIG["local_data_dir"],
            no_download=no_download,
            force_download=force_download,
        )
        files_gz = download(
            remote_file=remote_names_gz,
            remote_path=remote_path,
            local_path=CONFIG["local_data_dir"],
            no_download=no_download,
            force_download=force_download,
        )

    files_zip = files_zip + files_gz

    if files_zip is not None:
        for rf_zip_zero in files_zip:
            if rf_zip_zero.endswith(".gz"):
                rf_zip = rf_zip_zero[0:-3]
                # unzip .gz file to .zip file
                with gzip.open(rf_zip_zero, "rb") as f_in:
                    with open(rf_zip, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
            elif rf_zip_zero.endswith(".zip"):
                rf_zip = rf_zip_zero
            else:
                rf_zip = rf_zip_zero
            out_files_zip.append(rf_zip)
            # print('Start for unzipping process ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            foldername_unzipped = rf_zip[0:-19] + rf_zip[-8:-6] + "/" + rf_zip[-6:-4]

            # print('foldername_unzipped-------: ', foldername_unzipped)
            ### add??????
            if not os.path.isdir(foldername_unzipped):
                logging.info("Start unzipping: " + rf_zip + "  ------")
                with zipfile.ZipFile(rf_zip, "r") as zip_ref:
                    zip_ref.extractall(rf_zip[0:-16])
                if not os.path.isdir(foldername_unzipped):
                    # for the case of unzipping directly without the %d folder made.
                    # make %d folder
                    os.makedirs(foldername_unzipped)
                    # move .dat files
                    sourcepath = rf_zip[0:-16]
                    sourcefiles = os.listdir(sourcepath)
                    destinationpath = foldername_unzipped
                    logging.info("start to move files: --------------")
                    for file in sourcefiles:
                        if rf_zip[-16:-4] in file and file.endswith(".dat"):
                            shutil.move(
                                os.path.join(sourcepath, file),
                                os.path.join(destinationpath, file),
                            )

            else:
                logging.info(
                    "Unzipped folder: "
                    + foldername_unzipped
                    + " existed, skip unzipping  ------"
                )

    if files_zip is not None:
        for file in files_zip:
            out_files.append(file)
    out_files = sorted(out_files)

    if out_files_zip is not None:
        out_files_zip = list(set(out_files_zip))
        out_files_zip = sorted(out_files_zip)

    if downloadonly:
        return out_files_zip  # out_files

    remote_names_unzipped = dailynames(
        file_format=pathformat_unzipped, trange=trange, res=resolution
    )
    """
    files_unzipped = download(remote_file=remote_names_unzipped, remote_path=CONFIG['remote_data_dir'],
                         local_path=CONFIG['local_data_dir'], no_download=True)
    """
    remote_names_unzipped_existed = [
        rnud
        for rnud in remote_names_unzipped
        for ofz in out_files_zip
        if ofz[-16:-4] in rnud
    ]
    remote_names_unzipped = remote_names_unzipped_existed
    out_files_unzipped = [
        os.path.join(CONFIG["local_data_dir"], rf_res)
        for rf_res in remote_names_unzipped
    ]
    out_files_unzipped = sorted(out_files_unzipped)

    if out_files_unzipped == []:
        data_vars = []
    else:
        data_vars = read_data_files(
            out_files=out_files_unzipped,
            dtype=dtype,
            out_type=out_type,
            save_pickle=save_pickle,
        )
        # print('data_vars: ', data_vars, np.shape(data_vars))

    return data_vars

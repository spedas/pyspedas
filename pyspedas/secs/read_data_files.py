import os
import numpy as np
from pytplot import time_double
import pandas as pd
import time
import logging
import pickle
import os


def read_data_files(out_files=None, dtype=None, out_type="np", save_pickle=False):
    """
    Read data on a daily basis with a 10-secs or other resolution.

    Parameters
    ----------
    out_files : list of str
        The list of the downloaded data file paths.
        This list can be obtained from the load() function, using downloadonly=True.
    dtype : str
        The data which will be read ('EICS' or 'SECS').
    out_type : str
        The return type: 'np' for numpy array, 'df' for pandas dataframe, 'dc' for dictionary.
        The default is 'np'.
    save_pickle : bool
        Whether to save the output as a pickle file.

    Returns
    -------
    Varies (np.ndarray, pd.DataFrame, or dict)

        The data read from the files in the specified format.
        If out_type is 'np', the data is a numpy array.
        If out_type is 'df', the data is a pandas dataframe.
        If out_type is 'dc', the data is a dictionary.
    """

    if out_files is None:
        logging.error("No data files provided.")
        return None

    dtype = dtype.upper()

    file_names_arr_Dir = out_files
    start_time = time.time()
    # Reading the data at each time stamp (per resolution secs) on one specific date.

    # input the data into one pd data frame. (four columns)
    if out_type == "df":
        if dtype == "EICS":
            colnames = ["latitude", "longitude", "Jx", "Jy"]
        if dtype == "SECS":
            colnames = ["latitude", "longitude", "J"]
        data_all = []
        for idx, file in enumerate(file_names_arr_Dir):
            df = pd.read_csv(file, header=None, sep=r"\s+", skiprows=0, names=colnames)
            df["datetime"] = file[-19:-4]
            data_all.append(df)
        output = pd.concat(data_all, axis=0, ignore_index=True)

    elif out_type == "np":
        latitude = []
        longitude = []
        date_time = []
        if dtype == "EICS":
            Jx = []
            Jy = []
            for file in file_names_arr_Dir:
                di = np.loadtxt(file)
                num_row = np.shape(di)[0]
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                Jx.extend(di[:, 2])
                Jy.extend(di[:, 3])
                date_time.extend(np.full(num_row, file[-19:-4]))
            num_row2 = len(latitude)
            data_all = np.array([latitude, longitude, Jx, Jy, date_time])
            data_all = data_all.reshape([5, num_row2])
            data_all = np.transpose(data_all)

        if dtype == "SECS":
            J = []
            for file in file_names_arr_Dir:
                di = np.loadtxt(file)
                num_row = np.shape(di)[0]
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                J.extend(di[:, 2])
                date_time.extend(np.full(num_row, file[-19:-4]))
            num_row2 = len(latitude)
            data_all = np.array([latitude, longitude, J, date_time])
            data_all = data_all.reshape([4, num_row2])
            data_all = np.transpose(data_all)

        output = data_all

    elif out_type == "dc":
        data_dict = {}
        Jx = []
        Jy = []
        J = []

        date_time = []
        flag = 0
        filename_day1 = file_names_arr_Dir[0]

        for idx, file in enumerate(
            file_names_arr_Dir
        ):  # per dat file with 1 min resolution.
            if not os.path.isfile(file):
                continue  # jump ouf of the current iteration, into the next iteration of the same loop.
            if os.stat(file).st_size == 0:  # check if the file is empty.
                continue

            di = np.loadtxt(file)
            if np.shape(di)[0] > 0 and flag == 0:
                num_row = np.shape(di)[0]  # np array
                latitude = di[:, 0]  # np array
                longitude = di[:, 1]  # np array
                flag = 1

            if dtype == "EICS":
                Jx.append(di[:, 2])  # list [np.arrays]
                Jy.append(di[:, 3])  # list [np.arrays]
            if dtype == "SECS":
                J.append(di[:, 2])  # list [np.arrays]
            date_time.append(file[-19:-4])  # list of str

        date_time = np.array(date_time)  # np array of str
        date_time = time_double(date_time)  # np array of float
        if dtype == "EICS":
            Jx = np.vstack(Jx)  # np array
            Jy = np.vstack(Jy)  # np array
            data_dict = {
                "time": date_time,
                "latitude": latitude,
                "longitude": longitude,
                "Jx": Jx,
                "Jy": Jy,
            }
        if dtype == "SECS":
            J = np.vstack(J)  # np array
            data_dict = {
                "time": date_time,
                "latitude": latitude,
                "longitude": longitude,
                "J": J,
            }
        output = data_dict

    else:
        logging.error("Invalid output type." + str(out_type))
        return None

    if save_pickle == True:
        if out_type == "dc":  # too large, not useful.
            with open("data_dc.pkl", "wb") as f:
                pickle.dump(output, f)

        # f.close()
    logging.info(
        "running time of output "
        + out_type
        + ": --- %s seconds ---" % (time.time() - start_time)
    )

    return output

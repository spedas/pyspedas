import os
import json
import logging
from pyspedas.tplot_tools import time_double, time_string
from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.projects.mms.mec_ascii.mms_get_local_ancillary_files import mms_get_local_ancillary_files
from pyspedas.projects.mms.mec_ascii.mms_load_qf_tplot import mms_load_qf_tplot

from pyspedas.utilities.download import download, is_fsspec_uri
import fsspec

def mms_get_tetrahedron_qf(trange=['2015-10-16', '2015-10-17'], no_download=False,
    suffix='', always_prompt=False):
    """
    Helper routine for loading tetrahedron QF data (ASCII files from the SDC); not meant to be called directly
    """

    local_data_dir = CONFIG['local_data_dir']
    download_only = CONFIG['download_only']

    start_time = time_double(trange[0])-60*60*24.
    end_time = time_double(trange[1])

    # check if end date is anything other than 00:00:00, if so
    # add a day to the end time to ensure that all data is downloaded
    if type(trange[1]) == str:
        endtime_day = time_double(time_string(time_double(trange[1]), fmt='%Y-%m-%d'))
    else:
        endtime_day = time_double(time_string(trange[1], fmt='%Y-%m-%d'))

    if end_time > endtime_day:
        add_day = 60*60*24.
    else:
        add_day = 0

    start_time_str = time_string(start_time, fmt='%Y-%m-%d')
    end_time_str = time_string(end_time+add_day, fmt='%Y-%m-%d')


    user = None
    if not no_download:
        sdc_session, user = mms_login_lasp(always_prompt=always_prompt)

    out_files = []

    sep = "/" if is_fsspec_uri(local_data_dir) else os.path.sep
    out_dir = sep.join([local_data_dir, 'ancillary', 'mms', 'tetrahedron_qf'])

    if CONFIG['no_download'] != True and no_download != True:
        dates_for_query = '&start_date='+start_time_str+'&end_date='+end_time_str

        if user is None:
            url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/file_info/ancillary?sc_id=mms&product=defq'+dates_for_query
        else:
            url = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/file_info/ancillary?sc_id=mms&product=defq'+dates_for_query

        response_text = download(
            remote_file=url,
            session=sdc_session,
            no_wildcards=True,
            return_text=True,
        )
        if response_text is None:
            return
        http_json = json.loads(response_text)

        files_in_interval = http_json['files']

        for file in files_in_interval:
            out_file = sep.join([out_dir, file['file_name']])

            if is_fsspec_uri(out_file):
                protocol, path = out_file.split("://")
                fs = fsspec.filesystem(protocol)

                exists = fs.exists(out_file)
            else:
                exists = os.path.exists(out_file)

            if exists:
                if is_fsspec_uri(out_file):
                    f_size = fs.size(out_file)
                else:
                    f_size = os.stat(out_file).st_size

                if str(f_size) == str(file['file_size']):
                    out_files.append(out_file)
                    continue

            if user is None:
                download_url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/download/ancillary?file=' + file['file_name']
            else:
                download_url = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/download/ancillary?file=' + file['file_name']

            logging.info('Downloading ' + file['file_name'] + ' to ' + out_dir)

            downloaded_files = download(
                remote_file=download_url,
                local_path=out_dir,
                local_file=file['file_name'],
                session=sdc_session,
                no_wildcards=True,
                force_download=True,
            )
            if downloaded_files:
                out_files.append(out_file)

    if not no_download:
        sdc_session.close()

    if download_only:
        return

    # if no files are found remotely, try locally
    if len(out_files) == 0:
        out_files = mms_get_local_ancillary_files(trange=[start_time_str, end_time_str])

    return mms_load_qf_tplot(sorted(out_files), suffix=suffix, trange=trange)

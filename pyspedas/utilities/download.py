import os
import warnings
import requests
import logging
import fnmatch
import datetime
import pkg_resources

from pathlib import Path
from shutil import copyfileobj, copy
from tempfile import NamedTemporaryFile
from html.parser import HTMLParser

# the following is used to parse the links from an HTML index file
class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = {k: v for (k, v) in attrs}
            if 'href' in attrs:
                link = attrs['href']
                # kludge to support http://rbspice?.ftecs.com/
                if '/' in link:
                    link = link.split('/')[-1]
                try:
                    self.links.append((link))
                except AttributeError:
                    self.links = [(link)]
    

def download_file(url=None, filename=None, headers={}, username=None, password=None, verify=False, session=None):
    """
    Download a file and return its local path; this function is primarily meant to be called by the download function below
    
    Parameters:
        url: str
            Remote URL to download

        filename: str
            Local file name

        headers: dict
            Dictionary containing the headers to be passed to the requests get call

        username: str
            user name to be used in HTTP authentication

        password: str
            password to be used in HTTP authentication

        verify: bool
            Flag indicating whether or not to verify the SSL/TLS certificate

        session: requests.Session object
            Requests session object that allows you to persist things like HTTP authentication through multiple calls

    Returns:
        String containing the local file name

    """

    if session is None:
        session = requests.Session()
    
    if username != None:
        session.auth = (username, password)

    # check if the file exists, and if so, set the last modification time in the header
    # this allows you to avoid re-downloading files that haven't changed
    if os.path.exists(filename):
        headers['If-Modified-Since'] = (datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))).strftime('%a, %d %b %Y %H:%M:%S GMT')

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ResourceWarning)
        fsrc = session.get(url, stream=True, verify=verify, headers=headers)


    # need to delete the If-Modified-Since header so it's not set in the dictionary in subsequent calls
    if headers.get('If-Modified-Since') != None:
        del headers['If-Modified-Since']

    # the file hasn't changed
    if fsrc.status_code == 304:
        logging.info('File is current: ' + filename)
        fsrc.close()
        return filename

    # file not found 
    if fsrc.status_code == 404:
        logging.error('Remote file not found: ' + url)
        fsrc.close()
        return None

    # authentication issues
    if fsrc.status_code == 401 or fsrc.status_code == 403:
        logging.error('Unauthorized: ' + url)
        fsrc.close()
        return None

    if fsrc.status_code == 200:
        logging.info('Downloading ' + url + ' to ' + filename)
    else:
        logging.error(fsrc.reason)
        fsrc.close()
        return None

    ftmp = NamedTemporaryFile(delete=False)

    with open(ftmp.name, 'wb') as f:
        copyfileobj(fsrc.raw, f)

    # make sure the directory exists
    if not os.path.exists(os.path.dirname(filename)) and os.path.dirname(filename) != '':
        os.makedirs(os.path.dirname(filename))

    # if the download was successful, copy to data directory
    copy(ftmp.name, filename)

    fsrc.close()
    ftmp.close()
    
    logging.info('Download complete: ' + filename)

    return filename

def download(remote_path='', remote_file='', local_path='', local_file='', headers={}, username=None, password=None, verify=True, session=None, no_download=False, last_version=False):
    """
    Download one or more remote files and return their local paths.

    Parameters:
        remote_path: str
            String consisting of a common URL base for all remote files

        remote_file: str or list of str
            String or string array of URLs to remote files

        local_path: str
            String consisting of a common local path for all local files

        local_file: str or list of str
            String or string array of local destination file names

        headers: dict
            Dictionary containing the headers to be passed to the requests get call

        username: str
            user name to be used in HTTP authentication

        password: str
            password to be used in HTTP authentication

        verify: bool
            Flag indicating whether or not to verify the SSL/TLS certificate

        session: requests.Session object
            Requests session object that allows you to persist things like HTTP authentication through multiple calls

        no_download: bool
            Flag to not download remote files

        last_version: bool
            Flag to only download the last in file in a lexically sorted 
            list when multiple matches are found using wildcards

    Returns:
        String list specifying the full local path to all requested files

    """
    local_file_in = local_file

    if isinstance(remote_path, list):
        logging.error('Remote path must be a string')
        return

    if isinstance(local_path, list):
        logging.error('Local path must be a string')
        return

    if local_path == '':
        local_path = str(Path('').resolve())

    if username is not None and password is None:
        logging.error('Username provided without password')
        return

    if session is None:
        session = requests.Session()

    if username is not None:
        session.auth = requests.auth.HTTPDigestAuth(username, password)

    if headers.get('User-Agent') is None:
        try:
            release_version = pkg_resources.get_distribution("pyspedas").version
        except pkg_resources.DistributionNotFound:
            release_version = 'bleeding edge'
        headers['User-Agent'] = 'pySPEDAS ' + release_version

    out = []
    index_table={}

    if not isinstance(remote_file, list):
        remote_file = [remote_file]

    urls = [remote_path+rfile for rfile in remote_file]

    for url in urls:
        resp_data = None
        url_file = url[url.rfind("/")+1:]
        url_base = url.replace(url_file, '')

        # automatically use remote_file locally if local_file is not specified
        if local_file_in == '':
            # if remote_file is the entire url then only use the filename
            if remote_path == '':
                local_file = url_file
            else:
                local_file = url.replace(remote_path, '')

                if local_file == '': # remote_path was the full file name
                    local_file = remote_path[remote_path.rfind("/")+1:]

        filename = os.path.join(local_path, local_file)

        short_path = local_file[:1+local_file.rfind("/")]

        if no_download is False:
            # expand the wildcards in the url
            if '?' in url or '*' in url and no_download is False:
                if index_table.get(url_base) != None:
                    links = index_table[url_base]
                else:
                    logging.info('Downloading remote index: ' + url_base)

                    # we'll need to parse the HTML index file for the file list
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=ResourceWarning)
                        html_index = session.get(url_base, verify=verify, headers=headers)

                    if html_index.status_code == 404:
                        logging.error('Remote index not found: ' + url_base)
                        continue

                    if html_index.status_code == 401 or html_index.status_code == 403:
                        logging.error('Unauthorized: ' + url_base)
                        continue

                    # grab the links
                    link_parser = LinkParser()
                    link_parser.feed(html_index.text)

                    try:
                        links = link_parser.links
                        index_table[url_base] = links
                    except AttributeError:
                        links = []

                # find the file names that match our string
                # note: fnmatch.filter accepts ? (single character) and * (multiple characters)
                new_links = fnmatch.filter(links, url_file)

                if last_version and len(new_links) > 1:
                    new_links = sorted(new_links)
                    new_links = [new_links[-1]]

                if '?' in remote_path or '*' in remote_path:
                    # the user specified a wild card in the remote_path
                    remote_path = url_base

                # download the files
                for new_link in new_links:
                    resp_data = download(remote_path=remote_path, remote_file=short_path+new_link, local_path=local_path, username=username, password=password, verify=verify, headers=headers, session=session)
                    if resp_data is not None:
                        for file in resp_data:
                            out.append(file)
                session.close()
                continue

            resp_data = download_file(url=url, filename=filename, username=username, password=password, verify=verify, headers=headers, session=session)
        
        if resp_data is not None:
            if not isinstance(resp_data, list):
                resp_data = [resp_data]
            for file in resp_data:
                out.append(file)
        else:
            # download wasn't successful, search for local files
            logging.info('Searching for local files...')
                
            if local_path == '':
                local_path_to_search = str(Path('.').resolve())
            else:
                local_path_to_search = local_path

            for dirpath, dirnames, filenames in os.walk(local_path_to_search):
                matching_files = fnmatch.filter(filenames, local_file[local_file.rfind("/")+1:])
                for file in matching_files:
                    out.append(os.path.join(dirpath, file))

            out = sorted(out)

            if last_version:
                if len(out) > 1:
                    out = [out[-1]]

    session.close()
    return out
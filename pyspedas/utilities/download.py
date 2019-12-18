import os
import warnings
import requests
import logging
import fnmatch
import datetime

from shutil import copyfileobj, copy
from tempfile import NamedTemporaryFile
from html.parser import HTMLParser

# the following is used to parse the links from an HTML index file
class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = {k: v for (k, v) in attrs}
            if 'href' in attrs:
                try:
                    self.links.append((attrs['href']))
                except AttributeError:
                    self.links = [(attrs['href'])]
    

def download_file(url=None, filename=None):
    '''
        
    '''
    headers = {}

    # check if the file exists, and if so, set the last modification time in the header
    # this allows you to avoid re-downloading files that haven't changed
    if os.path.exists(filename):
        headers = {'If-Modified-Since': (datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))).strftime('%a, %d %b %Y %H:%M:%S GMT')}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ResourceWarning)
        fsrc = requests.get(url, stream=True, verify=True, headers=headers)
    
    # the file hasn't changed
    if fsrc.status_code == 304:
        logging.info('File is current: ' + filename)
        return filename

    # file not found 
    if fsrc.status_code == 404:
        logging.error('Remote file not found: ' + url)
        return None

    # authentication issues
    if fsrc.status_code == 401 or fsrc.status_code == 403:
        logging.error('Unauthorized: ' + url)
        return None

    if fsrc.status_code == 200:
        logging.info('Downloading ' + url + ' to ' + filename)

    ftmp = NamedTemporaryFile(delete=False)

    with open(ftmp.name, 'wb') as f:
        copyfileobj(fsrc.raw, f)

    # make sure the directory exists
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    # if the download was successful, copy to data directory
    copy(ftmp.name, filename)

    fsrc.close()
    ftmp.close()

    return filename

def download(remote_path='', remote_file='', local_path='', local_file=''):

    out = []
    if not isinstance(remote_file, list):
        remote_file = [remote_file]

    urls = [remote_path+rfile for rfile in remote_file]

    for url in urls:
        url_file = url[url.rfind("/")+1:]
        url_base = url.replace(url_file, '')

        # automatically use remote_file locally if local_file is not specified
        if local_file == '':
            # if remote_file is the entire url then only use the filename
            if remote_path == '':
                local_file = url_file
            else:
                local_file = url.replace(remote_path, '')

        filename = os.path.join(local_path, local_file)

        short_path = local_file[:1+local_file.rfind("/")]

        # expand the wildcards in the url
        if '?' in url or '*' in url:
            # we'll need to parse the HTML index file for the file list
            html_index = requests.get(url_base)

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
            except AttributeError:
                links = []

            # find the file names that match our string
            # note: fnmatch.filter accepts ? (single character) and * (multiple characters)
            new_links = fnmatch.filter(links, url_file)

            # download the files
            for new_link in new_links:
                resp_data = download(remote_path=remote_path, remote_file=short_path+new_link, local_path=local_path)
                if resp_data is not None:
                    for file in resp_data:
                        out.append(file)
            return out

        resp_data = download_file(url=url, filename=filename)
        if resp_data is not None:
            if not isinstance(resp_data, list):
                resp_data = [resp_data]
            for file in resp_data:
                out.append(file)
    return out
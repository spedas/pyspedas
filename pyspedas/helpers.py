# -*- coding: utf-8 -*-
"""
File:
    helpers.py

Description:
    Helper functions for pyspedas.
"""

import urllib
import os
import socket
import warnings


def download_files(url, locafile):
    """Get a file from internet and save it localy."""

    warnings.simplefilter("ignore", ResourceWarning)

    exists = False
    httpreq = None
    err = None
    ver = -1

    exists, err, ver, newurl = find_latest_url_version(url)
    if not exists:
        return exists, err, locafile

    url = newurl
    if ver != -1:
        locafile = locafile.replace('?', str(ver))

    # Create local directory if it does not exist
    dirPath = os.path.dirname(locafile)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    # Download file
    try:
        if not os.path.exists(locafile):
            httpreq = urllib.request.urlretrieve(url, locafile)
    except urllib.request.URLError as e:
        httpreq = None
        err = e
    except socket.error:
        pass

    if httpreq is not None:
        exists = True

    return exists, err, locafile


def url_exists(url):
    """Returns True if url exists, otherwise False"""

    ans = False
    try:
        hreq = urllib.request.urlopen(url)
        ans = True
        err = ''
        hreq.close()
    except urllib.request.URLError as e:
        ans = False
        err = e

    return ans, err


def find_latest_url_version(url):
    """Returns if a file exists and the latest version.
    Assumes max version = v04, should be changed if there are higher versions
    """

    exists = False
    err = ''
    ver = -1
    newurl = url
    if '?' in url:
        for ver in range(4, -1, -1):
            newurl = url.replace('?', str(ver))
            exists, err = url_exists(newurl)
            # print(exists, err, ver, newurl)
            if exists:
                break
    else:
        ver = -1
        newurl = url
        exists, err = url_exists(newurl)
        return exists, err, ver, newurl

    return exists, err, ver, newurl

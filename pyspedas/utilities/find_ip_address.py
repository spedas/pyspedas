import urllib

def find_ip_address():
    """ Uses api.ipify.org to get the public IP address, useful for troubleshooting data access issues in test suites"""
    url='http://api.ipify.org'
    page=urllib.request.urlopen(url)
    address=page.read().decode('utf-8')
    return address
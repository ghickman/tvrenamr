from hashlib import md5
from re import compile
from os.path import dirname, join
from urllib2 import Request, urlopen

from minimock import mock, restore

def invalid_xml(url, data=None, timeout=30):
    """Mock urllib2.urlopen and return a local file handle to invalid.xml"""
    return open(join(dirname(__file__), 'mocked_xml', 'invalid.xml'), 'r')

def mocked_xml(url, data=None, timeout=30):
    """Mock urllib2.urlopen and return """
    def return_file(lib, file_type):
        files = {'episode': '108', 'series': 'chuck'}
        mocked_xml = join(dirname(__file__), 'mocked_xml', lib, files[file_type] + '.xml')
        return open(mocked_xml, 'r')

    # workout the library we're working with
    m = compile('http:\/\/(www\.)?([\w]+)\.com').match(url)
    lib = m.group(2)
    if lib == 'thetvdb':
        if str.find(url, 'GetSeries') > 0:
            return return_file(lib, 'series')

        if str.find(url, 'en.xml') > 0:
            return_file(lib, 'episode')

    if lib == 'tvrage':
        return open(join(dirname(__file__), 'invalid.xml'), 'r')

def urlopen_stub(url, data=None, timeout=30):
    """
    Mock urllib2.urlopen and return a local file handle or create file if
    not existent and then return it.
    """

    if isinstance(url, Request):
        key = md5(url.get_full_url()).hexdigest()
    else:
        key = md5(url).hexdigest()
    data_file = join(dirname(__file__), 'cache', '%s.xml' % key)
    try:
        f = open(data_file, 'r')
    except IOError:
        restore() # restore normal function
        data = urlopen(url, data).read()
        mock('urlopen', returns_func=urlopen_stub, tracker=None) # re-mock it.
        with open(data_file, 'w') as f:
            f.write(data)
        f = open(data_file, 'r')
    return f

mock('urlopen', returns_func=urlopen_stub, tracker=None)


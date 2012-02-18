from hashlib import md5
from re import compile
from os.path import dirname, join

from minimock import mock, restore
import requests


class MockFile(file):
    status_code = 0

    @property
    def content(self):
        return self.read()


def invalid_xml(url, **kwargs):
    """Mock requests' get() and return a local file handle to invalid.xml"""
    bad_xml = join(dirname(__file__), 'mocked_xml', 'invalid.xml')
    with open(bad_xml, 'r') as f:
        return f


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


def mock_get(url, **kwargs):
    """
    Mock requets.get and return a local file handle or create file if
    not existent and then return it.
    """

    key = md5(url).hexdigest()
    file_path = join(dirname(__file__), 'cache', '{0}.xml'.format(key))
    try:
        f = MockFile(file_path, 'r')
    except IOError:
        restore() # restore normal function
        tmp = MockFile(file_path, 'w')
        tmp.write(requests.get(url).content)
        tmp.close()
        mock('requests.get', returns_func=mock_get, tracker=None) # re-mock it.
        f = MockFile(file_path, 'r')

    f.status_code = requests.codes.ok
    if len(f.content) < 1:
        f.status_code = requests.codes.not_found
    return f


mock('requests.get', returns_func=mock_get, tracker=None)


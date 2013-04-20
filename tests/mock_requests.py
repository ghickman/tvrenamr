import hashlib
import os

from minimock import mock, restore
import requests


test_dir = os.path.abspath(os.path.dirname(__file__))


def cache_folder_check(func):
    cache = os.path.join(test_dir, 'cache')
    if not os.path.exists(cache):
        os.mkdir(cache)
    return func


class MockFile(file):
    content = None
    ok = True
    status_code = 0

    def populate_content(self):
        self.content = self.read()


def bad_response(url, **kwargs):
    class Response(object):
        ok = False
    return Response()


@cache_folder_check
def invalid_xml(url, **kwargs):
    """Mock requests' get() and return a local file handle to invalid.xml"""
    bad_xml = os.path.join(test_dir, 'mocked_xml', 'invalid.xml')
    f = MockFile(bad_xml, 'r')
    f.status_code = requests.codes.ok
    f.populate_content()
    return f


@cache_folder_check
def initially_bad_xml(url, **kwargs):
    """
    Mock requests.get and return invalid xml from thetvdb to simulate one library
    falling over.
    """
    def get_file(filename):
        path = os.path.join(test_dir, 'mocked_xml', '{0}.xml'.format(filename))
        f = MockFile(path, 'r')
        f.status_code = requests.codes.ok
        f.populate_content()
        return f

    if 'thetvdb' in url:
        return get_file('invalid')

    if 'tvrage' in url:
        if 'search' in url:
            return get_file('show_id')
        return get_file('episode')


@cache_folder_check
def mock_get(url, **kwargs):
    """
    Mock requets.get and return a local file handle or create file if
    not existent and then return it.
    """
    key = hashlib.md5(url).hexdigest()
    file_path = os.path.join(test_dir, 'cache', '{0}.xml'.format(key))
    try:
        f = MockFile(file_path, 'r')
    except IOError:
        restore() # restore normal function
        tmp = MockFile(file_path, 'w')
        tmp.write(requests.get(url).content)
        tmp.close()
        mock('requests.get', returns_func=mock_get, tracker=None) # re-mock it.
        f = MockFile(file_path, 'r')

    f.populate_content()
    f.status_code = requests.codes.ok
    if not f.content:
        f.status_code = requests.codes.not_found
    return f


mock('requests.get', returns_func=mock_get, tracker=None)

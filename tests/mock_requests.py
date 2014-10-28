import hashlib
import os

from minimock import mock, restore

from tvrenamr.vendor import requests


test_dir = os.path.abspath(os.path.dirname(__file__))


def cache_folder_check(func):
    cache = os.path.join(test_dir, 'cache')
    if not os.path.exists(cache):
        os.mkdir(cache)
    return func


class MockResponse(requests.models.Response):
    def __init__(self, path, *args, **kwargs):
        super(MockResponse, self).__init__(*args, **kwargs)
        with open(path, 'r') as f:
            tmp = f.read()
            try:
                self._content = tmp.encode('utf-8')
            except UnicodeDecodeError:
                self._content = tmp  # python 2

        self.status_code = 200
        self.encoding = 'utf-8'


def bad_response(url, **kwargs):
    class Response(object):
        ok = False
    return Response()


@cache_folder_check
def invalid_xml(url, **kwargs):
    """Mock requests' get() and return a local file handle to invalid.xml"""
    bad_xml = os.path.join(test_dir, 'mocked_xml', 'invalid.xml')
    return MockResponse(bad_xml)


@cache_folder_check
def mock_get(url, **kwargs):
    """
    Mock requests.get with the contents of a local file. If the file doesn't
    exist, make the request and save to the file.
    """
    key = hashlib.md5(url.encode('utf-8')).hexdigest()
    file_path = os.path.join(test_dir, 'cache', '{0}.xml'.format(key))
    try:
        return MockResponse(file_path)
    except IOError:
        restore()  # restore normal function
        r = requests.get(url)
        with open(file_path, 'w') as tmp:
            try:
                tmp.write(r.text)
            except UnicodeEncodeError:
                tmp.write(r.content)  # python 2
        mock('requests.get', returns_func=mock_get, tracker=None)  # re-mock it.
        return MockResponse(file_path)


mock('requests.get', returns_func=mock_get, tracker=None)

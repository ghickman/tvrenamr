import hashlib
import os

import requests
from minimock import mock, restore

from .utils import build_path, join_path


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


def mock_get(url, **kwargs):
    """
    Mock requests.get with the contents of a local file. If the file doesn't
    exist, make the request and save to the file.
    """
    cache_dir = build_path(join_path('cache'))
    key = hashlib.md5(url.encode('utf-8')).hexdigest()
    file_path = os.path.join(cache_dir, '{}.xml'.format(key))
    try:
        return MockResponse(file_path)
    except IOError:
        restore()  # restore normal function
        r = requests.get(url)
        if not r.ok:
            mock('requests.get', returns_func=mock_get, tracker=None)  # re-mock it.
            return r
        with open(file_path, 'w') as tmp:
            try:
                tmp.write(r.text)
            except UnicodeEncodeError:
                tmp.write(r.content)  # python 2
        mock('requests.get', returns_func=mock_get, tracker=None)  # re-mock it.
        return MockResponse(file_path)


mock('requests.get', returns_func=mock_get, tracker=None)

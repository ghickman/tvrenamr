import os
import urllib2, urlparse
from hashlib import md5
from minimock import mock, Mock, restore

def urlopen_stub(url, data=None):
    """Mock urllib2.urlopen and return a local file handle or create file if not existent and then return it."""

    if isinstance(url, urllib2.Request):
        key = md5(url.get_full_url()).hexdigest()
    else:
        key = md5(url).hexdigest()
    data_file = os.path.join(os.path.dirname(__file__), 'data', "%s.xml" % key)
    try:
        f = open(data_file)
    except IOError:
        restore()
        data = urllib2.urlopen(url, data).read()
        # re-mock it.
        mock('urllib2.urlopen', returns_func=urlopen_stub, tracker=None)
        f = open(data_file, "w").write(data)
        f = open(data_file, "r")
    return f

mock('urllib2.urlopen', returns_func=urlopen_stub, tracker=None)
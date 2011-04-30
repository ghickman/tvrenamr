from hashlib import md5
from os.path import dirname, join
from urllib2 import Request, urlopen

from minimock import mock, restore

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
        f = open(data_file)
    except IOError:
        restore() # restore normal function
        data = urlopen(url, data).read()
        mock('urlopen', returns_func=urlopen_stub, tracker=None) # re-mock it.
        with open(data_file, 'w') as f:
            f.write(data)
        f = open(data_file, 'r')
    return f

mock('urlopen', returns_func=urlopen_stub, tracker=None)


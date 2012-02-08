from os import makedirs
from os.path import abspath, dirname, exists, join
from shutil import copytree, rmtree

from tvrenamr.config import Config
from tvrenamr.main import TvRenamr
from tvrenamr.tests import urlopenmock


class BaseTest(object):
    files = 'tests/files'
    working = 'tests/data/working'

    def __init__(self):
        self.path = abspath(dirname(__file__))

    def setup(self):
        if not exists(self.files):
            makedirs(self.files)
        with open(join(self.path, 'file_list'), 'r') as f:
            for fn in f.readlines():
                with open(abspath(join(self.files, fn.strip())), 'w') as f:
                    f.write('')
        self.config = Config(join(self.path, 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(self.files, self.working)

    def teardown(self):
        rmtree(self.working)


from os import makedirs
from os.path import abspath, dirname, exists, join
from shutil import rmtree

from tvrenamr.config import Config
from tvrenamr.main import TvRenamr
from tvrenamr.tests import urlopenmock


class BaseTest(object):
    files = 'tests/files'

    def setup(self):
        # if `file` isn't there, make it
        if not exists(self.files):
            makedirs(self.files)

        # absolute path to the file is pretty useful
        self.path = abspath(dirname(__file__))

        # build the file list
        with open(join(self.path, 'file_list'), 'r') as f:
            for fn in f.readlines():
                with open(abspath(join(self.files, fn.strip())), 'w') as f:
                    f.write('')

        # instantiate tvr
        self.config = Config(join(self.path, 'config.yml'))
        self.tv = TvRenamr(self.files, self.config)

    def teardown(self):
        rmtree(self.files)


from os import mkdir
from os.path import abspath, dirname, exists, join
from shutil import rmtree

from tvrenamr.config import Config
from tvrenamr.main import TvRenamr

import mock_requests
# make pyflakes STFU
assert mock_requests


class BaseTest(object):
    def setup(self):
        # absolute path to the file is pretty useful
        self.path = abspath(dirname(__file__))

        def join_path(path):
            return join(self.path, path)

        self.files = join_path('files')
        self.organised = join_path('organised')
        self.renamed = join_path('renamed')

        # if `file` isn't there, make it
        if not exists(self.files):
            mkdir(self.files)

        # build the file list
        with open(join(self.path, 'file_list'), 'r') as f:
            for fn in f.readlines():
                with open(abspath(join(self.files, fn.strip())), 'w') as f:
                    f.write('')

        # instantiate tvr
        self.config = Config(join(self.path, 'config.yml'))
        self.config.defaults['renamed'] = self.files
        self.tv = TvRenamr(self.files, self.config)

    def teardown(self):
        rmtree(self.files)


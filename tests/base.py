import logging
import os
import shutil

from tvrenamr.config import Config
from tvrenamr.main import File, TvRenamr

from . import mock_requests
# make pyflakes STFU
assert mock_requests


logging.disable(logging.CRITICAL)


class BaseTest(object):
    def setup(self):
        # absolute path to the file is pretty useful
        self.path = os.path.abspath(os.path.dirname(__file__))

        def join_path(path):
            return os.path.join(self.path, path)

        self.files = join_path('files')
        self.organised = join_path('organised')
        self.renamed = join_path('renamed')

        # if `file` isn't there, make it
        if not os.path.exists(self.files):
            os.mkdir(self.files)

        # build the file list
        with open(os.path.join(self.path, 'file_list'), 'r') as f:
            for fn in f.readlines():
                path = os.path.abspath(os.path.join(self.files, fn.strip()))
                with open(path, 'w') as f:
                    f.write('')

        # instantiate tvr
        self.config = Config(os.path.join(self.path, 'config.yml'))
        self.config.defaults['renamed'] = self.files
        self.tv = TvRenamr(self.files, self.config)

        self._file = File('The Big Bang Theory', '3', ['01'], 'mp4')
        self._file.episodes[0].title = 'The Electric Can Opener Fluctuation'

    def teardown(self):
        shutil.rmtree(self.files)

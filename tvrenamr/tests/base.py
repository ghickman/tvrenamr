from os.path import dirname, join
from shutil import copytree, rmtree

from tvrenamr.config import Config
from tvrenamr.main import TvRenamr
from tvrenamr.tests import urlopenmock


class BaseTest(object):
    files = 'tests/files'
    working = 'tests/data/working'

    def setUp(self):
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(self.files, self.working)

    def tearDown(self):
        rmtree(self.working)


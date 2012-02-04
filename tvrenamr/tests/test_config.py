from os.path import dirname, join
from shutil import copytree, rmtree

from nose.tools import assert_equal, assert_true

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.main import TvRenamr
import urlopenmock

class TestConfig(object):
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(files, self.working)

    def tearDown(self):
        rmtree(self.working)

        # def test passing in a
        # test passing in a show not in the config
        # test passing in a show in the config but with no x option
        # test passing in a show in the config with x option

    def test_defaults_are_used(self):
        # format: '%n - %s%e - %t%x'
        # library: thetvdb
        # organise: yes
        # renamed: tests/data/working
        # the: true
        pass

    def test_show_options_are_used(self):
        # format: '%n - %s%e - %t%x'
        # library: thetvdb
        # organise: yes
        # renamed: tests/data/working
        # the: true
        # canonical
        # output
        pass

    def test_falling_back_on_default_options_when_not_present_in_show(self):
        # format: '%n - %s%e - %t%x'
        # library: thetvdb
        # organise: yes
        # renamed: tests/data/working
        # the: true
        pass

    def test_getting_canonical_returns_shows_canonical_name_or_given_name_if_not_specified(self):
        # get_canonical(csi)
        # get_canonical(chuck)
        pass


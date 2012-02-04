from os.path import dirname, join
from shutil import copytree, rmtree

from mock import patch
from nose.tools import assert_raises

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.main import TvRenamr
import urlopenmock


class TestLibrariesFallback(object):
    invalid_xml_file = join(dirname(__file__), 'mocked_xml', 'invalid.xml')
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(files, self.working)

    def tearDown(self):
        rmtree(self.working)

    @patch('urllib2.urlopen', new=urlopenmock.invalid_xml)
    def test_rename_with_all_libraries_returning_invalid_xml(self):
        episode = Episode(self.tv.extract_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi'))
        assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name, episode)


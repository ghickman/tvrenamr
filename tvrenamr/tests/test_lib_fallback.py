from os.path import dirname, join

from mock import patch
from nose.tools import assert_raises

from tvrenamr.episode import Episode
from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.tests.base import BaseTest
import urlopenmock


class TestLibrariesFallback(BaseTest):
    invalid_xml_file = join(dirname(__file__), 'mocked_xml', 'invalid.xml')

    @patch('urllib2.urlopen', new=urlopenmock.invalid_xml)
    def test_rename_with_all_libraries_returning_invalid_xml(self):
        episode = Episode(self.tv.extract_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi'))
        assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name, episode)


from os.path import dirname, join

from mock import patch
from nose.tools import assert_raises
import requests
# make pyflakes STFU
assert requests

from tvrenamr.episode import Episode
from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.tests.base import BaseTest
from tvrenamr.tests.mock_requests import invalid_xml


class TestLibrariesFallback(BaseTest):
    invalid_xml_file = join(dirname(__file__), 'mocked_xml', 'invalid.xml')

    @patch('requests.get', new=invalid_xml)
    def test_rename_with_all_libraries_returning_invalid_xml(self):
        episode = Episode(self.tv.extract_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi'))
        assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name, episode)


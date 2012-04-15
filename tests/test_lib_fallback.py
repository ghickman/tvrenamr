from os.path import dirname, exists, join

from mock import patch
from nose.tools import assert_true, assert_raises
import requests
# make pyflakes STFU
assert requests
from tvrenamr.episode import Episode
from tvrenamr.errors import NoMoreLibrariesException

from .base import BaseTest
from .mock_requests import initially_bad_xml, invalid_xml


class TestLibrariesFallback(BaseTest):
    invalid_xml_file = join(dirname(__file__), 'mocked_xml', 'invalid.xml')

    @patch('requests.get', new=invalid_xml)
    def test_rename_with_all_libraries_returning_invalid_xml(self):
        episode = Episode(self.tv.extract_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi'))
        assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name, episode)

    @patch('requests.get', new=initially_bad_xml)
    def test_rename_with_tvdb_falling_over(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        final_fn = 'Chuck - 108 - Chuck Versus the Truth.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(exists(join(self.files, final_fn)))


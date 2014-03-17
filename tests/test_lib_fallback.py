from mock import patch
from pytest import raises

from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.main import Episode

from .base import BaseTest
from .mock_requests import initially_bad_xml, invalid_xml


class TestLibrariesFallback(BaseTest):
    @patch('tvrenamr.libraries.requests.get', new=invalid_xml)
    def test_rename_with_all_libraries_returning_invalid_xml(self):
        with raises(NoMoreLibrariesException):
            self.tv.retrieve_episode_title(self._file.episodes[0])

    @patch('tvrenamr.libraries.requests.get', new=initially_bad_xml)
    def test_rename_with_tvdb_falling_over(self):
        episode = Episode(self._file, '8')
        title = self.tv.retrieve_episode_title(episode)
        assert title == 'The Adhesive Duck Deficiency'

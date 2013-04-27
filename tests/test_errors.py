from os.path import join

from mock import patch
from nose.tools import assert_raises
from tvrenamr.episode import Episode
from tvrenamr.errors import (EpisodeAlreadyExistsInDirectoryException,
                             NoMoreLibrariesException,
                             IncorrectCustomRegularExpressionSyntaxException,
                             UnexpectedFormatException)

from .base import BaseTest
from .mock_requests import bad_response


class TestExceptionsAreRaised(BaseTest):
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_details_from_file, 'chuck.avi')

    @patch('requests.get', new=bad_response)
    def test_nonexistant_episode_doesnt_work_on_any_library(self):
        episode = Episode(**self.tv.extract_details_from_file('chuck.s99e05.avi'))
        assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name, episode)

    def test_episode_already_exists_raise_exception(self):
        fn = 'chuck.s02e05.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        path = self.tv.build_path(episode, organise=False)
        with open(join(self.files, 'Chuck - 205 - Chuck Versus Tom Sawyer.avi'), 'w'):
            assert_raises(EpisodeAlreadyExistsInDirectoryException, self.tv.rename, fn, path)

    def test_custom_syntax_snippets_missing_raises_exception(self):
        assert_raises(IncorrectCustomRegularExpressionSyntaxException,
                      self.tv.extract_details_from_file, 'chuck.s02e05.avi', '.')

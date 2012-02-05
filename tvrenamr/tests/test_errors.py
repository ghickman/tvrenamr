from os.path import dirname, join
from shutil import copytree, rmtree

from nose.tools import assert_raises

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.errors import (EpisodeAlreadyExistsInDirectoryException,
                             NoMoreLibrariesException,
                             IncorrectCustomRegularExpressionSyntaxException,
                             UnexpectedFormatException)
from tvrenamr.main import TvRenamr
import urlopenmock


class TestExceptionsAreRaised(object):
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(files, self.working)

    def tearDown(self):
        rmtree(self.working)

    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_details_from_file, 'chuck.avi')

    def test_nonexistant_episode_doesnt_work_on_any_library(self):
        episode = Episode(self.tv.extract_details_from_file('chuck.s99e05.avi'))
        assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name, episode)

    def test_episode_already_exists_raise_exception(self):
        with open(join(self.working, 'Chuck - 205 - Chuck Versus Tom Sawyer.avi'), 'w'):
            pass
        fn = 'chuck.s02e05.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        path = self.tv.build_path(episode, organise=False)
        assert_raises(EpisodeAlreadyExistsInDirectoryException, self.tv.rename, fn, path)

    def test_custom_syntax_snippets_missing_raises_exception(self):
        assert_raises(IncorrectCustomRegularExpressionSyntaxException,
                      self.tv.extract_details_from_file, 'chuck.s02e05.avi', '.')


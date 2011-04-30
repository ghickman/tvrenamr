from os.path import dirname, join
from shutil import copytree, rmtree

from nose.tools import assert_raises

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.errors import EpisodeAlreadyExistsInDirectoryException, EpisodeNotFoundException, \
        IncorrectCustomRegularExpressionSyntaxException, UnexpectedFormatException
from tvrenamr.main import TvRenamr
import urlopenmock

class TestExceptionsAreRaised(object):
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/data/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(files, self.working)

    def tearDown(self):
        rmtree(self.working)

    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_details_from_file, 'chuck.avi')

    def test_episode_not_found_exception_should_be_raised_when_episode_not_found(self):
        episode = Episode()
        episode.show, episode.season, episode.episode, episode.extension = self.tv.extract_details_from_file('chuck.s99e05.avi')
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, episode)

    def test_episode_already_exists_in_folder_exception_is_raised_when_new_file_name_already_exists_in_folder(self):
        fn = 'chuck.s02e05.avi'
        episode = Episode()
        episode.show, episode.season, episode.episode, episode.extension = self.tv.extract_details_from_file(fn)
        episode.title = self.tv.retrieve_episode_name(episode)
        path = self.tv.build_path(episode, organise=False)
        assert_raises(EpisodeAlreadyExistsInDirectoryException, self.tv.rename, fn, path)

    def test_incorrect_custom_regular_expression_syntax_exception_is_raised_when_any_of_the_custom_regular_expression_string_is_missing_the_defined_three_syntax_snippets(self):
        fn = 'chuck.s02e05.avi'
        assert_raises(IncorrectCustomRegularExpressionSyntaxException, self.tv.extract_details_from_file, fn, '.')


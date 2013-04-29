from os.path import isfile, join

from nose.tools import assert_equal, assert_true
from tvrenamr.episode import Episode
from tvrenamr.main import TvRenamr

from .base import BaseTest


class TestMain(BaseTest):
    def test_instantiate_core(self):
        assert_true(isinstance(TvRenamr('/', self.config), TvRenamr))

    def test_passing_in_a_show_name_renames_a_file_using_that_name(self):
        fn = 'doctor.who.s5e10.blah.HDTV.XViD.avi'
        final_fn = 'Doctor Who (2005) - 510 - Vincent and the Doctor.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.show_name = 'Doctor Who (2005)'
        episode.title = self.tv.retrieve_episode_name(episode)
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.files, final_fn)))

    def test_passing_in_a_season_number_to_retrieve_episode_name_returns_the_correct_episode_name_from_that_season(self):
        episode = Episode(**self.tv.extract_details_from_file('chuck.s1e08.avi'))
        episode.season = 2
        assert_equal(self.tv.retrieve_episode_name(episode), 'Chuck Versus the Gravitron')

    def test_passing_in_a_season_number_renames_a_file_using_that_season_number(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.season = 2
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.files, 'Chuck - 208 - Chuck Versus the Gravitron.avi')))

    def test_passing_in_an_episode_number_returns_the_correct_episode_title(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.episode = '9'
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.files, 'Chuck - 109 - Chuck Versus the Imported Hard Salami.avi')))

    def test_passing_in_an_episode_number_renames_a_file_using_that_episode_number(self):
        episode = Episode(**self.tv.extract_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi'))
        episode.episode = 9
        assert_equal(self.tv.retrieve_episode_name(episode), 'Chuck Versus the Imported Hard Salami')

    def test_setting_the_position_of_a_shows_leading_the_to_the_end_of_the_file_name(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name, the=True)
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.files, 'Big Bang Theory, The - 301 - The Electric Can Opener Fluctuation.avi')))

    def test_setting_an_episodes_format_as_name_season_episode_title(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        assert_equal(self.tv.build_path(
            episode, rename_dir=self.files, organise=False, output_format='%n - %s%e - %t%x'),
            join(self.files, 'Chuck - 108 - Chuck Versus the Truth.avi'))

    def test_setting_an_episodes_format_as_season_episode_title_name(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        assert_equal(self.tv.build_path(
            episode, rename_dir=self.files, organise=False, output_format='%s - %e - %t - %n%x'),
            join(self.files, '1 - 08 - Chuck Versus the Truth - Chuck.avi'))

    def test_setting_an_episodes_format_as_title_episode_season_name(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        assert_equal(self.tv.build_path(
            episode, rename_dir=self.files, organise=False, output_format='%t - %e - %s - %n%x'),
            join(self.files, 'Chuck Versus the Truth - 08 - 1 - Chuck.avi'))

    def test_extracting_season_from_file_format_s0e00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.s2e06.avi')['season'], '2')

    def test_extracting_season_from_file_format_s00e00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.s20e05.avi')['season'], '20')

    def test_extracting_episode_from_file_format_s0e00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.s2e05.avi')['episode'], '05')

    def test_extracting_episode_from_file_format_s00e00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.s20e05.avi')['episode'], '05')

    def test_extracting_season_from_file_format_0x00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.2x05.avi')['season'], '2')

    def test_extracting_season_from_file_format_00x00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.20x05.avi')['season'], '20')

    def test_extracting_episode_from_file_format_0x00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.2x05.avi')['episode'], '05')

    def test_extracting_episode_from_file_format_00x00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.20x05.avi')['episode'], '05')

    def test_extracting_season_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.205.avi')['season'], '2')

    def test_extracting_season_from_file_format_0000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.2005.avi')['season'], '20')

    def test_extracting_episode_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.205.avi')['episode'], '05')

    def test_extracting_episode_from_file_format_0000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.2005.avi')['episode'], '05')

    def test_extracting_season_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')['season'], '02')

    def test_extracting_episode_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')['episode'], '5')

    def test_extracting_season_with_custom_regular_expression_passing_in_season_digit_lengths_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.0250', user_regex='%n.%s{2}%e')['season'], '02')

    def test_extracting_season_with_custom_regular_expression_passing_in_episode_digit_lengths_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s%e{1}')['episode'], '5')

    # def test_removing_the_part_section_from_an_episode_in_a_multiple_episode_group(self):
    #   # need to find a way to force the use of part in the name.
    #   fn = 'stargate.sg-1.s9e03.blah.HDTV.XViD.avi'
    #   credentials = self.tv.extract_details_from_file(fn)
    #   names = self.tv.retrieve_episode_name(episode.show, season=episode.season, episode=episode.episode)
    #   name = self.tv.remove_part_from_multiple_episodes(names[0])
    #   new_fn = self.tv.set_output_format(names[0], season=episode.season, episode=episode.episode, title=names[1])
    #   path = self.tv.build_path(new_filename=new_fn, extension=credentials[3])
    #   self.tv.rename(fn, path)
    #   assert_true(isfile(join(self.files, 'Stargate SG-1 - 903 - Origin (3).avi')))


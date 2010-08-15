import os
import shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from main import TvRenamr

class TestMain(object):
    working = 'tests/data/working'
    
    def setUp(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    
    def test_instantiate_core(self):
        assert_true(isinstance(TvRenamr("/", log_level='critical'), TvRenamr))
    
    
    def test_passing_in_a_show_name_renames_a_file_using_that_name(self):
        fn = 'avatar.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['show'] = 'Avatar: The Last Airbender'
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        path = self.tv.build_path(organise=False, **credentials)
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.working, 'Avatar, The Last Airbender - 108 - Winter Solstice (2), Avatar Roku.avi')))
    
    
    def test_passing_in_a_season_number_to_retrieve_episode_name_returns_the_correct_episode_name_from_that_season(self):
        credentials = self.tv.extract_details_from_file('chuck.s1e08.blah.avi')
        credentials['season'] ='2'
        assert_equal(self.tv.retrieve_episode_name(**credentials), 'Chuck Versus the Gravitron')
    
    
    def test_passing_in_a_season_number_renames_a_file_using_that_season_number(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['season'] = '2'
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        credentials['show'] = self.tv.format_show_name(credentials['show'], the=False)
        path = self.tv.build_path(organise=False, **credentials)
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.working, 'Chuck - 208 - Chuck Versus the Gravitron.avi')))
    
    
    def test_passing_in_an_episode_number_returns_the_correct_episode_title(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['episode'] = '9'
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        credentials['show'] = self.tv.format_show_name(credentials['show'], the=None)
        path = self.tv.build_path(organise=False, **credentials)
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.working, 'Chuck - 109 - Chuck Versus the Imported Hard Salami.avi')))
    
    
    def test_passing_in_an_episode_number_renames_a_file_using_that_episode_number(self):
        credentials = self.tv.extract_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi')
        credentials['episode'] = '9'
        assert_equal(self.tv.retrieve_episode_name(**credentials), 'Chuck Versus the Imported Hard Salami')
    
    
    def test_setting_the_position_of_a_shows_leading_the_to_the_end_of_the_file_name(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        credentials['show'] = self.tv.format_show_name(credentials['show'], the=True)
        path = self.tv.build_path(organise=False, **credentials)
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.working, 'Big Bang Theory, The - 301 - The Electric Can Opener Fluctuation.avi')))
    
    
    def test_setting_an_episodes_format_as_name_season_episode_title(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        credentials['show'] = self.tv.format_show_name(credentials['show'], the=False)
        assert_equals(self.tv.build_path(rename_dir=self.working, organise=False, format='%n - %s%e - %t%x', **credentials), 'tests/data/working/Chuck - 108 - Chuck Versus the Truth.avi')
    
    
    def test_setting_an_episodes_format_as_season_episode_title_name(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        credentials['show'] = self.tv.format_show_name(credentials['show'], the=False)
        assert_equals(self.tv.build_path(rename_dir=self.working, organise=False, format='%s - %e - %t - %n%x', **credentials), 'tests/data/working/1 - 08 - Chuck Versus the Truth - Chuck.avi')
    
    
    def test_setting_an_episodes_format_as_title_episode_season_name(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        credentials['show'] = self.tv.format_show_name(credentials['show'], the=False)
        assert_equals(self.tv.build_path(rename_dir=self.working, organise=False, format='%t - %e - %s - %n%x', **credentials), 'tests/data/working/Chuck Versus the Truth - 08 - 1 - Chuck.avi')
    
    
    def test_extracting_season_from_file_format_s0e00(self):
        credentials = self.tv.extract_details_from_file("chuck.s2e06.avi")
        assert_equal(credentials['season'], '2')
    
    
    def test_extracting_season_from_file_format_s00e00(self):
        credentials = self.tv.extract_details_from_file("chuck.s20e05.avi")
        assert_equal(credentials['season'], '20')
    
    
    def test_extracting_episode_from_file_format_s0e00(self):
        credentials = self.tv.extract_details_from_file('chuck.s2e05.avi')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_episode_from_file_format_s00e00(self):
        credentials = self.tv.extract_details_from_file('chuck.s20e05')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_season_from_file_format_0x00(self):
        credentials = self.tv.extract_details_from_file("chuck.2x05.avi")
        assert_equal(credentials['season'], '2')
    
    
    def test_extracting_season_from_file_format_00x00(self):
        credentials = self.tv.extract_details_from_file("chuck.20x05.avi")
        assert_equal(credentials['season'], '20')
    
    
    def test_extracting_episode_from_file_format_0x00(self):
        credentials = self.tv.extract_details_from_file('chuck.2x05.avi')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_episode_from_file_format_00x00(self):
        credentials = self.tv.extract_details_from_file('chuck.20x05')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_season_from_file_format_000(self):
        credentials = self.tv.extract_details_from_file("chuck.205.avi")
        assert_equal(credentials['season'], '2')
    
    
    def test_extracting_season_from_file_format_0000(self):
        credentials = self.tv.extract_details_from_file("chuck.2005.avi")
        assert_equal(credentials['season'], '20')
    
    
    def test_extracting_episode_from_file_format_000(self):
        credentials = self.tv.extract_details_from_file('chuck.205.avi')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_episode_from_file_format_0000(self):
        credentials = self.tv.extract_details_from_file('chuck.2005')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_season_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')
        assert_equal(credentials['season'], '02')
    
    
    def test_extracting_episode_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')
        assert_equal(credentials['episode'], '5')
    
    
    def test_extracting_season_with_custom_regular_expression_passing_in_season_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_details_from_file('chuck.0250', user_regex='%n.%s{2}%e')
        assert_equal(credentials['season'], '02')
    
    
    def test_extracting_season_with_custom_regular_expression_passing_in_episode_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s%e{1}')
        assert_equal(credentials['episode'], '5')
    
    
    # def test_removing_the_part_section_from_an_episode_in_a_multiple_episode_group(self):
    #   # need to find a way to force the use of part in the name.
    #   fn = 'stargate.sg-1.s9e03.blah.HDTV.XViD.avi'
    #   credentials = self.tv.extract_details_from_file(fn)
    #   names = self.tv.retrieve_episode_name(show=credentials['show'], season=credentials['season'], episode=credentials['episode'])
    #   name = self.tv.remove_part_from_multiple_episodes(names[0])
    #   new_fn = self.tv.set_output_format(show=names[0], season=credentials['season'], episode=credentials['episode'], title=names[1])
    #   path = self.tv.build_path(new_filename=new_fn, extension=credentials[3])
    #   self.tv.rename(fn, path)
    #   assert_true(os.path.isfile(os.path.join(self.working, 'Stargate SG-1 - 903 - Origin (3).avi')))
    
    # def test_replacing_a_show_name_from_the_exceptions_file_returns_the_correct_show_name(self):
    #     fn = 'american.dad.s2e08.foo.bar.avi'
    #     credentials = self.tv.extract_details_from_file(fn)
    #     show_name = self.tv.convert_show_names_using_exceptions_file('tests/exceptions.txt', credentials['show'])
    #     assert_equal(show_name, 'american dad!')
    
    # def test_replacing_a_show_name_from_the_exceptions_file_renames_a_file_correctly(self):
    #     fn = 'american.dad.s2e08.foo.bar.avi'
    #     credentials = self.tv.extract_details_from_file(fn)
    #     credentials['show'] = self.tv.convert_show_names_using_exceptions_file('tests/exceptions.txt', credentials['show'])
    #     title = self.tv.retrieve_episode_name(show=credentials['show'], season=credentials['season'], episode=credentials['episode'])
    #     credentials['show'] = title['show']
    #     credentials['title'] = title['title']
    #     path = self.tv.build_path(show=credentials['show'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'])
    #     self.tv.rename(fn, path)
    #     assert_true(os.path.isfile(os.path.join(self.working, 'American Dad! - 208 - Irregarding Steve.avi')))
    # 
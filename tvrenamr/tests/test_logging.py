from os.path import isfile, join

from nose.tools import assert_true

from tvrenamr.episode import Episode
from tvrenamr.tests.base import BaseTest


class TestLogging(BaseTest):
    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        fn = 'avatar.s1e08.blah.HDTV.XViD.avi'
        episode = Episode(self.tv.extract_details_from_file(fn,
                          user_regex='%n.s%s{1}e%e{2}.blah'))
        episode.show_name = 'Avatar: The Last Airbender'
        episode.title = 'Winter Solstice (2): Avatar Roku'
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.files,
                    'Avatar, The Last Airbender - 108 - Winter Solstice (2), Avatar Roku.avi')))


import os
import shutil

from .base import BaseTest


class TestAutoMoving(BaseTest):
    organise = True

    def teardown(self):
        super(TestAutoMoving, self).teardown()
        shutil.rmtree(self.organised)
        os.mkdir(self.organised)

    def test_using_organise_uses_the_specified_organise_folder(self):
        path = self.tv.build_path(self._file, organise=self.organise, rename_dir=self.organised)
        organise_dir = os.path.join('/', *path.split('/')[:-3])
        assert self.organised == organise_dir

    def test_using_organise_uses_the_correct_show_folder_in_the_path(self):
        path = self.tv.build_path(self._file, organise=self.organise, rename_dir=self.organised)
        season_dir = path.split('/')[-3:][0]
        assert season_dir == self._file.show_name

    def test_using_organise_uses_the_correct_season_folder_in_the_path(self):
        path = self.tv.build_path(self._file, organise=self.organise, rename_dir=self.organised)
        season_dir = path.split('/')[-2:][0]
        assert season_dir == 'Season {0}'.format(self._file.season)

    def test_using_organise_uses_the_correct_filename(self):
        path = self.tv.build_path(self._file, organise=self.organise, rename_dir=self.organised)
        filename_base = path.split('/')[-1:][0].split(' - ')[-1:][0]
        filename = self._file.episodes[0].title + self._file.extension
        assert filename_base == filename

    def test_moving_the_leading_the_to_the_end_of_a_show_name_causes_the_show_folder_name_to_follow_suit_when_using_organise(self):
        show_name =  'Big Bang Theory, The'
        self._file.show_name = show_name
        path = self.tv.build_path(self._file, organise=self.organise, rename_dir=self.organised)
        show_dir = path.split('/')[-3:][0]
        assert show_dir == show_name

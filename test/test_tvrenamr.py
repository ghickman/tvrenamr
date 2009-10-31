import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr

class TestTvrenamr(object):
    working = 'test/data/working'
    
    def setUp(self):
        files = 'test/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    """
    - use no options
    - use -r
    - use -a and -r
    - use -n
    - use -s
    - use -e
    - use -t
    - use -o
    - use --regex
    - use exceptions file
    - use --deluge
    - use --deluge-share-ratio
    - use unexpected format
    """
    def test_single_rename_with_no_options(self):
        pass
    
    def test_single_rename_with_rename_folder_location_specified(self):
        pass
    
    def test_single_rename_with_rename_folder_location_specified_and_organise_option(self):
        pass
    
    def test_single_rename_with_name_option(self):
        pass
    
    def test_single_rename_with_season_option(self):
        pass
    
    def test_single_rename_with_episode_option(self):
        pass
    
    def test_single_rename_with_leading_the_moved_to_end_of_show_name_option(self):
        pass
    
    def test_single_rename_with_output_format_specified(self):
        pass
    
    def test_single_rename_with_custom_regular_expression_specified(self):
        pass
    
    def test_single_rename_with_exceptions_file_used(self):
        pass
    
    def test_single_rename_with_deluge_option(self):
        pass
    
    def test_single_rename_with_deluge_share_ratio_option(self):
        pass

    def test_single_rename_with_an_unexpected_format_raises_an_unexpected_format_exception(self):
        pass

    
    """
    - use recursive and no options
    - use recursive and -r
    - use recursive and -a and -r
    - use recursive and -n
    - use recursive and -s
    - use recursive and -e
    - use recursive and -t
    - use recursive and -o
    - use recursive and --regex
    - use recursive and exceptions file
    - use recursive and --deluge
    - use recursive and --deluge-share-ratio
    - use recursive and unexpected format
    """
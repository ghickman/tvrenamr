import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from tvrenamr.errors import UnexpectedFormatException

base = 'python tvrenamr.py'
working = 'tests/data/working'
renamed = 'tests/data/renamed'
organised = 'tests/data/organised'
exceptions = 'tests/exceptions.txt'
logging = 'info'

class TestScript(object):
    
    def setUp(self):
        files = 'tests/data/files'
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(working, fn))
    
    def tearDown(self):
        shutil.rmtree(working)
        os.mkdir(working)
    
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
        os.system('%s -l%s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, working))
        assert_true(os.path.exists('%s/Chuck - 108 - Chuck Versus The Truth.avi' % working))
    
    def test_single_rename_with_rename_folder_location_specified(self):
        os.system('%s -l%s -r%s %s/chuck.s1e10.blah.HDTV.XViD.avi' % (base, logging, renamed, working))
        assert_true(os.path.exists('%s/Chuck - 110 - Chuck Versus The Nemesis.avi' % renamed))
    
    def test_single_rename_with_rename_folder_location_specified_and_organise_option(self):
        os.system('%s -l%s --organise -r%s %s/chuck.s1e11.blah.HDTV.XViD.avi' % (base, logging, renamed, working))
        assert_true(os.path.exists('%s/Chuck/Season 1/Chuck - 111 - Chuck Versus The Crown Vic.avi' % renamed))
    
    def test_single_rename_with_name_option(self):
        os.system('%s -l%s -n%s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, '\'Stargate SG-1\'', working))
        assert_true(os.path.exists('%s/Stargate SG-1 - 108 - The Nox.avi' % working))
    
    def test_single_rename_with_season_option(self):
        os.system('%s -l%s -s2 %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, working))
        assert_true(os.path.exists('%s/Chuck - 208 - Chuck Versus The Gravitron.avi' % working))
    
    def test_single_rename_with_episode_option(self):
        os.system('%s -l%s -e9 %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, working))
        assert_true(os.path.exists('%s/Chuck - 109 - Chuck Versus The Imported Hard Salami.avi' % working))
    
    def test_single_rename_with_leading_the_moved_to_end_of_show_name_option(self):
        os.system('%s -l%s -t %s/The.Big.Bang.Theory.S03E01.HDTV.XViD-NoTV.avi' % (base, logging, working))
        assert_true(os.path.exists('%s/Big Bang Theory, The - 301 - The Electric Can Opener Fluctuation.avi' % working))
    
    def test_single_rename_with_output_format_specified(self):
        os.system('%s -l%s -o%s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, '\'%s%e - %n %t\'', working))
        assert_true(os.path.exists('%s/108 - Chuck Chuck Versus The Truth.avi' % working))
    
    def test_single_rename_with_custom_regular_expression_specified(self):
        os.system('%s -l%s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, working))
        assert_true(os.path.exists('%s/Chuck - 108 - Chuck Versus The Truth.avi' % working))
    
    def test_single_rename_with_exceptions_file_used(self):
        # os.system('%s -l%s -x%s %s/avatar.s1e08.blah.HDTV.XViD.avi' % (base, logging, exceptions, working))
        # assert_true(os.path.exists('%s/Avatar, The Last Airbender - 108 - Winter Solstice (2) - Avatar Roku.avi' % working))
        pass
    
    def test_single_rename_with_deluge_option(self):
        # os.system('%s -l%s --deluge %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, working))
        # assert_true(os.path.exists('%s/Chuck - 108 - Chuck Versus the Truth.avi' % working))
        pass
    
    def test_single_rename_with_deluge_share_ratio_option(self):
        # os.system('%s -l%s --deluge-share-ratio%d %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, logging, 2, working))
        # assert_true(os.path.exists('%s/Chuck - 108 - Chuck Versus the Truth.avi' % working))
        pass

    def test_single_rename_with_an_unexpected_format_raises_an_unexpected_format_exception(self):
        #assert_raises(UnexpectedFormatException, os.system('%s %s/\'West Wing.avi\'' % (base, logging, working)))
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

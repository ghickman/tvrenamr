import logging
from optparse import OptionParser
import os
import re
from series import Series
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/Users/madnashua/Projects/tvrenamr/tvrenamr.log',
                    filemode='a')

class TvRenamr():
    logging = None
    working_dir = None
    
    def __init__(self, working_dir, logging=None):
        self.working_dir = working_dir
        self.logging = logging
        
    def __extract_file_info(self, fn, user_regex=None):
        if re.compile(".*?\s-\s[\d]{3,4}\s-\s.*?\."+fn[-3:]).match(fn): raise Exception('Already in correct naming format: '+ fn)
        fn = fn.replace("_", ".")
        fn = fn.replace(" ", ".")
        if user_regex == None: regex = "(?P<series>[\w._]+)\.[Ss]?(?P<season>[0-9]{1,2})([Xx]|[Ee])(?P<episode>[0-9]{1,2})"
        else: regex = user_regex.replace('%s', "(?P<season>[0-9]{1,2})").replace('%e', '(?P<episode>[0-9]{1,2})')
        m = re.compile(regex).match(fn)
        if m != None: return [m.group('series').replace("."," "),str(int(m.group('season'))),m.group('episode'),fn[-4:]]
        else: raise Exception('Skipped due to unexpected format: '+ fn)
    
    def __build_file_name(self, fn):
        s = Series(fn[0])
        try: episode_name = s.get_episode_name(s.get_series_id(), fn[1], fn[2])
        except Exception, e: raise
        if len(fn[2]) == 1: fn[2] = "0" + fn[2]
        return s.name + " - " + fn[1] + fn[2] + " - " + episode_name + fn[3]
    
    def __build_auto_path(self, fn, series, season, auto_move):
        path = auto_move + series + "/Season " + season + "/"
        if os.path.exists(new_dir) == False: os.makedirs(new_dir)
        return path
    
    def __rename_file(self, fn, dest, new_fn):
        if os.path.exists(dest) == False:
            os.rename(os.path.join(self.working_dir, fn), dest)
            if self.logging == True: logging.info('Renamed: %s', fn)
        else: raise Exception('File Exists: '+ new_fn +' from: '+fn)
    
    def rename(self, fn, regex=None, renamed_dir=None, auto_move=False):
        """"
        
        """
        #stage
        try:
            f = self.__extract_file_info(fn,regex)
        except Exception, e: raise
        new_fn = self.__build_file_name(f)
        
        #build new path
        if renamed_dir == None: renamed_dir = self.working_dir
        if auto_move != False: 
            dest_path = self.__build_auto_path(new_fn, f[0], f[1], renamed_dir, auto_move)
        else: dest_path = os.path.join(renamed_dir, new_fn)
        
        #rename
        try:
            self.__rename_file(fn, dest_path, new_fn)
        except Exception, e: raise
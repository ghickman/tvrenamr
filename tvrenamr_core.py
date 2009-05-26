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
    renamed_dir = None
    working_dir = None
    
    def __init__(self, working_dir, logging=None):
        self.working_dir = working_dir
        self.logging = logging
        
    def extract_file_details(self, fn, user_regex=None):
        fn = fn.replace("_", ".")
        if user_regex == None: regex = "(?P<series>[\w._]+)\.s?(?P<season>[0-9]{1,2})(x|e)(?P<episode>[0-9]{1,2})"
        else: regex = user_regex.replace('%s', "(?P<season>[0-9]{1,2})").replace('%e', '(?P<episode>[0-9]{1,2})')
        m = re.compile(regex).match(fn)
        if m != None:
            return [m.group('series'),m.group('season'),m.group('episode'),fn[-4:]]
        else: raise Exception('Skipped due to unexpected format: '+ fn)
    
    def build_file_name(self, file_details):
        s = Series(file_details[0])
        try: episode_name = s.getEpisodeName(s.getSeriesId(), file_details[1], file_details[2])
        except Exception, e: raise Exception(e)
        return s.name + " - " + file_details[1] + file_details[2] + " - " + episode_name + file_details[3]
    
    def build_directory_structure(self, file_details):
        new_dir = file_details[0] + "/Season " + file_details[1] + "/"
        print new_dir
        return new_dir
    
    def rename(self, fn, regex=None):
        f = self.extract_file_details(fn, regex)
        new_fn = self.build_file_name(f)
        if os.path.exists(self.working_dir + new_fn) == False:
            os.rename(os.path.join(self.working_dir, fn), os.path.join(self.working_dir, new_fn))
            if self.logging == True: logging.info('Renamed: %s', new_fn)
        else: raise Exception('File Exists: '+ new_fn +' from '+ fn)
        
    def rename_and_auto_move(self, fn, auto_move_dir, regex=None):
        f = self.extract_file_details(fn, regex)
        new_fn = self.build_file_name(f)
        new_dir = self.build_directory_structure(f)
        if os.path.exists(os.path.join(auto_move_dir, new_dir)) == False: os.makedirs(os.path.join(auto_move_dir, new_dir))
        os.rename(os.path.join(self.working_dir, fn), os.path.join(auto_move_dir, new_dir, new_fn))
                
    def rename_and_move(self, fn, renamed_dir, regex=None):
        f = self.extract_file_details(fn, regex)
        new_fn = self.build_file_name(f)
        if os.path.exists(renamed_dir) == False: os.makedirs(renamed_dir)
        os.rename(os.path.join(self.working_dir, fn), os.path.join(renamed_dir, new_fn))
                              
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
    
    def __init__(self, working_dir):
        self.working_dir = working_dir
        
    def extract_file_details(self, fn):
        #sanitize input
        ext = fn[-4:]
        self.fn = fn.replace("_", ".")
        m = re.compile("[Ss](\d{2})[Ee](\d{2})").split(fn)
        if m and len(m) > 1:
            m[0] = m[0].replace(".", " ")
            return [m[0].strip(),str(int(m[1])),m[2],ext]
        else:
            #logging.warning('Incorrect format for auto-renaming: %s', fn)
            raise Exception('Incorrect format for auto-renaming: %s', fn)
    
    def build_file_name(self, file_details):
        s = Series(file_details[0])
        try:
            episode_name = s.getEpisodeName(s.getSeriesId(), file_details[1], file_details[2])
        except Exception, e:
            raise Exception(e)
            #SORT EXCEPTIONS
        
        return s.name + " - " + file_details[1] + file_details[2] + " - " + episode_name + file_details[3]
    
    def build_directory_structure(self, file_details):
        new_dir = file_details[0] + "/Season " + file_details[1] + "/"
        print new_dir
        return new_dir
    
    def rename(self, fn):
        #THROW EXCEPTIONS
        f = self.extract_file_details(fn)
        new_fn = self.build_file_name(f)
        if os.path.exists(self.working_dir + new_fn) == False:
            os.rename(os.path.join(self.working_dir, fn), os.path.join(self.working_dir, new_fn))
            logging.info('Renamed: %s', new_fn)
        else:
            raise Exception('File Exists: %s from %s', new_fn, fn)
        
    def rename_and_auto_move(self, fn, auto_move_dir):
        f = self.extract_file_details(fn)
        new_fn = self.build_file_name(f)
        new_dir = self.build_directory_structure(f)
        if os.path.exists(os.path.join(auto_move_dir, new_dir)) == False: os.makedirs(os.path.join(auto_move_dir, new_dir))
            
        os.rename(os.path.join(self.working_dir, fn), os.path.join(auto_move_dir, new_dir, new_fn))
                
    def rename_and_move(self, fn, renamed_dir):
        f = self.extract_file_details(fn)
        new_fn = self.build_file_name(f)
        if os.path.exists(renamed_dir) == False: os.makedirs(renamed_dir)
            
        os.rename(os.path.join(self.working_dir, fn), os.path.join(renamed_dir, new_fn))
                              
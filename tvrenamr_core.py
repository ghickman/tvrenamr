import os, re, sys

from errors import *

class TvRenamr():
    working_dir = None
    
    def __init__(self, working_dir):
        self.working_dir = working_dir
    
    def extract_episode_details_from_file(self, fn, user_regex=None):
        """
        Looks at the file given and extracts from it the show title, it's season number and episode number using regular expression ninja skills. The 
        default formats accepted are: series.0x00.xxx or series.s0e00.xxx
        A user can specify their own regular expression for a format not already covered.
        """
        if re.compile(".*?\s-\s[\d]{3,4}\s-\s.+?\."+fn[-3:]).match(fn): raise AlreadyNamedException(fn)
        fn = fn.replace("_", ".").replace(" ", ".")
        if user_regex == None: regex = "(?P<series>[\w\s._]+)\.[Ss]?(?P<season>[\d]{1,2}?)([Xx]|[Ee])(?P<episode>[\d]{1,2})"
        else: regex = user_regex.replace('%n', '(?P<series>[\w\s._]+)').replace('%s', "(?P<season>[0-9]{1,2}?)").replace('%e', '(?P<episode>[0-9]{1,2})')
        m = re.compile(regex).match(fn)
        if m != None:
            series = m.group('series').replace('.',' ')
            if re.compile('\s{1}[\d]{4}').match(series[-5:]) != None: series = "%s(%s)" % (series[:-4], series[-4:])
            return [series,m.group('season'),m.group('episode'),fn[-4:]]
        else: raise UnexpectedFormatException(fn)
    
    def retrieve_episode_name(self, series, season, episode, library=None):
        """
        Retrieves the name of a given episode. The series name, season and episode numbers must be specified and the library to get the episode's name
        can be specified by the user.
        """
        if library == 'tvrage': from tvrage import TvRage as library
        else: from thetvdb import TheTvDb as library
        lib = library(series)
        return lib.get_episode_name(season,episode)
    
    def build_path(self, details, series_name, episode_name, renamed_dir=None, auto_move=None):
        """
        Builds the new path for the file to be renamed to, by default this is the working directory. Users can specify a directoy to move files to 
        once renamed using the renamed_dir option. The auto_move option can be used to specify a top level directory where files will be placed in
        season and series folders, i.e. series -> season 1 -> episodes
        """
        if len(details[2]) == 1: details[2] = "0"+ details[2]
        new_fn = series_name +" - "+ str(int(details[1])) + details[2] +" - "+ episode_name + details[3]
        if auto_move != None: renamed_dir = auto_move + details[0] +"/Season "+ str(int(details[1])) +"/"+ new_fn
        elif renamed_dir == None: renamed_dir = self.working_dir
        return os.path.join(renamed_dir, new_fn)
    
    def rename(self, fn, new_fn):
        """
        """
        if os.path.exists(new_fn) == False: os.rename(os.path.join(self.working_dir, fn), new_fn)
        else: raise EpisodeAlreadyExistsInFolderException(fn,new_fn)
    
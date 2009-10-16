import os, re, sys

from errors import *

class TvRenamr():
    working_dir = None
    
    def __init__(self, working_dir):
        self.working_dir = working_dir
    
    def extract_episode_details_from_file(self, fn, user_regex=None):
        """
        Looks at the file given and extracts from it the show title, it's season number and episode number using regular expression ninja skills. The 
        default formats accepted are: series.0x00.xxx or series.s0e00.xxx or series.000.xxx
        A user can specify their own regular expression for a format not already covered.
        """
        #if re.compile(".*?\s-\s[\d]{3,4}\s-\s.+?\."+fn[-3:]).match(fn): raise AlreadyNamedException(fn)
        fn = fn.replace("_", ".").replace(" ", ".")
        print fn
        regex = self.__build_regex(user_regex)
        print regex 
        m = re.compile(regex).match(fn)
        if m is not None:
            series = m.group('series').replace('.',' ')
            #if re.compile('\s{1}[\d]{4}').match(series[-5:]) != None: series = "%s(%s)" % (series[:-4], series[-4:])
            return [series,m.group('season'),m.group('episode'),fn[-4:]]
        else: raise UnexpectedFormatException(fn)
    
    def convert_show_names_using_exceptions_file(self, exceptions_file, show_name):
        """
        Converts a show name to a new name.
        """
        # print show_name
        # print exceptions_file
        import fileinput as f
        try:
            for show in [line.strip().split(' => ') for line in f.input(exceptions_file) if not line.startswith('#')]:
                if show[0] == show_name: return show[1]
        except: raise Exception #needs to be an info log to say the show wasn't found in the file, continuing with regex'd name
    
    def retrieve_episode_name(self, series, season, episode, library=None):
        """
        Retrieves the name of a given episode. The series name, season and episode numbers must be specified and the library to get the episode's name
        can be specified by the user.
        """
        if library == 'tvrage': from tvrage import TvRage as library
        else: from thetvdb import TheTvDb as library
        lib = library(series)
        return lib.get_episode_name(season,episode)
    
    def set_position_of_leading_the_to_end_of_show_name(self, show_name):
        if not(show_name.startswith('The ')): raise NoLeadingTheException(show_name)
        return show_name[4:]+', The'
    
    def remove_part_from_multiple_episodes(self, show_name):
        return show_name.replace('(Part ','(')
    
    def format_output(self, show_name, user_regex=None):
        pass
    
    def build_path(self, series, season, episode, episode_name, extension, renamed_dir=None, auto_move=None):
        """
        Builds the new path for the file to be renamed to, by default this is the working directory. Users can specify a directory to move files to 
        once renamed using the renamed_dir option. The auto_move option can be used to specify a top level directory where files will be placed in
        season and series folders, i.e. series/season 1/episodes
        """
        if len(episode) == 1: episode = '0'+ episode
        new_fn = series +" - "+ str(int(season)) + episode +" - "+ episode_name + extension
        if auto_move is not None: renamed_dir = self.__build_auto_move_path(auto_move, series, season)
            
        elif renamed_dir is None: renamed_dir = self.working_dir
        return os.path.join(renamed_dir, new_fn)
    
    def clean_names(self, fn, character_to_replace=':', replacement_character=' -'):
        """
        Cleans the string passed in, making it be safe for all file systems. Also allows the user to specify the new characters to be used.
        """
        print fn
        return fn.replace(character_to_replace, replacement_character)
    
    def rename(self, fn, new_fn):
        """
        Renames the file passed in to the new filename path passed in and returns the new filename
        """
        if not os.path.exists(new_fn):
            os.rename(os.path.join(self.working_dir, fn), new_fn)
            renamed = os.path.split(new_fn)
            return renamed[1]
        else: raise EpisodeAlreadyExistsInFolderException(fn,new_fn)
    
    def __build_regex(self, regex=None):
        """
        Builds the regular expression to extract the files details.
        """
        series = '(?P<series>[\w\s.,_-]+)'
        season = '(?P<season>[\d]{1,2})'
        episode = '(?P<episode>[\d]{2})'
        
        if regex is None: return series+'\.[Ss]?'+season+'([Xx]|[Ee]|)'+episode
        
        regex = regex.replace('%n', series)
        if regex.find('%s{') is not -1:  # %s{n}
            r = regex.split('%s{')[1][:1]
            regex = regex.replace('%s{'+r+'}', season.replace('1,2', r))
        if regex.find('%e{') is not -1: # %e{n}
            r = regex.split('%e{')[1][:1]
            regex = regex.replace('%e{'+r+'}', episode.replace('2', r))
        if regex.find('%s') is not -1: regex = regex.replace('%s', season) # %s
        if regex.find('%e') is not -1: regex = regex.replace('%e', episode) # %e
        return regex
        if regex.find('%s') is -1 or regex.find('%e') is -1: raise Exception # no correct syntax found
    
    def __build_auto_move_path(self, auto_move_start_path, series_name, season_number):
        """
        Constructs a directory path using the series name and season number of an episode.
        """
        if auto_move_start_path[-1:] != '/': auto_move_start_path = auto_move_start_path +'/'
        path = auto_move_start_path + series_name +'/Season '+ str(int(season_number)) +'/'
        if not os.path.exists(path): os.makedirs(path)
        return path
    
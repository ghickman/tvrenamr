import fileinput
import logging
import os
import re
import sys

from errors import *

log = logging.getLogger('Core')

class TvRenamr():
    def __init__(self, working_dir, log_level='info'):
        self.working_dir = working_dir
        # set the log level on the pacakge level logger
        logging.getLogger().setLevel(self.__set_log_level(log_level))
    
    def extract_episode_details_from_file(self, fn, user_regex=None):
        """
        Looks at the file given and extracts from it the show title, it's season number and episode number 
        using regular expression magic. The default formats accepted are: series.0x00.xxx or series.s0e00.xxx 
        or series.000.xxx
        A user can specify their own regular expression for a format not already covered.
        """
        #if re.compile(".*?\s-\s[\d]{3,4}\s-\s.+?\."+fn[-3:]).match(fn): raise AlreadyNamedException(fn)
        fn = fn.replace("_", ".").replace(" ", ".")
        log.info('Renaming file: '+fn)
        regex = self.__build_regex(user_regex)
        log.info('Renaming using: '+regex)
        m = re.compile(regex).match(fn)
        if m is not None:
            series = m.group('series').replace('.',' ')
            #if re.compile('\s{1}[\d]{4}').match(series[-5:]) != None: series = "%s(%s)" % (series[:-4], series[-4:])
            return {'series': series, 'season': m.group('season'), 'episode': m.group('episode'), 'extension': fn[-4:]}
        else: raise UnexpectedFormatException(fn)
    
    def convert_show_names_using_exceptions_file(self, exceptions_file, show_name):
        """
        Converts a show name to a new name specified in the exceptions_file. This method is designed for use in
        conjunction with the daemon.
        """
        for show in [line.strip().split(' => ') for line in fileinput.input(exceptions_file) if not line.startswith('#')]:
            if show[0] == show_name:
                log.debug('Replacing '+show_name+' with '+show[1])
                return show[1]
            else: log.warning(show_name+' wasn\'t found in the exceptions file')
    
    def retrieve_episode_name(self, series, season, episode, library=None):
        """
        Retrieves the name of a given episode. The series name, season and episode numbers must be specified 
        to get the episode's name. The library can be specified by the user, but by default TheTvDb will be
        used.
        """
        if library == 'tvrage':
            from lib.tvrage import TvRage as library
            log.debug('Opening TvRage library')
        else: 
            from lib.thetvdb import TheTvDb as library
            log.debug('Opening TheTvDb library')
        lib = library(series)
        name = lib.get_episode_name(season,episode)
        log.info('Retrieved: '+name['title'])
        return name
    
    def set_position_of_leading_the_to_end_of_series_name(self, show_name):
        """Moves the leading the of a series name to the end of the series name."""
        if not(show_name.startswith('The ')): raise NoLeadingTheException(show_name)
        log.debug('Moving the leading \'The\' to end of: '+show_name)
        return show_name[4:]+', The'
    
    def remove_part_from_multiple_episodes(self, show_name):
        """
        In episode titles of multiple part episodes that use the format (Part n) remove the 'Part ' section so
        the format is (n)
        """
        log.debug('Removing Part from episode name')
        return show_name.replace('(Part ','(')
    
    def set_format_for_multiple_part_episodes(self, show_name, format):
        """
        Set the format for multiple part episodes and return a formatted episode title
        """
        # find the current multiple part section
        # extract multipart number
        # build new episode title
        pass
    
    def build_path(self, series, season, episode, title, extension, format=None, renamed_dir=None, organise=False):
        """
        Set the output format for the file name of a renamed show. By default the format is: 
        Show Name - Season NumberEpisode Number - Episode Title.format.
        
        Builds the new path for the file to be renamed to, by default this is the working directory. Users can 
        specify a directory to move files to once renamed using the renamed_dir option. The auto_move option 
        can be used to specify a top level directory where files will be placed in season and series folders, 
        i.e. series/season 1/episodes
        """
        if format is None: format = '%n - %s%e - %t'
        else:
            error = []
            if format.find('%n') is -1: error.append('series name')
            if format.find('%s') is -1: error.append('season')
            if format.find('%e') is -1: error.append('episode')
            if format.find('%t') is -1: error.append('episode title')
            if len(error) is not 0 : raise OutputFormatMissingSyntaxException(error)
        
        if len(episode) == 1: episode = '0'+ episode
        formatted = format.replace('%n', series.replace(series[:1], series[:1].upper(), 1)).replace('%s', str(int(season))).replace('%e', episode).replace('%t', title)
        log.info('Destination file: '+formatted)
        
        if renamed_dir is None: renamed = self.working_dir
        else: renamed = renamed_dir
        
        if organise is True: renamed = self.__build_organise_path(renamed, series, season)
        
        log.debug('Destination directory: '+renamed)
        return os.path.join(renamed, formatted+extension)
    
    def clean_names(self, fn, character_to_replace=':', replacement_character=' -'):
        """
        Cleans the string passed in, making it be safe for all file systems. Also allows the user to specify 
        the new characters to be used.
        """
        print fn
        return fn.replace(character_to_replace, replacement_character)
    
    def rename(self, fn, new_fn):
        """
        Renames the file passed in to the new filename path passed in and returns the new filename
        """
        if not os.path.exists(new_fn):
            log.info('Beginning rename')
            os.rename(os.path.join(self.working_dir, fn), new_fn)
            renamed = os.path.split(new_fn)
            log.debug('Renamed '+fn+' to '+renamed[1])
            return renamed[1]
        else: raise EpisodeAlreadyExistsInFolderException(fn,new_fn)
    
    def __set_log_level(self, level):
        LEVELS = {
            'debug': logging.DEBUG,     #10
            'info': logging.INFO,       #20
            'warning': logging.WARNING, #30
            'error': logging.ERROR,     #40
            'critical': logging.CRITICAL#50
        }
        return LEVELS.get(level, logging.NOTSET)
    
    def __build_regex(self, regex=None):
        """
        Builds the regular expression to extract the files details.
        """
        series = '(?P<series>[\w\s.,_-]+)'
        season = '(?P<season>[\d]{1,2})'
        episode = '(?P<episode>[\d]{2})'
        
        if regex is None: return series+'\.[Ss]?'+season+'([Xx]|[Ee]|)'+episode
        if regex.find('%s') is -1 or regex.find('%e') is -1: raise IncorrectCustomRegularExpressionSyntaxException(regex)
        
        # series name
        regex = regex.replace('%n', series)
        
        # season number
        # %s{n}
        if regex.find('%s{') is not -1:
            log.debug('User set season digit number found')
            r = regex.split('%s{')[1][:1]
            log.debug('User specified '+r+' season digits')
            regex = regex.replace('%s{'+r+'}', season.replace('1,2', r))
            log.debug('Season regex set: '+regex)
        
        # %s
        if regex.find('%s') is not -1:
            regex = regex.replace('%s', season)
            log.debug('Season regex set: '+regex)
        
        # episode number
        # %e{n}
        if regex.find('%e{') is not -1:
            log.debug('User set episode digit number found')
            r = regex.split('%e{')[1][:1]
            log.debug('User specified '+r+' episode digits')
            regex = regex.replace('%e{'+r+'}', episode.replace('2', r))
            log.debug('Episode regex set: '+regex)
        
        # %e
        if regex.find('%e') is not -1:
            regex = regex.replace('%e', episode)
            log.debug('Episode regex set: '+regex)
        
        return regex
    
    def __build_organise_path(self, start_path, series_name, season_number):
        """
        Constructs a directory path using the series name and season number of an episode.
        """
        if start_path[-1:] != '/': start_path = start_path +'/'
        path = start_path + series_name +'/Season '+ str(int(season_number)) +'/'
        if not os.path.exists(path):
            os.makedirs(path)
            log.debug('Directories created for path: '+path)
        return path
    
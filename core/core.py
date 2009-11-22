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
        logging.getLogger().setLevel(self.__set_log_level(log_level))
    
    def extract_episode_details_from_file(self, fn, user_regex=None):
        """
        Looks at the file given and extracts from it the show title, it's season number and episode number 
        using regular expression magic. The default formats accepted are: series.0x00.xxx or series.s0e00.xxx 
        or series.000.xxx
        A user can specify their own regular expression for a format not already covered.
        
        :param fn: The file name passed in.
        :param user_regex: A user specified regular expression. Defaults to None.
        
        :returns: The show name, season number, episode number and last four characters (assumed to be the extension) extracted from
        the file passed in.
        :rtype: A dictionary with the keys 'show', 'season', 'episode' and 'extension'.
        """
        fn = fn.replace("_", ".").replace(" ", ".")
        log.info('Renaming file: '+fn)
        regex = self.__build_regex(user_regex)
        log.info('Renaming using: '+regex)
        m = re.compile(regex).match(fn)
        if m is not None:
            show = m.group('show').replace('.',' ').strip()
            log.debug('Returned show: %s, season: %s, episode: %s, extension: %s' % (show, m.group('season'), m.group('episode'), fn[-4:]))
            return {'show': show, 'season': m.group('season'), 'episode': m.group('episode'), 'extension': fn[-4:]}
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
    
    def retrieve_episode_name(self, show, season, episode, library='tvrage'):
        """
        Retrieves the name of a given episode. The series name, season and episode numbers must be specified 
        to get the episode's name. The library can be specified by the user, but will default to Tv Rage.
        
        :param show: The show name to search for.
        :param season: The season number to search for.
        :param episode: The episode number to search for.
        :param library: The library to search in.
        
        :returns: The episode title.
        :rtype: A string.
        """
        if library == 'thetvdb':
            from lib.thetvdb import TheTvDb as library
            log.debug('Opening The Tv Db library')
        elif library == 'tvrage':
            from lib.tvrage import TvRage as library
            log.debug('Opening Tv Rage library')
        
        lib = library(show)
        return lib.get_episode_name(str(int(season)), episode)
    
    def move_leading_the_to_trailing_the(self, show_name):
        """
        Moves the leading 'The' of a show name to a trailing 'The'. A comma and space are added before the new 'The'.
        
        :param show_name: The show name.
        
        :returns: The new show name.
        :rtype: A string.
        """
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
    
    def build_path(self, show, season, episode, title, extension, format=None, renamed_dir=None, organise=False):
        """
        Set the output format for the file name of a renamed show. By default the format is: 
        Show Name - Season NumberEpisode Number - Episode Title.format.
        
        Builds the new path for the file to be renamed to, by default this is the working directory. Users can 
        specify a directory to move files to once renamed using the renamed_dir option. The auto_move option 
        can be used to specify a top level directory where files will be placed in season and show folders, 
        i.e. Show/Season 1/episodes
        
        :param show: The show name.
        :param season: The season number.
        :param episode: The episode number.
        :param title: The episode title.
        :param extension: The file extension.
        :param format: The order in of the show name, season and episode numbers, episode title and extension in the renamed file's name.
        :param renamed_dir: The directory to place the renamed file into.
        :param organise: A boolean to set whether the renamed directory path should be constructed from the show name and season number.
        
        :returns: The full path to the new file including the formatted file name.
        :rtype: A string.
        """
        if format is None: format = '%n - %s%e - %t'
        else:
            error = []
            if format.find('%n') is -1: error.append('show name')
            if format.find('%s') is -1: error.append('season')
            if format.find('%e') is -1: error.append('episode')
            if format.find('%t') is -1: error.append('episode title')
            if len(error) is not 0 : raise OutputFormatMissingSyntaxException(error)
        
        if len(episode) == 1: episode = '0'+ episode
        formatted = format.replace('%n', show.replace(show[:1], show[:1].upper(), 1)).replace('%s', str(int(season))).replace('%e', episode).replace('%t', title)
        log.info('Destination file: '+formatted)
        
        if renamed_dir is None: renamed = self.working_dir
        else: renamed = renamed_dir
        
        if organise is True: renamed = self.__build_organise_path(renamed, show, season)
        
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
        
        :param fn: The file to rename.
        :param new_fn: The name to rename the file to.
        """
        if not os.path.exists(new_fn):
            log.info('Beginning rename')
            os.rename(os.path.join(self.working_dir, fn), new_fn)
            renamed = os.path.split(new_fn)
            log.debug('Renamed '+fn+' to '+renamed[1])
        else: raise EpisodeAlreadyExistsInDirectoryException(fn, os.path.split(new_fn)[0])
    
    def __set_log_level(self, level):
        """
        Converts a user specified log level into a logging object level. By default this is Info.
        
        :param level: The log level to set.
        
        :returns: A log level useable by a logging object
        :rtype: A string.
        
        """
        LEVELS = {
            'debug': logging.DEBUG,     #10
            'info': logging.INFO,       #20
            'warning': logging.WARNING, #30
            'error': logging.ERROR,     #40
            'critical': logging.CRITICAL#50
        }
        return LEVELS.get(level, logging.INFO)
    
    def __build_regex(self, regex=None):
        """
        Builds the regular expression to extract a files details. Custom syntax can be used in the regular expression to help specify
        parts of the episode's file name. These custom syntax snippets are replaced by the regular expression blocks show.
        
        %n - [\w\s.,_-]+ - The show name.
        %s - [\d]{1,2} - The season number.
        %e - [\d]{2} - The episode number.
        
        :param regex: The regular expression string.
        
        :returns: An actual regular expression.
        :rtype: A string.
        """
        series = '(?P<show>[\w\s.,_-]+)'
        season = '(?P<season>[\d]{1,2})'
        episode = '(?P<episode>[\d]{2})'
        
        if regex is None: return series+'\.[Ss]?'+season+'[XxEe]?'+episode
        if regex.find('%s') is -1 or regex.find('%e') is -1: raise IncorrectCustomRegularExpressionSyntaxException(regex)
        
        # series name
        regex = regex.replace('%n', series)
        
        # season number
        # %s{n}
        if regex.find('%s{') is not -1:
            log.debug('Season digit number found')
            r = regex.split('%s{')[1][:1]
            log.debug('Specified '+r+' season digits')
            s = season.replace('1,2', r)
            regex = regex.replace('%s{'+r+'}', s)
            log.debug('Season regex set: %s' % s)
        
        # %s
        if regex.find('%s') is not -1:
            regex = regex.replace('%s', season)
            log.debug('Default season regex set: %s' % regex)
        
        # episode number
        # %e{n}
        if regex.find('%e{') is not -1:
            log.debug('User set episode digit number found')
            r = regex.split('%e{')[1][:1]
            log.debug('User specified '+r+' episode digits')
            e = episode.replace('2', r)
            regex = regex.replace('%e{'+r+'}', e)
            log.debug('Episode regex set: %s' % e)
        
        # %e
        if regex.find('%e') is not -1:
            regex = regex.replace('%e', episode)
            log.debug('Default episode regex set: %s' % regex)
        
        return regex
    
    def __build_organise_path(self, start_path, show_name, season_number):
        """
        Constructs a directory path using the show name and season number of an episode.
        
        :param start_path: The root path to construct the new path under.
        :param show_name: The show name.
        :param season_number: The season number.
        
        :return: The path to move a renamed episode to.
        :rtype: A string.
        """
        if start_path[-1:] != '/': start_path = start_path +'/'
        path = start_path + series_name +'/Season '+ str(int(season_number)) +'/'
        if not os.path.exists(path):
            os.makedirs(path)
            log.debug('Directories created for path: '+path)
        return path
    
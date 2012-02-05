import logging
import os
import re

from errors import *
from lib.thetvdb import TheTvDb
from lib.tvrage import TvRage

log = logging.getLogger('Core')


class TvRenamr():

    def __init__(self, working_dir, config, debug=False, dry=False):
        """
        :param working_dir: The working directory.
        :type working_dir: A string.

        :param log_level: The log level to set.
        :type log_level: A string that defaults to info.

        :param log_file: The location to use for the log file
        :type log_file: A string or None.
        """
        self.working_dir = working_dir
        self.dry = dry
        self.debug = debug
        self.config = config

    def remove_part_from_multiple_episodes(self, show_name):
        """
        In episode titles of multiple part episodes that use the format
        (Part n) remove the 'Part ' section so the format is (n).

        :param show_name: The show name to sanitise.
        :type show_name: A string.

        :returns: The show name with sanitised multi-episode section.
        :rtype: A string.
        """
        log.debug('Removing Part from episode name')
        return show_name.replace('(Part ', '(')

    def extract_details_from_file(self, fn, user_regex=None):
        """
        Looks at the file given and extracts from it the show title, it's
        season number and episode number using regular expression magic.
        The default formats accepted are: series.0x00.xxx or series.s0e00.xxx
        A user can specify their own regular expression for a format not
        already covered.

        :param fn: The file name passed in.
        :type fn: String.

        :param user_regex: A user specified regular expression.
        :type user_regex: A string or None.

        :raises UnexpectedFormatException: Raised if the file is in an
        unexpected format.

        :returns: The show name, season number, episode number and last four
        characters (assumed to be the extension) extracted from the file
        passed in.
        :rtype: A dictionary with the keys 'show', 'season', 'episode' and
        'extension'.
        """
        fn = fn.replace("_", ".").replace(" ", ".")
        log.log(22, 'Renaming: %s' % fn)
        regex = self.__build_regex(user_regex)
        log.debug('Renaming using: ' + regex)
        m = re.compile(regex).match(fn)
        if m is not None:
            show = m.group('show').replace('.', ' ').strip()
            ext = os.path.splitext(fn)[1]
            details = (show, m.group('season'), m.group('episode'), ext)
            log.debug('Returned show: %s, season: %s, episode: %s, extension: %s' % details)
            return details
        else:
            raise UnexpectedFormatException(fn)

    def retrieve_episode_name(self, episode, library='thetvdb', canonical=None):
        """
        Retrieves the name of a given episode. The series name, season and
        episode numbers must be specified to get the episode's name. The
        library specified by the user will be used first but will fall back
        to the other library if an error occurs.

        The first library defaults to The Tv DB.

        :param the:
        :param library: The library to search.

        :returns: The episode title.
        :rtype: A string.
        """
        libraries = [
            TheTvDb,
            TvRage
        ]
        [libraries.insert(0, libraries.pop(libraries.index(lib)))
        for lib in libraries if lib.__name__.lower() == library]

        if canonical:
            episode.show_name = canonical
        else:
            episode.show_name = self.config.get_canonical(episode.show_name)
        log.debug('Show Name: %s' % episode.show_name)

        # loop the libraries until one works
        for lib in libraries:
            try:
                log.debug('Using %s' % lib.__name__)
                self.library = lib(episode.show_name, episode.season, episode.episode)
                break # first library worked - nothing to see here
            except (EmptyEpisodeNameException, EpisodeNotFoundException,
                    NoNetworkConnectionException, ShowNotFoundException,
                    XMLEmptyException):
                if lib == libraries[-1]:
                    raise NoMoreLibrariesException
                continue

        self.title = self.library.title
        log.info('Episode: %s' % self.title)

        return self.title

    def format_show_name(self, show_name, the=None, override=None):
        if the is None:
            the = self.config.get(show_name, 'the')

        try:
            show_name = self.config.get_output(show_name)
            log.debug('Using config output name: %s' % show_name)
        except ShowNotInConfigException:
            show_name = self.library.show
            log.debug('Using the formatted show name retrieved by the library:'
                        ' %s' % show_name)

        if override is not None:
            show_name = override
            log.debug('Overrode show name with: %s' % show_name)

        if the is True:
            show_name = self.__move_leading_the_to_trailing_the(show_name)

        log.debug('Final show name: %s' % show_name)

        return show_name

    def build_path(self, episode, rename_dir=None, organise=None, format=None):
        """
        Build the full destination path and filename of the renamed file Set
        the output format for the file name of a renamed show.
        By default the format is:

        Show Name - Season NumberEpisode Number - Episode Title.format.

        Builds the new path for the file to be renamed to, by default this is
        the working directory. Users can specify a directory to move files to
        once renamed using the renamed_dir option. The auto_move option can be
        used to specify a top level directory where files will be placed in
        season and show folders, i.e. Show/Season 1/episodes

        :param kwargs
        :param format: The output format of the show name, season and episode
        numbers, episode title and extension in the renamed file's name.
        :param renamed_dir: The directory to place the renamed file into.
        :param organise: A boolean to set whether the renamed directory path
        should be constructed from the show name and season number.

        :returns: The full path to the new file including the formatted file
        name.
        :rtype: A string.
        """
        episode.show_name = self.__clean_names(episode.show_name)
        episode.title = self.__clean_names(episode.title, '/',)
        if len(episode.episode) == 1:
            episode.episode = '0' + episode.episode

        if format is None:
            format = self.config.get(episode.show_name, 'format') or '%n - %s%e - %t%x'
        if '%x' not in format:
            format = format + '%x'
        format = format.replace('%n', episode.show_name)\
                        .replace('%s', str(int(episode.season)))\
                        .replace('%e', episode.episode)\
                        .replace('%t', self.__clean_names(episode.title))\
                        .replace('%x', episode.extension)

        if rename_dir is None:
            rename_dir = self.config.get(episode.show_name, 'renamed')
        if rename_dir is False:
            rename_dir = self.working_dir

        if organise is None:
            organise = self.config.get(episode.show_name, 'organise')

        if organise is True:
            rename_dir = self.__build_organise_path(rename_dir, \
                                    episode.show_name, episode.season)

        log.log(22, 'Directory: %s' % rename_dir)
        path = os.path.join(rename_dir, format)
        log.debug('Full path: %s' % path)
        return path

    def rename(self, current_filepath, destination_filepath):
        """
        Renames the file passed in to the new filename path passed in and
        returns the new filename

        :param fn: The file to rename.
        :param new_fn: The name to rename the file to.

        :raises EpisodeAlreadyExistsInDirectoryException: Raised when the
        destination file already
        exists in chosen directory.
        """
        if not os.path.exists(destination_filepath):
            log.debug(os.path.join(self.working_dir, current_filepath))
            log.debug(destination_filepath)
            if not self.dry and not self.debug:
                os.rename(os.path.join(self.working_dir, current_filepath), \
                            destination_filepath)
            destination_file = os.path.split(destination_filepath)[1]
            log.log(26, 'Renamed: \"%s\"' % destination_file)
        else:
            raise EpisodeAlreadyExistsInDirectoryException(destination_filepath)

    def __build_organise_path(self, start_path, show_name, season_number):
        """
        Constructs a directory path using the show name and season number of
        an episode.

        :param start_path: The root path to construct the new path under.
        :param show_name: The show name.
        :param season_number: The season number.

        :return: The path to move a renamed episode to.
        :rtype: A string.
        """
        if start_path[-1:] != '/':
            start_path = start_path + '/'
        path = start_path + show_name + '/Season ' + str(int(season_number)) + '/'
        if not os.path.exists(path) and not self.dry and not self.debug:
            os.makedirs(path)
            log.debug('Directories created for path: ' + path)
        return path

    def __build_regex(self, regex=None):
        """
        Builds the regular expression to extract a files details. Custom syntax
        can be used in the regular expression to help specify parts of the
        episode's file name. These custom syntax snippets are replaced by the
        regular expression blocks show.

        %n - [\w\s.,_-]+ - The show name.
        %s - [\d]{1,2} - The season number.
        %e - [\d]{2} - The episode number.

        :param regex: The regular expression string.

        :returns: An actual regular expression.
        :rtype: A string.
        """
        series = r"(?P<show>[\w\s.',_-]+?)"
        season = r"(?P<season>[\d]{1,2})"
        episode = r"(?P<episode>[\d]{2})"

        if regex is None:
            return series + r"\.[Ss]?" + season + r"[XxEe]?" + episode + r"\.|-"
        if regex.find('%s') is -1 or regex.find('%e') is -1:
            raise IncorrectCustomRegularExpressionSyntaxException(regex)

        # series name
        regex = regex.replace('%n', series)

        # season number
        # %s{n}
        if regex.find('%s{') is not -1:
            log.debug('Season digit number found')
            r = regex.split('%s{')[1][:1]
            log.debug('Specified ' + r + ' season digits')
            s = season.replace('1,2', r)
            regex = regex.replace('%s{' + r + '}', s)
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
            log.debug('User specified' + r + ' episode digits')
            e = episode.replace('2', r)
            regex = regex.replace('%e{' + r + '}', e)
            log.debug('Episode regex set: %s' % e)

        # %e
        if regex.find('%e') is not -1:
            regex = regex.replace('%e', episode)
            log.debug('Default episode regex set: %s' % regex)

        return regex

    def __clean_names(self, filename, before=':', after=','):
        """
        Cleans the string passed in, making it be safe for all file systems.
        Also allows the user to specify the new characters to be used.

        :param fn: The string to replace characters in.
        :type fn: A string.

        :param original: The character to replace.
        :type original: A string that defaults to a colon ':'.

        :param after: The replacement character.
        :type after: A string that defaults to a comma ','.

        :returns: The file
        :rtype: A string.
        """
        return filename.replace(before, after)

    def __move_leading_the_to_trailing_the(self, show_name):
        """
        Moves the leading 'The' of a show name to a trailing 'The'.
        A comma and space are added before the new 'The'.

        :param show_name: The show name.
        :type show_name: A string.

        :raises NoLeadingTheException: Raised when a show name doesn't have a
        leading The.

        :returns: The new show name.
        :rtype: A string.
        """
        if not(show_name.startswith('The ')):
            return show_name
        log.debug('Moving leading \'The\' to end of: ' + show_name)
        return show_name[4:] + ', The'


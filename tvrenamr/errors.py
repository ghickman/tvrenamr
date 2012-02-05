import logging

log = logging.getLogger('Error')

error = 'Alert: '


class AlreadyNamedException(Exception):
    """
    Raised when the format of the file being passed in is the same as the
    output format

    :param fn: The file that is already in the correct naming format.
    """

    def __init__(self, fn):
        log.error('Already in correct naming format: %s' % fn)


class ConfigNotFoundException(Exception):
    """
    Exception that is raised when a file with the same name as the renamed file
    exists in the destination folder

    :param fn: The destination file name.
    :param dest: The destination directory.
    """

    def __init__(self):
        log.error('A config could not be found. Please place one in either '
                    '~/.tvrenamr/config.yml or the tvrenamr root directory. '
                    'An example config: http://gist.github.com/586062')


class EmptyEpisodeNameException(Exception):
    """
    Raised when the episode XML document is returned but the name field is empty

    This is usually seen when a season is new enough that the episode names
    aren't fully known
    """

    def __init__(self, library):
        log.error('The episode name was not found. The record on %s is likely '
                    'incomplete.' % library)


class EpisodeAlreadyExistsInDirectoryException(Exception):
    """
    Exception that is raised when a file with the same name as the renamed file
    exists in the destination folder

    :param fn: The destination file name.
    :param dest: The destination directory.
    """

    def __init__(self, destination_path):
        log.error('File already exists: %s' % destination_path)


class EpisodeNotFoundException(Exception):
    """
    Exception raised when an episode cannot be found in the database of
    whichever library was used.

    :param library: The library where the episode could't be found.
    :param show: The show name that was searched for.
    :param season: The season number that was searched for.
    :param episode: The episode number that was searched for.
    """

    def __init__(self, library, show, season, episode):
        log.error('"%s - %s%s" could not be found on %s' % (show, season, episode, library))


class IncorrectCustomRegularExpressionSyntaxException(Exception):
    """
    The syntax used in a custom regular expression was incorrect.

    :param regex: The regular expression.
    """

    def __init__(self, regex):
        log.error('The regular expression provided does not contain the '
                    'required custom syntax.')


class NoMoreLibrariesException(Exception):
    """
    All libraries have returned invalid XML.
    """

    def __init__(self):
        log.error('No libraries left to fall back to. Exiting...')


class OutputFormatMissingSyntaxException(Exception):
    """
    The output format string is missing syntax.

    :param syntax: The syntax string required.
    """

    def __init__(self, syntax):
        if len(syntax) > 1:
            t = ', '
            errors = t.join(syntax)
        else:
            errors = syntax[0]
        log.error('The output format is missing the following format elements: '
                    '%s' % errors)


class SeriesIdNotFoundException(Exception):
    """
    SUPERFLOUOUS!

    :param library:
    :param show: The show name searched for.
    """

    def __init__(self, library, show):
        log.error('Id could not be found for \'%s\' while searching %s' % \
                    (show, library))


class ShowNotFoundException(Exception):
    """
    Raised when a show cannot be found by the specified library.

    :param library: The library that was searched.
    :param show: The show name searched for.
    """

    def __init__(self, library, show):
        log.error('\'%s\' could not be found on %s' % (show, library))


class ShowNotInConfigException(Exception):
    """
    The specified show wasn't found in the exceptions list

    :param show: The show name not found.
    """

    def __init__(self, show):
        log.debug('\'%s\' is not in the Config. Falling back on name extracted from'
                    ' the filename' % show)


class ShowNotInExceptionsList(Exception):
    """
    The specified show wasn't found in the exceptions list

    :param show: The show name not found.
    """

    def __init__(self, show):
        log.warning('%s is not in the Exceptions list' % show)


class NoLeadingTheException(Exception):
    """
    Raised when the file passed in has no leading The in the show name

    :param show: The show name with no leading The.
    """

    def __init__(self, show):
        log.warning('%s has no leading The' % show)


class NoNetworkConnectionException(Exception):
    """
    Raised when no connection to the desired library is detected
    This will be raised if either the library or the internet connection itself
    is down
    """

    def __init__(self, library):
        log.error('%sTV Renamr could not connect to %s. Please check your '
                    'internet connection and try again.' % (error, library))


class UnexpectedFormatException(Exception):
    """
    Raised when the file passed in is in an unexpected format

    :param fn: The file name that was in an unexpected format.
    """

    def __init__(self, fn):
        log.error('File in an unexpected format: %s' % fn)


class XMLEmptyException(Exception):
    """
    Raised when the XML document retrieved from a library is empty.

    :param library: The library the exception was raised in.
    :param show: The show name.
    """

    def __init__(self, library, show):
        log.error('The XML file retrieved from %s was empty while looking for '
                    '%s.' % (library, show))

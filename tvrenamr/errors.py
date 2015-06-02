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
        log.error('Already in correct naming format: {0}'.format(fn))


class EmptyEpisodeTitleException(Exception):
    """
    Raised when the episode XML document is returned but the name field is empty

    This is usually seen when a season is new enough that the episode names
    aren't fully known
    """
    def __init__(self, library):
        log.error('The episode name was not found. The record on {0} is likely '
                  'incomplete.'.format(library))


class EpisodeAlreadyExistsInDirectoryException(Exception):
    """
    Exception that is raised when a file with the same name as the renamed file
    exists in the destination folder

    :param fn: The destination file name.
    :param dest: The destination directory.
    """
    def __init__(self, destination_path):
        log.error('File already exists: {0}'.format(destination_path))


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
        args = (show, season, episode, library)
        log.error('"{0} - {1}{2}" could not be found on {3}'.format(*args))


class IncorrectCustomRegularExpressionSyntaxException(Exception):
    """
    The syntax used in a custom regular expression was incorrect.

    :param regex: The regular expression.
    """
    def __init__(self, regex):
        log.error('The regular expression provided does not contain the '
                  'required custom syntax.')


class InvalidXMLException(Exception):
    """
    Raised when the XML document retrieved from a library is empty.

    :param library: The library the exception was raised in.
    :param show: The show name.
    """
    def __init__(self, library, show):
        log.error('The XML file retrieved from {0} was empty or invalid while '
                  'looking for {1}.'.format(library, show))
        log.error('This could be indicative of a Show or Episode not being found.')


class MissingInformationException(Exception):
    """
    Not enough information to rename a file
    """
    def __init__(self, err):
        log.error('{0} is required to rename files.'.format(err))


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
                  '{0}'.format(errors))


class ShowNotFoundException(Exception):
    """
    Raised when a show cannot be found by the specified library.

    :param library: The library that was searched.
    :param show: The show name searched for.
    """
    def __init__(self, library, show):
        log.error('"{0}" could not be found on {1}'.format(show, library))


class ShowNotInExceptionsList(Exception):
    """
    The specified show wasn't found in the exceptions list

    :param show: The show name not found.
    """
    def __init__(self, show):
        log.warning('{0} is not in the Exceptions list'.format(show))


class NoLeadingTheException(Exception):
    """
    Raised when the file passed in has no leading The in the show name

    :param show: The show name with no leading The.
    """
    def __init__(self, show):
        log.warning('{0} has no leading The'.format(show))


class NoNetworkConnectionException(Exception):
    """
    Raised when no connection to the desired library is detected

    This will be raised if either the library or the internet connection itself
    is down.
    """
    def __init__(self, library):
        log.error('{0}TV Renamr could not connect to {1}. Please check your '
                  'internet connection and try again.'.format(error, library))


class UnexpectedFormatException(Exception):
    """
    Raised when the file passed in is in an unexpected format

    :param fn: The file name that was in an unexpected format.
    """
    def __init__(self, fn):
        log.error('File in an unexpected format: {0}'.format(fn))

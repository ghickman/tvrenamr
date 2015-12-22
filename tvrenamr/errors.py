import logging


log = logging.getLogger('Error')


error = 'Alert: '


class EmptyEpisodeTitleException(Exception):
    """
    Raised when the episode XML document is returned but the name field is empty

    This is usually seen when a season is new enough that the episode names
    aren't fully known
    """
    def __init__(self, library):
        msg = 'The episode name was not found. The record on %s is likely incomplete.'
        log.error(msg, library)


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
        msg = '"%s - %s%s" could not be found on %s'
        log.error(msg, show, season, episode, library)


class IncorrectRegExpException(Exception):
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
        msg = 'The XML file retrieved from %s was empty or invalid while looking for %s.'
        log.error(msg, library, show)
        log.error('This could be indicative of a Show or Episode not being found.')


class MissingInformationException(Exception):
    """
    Not enough information to rename a file
    """
    def __init__(self, err):
        log.error('%s is required to rename files.', err)


class NetworkException(Exception):
    """
    Raised when no connection to the desired library is detected

    This will be raised if either the library or the internet connection itself
    is down.
    """
    def __init__(self, library):
        msg = '%sTV Renamr could not connect to %s. Please check your internet connection and try again.'
        log.error(msg, error, library)


class OutputFormatMissingSyntaxException(Exception):
    """
    The output format string is missing syntax.

    :param syntax: The syntax string required.
    """
    def __init__(self, syntax):
        errors = ', '.join(syntax)
        msg = 'The output format is missing the following format elements: %s'
        log.error(msg, errors)


class PathExistsException(Exception):
    """
    Exception that is raised when a file with the same name as the renamed file
    exists in the destination folder

    :param fn: The destination file name.
    :param dest: The destination directory.
    """
    def __init__(self, destination_path):
        log.error('File already exists: %s', destination_path)


class ShowNotFoundException(Exception):
    """
    Raised when a show cannot be found by the specified library.

    :param library: The library that was searched.
    :param show: The show name searched for.
    """
    def __init__(self, library, show):
        log.error('"%s" could not be found on %s', show, library)


class ShowNotInExceptionsList(Exception):
    """
    The specified show wasn't found in the exceptions list

    :param show: The show name not found.
    """
    def __init__(self, show):
        log.warning('%s is not in the Exceptions list', show)


class UnexpectedFormatException(Exception):
    """
    Raised when the file passed in is in an unexpected format

    :param fn: The file name that was in an unexpected format.
    """
    def __init__(self, fn):
        log.error('File in an unexpected format: %s', fn)

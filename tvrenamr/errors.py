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
        log.error('A config could not be found. Please place one in \
                    ~/.tvrenamr/config.yml or specify a location')


class EpisodeAlreadyExistsInDirectoryException(Exception):
    """
    Exception that is raised when a file with the same name as the renamed file
    exists in the destination folder

    :param fn: The destination file name.
    :param dest: The destination directory.
    """

    def __init__(self, destination_path):
        import os
        path, filename = os.path.split(destination_path)
        log.error('\'%s\' already exists in: %s' % (filename, path))


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
        log.error('%s - %s%s could not be found on %s' % \
                    (show, season, episode, library))


class IncorrectCustomRegularExpressionSyntaxException(Exception):
    """
    The syntax used in a custom regular expression was incorrect.

    :param regex: The regular expression.
    """

    def __init__(self, regex):
        log.error('The regular expression provided does not contain the \
                    required custom syntax.')


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
        log.error('The output format is missing the following format elements:\
                    %s' % errors)


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
        log.error('%s could not be found on %s' % (show, library))


class ShowNotInConfigException(Exception):
    """
    The specified show wasn't found in the exceptions list

    :param show: The show name not found.
    """

    def __init__(self, show):
        log.debug('%s is not in the Config - falling back on name extracted \
                    from the file' % show)


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
        log.error('%sTV Renamr could not connect to %s. Please check your \
                    internet connection and try again.' % (error, library))


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
        log.error('The XML file retrieved from %s was empty while looking for\
                    %s.' % (library, show))

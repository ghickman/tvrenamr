import logging

log = logging.getLogger('Error')

class AlreadyNamedException(Exception):
    """Raised when the format of the file being passed in is the same as the output format"""
    def __init__(self, fn):
        log.error('Already in correct naming format: %s' % fn)

class EpisodeAlreadyExistsInFolderException(Exception):
    """Exception that is raised when a file with the same name as the renamed file exists in the destination folder"""
    def __init__(self, fn, dest):
        log.error('\'%s\' already exists in: %s' % (fn, dest))
    
class EpisodeNotFoundException(Exception):
    """Exception raised when an episode cannot be found in the database of whichever library was used"""
    def __init__(self, library, series, season, episode):
        log.error('%s - %s%s could not be found on %s' % (series, season, episode, library))

class IncorrectCustomRegularExpressionSyntaxException(Exception):
    """"""
    def __init__(self, regex):
        log.error('The regular expression provided does not contain the required custom syntax.')

class OutputFormatMissingSyntaxException(Exception):
    """"""
    def __init__(self,syntax):
        if len(syntax) > 1:
            t = ', '
            errors = t.join(syntax)
        else: errors = syntax[0]
        log.error('The output format is missing the following format elements: %s' % errors)

class SeriesIdNotFoundException(Exception):
    """"""
    def __init__(self,show):
        log.error('Id could not be found for: %s'%show)

class ShowNotFoundException(Exception):
    """"""
    def __init__(self,show):
        log.error('%s could not be found' % show)

class ShowNotInExceptionsList(Exception):
    """The specified show wasn't found in the exceptions list"""
    def __init__(self,show):
        log.warning('%s is not in the Exceptions list' % show)

class NoLeadingTheException(Exception):
    """"""
    def __init__(self,show=None):
        if show is not None: log.error('%s has no leading the' % show)
        else: log.warning('No leading the found')

class UnexpectedFormatException(Exception):
    """"""
    def __init__(self,fn):
        log.error('File in an unexpected format: %s' % fn)

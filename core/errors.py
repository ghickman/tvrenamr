import logging

log = logging.getLogger('Error')

class AlreadyNamedException(Exception):
    """Raised when the format of the file being passed in is the same as the output format"""
    def __init__(self, fn):
        log.error('Already in correct naming format: %s' % fn)

class EpisodeAlreadyExistsInFolderException(Exception):
    """
    """
    def __init__(self,fn,new_fn):
        msg = "This episode already exists in the specified destination: %s" %new_fn
        log.error(msg)
        print msg
    
class EpisodeNotFoundException(Exception):
    """
    """
    def __init__(self,series,season,episode):
        log.error('%s - %s%s could not be found' % (series, season, episode))

class IncorrectCustomRegularExpressionSyntaxException(Exception):
    def __init__(self,string):
        msg = 'The regular expression provided does not contain the required custom syntax.'
        log.error(msg)
        print msg

class OutputFormatMissingSyntaxException(Exception):
    def __init__(self,syntax):
        if len(syntax) > 1:
            t = ', '
            errors = t.join(syntax)
        else: errors = syntax[0]
        msg = 'The output format is missing the following format elements: '+errors
        log.error(msg)
        print msg

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
        log.debug('%s is not in the Exceptions list' % show)

class NoLeadingTheException(Exception):
    """"""
    def __init__(self,show=None):
        if show is not None: log.error('%s has no leading the' % show)
        else: log.warning('No leading the found')

class UnexpectedFormatException(Exception):
    """
    """
    def __init__(self,fn):
        msg = "The file was in an unexpected format: "+fn
        log.error(msg)
        print msg

import logging

log = logging.getLogger('Lib Package')

"""
import the errors module - this feels like a horrible way to do it but it's
the only way I could make it work currently.
"""

try:
    # when installed as a package
    log.debug('Attempting to import errors from tvrenamr package')
    from tvrenamr.errors import EmptyEpisodeNameException, \
                                EpisodeNotFoundException, \
                                NoNetworkConnectionException, \
                                ShowNotFoundException, \
                                XMLEmptyException
except ImportError:
    # when run locally
    log.debug('Failed to import errors from package, falling back to relative \
                import')
    from . errors import EmptyEpisodeNameException, \
                            EpisodeNotFoundException, \
                            NoNetworkConnectionException, \
                            ShowNotFoundException, \
                            XMLEmptyException

log.debug('Errors imported successfully')

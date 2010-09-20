import logging

log = logging.getLogger('Lib Package')

# import errors modules - this is horrible but the only way it will work currently.
try:
    # when installed as a package
    log.debug('Attempting to import errors from tvrenamr package')
    from tvrenamr.errors import EpisodeNotFoundException, NoNetworkConnectionException, ShowNotFoundException, XMLEmptyException
except ImportError:
    # when run locally
    log.debug('Failed to import errors from package, falling back to relative import')
    from . errors import EpisodeNotFoundException, NoNetworkConnectionException, ShowNotFoundException, XMLEmptyException
log.debug('Errors imported successfully')
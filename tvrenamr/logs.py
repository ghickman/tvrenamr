import logging
import logging.handlers
import os


def convert_log_level(level=26):
    """
    Get a numeric log level from a string. The default 26 is for SHORT logs.

    :param level
    :return level
    """
    # annoying but the level can be passed in as None
    if not level:
        level = 26

    levels = {'notset': 0, 'debug': 10, 'info': 20, 'minimal': 22,
              'short': 26, 'warning': 30, 'error': 40, 'critical': 50}

    if isinstance(level, str):
        level = levels.get(level)

    return level


def get_log_file(filename=None):
    # make sure the log directory exists and place the log file there
    if filename is None:
        filename = os.path.join(
            os.path.expanduser('~'),
            '.tvrenamr',
            'tvrenamr.log'
        )
    filename = filename.replace('~', os.path.expanduser('~'))
    try:
        os.makedirs(os.path.split(filename)[0])
    except OSError:
        pass

    return filename


def start_logging(filename, log_level, quiet=False):
    """
    Setup the file logging and start the root logger
    """
    filename = get_log_file(filename)
    log_level = convert_log_level(log_level)

    # add the custom levels
    logging.addLevelName(22, 'MINIMAL')
    logging.addLevelName(26, 'SHORT')

    # setup log file
    file_format = '%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s'
    handler = logging.handlers.RotatingFileHandler(filename, maxBytes=1048576, backupCount=10)
    handler.setFormatter(logging.Formatter(file_format, '%Y-%m-%dT%H:%M'))
    logging.getLogger().addHandler(handler)

    logging.getLogger().setLevel(logging.DEBUG)

    if not quiet:
        # setup the console logs to debug
        # debug
        if log_level is 10:
            console_format = '%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s'
            console_datefmt = '%Y-%m-%d %H:%M'
        else:
            console_format = '%(message)s'
            console_datefmt = ''

        console_formatter = logging.Formatter(console_format, console_datefmt)

        # define a Handler with the given level and outputs to the console
        console = logging.StreamHandler()
        console.setLevel(log_level)

        # set the console format & attach the handler to the root logger with it.
        console.setFormatter(console_formatter)
        logging.getLogger().addHandler(console)

import logging

from lib.log_utils import *

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
    logging.basicConfig(level = logging.DEBUG,
                        format = file_format,
                        datefmt = '%m-%d %H:%M',
                        filename = filename,
                        filemode = 'w')

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

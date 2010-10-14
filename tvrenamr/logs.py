import os
import sys
import logging
import logging.handlers


def start_logging(filename=None, debug=False, quiet=False, log_level=26):
    # make sure the log directory exists and place the log file there
    if filename == None:
        filename = os.path.join(os.path.expanduser('~'), \
                                    '.tvrenamr', 'tvrenamr.log')
    filename = filename.replace('~', os.path.expanduser('~'))
    try:
        os.makedirs(os.path.split(filename)[0])
    except OSError:
        pass

    # add the custom levels
    logging.addLevelName(22, 'MINIMAL')
    logging.addLevelName(26, 'SHORT')

    # set defaults
    console_format = '%(message)s'
    console_datefmt = ''
    file_format = '%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s'
    level = log_level

    # set the level and format for debug mode
    if debug:
        console_format = '%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s'
        console_datefmt = '%Y-%m-%d %H:%M'

    console_formatter = logging.Formatter(console_format, console_datefmt)

    # set up logging to file - see previous section for more details
    logging.basicConfig(level = logging.DEBUG,
                        format = file_format,
                        datefmt = '%m-%d %H:%M',
                        filename = filename,
                        filemode = 'w')

    # define a Handler with the given level and outputs to the console
    console = logging.StreamHandler()
    console.setLevel(level)

    # set the console format and attach the handler to the root logger with it.
    console.setFormatter(console_formatter)
    logging.getLogger().addHandler(console)

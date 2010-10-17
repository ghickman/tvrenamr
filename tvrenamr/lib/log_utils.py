import os
import os.path

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
    if filename == None:
        filename = os.path.join(os.path.expanduser('~'), \
                                    '.tvrenamr', 'tvrenamr.log')
    filename = filename.replace('~', os.path.expanduser('~'))
    try:
        os.makedirs(os.path.split(filename)[0])
    except OSError:
        pass

    return filename

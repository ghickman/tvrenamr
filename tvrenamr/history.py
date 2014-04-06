import functools
import logging
import os
import pydoc
import sys

from .logs import get_log_file


log = logging.getLogger('tvrenamr.history')


def parse_history(log_file_location):
    log_file = get_log_file(log_file_location)

    if not os.path.getsize(log_file):
        log.critical('No log file found, exiting.')
        sys.exit(1)

    with open(log_file, 'r') as f:
        logs = f.readlines()

    shows = list(filter(lambda x: 'Renamed:' in x, logs))

    def show_len(show):
        return len(show.split('Renamed: ')[1].split(' - ')[0]) - 1

    longest = max(map(show_len, shows))

    def sanitise_log(log, longest):
        dt, name = log.split('Renamed: ')
        dt = dt.split(' ')[0].replace('T', ' ')
        show, number, title = name.split(' - ')
        name = (name.replace(show, show.lstrip('"').strip().ljust(longest), 1)
                    .replace(number, number.ljust(4), 1)
                    .replace(' - ', ' | '))
        return '{0} | {1}'.format(dt, name.rstrip('"\n'))

    sanitise = functools.partial(sanitise_log, longest=longest)

    shows = map(sanitise, shows)
    return pydoc.pager('\n'.join(shows))

import os
import sys

from tvrenamr.config import Config


def build_file_list(paths, recursive=False, ignore_filelist=()):
    """Finds files from a list of paths"""
    for path in paths:
        if os.path.isfile(path):
            yield os.path.split(path)

        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fname in files:
                    path = os.path.join(root, fname)
                    if path not in ignore_filelist:
                        yield os.path.split(path)

                if not recursive:
                    break


def get_config(path=None):
    """Get the first viable config from the list of possiblities"""
    def exists(x):
        return x is not None and os.path.exists(x)

    possible_configs = iter(filter(exists, (
        path,
        os.path.join(sys.path[0], 'config.yml'),
        os.path.expanduser('~/.tvrenamr/config.yml'),
    )))

    location = next(possible_configs, None)

    return Config(location)


def sanitise_log(log, longest):
    dt, name = log.split('Renamed: ')
    dt = dt.split(' ')[0].replace('T', ' ')
    show, number, _ = name.split(' - ')
    name = (name.replace(show, show.lstrip('"').strip().ljust(longest), 1)
                .replace(number, number.ljust(4), 1)
                .replace(' - ', ' | '))
    return '{} | {}'.format(dt, name.rstrip('"\n'))


def start_dry_run(logger):
    logger('Dry Run beginning.')
    logger('-' * 70)
    logger('')


def stop_dry_run(logger):
    logger('')
    logger('-' * 70)
    logger('Dry Run complete. No files were harmed in the process.')
    logger('')

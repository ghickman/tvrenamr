import logging
import sys

import yaml

from .errors import ShowNotInConfigException


class Config(object):

    def __init__(self, config):
        self.log = logging.getLogger('Config')

        self.config = self._load_config(config)

        self.log.debug('Config loaded')

        self.defaults = self._get_defaults()
        self.log.debug('Defaults retrieved')

    def exists(self, show):
        if show in self.config:
            return True
        else:
            return False

    def get(self, show, option, default=None):
        try:
            return self.config[show][option]
        except KeyError:
            try:
                return self.defaults[option]
            except KeyError:
                return default

    def get_canonical(self, show):
        try:
            return self.config[show]['canonical']
        except KeyError:
            try:
                return self.config[show.lower()]['canonical']
            except KeyError:
                self.log.debug('No canonical defined, returning: {0}'.format(show))
                return show

    def _get_defaults(self):
        if 'defaults' in self.config:
            return self.config['defaults']
        else:
            message = """
            The defaults section of your config is missing.

            For an example see: https://gist.github.com/586062
            """
            raise NameError(message)

    def get_output(self, show):
        try:
            return self.config[show.lower()]['output']
        except KeyError:
            try:
                return self.config[show.lower()]['canonical']
            except KeyError:
                raise ShowNotInConfigException(show)

    def _load_config(self, config):
        try:
            with open(config, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.log.critical(e)
            print('')
            print('-' * 79)
            print(' Malformed configuration file, common reasons:')
            print('-' * 79)
            print('')
            print(' o Indentation error')
            print(' o Missing : from end of the line')
            print(' o Non ASCII characters (use UTF8)')
            print(" o If text contains any of :[]{}% characters it must be single-quoted ('')\n")
            lines = 0
            if hasattr(e, 'problem') and e.problem is not None:
                print(' Reason: {0}\n'.format(e.problem))
                if e.problem == 'mapping values are not allowed here':
                    print(' ----> MOST LIKELY REASON: Missing : from end of the line!')
                    print('')
            if hasattr(e, 'context_mark') and e.context_mark is not None:
                args = (e.context_mark.line, e.context_mark.column)
                print(' Check configuration near line {0}, column {1}'.format(*args))
                lines += 1
            if hasattr(e, 'problem_mark') and e.problem_mark is not None:
                args = (e.problem_mark.line, e.problem_mark.column)
                print(' Check configuration near line {0}, column {1}'.format(*args))
                lines += 1
            if lines:
                print('')
            if lines == 1:
                print(' Fault is almost always in this or previous line\n')
            if lines == 2:
                print(' Fault is almost always in one of these lines or previous ones\n')
            sys.exit(1)

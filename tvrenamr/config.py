from logging import getLogger
from sys import exit

from yaml import safe_load

from errors import ShowNotInConfigException


error = """

------------------------------------------------------------------------------
Malformed configuration file, common reasons:'
------------------------------------------------------------------------------

o Indentation error'
o Missing : from end of the line'
o Non ASCII characters (use UTF8)'
o If text contains any of :[]{}% characters it must be single-quoted ('')"

"""


class Config():

    def __init__(self, config):
        self.log = getLogger('Config')

        self.config = self._load_config(config)

        self.log.debug('Config loaded')

        self.defaults = self._get_defaults()
        self.log.debug('Defaults retrieved')

    def exists(self, show):
        if show in self.config:
            return True
        else:
            return False

    def get(self, show, option):
        try:
            return self.config[show][option]
        except KeyError:
            try:
                return self.defaults[option]
            except KeyError:
                return False

    def get_canonical(self, show):
        try:
            return self.config[show]['canonical']
        except KeyError:
            try:
                return self.config[show.lower()]['canonical']
            except KeyError:
                self.log.debug('No canonical defined, returning: %s' % show)
                return show

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
            return safe_load(file(config))
        except Exception as e:
            self.log.critical(e)
            self.log.critical(error)
            lines = 0
            if e.problem is not None:
                self.log.critical('Reason: {0}'.format(e.problem))
                if e.problem == 'mapping values are not allowed here':
                    self.log.critical('----> MOST LIKELY REASON: Missing `:` from end of the line!')
            if e.context_mark is not None:
                self.log.critical('Check configuration near line {0}, column {1}'.format(
                                  e.context_mark.line, e.context_mark.column))
                lines += 1
            if e.problem_mark is not None:
                self.log.critcal('Check configuration near line {0}, column {1}'.format(
                                 e.problem_mark.line, e.problem_mark.column))
                lines += 1
            if lines == 1:
                self.log.critical('Fault is almost always in this or previous line')
            if lines == 2:
                self.log.critical('Fault is almost always in one of these lines or previous ones')
            exit(1)

    def _get_defaults(self):
        if 'defaults' in self.config:
            return self.config['defaults']
        else:
            message = """
            The defaults section of your config is missing.

            For an example see: https://gist.github.com/586062
            """
            raise NameError(message)


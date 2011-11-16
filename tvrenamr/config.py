from logging import getLogger
from sys import exit

from yaml import safe_load

from errors import ShowNotInConfigException


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
        except Exception, e:
            self.log.critical(e)
            print ''
            print '-' * 79
            print ' Malformed configuration file, common reasons:'
            print '-' * 79
            print ''
            print ' o Indentation error'
            print ' o Missing : from end of the line'
            print ' o Non ASCII characters (use UTF8)'
            print " o If text contains any of :[]{}% characters it must be \
                    single-quoted ('')\n"
            lines = 0
            if e.problem is not None:
                print ' Reason: %s\n' % e.problem
                if e.problem == 'mapping values are not allowed here':
                    print ' ----> MOST LIKELY REASON: Missing : from end of \
                            the line!'
                    print ''
            if e.context_mark is not None:
                print ' Check configuration near line %s, column %s' % \
                        (e.context_mark.line, e.context_mark.column)
                lines += 1
            if e.problem_mark is not None:
                print ' Check configuration near line %s, column %s' % \
                        (e.problem_mark.line, e.problem_mark.column)
                lines += 1
            if lines:
                print ''
            if lines == 1:
                print ' Fault is almost always in this or previous line\n'
            if lines == 2:
                print ' Fault is almost always in one of these lines or \
                        previous ones\n'
            # if self.options.debug:
                # raise
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


import collections
import logging
import sys

import yaml


class Config(object):
    def __init__(self, config=None, show=None):
        self.log = logging.getLogger('tvrenamr.config')

        self.config = self._load_config(config)
        self.show = show

        self.log.debug('Config loaded')

    def get(self, key, show=None, default=None, override=None):
        """
        Get a configuration option

        This method is a convenient wrapper for asking for a config value in
        one place.

        At a higher level options are picked in this order:
         * cli
         * config
         * filename

        Internally this is handled as:
         * Override Option
           Picked first allowing a command line option to be passed in and used
           with the highest priority.

         * Show Specific Config
           The key is looked up under the show name in the yaml file. If this
           lookup fails the lowercased version of the show name is also tried.

         * Default Config
           The key is looked up in the defaults section of the yaml file.

         * Default Option
           If all the other options fail the default option passed into this
           method is returned as a last resort.
        """
        if override is not None:
            return override

        if show is None and self.show is None:
            raise Exception('You must provide a show name to use this method')

        try:
            return self.config[show][key]
        except KeyError:
            try:
                return self.config[show.lower()][key]
            except KeyError:
                try:
                    return self.config['defaults'][key]
                except KeyError:
                    return default

    def get_output(self, show, override=None):
        output = self.get(show, 'output', override=override)

        if output is None:
            output = self.get(show, 'canonical', override=override)

        return output

    def _load_config(self, config):
        if config is None:
            self.log.info('No config found, continuing with defaults.')
            return collections.defaultdict(dict)

        try:
            with open(config, 'r') as f:
                return yaml.safe_load(f)
        except yaml.error.YAMLError as e:
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
                print(' Reason: {}\n'.format(e.problem))
                if e.problem == 'mapping values are not allowed here':
                    print(' ----> MOST LIKELY REASON: Missing : from end of the line!')
                    print('')
            if hasattr(e, 'context_mark') and e.context_mark is not None:
                args = (e.context_mark.line, e.context_mark.column)
                print(' Check configuration near line {}, column {}'.format(*args))
                lines += 1
            if hasattr(e, 'problem_mark') and e.problem_mark is not None:
                args = (e.problem_mark.line, e.problem_mark.column)
                print(' Check configuration near line {}, column {}'.format(*args))
                lines += 1
            if lines:
                print('')
            if lines == 1:
                print(' Fault is almost always in this or previous line\n')
            if lines == 2:
                print(' Fault is almost always in one of these lines or previous ones\n')
            sys.exit(1)

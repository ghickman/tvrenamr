import logging
import os
import sys

import yaml

class Config():
    def __init__(self, config):
        self.config = {}
        self.defaults = {}
        
        self.__load_config(config)
        self.__get_defaults()
        
        # self.log = logging.getLogger('Config')
        # print self.config
    
                                      
    def get_deluge(self):             
        if not show in self.config: return self.defaults['deluge']
        else:                         
            try: return self.config[show]['deluge']
            except KeyError: return self.defaults['deluge']
                                      
    
    def get_format(self, show):
        if not show in self.config: return self.defaults['format']
        else:
            try: return self.config[show]['format']
            except KeyError: return self.defaults['format']
    
    def get_rename_dir(self, show):
        if not show in self.config: return self.defaults['renamed']
        else:
            try: return self.config[show]['renamed']
            except KeyError: return self.defaults['renamed']
    
    
    def get_the(self, show):
        if not show in self.config: return self.defaults['the']
        else:
            try: return self.config[show]['the']
            except KeyError: return self.defaults['the']
    
    
    def __load_config(self, config):
        try:
            self.config = yaml.safe_load(file(config))
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
            print " o If text contains any of :[]{}% characters it must be single-quoted ('')\n"
            lines = 0
            if e.problem is not None:
                print ' Reason: %s\n' % e.problem
                if e.problem == 'mapping values are not allowed here':
                    print ' ----> MOST LIKELY REASON: Missing : from end of the line!'
                    print ''
            if e.context_mark is not None:
                print ' Check configuration near line %s, column %s' % (e.context_mark.line, e.context_mark.column)
                lines += 1
            if e.problem_mark is not None:
                print ' Check configuration near line %s, column %s' % (e.problem_mark.line, e.problem_mark.column)
                lines += 1
            if lines:
                print ''
            if lines == 1:
                print ' Fault is almost always in this or previous line\n'
            if lines == 2:
                print ' Fault is almost always in one of these lines or previous ones\n'
            # if self.options.debug:
                # raise
            sys.exit(1)
    
    
    def __get_defaults(self):
        if 'defaults' in self.config: self.defaults = self.config['defaults']
    
    

conf = os.path.join(sys.path[0], 'config.yml')
# print conf
c = Config(conf)

# print c.get_rename_dir()
print c.get_the('the simpsons')
# print c.get_format()
# print c.get_deluge()
# print c.get_show_options('csi')
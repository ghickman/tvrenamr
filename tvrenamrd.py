import logging
import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CREATE, IN_MOVED_TO, IN_ISDIR
from core.core import TvRenamr
from core.errors import *
from optparse import OptionParser

class WatchFolder(ProcessEvent):
    def __init__(self):
        self.log = logging.getLogger('tvrenamr.daemon')
    
    def process_IN_MOVED_TO(self, event):
        self.log.debug('MOVED: '+event.pathname)
        if not event.name.startswith('.'):
            if event.dir:
                for each_tuple in os.walk(event.pathname):
                    for fname in each_tuple[2]:
                        self.__rename([each_tuple[0], fname])
            else: self.__rename(os.path.split(event.pathname))
    
    def process_IN_CREATE(self, event):
        self.log.debug('CREATE: '+event.pathname)
        if not event.name.startswith('.') and not event.dir: self.__rename(os.path.split(event.pathname))
    
    def __rename(self, pathname):
        tv = TvRenamr(pathname[0], 'debug')
        try:
            credentials = tv.extract_episode_details_from_file(pathname[1])
            if options.exceptions is not None: credentials['series'] = tv.convert_show_names_using_exceptions_file(options.exceptions, credentials['series'])
            title = tv.retrieve_episode_name(credentials['series'],credentials['season'],credentials['episode'])
            credentials['series'] = title['series']
            if options.the:
                try: credentials['series'] = tv.set_position_of_leading_the_to_end_of_show_name(credentials['series'])
                except NoLeadingTheException: pass
            credentials['title'] = title['title']
            path = tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], renamed_dir=options.renamed, organise=options.organise, format=options.output_format)
            tv.rename(pathname[1],path)
        except Exception, e: print e

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option('-a', '--auto', action='store_true', dest='organise', help='Automatically move renamed files to the directory specified in renamed and organise them appropriated according to their show name and season number')
    parser.add_option('-o', '--output', dest='output_format', help='Set the output format for the episodes being renamed')
    parser.add_option('-r', "--renamed", dest='renamed', help='The directory to move renamed files to, if not specified the working directory is used')
    parser.add_option('-t', '--the', action='store_true', dest='the', help='Set the position of \'The\' in a show\'s name to the end of the file')
    parser.add_option('-x', '--exceptions', dest='exceptions', help='Set the location of the exceptions file')
    (options, args) = parser.parse_args()
    if len(args) is not 1: parser.error('wrong number of arguments')
    
    # working_dir = "/opt/tvrenamr/working"
    working_dir = args[0]
    # options.renamed = "/opt/tvrenamr/TV"
    
    wm = WatchManager()
    p = WatchFolder()
    notifier = Notifier(wm, p)

    mask = IN_MOVED_TO | IN_CREATE  # watched events -> add IN_DONT_FOLLOW to not follow symlinks, and IN_CREATE to watch created files
    wdd = wm.add_watch(working_dir, mask, rec=True, auto_add=True) #watch this directory, with mask(s), recursively
    notifier.loop()#daemonize=True, pid_file='/opt/tvrenamr/tvrenamrd.pid', force_kill=True, stdout='/opt/tvrenamr/stdout.txt')
else: print 'This script is only designed to be run standalone'
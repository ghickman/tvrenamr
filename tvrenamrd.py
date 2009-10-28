import logging
import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CREATE, IN_MOVED_TO, IN_ISDIR
from core.core import TvRenamr
from tvrenamr.py import rename

working_dir = "/opt/tvrenamr/working"
renamed_dir = "/opt/tvrenamr/TV"

class WatchFolder(ProcessEvent):
    def __init__(self):
        self.log = logging.getLogger('tvrenamr.daemon')
    
    def process_IN_MOVED_TO(self, event):
        if not event.name.startswith('.') and not event.dir: self.__rename(event.name)
    
    def process_IN_CREATE(self, event):
        # print event.name
        # print event.pathname
        if not event.name.startswith('.') and not event.dir: self.__rename(os.path.split(event.pathname))
    
    def __rename(self, pathname):
        rename(pathname)
        # print pathname
        #         tv = TvRenamr(pathname[0])
        #         try:
        #             credentials = tv.extract_episode_details_from_file(pathname[1])
        #             title = tv.retrieve_episode_name(credentials['series'],credentials['season'],credentials['episode'])
        #             credentials['series'] = tv.set_position_of_leading_the_to_end_of_series_name(title['series'])
        #             credentials['title'] = title['title']
        #             print credentials
        #             path = tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], auto_move=renamed_dir)
        #             print path
        #             tv.rename(pathname[1], path)
        #         except Exception, e: print e

wm = WatchManager()
p = WatchFolder()
notifier = Notifier(wm, p)

mask = IN_MOVED_TO | IN_CREATE | IN_ISDIR  # watched events -> add IN_DONT_FOLLOW to not follow symlinks, and IN_CREATE to watch created files
wdd = wm.add_watch(working_dir, mask, rec=True, auto_add=True) #watch this directory, with mask(s), recursively
notifier.loop()#daemonize=True, pid_file='/opt/tvrenamr/tvrenamrd.pid', force_kill=True, stdout='/opt/tvrenamr/stdout.txt')
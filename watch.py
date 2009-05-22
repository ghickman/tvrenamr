from pyinotify import WatchManager, Notifier, ThreadedNotifier, ProcessEvent, IN_CREATE
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/madnashua/projects/tvrenamr/watch.log',
                    filemode='a')

wm = WatchManager()  # Watch Manager
working_dir = "/mnt/media/Sandbox"
mask = IN_CREATE  # watched events -> add IN_DONT_FOLLOW to not follow symlinks

class PTmp(ProcessEvent):
    def process_IN_CREATE(self, event):
        logging.info('Creaing: %s', event.pathname)
        #print "Creating:", event.pathname
        #rename file

p = PTmp()
notifier = Notifier(wm, p)

wdd = wm.add_watch(working_dir, mask, rec=True) #watch this directory, with this mask, recursively
notifier.loop(daemonize=True, pid_file='/tmp/pyinotify.pid', force_kill=True, stdout='/tmp/stdout.txt')
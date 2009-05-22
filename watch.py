from pyinotify import WatchManager, Notifier, ThreadedNotifier, ProcessEvent, IN_CREATE

wm = WatchManager()  # Watch Manager
working_dir = "/mnt/media/Sandbox"
mask = IN_CREATE  # watched events -> add IN_DONT_FOLLOW to not follow symlinks

class PTmp(ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname
        #rename file

p = PTmp()
notifier = Notifier(wm, p)

wdd = wm.add_watch(working_dir, mask, rec=True)
notifier.loop(daemonize=True, pid_file='/tmp/pyinotify.pid', force_kill=True, stdout='/tmp/stdout.txt')
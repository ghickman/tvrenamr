import os
import sys
import exceptions
from deluge.ui.client import client
from twisted.internet import reactor, defer
from deluge.log import setupLogger
setupLogger()

def get_deluge_ignore_file_list(cb_method, ratio, path):
    """
    Compiles a list of files using the Deluge Torrent client that should
    be ignored from the renaming process because of a given set of factors.

    :param cb_method: Use this to define a method to be called once data has been found.
    :param ratio: The minium share ratio of a torrent file before it can be accepted into the
    renaming process (i.e. not part of this list) You may set this to 0 to perform no ratio checking.
    :param path: The working directory of the script, not used here but is passed to the `cb_method`

    :returns: Nothing, however calls the `cb_method` function.
    """

    def on_connect(result):
        """
        Callback for a successful connection to Deluge.
        Several callbacks are defined here and a call to get_session_state() is made
        """
        def on_get_session_state(result):
            """
            Callback for the get_session_state() method.
            """
            # Get torrent information using the list of ID's we gained from
            # get_session_state().
            client.core.get_torrents_status({'id': result},
                ['name', 'ratio', 'is_finished', 'files', 'save_path']).addCallback(on_torrents_status)

        def on_torrents_status(result):
            """
            Callback for the torrent_status() method.
            This method contains the actual ratio checking and is_finished.

            Once the list has been compiled the method defined in `cb_method` is called.
            """
            torrent_filelist = []
            for torrent_id, status in result.items():
                # Meh, float should be fine for this. Not mission critical.
                # We're going to ignore anything that hasn't either met our
                # ratio or is not yet finished.
                if float(ratio) > float(status['ratio']) \
                    or status['is_finished'] is False:
                        for f in status['files']:
                            torrent_filelist.append(os.path.join(status['save_path'], f['path']))

            client.disconnect()
            reactor.stop()

            # Catch system exits and ignore them.
            try:
                cb_method(path, ignore_filelist=torrent_filelist)
            except exceptions.SystemExit:
                pass

        # Get a list of torrent ID's from deluge.
        client.core.get_session_state().addCallback(on_get_session_state)

    def on_connect_fail(result):
        """
        Callback method for an unsuccessful connection to Deluge.
        """
        print "Failed to connect to the Deluge daemon, sure it's running?"
        print 'Exiting...'

        client.disconnect()
        reactor.stop()
        sys.exit()

    client.connect().addCallback(on_connect).addErrback(on_connect_fail)
    reactor.run()

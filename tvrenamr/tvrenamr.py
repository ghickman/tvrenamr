#!/usr/bin/python

import os
import sys
from optparse import OptionParser, SUPPRESS_HELP

__version__ ='gash'

from errors import *
from logs import start_logging
from main import TvRenamr

log = logging.getLogger('Core')

parser = OptionParser(usage="tvr [options] <file/folder>", version="Tv Renamr 2.1.4")
# parser.add_option('--config', dest='config', help='')
parser.add_option('-c', '--canonical', dest='canonical', help='Set the show\'s canonical name to use when performing the online lookup.')
parser.add_option('--debug', action='store_true', dest='debug', help=SUPPRESS_HELP)
parser.add_option('--deluge', action='store_true', dest='deluge', help='Checks Deluge to make sure the file has been completed before renaming.')
parser.add_option('--deluge-ratio', dest='deluge_ratio', help='Checks Deluge for completed and that the file has at least reached X share ratio.')
parser.add_option('-d', '--dry-run', dest='dry', action='store_true', help='Dry run your renaming.')
parser.add_option('-e', '--episode', dest='episode', help='Set the episode number. Currently this will cause errors when working with more than one file.')
parser.add_option('--ignore-filelist', dest='ignore_filelist', help=SUPPRESS_HELP)
parser.add_option('--ignore-recursive', action='store_true', dest='ignore_recursive', help='Only use files from the root of a given directory, not entering any sub-directories.')
parser.add_option('-l', '--log_file', dest='log_file', help='Set the log file location.')
parser.add_option('--log_level', dest='log', help='Set the log level. Options: debug, info, warning, error and critical.')
parser.add_option('--library', dest='library', default='thetvdb', help='Set the library to use for retrieving episode titles. Options: thetvdb & tvrage.')
parser.add_option('-n', '--name', dest='name', help='Set the show\'s name. This will be used as the show\'s when the renaming is completed.')
# parser.add_option('--no-config', dest='no_config', action='store_true', help='Ignore the config')
parser.add_option('-o', '--output', dest='output_format', help='Set the output format for the episodes being renamed.')
parser.add_option('--organise', action='store_true', dest='organise', help='Organise renamed files into folders based on their show name and season number.')
parser.add_option('--no-organise', action='store_false', dest='organise', help='Explicitly tell Tv Renamr not to organise renamed files. Used to override the config.')
parser.add_option('-q', '--quiet', action='store_true', dest='quiet', help='Don\'t output logs to the command line')
parser.add_option('-r', '--recursive', action='store_true', dest='recursive', help='Recursively lookup files in a given directory')
parser.add_option('--rename-dir', dest='rename_dir', help='The directory to move renamed files to, if not specified the working directory is used.')
parser.add_option('--no-rename-dir', action='store_false', dest='rename_dir', help='Explicity tell Tv Renamr not to move renamed files. Used to override the config.')
parser.add_option('--regex', dest='regex', help='The regular expression to use when extracting information from files.')
parser.add_option('-s', '--season', dest='season', help='Set the season number.')
parser.add_option('-t', '--the', action='store_true', dest='the', help='Set the position of \'The\' in a show\'s name to the end of the file')
options, args = parser.parse_args()

class FrontEnd():
    def __init__(self, path):
        # start logging
        start_logging(options.log_file, options.debug, options.quiet)
        
        # determine type
        try:
            file_list = self.__determine_type(path, options.recursive, options.ignore_filelist)
        except Exception: parser.error('\'%s\' is not a file or directory. Ruh Roe!' % path)
        
        # kick off a rename for each file in the list
        for details in file_list:
            if options.dry or options.debug: self.__start_dry_run()
            self.rename(details)
            if options.dry or options.debug: self.__stop_dry_run()
    
    
    def __determine_type(self, path, recursive=False, ignore_filelist=None):
        """
        Determines which files need to be processed for renaming.
        
        :param path: The input file or directory.
        :param ignore_recursive: To ignore a recursive search for files if 'path' is a directory.
        Default is False.
        :param ignore_filelist: Optional set of files to ignore from renaming. Often used by filtering
        methods such as Deluge.
        
        :returns: A list of files to be renamed.
        :rtype: A list of dictionaries, who's keys are 'directory' and 'filename'.
        """
        if os.path.isdir(path):
            filelist = []
            for root, dirs, files in os.walk(path):
                for fname in files:
                    # If we have a file we should be ignoring and skipping it.
                    if ignore_filelist is not None and (os.path.join(root, fname) in ignore_filelist):
                        continue
                    filelist.append((root, fname))
                # Don't want a recusive walk?
                if not recursive: break
            return filelist
        elif os.path.isfile(path):
            return [os.path.split(path)]
        else:
            raise Exception
    
    
    def rename(self, details):
        working, filename = details
        tv = TvRenamr(working, options.log, options.log_file, options.debug, options.quiet, options.dry)
        try:
            credentials = tv.extract_details_from_file(filename, user_regex=options.regex)
        
            if options.season: credentials['season']=options.season
            if options.episode: credentials['episode']=options.episode
        
            credentials['title'] = tv.retrieve_episode_name(library=options.library,
                                                        canonical=options.canonical, **credentials)
            credentials['show'] = tv.format_show_name(show=credentials['show'], the=options.the,
                                                        override=options.name)
        
            path = tv.build_path(dry=options.dry, rename_dir=options.rename_dir, \
                                organise=options.organise, format=options.output_format, **credentials)
        
            tv.rename(filename,path)
        except Exception, e:
            log.critical(e)
            pass
    
    
    def __start_dry_run(self):
        log.info('Dry Run beginning.')
        log.info('-'*70)
        log.info('')
    
    
    def __stop_dry_run(self):
        log.info('')
        log.info('-'*70)
        log.info('Dry Run complete. No files were harmed in the process.')
        log.info('')
    


def run():
    try:
        # Need to capture the Deluge arguments here, before we enter rename so we can instead pass it
        # as a callback to be called once we've fetched the required information from deluge.
        if options.deluge or options.deluge_ratio:
            if options.deluge and not options.deluge_ratio: options.deluge_ratio = 0
            from lib.filter_deluge import get_deluge_ignore_file_list
            get_deluge_ignore_file_list(rename, options.deluge_ratio, args[0])
        else: FrontEnd(args[0])
    except IndexError:
        if options.debug: print 'Debug: No file or directory specified, using current directory'
        FrontEnd(os.getcwd())


if __name__=="__main__": run()
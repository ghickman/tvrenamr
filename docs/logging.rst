.. _logging:

Logging and Command Line Output
===============================

The logging level for the log file is always ``debug``, however the amount of information you see in your console can be modified. Use the ``--log-level`` option (``-l`` for short) to select one of the output options:

* ``short``
* ``minimal``
* ``info``
* ``debug``

Given the filename ``chuck.S01E02.avi`` to rename, the log levels would show the following information:

Short
~~~~~

    | Renamed: "Chuck - 102 - Chuck Versus the Helicopter.avi"

Minimal
~~~~~~~

    | Renaming: chuck.S01E02.avi
    | Directory: /Volumes/Media/TV/Chuck/Season 1/
    | Renamed: "Chuck - 102 - Chuck Versus the Helicopter.avi"

Info
~~~~

    | Renaming: chuck.S01E02.avi
    | Searching: chuck
    | Episode: Chuck Versus the Helicopter
    | Directory: /Volumes/Media/TV/Chuck/Season 1/
    | Renamed: "Chuck - 102 - Chuck Versus the Helicopter.avi"

Debug
~~~~~

    | 2010-10-17 20:40 DEBUG    Config      Config loaded
    | 2010-10-17 20:40 DEBUG    Config      Defaults retrieved
    | 2010-10-17 20:40 SHORT    Core        Dry Run beginning.
    | 2010-10-17 20:40 SHORT    Core        ----------------------------------------------------------------------
    | 2010-10-17 20:40 SHORT    Core        
    | 2010-10-17 20:40 MINIMAL  Core        Renaming: chuck.S01E02.avi
    | 2010-10-17 20:40 DEBUG    Core        Renaming using: (?P<show>[\w\s.,_-]+)\.[Ss]?(?P<season>[\d]{1,2})[XxEe]?(?P<episode>[\d]{2})
    | 2010-10-17 20:40 DEBUG    Core        Returned show: chuck, season: 01, episode: 02, extension: .avi
    | 2010-10-17 20:40 DEBUG    Core        Imported The Tv Db library
    | 2010-10-17 20:40 INFO     The Tv DB   Searching: chuck
    | 2010-10-17 20:40 DEBUG    The Tv DB   Retrieving series id for chuck
    | 2010-10-17 20:40 DEBUG    The Tv DB   Series url: http://www.thetvdb.com/api/GetSeries.php?seriesname=chuck
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML: Attempting to parse
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML retrieved, searching for series
    | 2010-10-17 20:40 DEBUG    The Tv DB   Series chosen: Chuck
    | 2010-10-17 20:40 DEBUG    The Tv DB   Retrieved show id: 80348
    | 2010-10-17 20:40 DEBUG    The Tv DB   Retrieved canonical show name: Chuck
    | 2010-10-17 20:40 DEBUG    The Tv DB   Episode URL: http://www.thetvdb.com/api/C4C424B4E9137AFD/series/80348/default/1/2/en.xml
    | 2010-10-17 20:40 DEBUG    The Tv DB   Attempting to retrieve episode name
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML: Retreived
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML: Attempting to parse
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML: Parsed
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML: Episode document retrived for Chuck - 0102
    | 2010-10-17 20:40 DEBUG    The Tv DB   XML: Attempting to finding the episode name
    | 2010-10-17 20:40 DEBUG    The Tv DB   Retrieved episode name: Chuck Versus the Helicopter
    | 2010-10-17 20:40 INFO     Core        Episode: Chuck Versus the Helicopter
    | 2010-10-17 20:40 DEBUG    Error       'chuck' is not in the Config. Falling back on name extracted from the filename
    | 2010-10-17 20:40 DEBUG    Core        Using the formatted show name retrieved by the library: Chuck
    | 2010-10-17 20:40 DEBUG    Core        Final show name: Chuck
    | 2010-10-17 20:40 MINIMAL  Core        Directory: /Volumes/Media/TV/Chuck/Season 1/
    | 2010-10-17 20:40 DEBUG    Core        Full path: /Volumes/Media/TV/Chuck/Season 1/Chuck - 102 - Chuck Versus the Helicopter.avi
    | 2010-10-17 20:40 MINIMAL  Core        Renamed: "Chuck - 102 - Chuck Versus the Helicopter.avi"
    | 2010-10-17 20:40 SHORT    Core        
    | 2010-10-17 20:40 SHORT    Core        ----------------------------------------------------------------------
    | 2010-10-17 20:40 SHORT    Core        Dry Run complete. No files were harmed in the process.
    | 2010-10-17 20:40 SHORT    Core

Debug will automatically perform a dry run rename since it was designed to be used for testing. However this is the format you will see in your log file, minus the dry run.

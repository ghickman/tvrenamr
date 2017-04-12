.. _usage:

Usage
=====

In your favourite terminal rename a specific file:

.. code-block:: bash

    $ tvr file

or a folder of files:

.. code-block:: bash

    $ tvr folder

or files with a specific extension:

.. code-block:: bash

    $ tvr *.mkv

or files in the current directory:

.. code-block:: bash

    $ tvr


Options
-------

Tv Renamr accepts the following options which take precedent over any options set in the :ref:`config`.

--config            Select a location for your config file. If the path is invalid the default locations will be used.
--copy              Copy instead of moving the files.
--no-copy           Explicity tell Tv Renamr not to copy instead of moving the files. Used to override the config.
-c, --canonical     Set the show's canonical name to use when performing the online lookup.
-d, --dry-run       Dry run your renaming.
-e, --episode       Set the episode number. Currently this will cause errors when working with more than one file.
--history           Display a list of shows renamed using the system pager.
--ignore-recursive  Only use files from the root of a given directory, not entering any sub-directories.
--log-file          Set the log file location.
-l, --log-level     Set the log level. Options: short, minimal, info and debug.
-n, --name          Set the episode's name.
--no-cache          Force all renames to ignore the cache.
-o, --output        Set the output format for the episodes being renamed.
--organise          Organise renamed files into folders based on their show name and season number.
--no-organise       Explicitly tell Tv Renamr not to organise renamed files. Used to override the config.
-p, --partial       Allow partial regex matching of the filename.
-q, --quiet         Don't output logs to the command line.
-r, --recursive     Recursively lookup files in a given directory.
--rename-dir        The directory to move renamed files to, if not specified the working directory is used.
--no-rename-dir     Explicity tell Tv Renamr not to move renamed files. Used to override the config.
--regex             The regular expression to use when extracting information from files.
-s, --season        Set the season number.
--show              Set the show's name (will search for this name).
--show-override     Override the show's name (only replaces the show's name in the final file).
--specials          Set the show's specials folder (defaults to "Season 0").
--symlink           Create symbolic links instead of moving the files.
--no-symlink        Explicity tell Tv Renamr not to create symlinks. Used to override the config.
-t, --the           Set the position of 'The' in a show's name to the end of the show name.

Examples
~~~~~~~~

.. code-block:: bash

    $ tvr

.. code-block:: bash

    $ tvr --recursive /path/to/a/directory/

.. code-block:: bash

    $ tvr --organise -r /path/to/a/directory/ /path/to/a/file.mkv

.. code-block:: bash

    $ tvr --season 1 --name chuck /path/to/a/file/the_file.mkv


History
~~~~~~~

Use the history command to parse your logs for a list of files you've renamed:

.. code-block:: bash

    $ tvr --history

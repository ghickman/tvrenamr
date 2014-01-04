.. _usage:

Usage
=====

In your favourite terminal run:

.. code-block:: bash

    $ tvr file

or

.. code-block:: bash

    $ tvr folder

or

.. code-block:: bash

    $ tvr .avi


Options
-------

Tv Renamr accepts the following options which take precedent over any options set in the :ref:`config`.

-c, --canonical  Set the show's canonical name to use when performing the online lookup.
-d, --dry-run    Dry run your renaming.
-e, --episode    Set the episode number. Currently this will cause errors when working with more than one file.
--log-file       Set the log file location.
-l, --log-level  Set the log level. Options: short, minimal, info and debug.
--library        Set the library to use for retrieving episode titles. Options: thetvdb & tvrage.
-n, --name       Set the show's name. This will be used as the show's when the renaming is completed.
-o, --output     Set the output format for the episodes being renamed.
--organise       Organise renamed files into folders based on their show name and season number.
--no-organise    Explicitly tell Tv Renamr not to organise renamed files. Used to override the config.
-q, --quiet      Don't output logs to the command line.
-r, --recursive  Recursively lookup files in a given directory.
--rename-dir     The directory to move renamed files to, if not specified the working directory is used.
--no-rename-dir  Explicitly tell Tv Renamr not to move renamed files. Used to override the config.
--regex          The regular expression to use when extracting information from files.
-s, --season     Set the season number.
-t, --the        Set the position of 'The' in a show's name to the end of the file.

Examples
~~~~~~~~

.. code-block:: bash

    $ tvr

.. code-block:: bash

    $ tvr --recursive /path/to/a/directory/

.. code-block:: bash

    $ tvr --organise -r '/path/to/a/directory/' /path/to/a/directory/[a_file.avi]

.. code-block:: bash

    $ tvr --season '1' --name 'chuck' /path/to/a/file/the_file.avi


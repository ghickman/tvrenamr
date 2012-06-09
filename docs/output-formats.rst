.. _output-formats:

Custom Output
=============

It is possible to set a custom output format for your files using the ``-o`` command line option and the same syntax used with :ref:`custom-regexs`:

* ``%n`` - Show
* ``%s`` - Season
* ``%e`` - Episode
* ``%t`` - Title
* ``%x`` - Extension

Example
~~~~~~~

.. code-block:: bash

    $ tvr -o "%s%e - %n - %t%x" chuck.S01E02.avi

.. note::

    Not including the ``%x`` section on Windows systems can cause problems when trying to run your media files.

The ``-o`` option is equivalent to the ``format`` option in the :ref:`config`
which can be set for a show or in the defaults section.

.. _config:

Config
======

For ease of use Tv Renamr uses a config file. By default it looks for it in
``~/.tvrenamr/config.yml``, an example is listed :ref:`below <example>` which
shows all the possible default values you can use.

Defaults
--------
The defaults segment should be self-explanatory but I'll list them just for
completeness. The listed values are the assumed defaults if any of the options
are not added.

Format
~~~~~~
The output format for files to be renamed to.

.. code-block:: yaml

    format: '%n - %s%e - %t%x'

* ``%n``: Show name
* ``%s``: Season Number
* ``%e``: Episode Number
* ``%t``: Episode Title
* ``%x``: Extension

.. note::

    The extension part includes the period ``(.)`` part of the file's
    extension and is also optional.

Library
~~~~~~~
The online database to use for episode names. Options are: thetvdb or tvrage

.. code-block:: yaml

    library: thetvdb

Organise
~~~~~~~~
Organise your files within the renamed directory.

.. code-block:: yaml

    organise: yes

Renamed
~~~~~~~
The directory to move your renamed files to.

.. code-block:: yaml

    renamed: /Volumes/Media/TV/

The
~~~
If a show has a leading 'The', such as 'The Big Bang Theory', move it to the
end of the show name, i.e. 'Big Bang Theory, The'.

.. code-block:: yaml

    the: true

Tv Shows
--------
Below the defaults are shows that won't get renamed correctly using the default
options. Taking CSI as the example you have:

.. code-block:: yaml

    csi:
        canonical: "CSI: Crime Scene Investigation"
        output: "CSI, Crime Scene Investigation"

Show Name
~~~~~~~~~
In the above example ``csi`` is used to match the show name in the downloaded
file name, which might look something like this ``csi.s10e01.blah.blah.avi``.

Canonical
~~~~~~~~~
The name used by the online database(s) for a show.

Since The TVDb and Tv Rage both list CSI as *CSI: Crime Scene Investigation*
the ``canonical`` option is used.

.. code-block:: yaml

    canonical: "CSI: Crime Scene Investigation"

.. note::

    This method is the easiest way to deal with shows with a year in the name
    too, i.e. Castle (2009).

Output
~~~~~~
The show name to use when writing the new filename.

The canonical show name contains a colon which most filesystems won't play nice with 

.. code-block:: yaml

    output: "CSI, Crime Scene Investigation"

Format
~~~~~~
The output format to use when writing the new filename.

.. code-block:: yaml

    format: %n - %s%e

.. warning::

    The colon ``(:)`` and comma ``(,)`` characters are `reserved`_ in
    YAML so must be quoted.

.. _reserved: http://www.yaml.org/spec/1.2/spec.html#id2806177

.. _example:

.. code-block:: yaml

    defaults:
      format: '%n - %s%e - %t%x'
      library: thetvdb
      organise: yes
      renamed: /Volumes/Media/TV/
      the: true

    '24':
      format: '%n - %s%e'

    american dad:
      canonical: American Dad!

    castle 2009:
      canonical: Castle (2009)

    csi:
      canonical: "CSI: Crime Scene Investigation"
      output: "CSI, Crime Scene Investigation"

    doctor who 2005:
      canonical: Doctor Who (2005)

    the it crowd:
      the: false

    the simpsons:
      the: false

    v 2009:
      canonical: V (2009)
      output: V

Spaces
~~~~~~
any space will be replace for a dot when this option is false

.. code-block:: yaml

    spaces: false

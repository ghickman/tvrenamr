.. _custom-regexs:

Custom Regular Expressions
==========================

By default TV Renamr will match shows in the formats:

* show.s0e00
* show.0x00

However you can specify custom regular expressions if your files aren't in either of these formats. Some custom regular expression syntax has been used to help you specify different parts of the filename:

* Show: ``%n`` - ``(?P<show>[\w\s.,_-]+)``
* Season: ``%s`` - ``(?P<season>[\d]{1,2})``
* Episode: ``%e`` - ``(?P<episode>[\d]{2})``

It is also possible to specify how many digits there are in the season and episode sections of the filename using the syntax:

* Season: ``%s{n}``
* Episode: ``%e{n}``

where the n in ``{n}`` specifies how many digits are in each of the sections.

.. note::

    All spaces are converted to periods before your regular expression is run.

Python regular expression syntax can be found `here`_.

.. _here: http://www.python.org/doc/2.6.1/library/re.html#regular-expression-syntax


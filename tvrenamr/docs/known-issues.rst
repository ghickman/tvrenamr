.. _known-issues:

Known Issues
============

Please report any bugs or feature requests to the issue tracker on `Github`_.

.. _Github: http://github.com/ghickman/tvrenamr/issues

Colons
------

All colons ``:`` are converted to commas ``,`` in both the show name and the episode title. This stops issues that can arise with network shares and gives a cleaner format on windows where python replaces the colon character with a backslash ``\``.

Years in Show Names
-------------------

Shows with a year in the canonical title, i.e. Doctor Who (2005), will fail if this year isn't specified in the show name inside brackets. You'll need to set this as the canonical name in the config file.

Multiple Episodes
-----------------

Multiple episode files are just not coped with at all. The first episode is usually picked up so the file will be renamed using this.

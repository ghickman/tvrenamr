.. _installation:

Installation
============

Requirements
------------

* Python 2.7+, Python 3.3+
* The Interwebs


Python Package Index
--------------------

Install Tv Renamr with your favourite Python package manager.
We recommend pipsi_ to avoid polluting your global env.

.. _pipsi: https://github.com/mitsuhiko/pipsi

.. code-block:: bash

    pipsi install tvrenamr

However if you're more comfortable with pip that will also work:

.. code-block:: bash

    pip install tvrenamr

.. note::

    You might need to be an administrator to do this.

A nice shiny ``tvr`` script is now installed in the relevant directory on your
python path.

.. note::

    If you don't have pip installed you'll get an error message. Instructions on
    how to install pip can be found `here`_.

.. _here: http://www.pip-installer.org/en/latest/installing.html


Source: GitHub
--------------

.. code-block:: bash

    git clone https://github.com/ghickman/tvrenamr.git
    cd tvrenamr
    pip install -e .

.. warning::

    You may probably need to be an administrator to run the ``python setup.py
    install`` line.

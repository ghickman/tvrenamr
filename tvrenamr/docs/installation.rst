.. _installation:

Installation
============

Requirements
------------

* Python 2.6+
* PyYaml
* The Interwebs


Python Package Index
--------------------

Install Tv Renamr with your favourite Python package manager:

.. code-block:: bash

    pip install tvrenamr

.. note::

    You might need to be an administrator to do this.

A nice shiny ``tvr`` script is now installed in the relevant directory on your
python path.

.. note::

    If you don't have pip install you'll get an error message. Instructions on
    how to install pip can be found `here`_.

.. _here: http://www.pip-installer.org/en/latest/installing.html

Windows
~~~~~~~

Due to a problem with easy_install/pip and Tv Renamr's option parsing code it
isn't possible to use easy_install or pip for installation just yet, but it
might get fixed in the future.

Source: GitHub
--------------

.. code-block:: bash

    git clone https://github.com/ghickman/tvrenamr.git
    cd tvrenamr
    python setup.py install

.. warning::

    You may probably need to be an administrator to run the ``python setup.py
    install`` line.

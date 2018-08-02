Djangolib
=========


Installation
------------

.. code-block:: bash

    pip install unicef-djangolib


Setup
-----

Add ``unicef_djangolib`` to ``INSTALLED_APPS`` in settings

.. code-block:: bash

    INSTALLED_APPS = [
        ...
        'unicef_djangolib',
    ]


Usage
-----

TODO

Contributing
------------

Environment Setup
~~~~~~~~~~~~~~~~~

To install the necessary libraries

.. code-block:: bash

    $ make install


Coding Standards
~~~~~~~~~~~~~~~~

See `PEP 8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ for complete details on the coding standards.

To run checks on the code to ensure code is in compliance

.. code-block:: bash

    $ make lint


Testing
~~~~~~~

Testing is important and tests are located in `tests/` directory and can be run with;

.. code-block:: bash

    $ make test

Coverage report is viewable in `build/coverage` directory, and can be generated with;


Project Links
~~~~~~~~~~~~~

 - Continuous Integration - https://circleci.com/gh/unicef/unicef-djangolib/tree/develop
 - Source Code - https://github.com/unicef/unicef-djangolib



Links
-----

+--------------------+----------------+--------------+--------------------+
| Stable             |                | |master-cov| |                    |
+--------------------+----------------+--------------+--------------------+
| Development        |                | |dev-cov|    |                    |
+--------------------+----------------+--------------+--------------------+
| Source Code        |https://github.com/unicef/unicef-djangolib          |
+--------------------+----------------+-----------------------------------+
| Issue tracker      |https://github.com/unicef/unicef-djangolib/issues   |
+--------------------+----------------+-----------------------------------+


.. |master-cov| image:: https://circleci.com/gh/unicef/unicef-djangolib/tree/master.svg?style=svg
                    :target: https://circleci.com/gh/unicef/unicef-djangolib/tree/master


.. |dev-cov| image:: https://circleci.com/gh/unicef/unicef-djangolib/tree/develop.svg?style=svg
                    :target: https://circleci.com/gh/unicef/unicef-djangolib/tree/develop


Compatibility Matrix
--------------------

.. image:: https://travis-matrix-badges.herokuapp.com/repos/unicef/unicef-djangolib/branches/develop

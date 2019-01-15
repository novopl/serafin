
#######
serafin
#######

**serafin** is a python library that allows to selectively serialize different
kinds of python object into something that can be dumped to JSON or YAML.

.. note::
The project follows the semantic versioning scheme: Until 1.0 the minor

        * The *patch* versions only include bugfixes and changes that do not
          modify the existing interface. You can safely update a patch version
          without worrying it will break your code.
        * The *minor* versions will contain changes to the interface. With a
          single version update your code will most likely work or might require
          small adjustments. The more minor versions you update at once the
          bigger the chance that something will brake.
        * The *major* versions are reserved for significant refactorings and
          architecture changes. This should not happen very often so the major
          version should not change much.

.. note::
    The CircleCI builds can be found
    `here <https://circleci.com/gh/novopl/serafin>`_

.. readme_inclusion_marker

Installation
============

.. code-block:: shell

    $ pip install serafin


Contributing
============

Cloning and setting up the development repo
-------------------------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/serafin.git
    $ cd serafin
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install .
    $ pip install -r ops/devrequirements.txt
    $ peltak git add-hoooks


Running tests
.............

**Config**: The types of tests are defined in ``pelconf.py`` and the
pytest configuration is defined in ``ops/tools/pytest.ini``.

.. code-block:: shell

    $ peltak test

Linting
.......

**Config**: The list of locations to lint is defined in ``pelconf.py`` and the
linters configuration is defined in ``ops/tools/{pylint,pep8}.ini``.

.. code-block:: shell

    $ peltak lint

Generating docs
...............

**Config**: The list of documented files and general configuration is in
``pelconf.py`` and the Sphinx configuration is defined in ``docs/conf.py``.

.. code-block:: shell

    $ peltak docs


#######
serafin
#######

**serafin** is a python library that allows to selectively serialize different
kinds of python object into something that can be dumped to JSON or YAML.

.. note::
    This library is a bit older code of mine, but I've been using it for years
    now in my private projects and it's been pretty stable. The code is quite
    well tested except for integrations with SQLAchemy and django which are
    quite recent additions.

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

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/serafin.git
    $ cd serafin
    $ virtualenv env
    $ source ./env/bin/activate
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

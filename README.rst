lib_detect_encoding
===================


Version v1.0.0 as of 2023-10-14 see `Changelog`_

|build_badge| |codeql| |license| |jupyter| |pypi|
|pypi-downloads| |black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/lib_detect_encoding/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/lib_detect_encoding/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/lib_detect_encoding/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/lib_detect_encoding/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/lib_detect_encoding/master?filepath=lib_detect_encoding.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/lib-detect-encoding?label=PyPI%20Package
   :target: https://badge.fury.io/py/lib_detect_encoding

.. badge until 2023-10-08:
.. https://img.shields.io/codecov/c/github/bitranox/lib_detect_encoding
.. badge from 2023-10-08:
.. |codecov| image:: https://codecov.io/gh/bitranox/lib_detect_encoding/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/lib_detect_encoding

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/lib_detect_encoding?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/lib_detect_encoding/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/lib_detect_encoding?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/lib_detect_encoding/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/lib_detect_encoding?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/lib_detect_encoding/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/lib_detect_encoding/badge.svg
   :target: https://snyk.io/test/github/bitranox/lib_detect_encoding

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/lib-detect-encoding
   :target: https://pypi.org/project/lib-detect-encoding/
   :alt: PyPI - Downloads

put your description of the project under .docs/description.rst

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12-dev, pypy-3.9, pypy-3.10 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/lib_detect_encoding/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/lib_detect_encoding/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_detect_encoding/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_detect_encoding/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_detect_encoding/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=lib_detect_encoding.ipynb>`_

Usage
-----------

.. code-block:: python

    def get_system_preferred_encoding() -> str:
        """ returns the system preferred encoding in lowercase. Works on posix, windows and WINE
        On windows, the python default function "locale.getpreferredencoding" sometimes reports falsely cp1252 instead of cp850,
        therefore we check also with windows command "chcp" for the correct preferred codepage
        Note that the python codec name will be returned, such as : utf_8, utf_8_sig etc.
        see: https://docs.python.org/3/library/codecs.html#standard-encodings
        """

.. code-block:: python

    def get_file_encoding(raw_bytes: bytes) -> str:
        """ returns the encoding for the raw_bytes passed.
        if the confidence of the detection is below 95 percent, the system default encoding will be returned
        Note that the python codec name will be returned, such as : utf_8, utf_8_sig etc.
        see: https://docs.python.org/3/library/codecs.html#standard-encodings

        >>> # Setup
        >>> import pathlib
        >>> path_testfile_utf8 = pathlib.Path(__file__).parent.parent / "tests/testfile_utf8.txt"
        >>> raw_utf8_bytes = path_testfile_utf8.read_bytes()

        >>> # Test get encoding from bytes
        >>> assert get_file_encoding(raw_utf8_bytes) == 'utf_8'

        >>> # test get encoding with low confidence (returning system default encoding)
        >>> assert get_file_encoding(b'') is not None
        >>> assert get_file_encoding(b'x') is not None
        >>> assert len(get_file_encoding(b'x')) > 0

        """

.. code-block:: python

    def get_language_by_codec_name(codec_name: str) -> str:
        """ get the language by python codec name

        >>> # Test OK
        >>> assert  get_language_by_codec_name('utf-8') == "all languages"
        >>> assert  get_language_by_codec_name('utf-8') == "all languages"

        >>> # Test unknown encoding
        >>> get_language_by_codec_name('unknown')
        Traceback (most recent call last):
            ...
        KeyError: 'codec "unknown" not found'

        >>> # Test if language is present for all codepage_aliases
        >>> for codec_alias in codec_aliases: \
                codec_language = get_language_by_codec_name(codec_alias)
        """

Usage from Commandline
------------------------

.. code-block::

   Usage: lib_detect_encoding [OPTIONS] COMMAND [ARGS]...

     detects encodings of raw files, or the system default encoding

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     get_file_encoding              get encoding from a (text)file
     get_language                   get the language from a codec name
     get_system_preferred_encoding  get the system preferred encoding
     info                           get program informations

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade lib_detect_encoding


- to install the latest release from PyPi via pip, including test dependencies:

.. code-block::

    python -m pip install --upgrade lib_detect_encoding[test]

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/lib_detect_encoding.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_detect_encoding

    # for the latest development version :
    lib_detect_encoding @ git+https://github.com/bitranox/lib_detect_encoding.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/lib_detect_encoding.git
    $ cd lib_detect_encoding
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_detect_encoding.git
    $ cd lib_detect_encoding

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click
    cli_exit_tools
    chardet
    lib_log_utils
    lib_platform

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_detect_encoding/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

v1.0.0
--------
2023-10-14:
    - create mypy cache dir '.mypy_cache'
    - require minimum python 3.8
    - remove python 3.7 tests
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

0.0.1
-----
2019-07-22: Initial public release


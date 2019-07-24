"""Setuptools entry point."""
import codecs
import os
import subprocess
import sys


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", package])


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

description = 'Detect Encoding'

dirname = os.path.dirname(__file__)
readme_filename = os.path.join(dirname, 'README.rst')

long_description = description
if os.path.exists(readme_filename):
    try:
        readme_content = codecs.open(readme_filename, encoding='utf-8').read()
        long_description = readme_content
    except Exception:
        pass

install('https://github.com/bitranox/lib_platform/archive/master.zip')

setup(
    name='lib_detect_encoding',
    version='0.0.1',
    url='https://github.com/bitranox/lib_detect_encoding',
    packages=['lib_detect_encoding'],
    install_requires=['pytest', 'typing', 'chardet'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    description=description,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Robert Nowotny',
    author_email='rnowotny1966@gmail.com',
    classifiers=CLASSIFIERS,
    )

# install_requires: what other distributions need to be installed when this one is.
# setup_requires: what other distributions need to be present in order for the setup script to run
# tests_require: If your project’s tests need one or more additional packages besides those needed to install it,
#                you can use this option to specify them

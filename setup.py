"""Setuptools entry point."""
import codecs
import os
import subprocess
import sys


def install_requirements_when_using_setup_py():
    proc = subprocess.Popen([sys.executable, "-m", "pip", "install", '-r', './requirements_setup.txt'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    encoding = sys.getdefaultencoding()
    print(stdout.decode(encoding))
    print(stderr.decode(encoding))

    if proc.returncode != 0:
        raise RuntimeError('Error installing requirements_setup.txt')


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

install_requirements_when_using_setup_py()

setup(
    name='lib_detect_encoding',
    version='0.0.1',
    url='https://github.com/bitranox/lib_detect_encoding',
    packages=['lib_detect_encoding'],
    description=description,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Robert Nowotny',
    author_email='rnowotny1966@gmail.com',
    classifiers=CLASSIFIERS,
    # specify what a project minimally needs to run correctly
    install_requires=['chardet', 'lib_platform'],
    # minimally needs to run the setup script, dependencies needs also to put here for setup.py install test
    setup_requires=['pytest-runner', 'chardet', 'lib_platform'],
    # minimally needs to run tests
    tests_require=['pytest']
    )

# STDLIB
import logging
import os
import pathlib
import subprocess
import sys

logger = logging.getLogger()
package_dir = 'lib_detect_encoding'
cli_filename = 'lib_detect_encoding_cli.py'
os.environ['PYTEST_IS_RUNNING'] = 'True'  # to be able to detect pytest when running the cli command

path_cli_command = pathlib.Path(__file__).resolve().parent.parent / package_dir / cli_filename


def call_cli_command(commandline_args: str = '') -> bool:
    command = ' '.join([sys.executable, str(path_cli_command), commandline_args])
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return True


def test_cli_commands() -> None:
    """
    >>> test_cli_commands()
    """
    path_testfile = pathlib.Path(__file__).parent / 'testfile_utf8.txt'
    assert not call_cli_command('--unknown_option')
    assert call_cli_command('--version')
    assert call_cli_command('-h')
    assert call_cli_command('info')
    assert call_cli_command('--traceback info')
    assert call_cli_command('get_system_preferred_encoding')
    # test with parameter
    assert call_cli_command(f'get_file_encoding {path_testfile}')
    # test with wrong parameter
    assert not call_cli_command('get_file_encoding unknown.txt')
    # test with missing parameter --> NOOP
    """
    Note on Non-Empty Variadic Arguments :
    If you come from argparse, you might be missing support for setting nargs to + to indicate that at least one argument is required.
    This is supported by setting required=True. However, this should not be used if you can avoid it as we believe scripts should gracefully
    degrade into becoming noops if a variadic argument is empty.
    The reason for this is that very often, scripts are invoked with wildcard inputs from the command line
    and they should not error out if the wildcard is empty.
    """
    assert call_cli_command('get_file_encoding')

    # test get language
    assert call_cli_command('get_language cp865')
    # test get language with missing parameter
    assert call_cli_command('get_language')

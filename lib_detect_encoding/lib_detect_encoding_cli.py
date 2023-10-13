# STDLIB
import pathlib
import sys
from typing import Optional

# EXT
import click

# OWN
import cli_exit_tools

# PROJ
try:
    from . import __init__conf__
    from . import lib_detect_encoding
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    # imports for doctest
    import __init__conf__                   # type: ignore  # pragma: no cover
    import lib_detect_encoding      # type: ignore  # pragma: no cover

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def info() -> None:
    """
    >>> info()
    Info for ...

    """
    __init__conf__.print_info()


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)    # type: ignore
@click.version_option(version=__init__conf__.version,
                      prog_name=__init__conf__.shell_command,
                      message=f'{__init__conf__.shell_command} version {__init__conf__.version}')
@click.option('--traceback/--no-traceback', is_flag=True, type=bool, default=None, help='return traceback information on cli')
def cli_main(traceback: Optional[bool] = None) -> None:
    if traceback is not None:
        cli_exit_tools.config.traceback = traceback


@cli_main.command('info', context_settings=CLICK_CONTEXT_SETTINGS)      # type: ignore
def cli_info() -> None:
    """ get program informations """
    info()


@cli_main.command('get_system_preferred_encoding', context_settings=CLICK_CONTEXT_SETTINGS)      # type: ignore
def cli_get_system_preferred_encoding() -> None:
    """ get the system preferred encoding """
    print(lib_detect_encoding.get_system_preferred_encoding())


@cli_main.command('get_file_encoding', context_settings=CLICK_CONTEXT_SETTINGS)      # type: ignore
@click.argument('filename', type=click.Path(exists=True), required=False)
def cli_get_file_encoding(filename) -> None:
    """ get encoding from a (text)file """

    """
    Note on Non-Empty Variadic Arguments :
    If you come from argparse, you might be missing support for setting nargs to + to indicate that at least one argument is required.
    This is supported by setting required=True. However, this should not be used if you can avoid it as we believe scripts should gracefully
    degrade into becoming noops if a variadic argument is empty.
    The reason for this is that very often, scripts are invoked with wildcard inputs from the command line
    and they should not error out if the wildcard is empty.
    """
    if filename:
        raw_bytes = pathlib.Path(filename).read_bytes()
        print(lib_detect_encoding.get_file_encoding(raw_bytes))


@cli_main.command('get_language', context_settings=CLICK_CONTEXT_SETTINGS)      # type: ignore
@click.argument('codec_name', type=click.STRING, required=False)
def cli_get_language_by_codec_name(codec_name: str) -> None:
    """ get the language from a codec name """

    """
    Note on Non-Empty Variadic Arguments :
    If you come from argparse, you might be missing support for setting nargs to + to indicate that at least one argument is required.
    This is supported by setting required=True. However, this should not be used if you can avoid it as we believe scripts should gracefully
    degrade into becoming noops if a variadic argument is empty.
    The reason for this is that very often, scripts are invoked with wildcard inputs from the command line
    and they should not error out if the wildcard is empty.
    """
    if codec_name:
        print(lib_detect_encoding.get_language_by_codec_name(codec_name))


# entry point if main
if __name__ == '__main__':
    try:
        cli_main()      # type: ignore
    except Exception as exc:
        cli_exit_tools.print_exception_message()
        sys.exit(cli_exit_tools.get_system_exit_code(exc))
    finally:
        cli_exit_tools.flush_streams()

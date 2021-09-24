# STDLIB
import locale
import logging
import platform
import subprocess

# EXT
import chardet          # type: ignore

# OWN
import lib_platform     # type: ignore


def _disable_chardet_confidence_logging() -> None:
    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
    logging.getLogger('chardet.universaldetector').setLevel(logging.INFO)


_disable_chardet_confidence_logging()

logger = logging.getLogger()


def detect_encoding(raw_bytes: bytes) -> str:
    """
    >>> assert detect_encoding(b'') is not None
    >>> assert detect_encoding(b'x') is not None
    >>> assert len(detect_encoding(b'x')) > 0
    """
    detected = chardet.detect(raw_bytes)
    encoding = str(detected['encoding'])
    confidence = detected['confidence']
    # locale.getpreferredencoding sometimes reports cp1252, but is cp850, so check with chcp
    if confidence < 0.95:
        encoding = get_encoding()
    return encoding


def get_encoding() -> str:
    if lib_platform.is_platform_posix:
        return get_encoding_linux()
    elif lib_platform.is_platform_windows:
        return get_encoding_windows()
    else:
        raise RuntimeError(f'Operating System {platform.system()} not supported')


def get_encoding_linux() -> str:
    os_encoding = locale.getpreferredencoding()
    return os_encoding


def get_encoding_windows() -> str:
    """
    >>> my_encoding = get_encoding_windows()
    >>> assert my_encoding == 'cp850' or my_encoding == 'utf8'
    """

    # you might add more encodings, see https://docs.python.org/2.4/lib/standard-encodings.html
    encodings = [('437', 'cp437'),     # United states
                 ('850', 'cp850'),     # Multilingual Latin1
                 ('852', 'cp852'),     # Slavic (Latin II)
                 ('855', 'cp855'),     # Cyrillic (Russian)
                 ('857', 'cp857'),     # Turkish
                 ('860', 'cp860'),     # Portuguese
                 ('861', 'cp861'),     # Icelandic
                 ('863', 'cp863'),     # Canadian-French
                 ('865', 'cp865'),     # Nordic
                 ('860', 'cp860'),     # Portuguese
                 ('866', 'cp866'),     # Russian
                 ('869', 'cp869'),     # Modern Greek
                 ('860', 'cp860'),     # Portuguese
                 ('1252', 'cp1252'),   # West European Latin
                 ('65000', 'utf7'),    # all languages
                 ('65001', 'utf8')     # all languages
                 ]

    # locale.getpreferredencoding sometimes reports cp1252, but is cp850, so check with chcp (especially when shell=True)

    os_encoding = locale.getpreferredencoding()

    if lib_platform.is_platform_windows_wine:   # no chcp command on wine
        logger.warning('assume wine encoding cp850')
        chcp_response = '850'
    elif lib_platform.is_platform_posix:        # we called a wine program on linux probably
        chcp_response = '850'
    else:
        my_process = subprocess.Popen(['chcp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = my_process.communicate()
        chcp_response = stdout.decode(os_encoding)

    for encoding_number, encoding in encodings:
        if encoding_number in chcp_response:
            return encoding

    logger.warning('can not detect windows encoding with chcp, using cp850')
    return 'cp850'

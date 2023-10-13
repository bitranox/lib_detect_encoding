# STDLIB
import locale
import logging
import platform
import subprocess
import sys

# EXT
import chardet

# OWN
import lib_log_utils
import lib_platform

# you might add more encodings, see https://docs.python.org/3/library/codecs.html#standard-encodings
# https://learn.microsoft.com/de-de/windows/win32/intl/code-page-identifiers
# this maps the windows codepage identifier to the python encoding name

# codepage_aliases only contain values mentioned in Standard Encodings from https://docs.python.org/3/library/codecs.html#standard-encodings
# all values are lowercase, "-" is replaced with "_"
codec_aliases = {"ascii": "ascii", "646": "ascii" , "us_ascii": "ascii",  # English
                 "big5": "big5", "big5_tw": "big5", "csbig5": "big5",  # Traditional Chinese
                 "big5hkscs": "big5hkscs", "big5_hkscs": "big5hkscs", "hkscs": "big5hkscs",  # Traditional Chinese
                 "cp037": "cp037", "ibm037": "cp037", "ibm039": "cp037", "037": "cp037",  # English
                 "cp273": "cp273", "273": "cp273", "ibm273": "cp273", "csibm273": "cp273",  # German
                 "cp424": "cp424", "ebcdic_cp_he": "cp424", "ibm424": "cp424", "424": "cp424",  # Hebrew
                 "cp437": "cp437", "437": "cp437", "ibm437": "cp437",  # English, United States
                 "cp500": "cp500", "ebcdic_cp_be": "cp500", "ebcdic_cp_ch": "cp500", "ibm500": "cp500", "500": "cp500",  # Western Europe
                 "cp720": "cp720", "720": "cp720",  # Arabic
                 "cp737": "cp737", "737": "cp737",  # Greek
                 "cp775": "cp775", "ibm775": "cp775", "775": "cp775",  # Baltic languages
                 "cp850": "cp850", "850": "cp850", "ibm850": "cp850",  # Western Europe
                 "cp852": "cp852", "852": "cp852", "ibm852": "cp852",  # Central and Eastern Europe
                 "cp855": "cp855", "855": "cp855", "ibm855": "cp855",  # Bulgarian, Belarusian , Macedonian, Russian, Serbian
                 "cp856": "cp856", "856": "cp856",  # Hebrew
                 "cp857": "cp857", "857": "cp857", "ibm857": "cp857",  # Turkish
                 "cp858": "cp858", "858": "cp858", "ibm858": "cp858",  # Western Europe
                 "cp860": "cp860", "860": "cp860", "ibm860": "cp860",  # Portuguese
                 "cp861": "cp861", "861": "cp861", "ibm861": "cp861", "cp_is": "cp861",  # Icelandic
                 "cp862": "cp862", "862": "cp862", "ibm862": "cp862",  # Hebrew
                 "cp863": "cp863", "863": "cp863", "ibm863": "cp863",  # Canadian-French
                 "cp864": "cp864", "864": "cp864", "ibm864": "cp864",  # Arabic
                 "cp865": "cp865", "865": "cp865", "ibm865": "cp865",  # Danish, Norwegian
                 "cp866": "cp866", "866": "cp866", "ibm866": "cp866",  # Russian
                 "cp869": "cp869", "869": "cp869", "ibm869": "cp869", "cp_gr": "cp869",  # Modern Greek
                 "cp874": "cp874", "874": "cp874",  # Thai
                 "cp875": "cp875", "875": "cp875",  # Greek
                 "cp932": "cp932", "932": "cp932", "ms932": "cp932", "mskanji": "cp932", "ms_kanji": "cp932",  # Japanese
                 "cp949": "cp949", "949": "cp949", "ms949": "cp949", "uhc": "cp949",  # Korean
                 "cp950": "cp950", "950": "cp950", "ms950": "cp950",  # Traditional Chinese
                 "cp1006": "cp1006", "1006": "cp1006",  # Urdu
                 "cp1026": "cp1026", "1026": "cp1026", "ibm1026": "cp1026",  # Turkish
                 "cp1125": "cp1125", "1125": "cp1125", "ibm1125": "cp1125", "cp866u": "cp1125", "ruscii": "cp1125",  # Ukrainian
                 "cp1140": "cp1140", "1140": "cp1140", "ibm1140": "cp1140",  # Western Europe
                 "cp1250": "cp1250", "1250": "cp1250", "windows_1250": "cp1250",  # Central and Eastern Europe
                 "cp1251": "cp1251", "1251": "cp1251", "windows_1251": "cp1251",  # Bulgarian, Belarusian, Macedonian, Russian, Serbian
                 "cp1252": "cp1252", "1252": "cp1252", "windows_1252": "cp1252",  # Western Europe
                 "cp1253": "cp1253", "1253": "cp1253", "windows_1253": "cp1253",  # Greek
                 "cp1254": "cp1254", "1254": "cp1254", "windows_1254": "cp1254",  # Turkish
                 "cp1255": "cp1255", "1255": "cp1255", "windows_1255": "cp1255",  # Hebrew
                 "cp1256": "cp1256", "1256": "cp1256", "windows_1256": "cp1256",  # Arabic
                 "cp1257": "cp1257", "1257": "cp1257", "windows_1257": "cp1257",  # Baltic languages
                 "cp1258": "cp1258", "1258": "cp1258", "windows_1258": "cp1258",  # Vietnamese
                 "euc_jp": "euc_jp", "eucjp": "euc_jp", "ujis": "euc_jp", "u_jis": "euc_jp",  # Japanese
                 "euc_jis_2004": "euc_jis_2004", "jisx0213": "euc_jis_2004", "eucjis2004": "euc_jis_2004",  # Japanese
                 "euc_jisx0213": "euc_jisx0213", "eucjisx0213": "euc_jisx0213",  # Japanese
                 "euc_kr": "euc_kr", "euckr": "euc_kr", "korean": "euc_kr", "ksc5601": "euc_kr",  # Korean
                 "ks_c_5601": "euc_kr", "ks_c_5601_1987": "euc_kr", "ksx1001": "euc_kr", "ks_x_1001": "euc_kr",  # Korean
                 "gb2312": "gb2312", "chinese": "gb2312", "csiso58gb231280": "gb2312", "euc_cn": "gb2312",  # Simplified Chinese
                 "euccn": "gb2312", "eucgb2312_cn": "gb2312", "gb2312_1980": "gb2312", "gb2312_80": "gb2312",  # Simplified Chinese
                 "iso_ir_58": "gb2312",  # Simplified Chinese
                 "gbk": "gbk", "936": "gbk", "cp936": "gbk", "ms936": "gbk",  # Unified Chinese
                 "gb18030": "gb18030", "gb18030_2000": "gb18030",  # Unified Chinese
                 "hz": "hz", "hzgb": "hz", "hz_gb": "hz", "hz_gb_2312": "hz",  # Simplified Chinese
                 "iso2022_jp": "iso2022_jp", "csiso2022jp": "iso2022_jp", "iso2022jp": "iso2022_jp", "iso_2022_jp": "iso2022_jp",  # Japanese
                 "iso2022_jp_1": "iso2022_jp_1", "iso2022jp_1": "iso2022_jp_1", "iso_2022_jp_1": "iso2022_jp_1",  # Japanese
                 "iso2022_jp_2": "iso2022_jp_2", "iso2022jp_2": "iso2022_jp_2",  # Japanese, Korean, Simplified Chinese, Western Europe, Greek
                 "iso_2022_jp_2": "iso2022_jp_2",  # Japanese, Korean, Simplified Chinese, Western Europe, Greek
                 "iso2022_jp_2004": "iso2022_jp_2004", "iso2022jp_2004": "iso2022_jp_2004", "iso_2022_jp_2004": "iso2022_jp_2004",  # Japanese
                 "iso2022_jp_3": "iso2022_jp_3", "iso2022jp_3": "iso2022_jp_3", "iso_2022_jp_3": "iso2022_jp_3",  # Japanese
                 "iso2022_jp_ext": "iso2022_jp_ext", "iso2022jp_ext": "iso2022_jp_ext", "iso_2022_jp_ext": "iso2022_jp_ext",  # Japanese
                 "iso2022_kr": "iso2022_kr", "csiso2022kr": "iso2022_kr", "iso2022kr": "iso2022_kr", "iso_2022_kr": "iso2022_kr",  # Korean
                 "latin_1": "latin_1", "iso_8859_1": "latin_1", "iso8859_1": "latin_1", "8859": "latin_1", "cp819": "latin_1",  # Western Europe
                 "819": "latin_1", "latin": "latin_1", "latin1": "latin_1", "l1": "latin_1",  # Western Europe
                 "iso8859_2": "iso8859_2", "iso_8859_2": "iso8859_2", "latin2": "iso8859_2", "l2": "iso8859_2",  # Central and Eastern Europe
                 "iso8859_3": "iso8859_3", "iso_8859_3": "iso8859_3", "latin3": "iso8859_3", "l3": "iso8859_3",  # Esperanto, Maltese
                 "iso8859_4": "iso8859_4", "iso_8859_4": "iso8859_4", "latin4": "iso8859_4", "l4": "iso8859_4",  # Baltic languages
                 "iso8859_5": "iso8859_5", "iso_8859_5": "iso8859_5", "cyrillic": "iso8859_5",  # Bulgarian, Belarusian , Macedonian, Russian, Serbian
                 "iso8859_6": "iso8859_6", "iso_8859_6": "iso8859_6", "arabic": "iso8859_6",  # Arabic
                 "iso8859_7": "iso8859_7", "iso_8859_7": "iso8859_7", "greek": "iso8859_7", "greek8": "iso8859_7",  # Greek
                 "iso8859_8": "iso8859_8", "iso_8859_8": "iso8859_8", "hebrew": "iso8859_8",  # Hebrew
                 "iso8859_9": "iso8859_9", "iso_8859_9": "iso8859_9", "latin5": "iso8859_9", "l5": "iso8859_9",  # Turkish
                 "iso8859_10": "iso8859_10", "iso_8859_10": "iso8859_10", "latin6": "iso8859_10", "l6": "iso8859_10",  # Nordic languages
                 "iso8859_11": "iso8859_11", "iso_8859_11": "iso8859_11", "thai": "iso8859_11",  # Thai languages
                 "iso8859_13": "iso8859_13", "latin7": "iso8859_13", "l7": "iso8859_13",  # Baltic languages
                 "iso8859_14": "iso8859_14", "iso_8859_14": "iso8859_14", "latin8": "iso8859_14", "l8": "iso8859_14",  # Celtic languages
                 "iso8859_15": "iso8859_15", "iso_8859_15": "iso8859_15", "latin9": "iso8859_15", "l9": "iso8859_15",  # Western Europe
                 "iso8859_16": "iso8859_16", "iso_8859_16": "iso8859_16", "latin10": "iso8859_16", "l10": "iso8859_16",  # South-Eastern Europe
                 "johab": "johab", "cp1361": "johab", "1361": "johab", "ms1361": "johab",  # Korean
                 "koi8_r": "koi8_r",  # Russian
                 "koi8_t": "koi8_t",  # Tajik
                 "koi8_u": "koi8_u",  # Ukrainian
                 "kz1048": "kz1048", "kz_1048": "kz1048", "strk1048_2002": "kz1048", "rk1048": "kz1048",  # Kazakh
                 "mac_cyrillic": "mac_cyrillic", "maccyrillic": "mac_cyrillic",  # Bulgarian, Belarusian, Macedonian, Russian, Serbian
                 "mac_greek": "mac_greek", "macgreek": "mac_greek",  # Greek
                 "mac_iceland": "mac_iceland", "maciceland": "mac_iceland",  # Icelandic
                 "mac_latin2": "mac_latin2", "maclatin2": "mac_latin2", "maccentraleurope": "mac_latin2",  # Central and Eastern Europe
                 "mac_centeuro": "mac_latin2",  # Central and Eastern Europe
                 "mac_roman": "mac_roman", "macroman": "mac_roman", "macintosh": "mac_roman",  # Western Europe
                 "mac_turkish": "mac_turkish", "macturkish": "mac_turkish",  # Turkish
                 "ptcp154": "ptcp154", "csptcp154": "ptcp154", "pt154": "cp154", "154": "ptcp154", "cyrillic_asian": "ptcp154",  # Kazakh
                 "shift_jis": "shift_jis", "csshiftjis": "shift_jis", "shiftjis": "shift_jis",  # Japanese
                 "sjis": "shift_jis", "s_jis": "shift_jis",  # Japanese
                 "shift_jis_2004": "shift_jis_2004", "shiftjis2004": "shift_jis_2004",  # Japanese
                 "sjis_2004": "shift_jis_2004", "sjis2004": "shift_jis_2004",  # Japanese
                 "shift_jisx0213": "shift_jisx0213", "shiftjisx0213": "shift_jisx0213",  # Japanese
                 "sjisx0213": "shift_jisx0213", "s_jisx0213": "shift_jisx0213",  # Japanese
                 "utf_32": "utf_32", "u32": "utf_32", "utf32": "utf_32",  # all languages
                 "utf_32_be": "utf_32_be", "utf_32be": "utf_32_be",  # all languages
                 "utf_32_le": "utf_32_le", "utf_32le": "utf_32_le",  # all languages
                 "utf_16": "utf_16", "utf16": "utf_16", "u16": "utf_16",  # all languages
                 "utf_16_be": "utf_16_be", "utf_16be": "utf_16_be",  # all languages
                 "utf_16_le": "utf_16_le", "utf_16le": "utf_16_le",  # all languages
                 "utf_7": "utf_7", "u7": "utf_7", "unicode_1_1_utf_7": "utf_7", "65000": "utf_7", "cp65000": "utf_7",  # all languages
                 "utf_8": "utf_8", "u8": "utf_8", "utf": "utf_8", "utf8": "utf_8", "65001": "utf_8", "cp65001": "utf_8",  # all languages
                 "utf_8_sig": "utf_8_sig",  # all languages
                 }


# codepage_aliases_relaxed only contain values mentioned in Standard Encodings from https://docs.python.org/3/library/codecs.html#standard-encodings
# all values are lowercase, "-" and "_" are replaced with "" - so we have a smaller list which might map encodings more flexible.
codec_aliases_relaxed = {"ascii": "ascii", "646": "ascii" , "usascii": "ascii",  # English
                         "big5": "big5", "big5tw": "big5", "csbig5": "big5",  # Traditional Chinese
                         "big5hkscs": "big5hkscs", "hkscs": "big5hkscs",  # Traditional Chinese
                         "cp037": "cp037", "ibm037": "cp037", "ibm039": "cp037", "037": "cp037",  # English
                         "cp273": "cp273", "273": "cp273", "ibm273": "cp273", "csibm273": "cp273",  # German
                         "cp424": "cp424", "ebcdiccphe": "cp424", "ibm424": "cp424", "424": "cp424",  # Hebrew
                         "cp437": "cp437", "437": "cp437", "ibm437": "cp437",  # English, United States
                         "cp500": "cp500", "ebcdiccpbe": "cp500", "ebcdiccpch": "cp500", "ibm500": "cp500", "500": "cp500",  # Western Europe
                         "cp720": "cp720", "720": "cp720",  # Arabic
                         "cp737": "cp737", "737": "cp737",  # Greek
                         "cp775": "cp775", "ibm775": "cp775", "775": "cp775",  # Baltic languages
                         "cp850": "cp850", "850": "cp850", "ibm850": "cp850",  # Western Europe
                         "cp852": "cp852", "852": "cp852", "ibm852": "cp852",  # Central and Eastern Europe
                         "cp855": "cp855", "855": "cp855", "ibm855": "cp855",  # Bulgarian, Belorussian, Macedonian, Russian, Serbian
                         "cp856": "cp856", "856": "cp856",  # Hebrew
                         "cp857": "cp857", "857": "cp857", "ibm857": "cp857",  # Turkish
                         "cp858": "cp858", "858": "cp858", "ibm858": "cp858",  # Western Europe
                         "cp860": "cp860", "860": "cp860", "ibm860": "cp860",  # Portuguese
                         "cp861": "cp861", "861": "cp861", "ibm861": "cp861", "cpis": "cp861",  # Icelandic
                         "cp862": "cp862", "862": "cp862", "ibm862": "cp862",  # Hebrew
                         "cp863": "cp863", "863": "cp863", "ibm863": "cp863",  # Canadian-French
                         "cp864": "cp864", "864": "cp864", "ibm864": "cp864",  # Arabic
                         "cp865": "cp865", "865": "cp865", "ibm865": "cp865",  # Danish, Norwegian
                         "cp866": "cp866", "866": "cp866", "ibm866": "cp866",  # Russian
                         "cp869": "cp869", "869": "cp869", "ibm869": "cp869", "cpgr": "cp869",  # Modern Greek
                         "cp874": "cp874", "874": "cp874",  # Thai
                         "cp875": "cp875", "875": "cp875",  # Greek
                         "cp932": "cp932", "932": "cp932", "ms932": "cp932", "mskanji": "cp932",  # Japanese
                         "cp949": "cp949", "949": "cp949", "ms949": "cp949", "uhc": "cp949",  # Korean
                         "cp950": "cp950", "950": "cp950", "ms950": "cp950",  # Traditional Chinese
                         "cp1006": "cp1006", "1006": "cp1006",  # Urdu
                         "cp1026": "cp1026", "1026": "cp1026", "ibm1026": "cp1026",  # Turkish
                         "cp1125": "cp1125", "1125": "cp1125", "ibm1125": "cp1125", "cp866u": "cp1125", "ruscii": "cp1125",  # Ukrainian
                         "cp1140": "cp1140", "1140": "cp1140", "ibm1140": "cp1140",  # Western Europe
                         "cp1250": "cp1250", "1250": "cp1250", "windows1250": "cp1250",  # Central and Eastern Europe
                         "cp1251": "cp1251", "1251": "cp1251", "windows1251": "cp1251",  # Bulgarian, Belorussian, Macedonian, Russian, Serbian
                         "cp1252": "cp1252", "1252": "cp1252", "windows1252": "cp1252",  # Western Europe
                         "cp1253": "cp1253", "1253": "cp1253", "windows1253": "cp1253",  # Greek
                         "cp1254": "cp1254", "1254": "cp1254", "windows1254": "cp1254",  # Turkish
                         "cp1255": "cp1255", "1255": "cp1255", "windows1255": "cp1255",  # Hebrew
                         "cp1256": "cp1256", "1256": "cp1256", "windows1256": "cp1256",  # Arabic
                         "cp1257": "cp1257", "1257": "cp1257", "windows1257": "cp1257",  # Baltic languages
                         "cp1258": "cp1258", "1258": "cp1258", "windows1258": "cp1258",  # Vietnamese
                         "eucjp": "euc_jp", "ujis": "euc_jp",  # Japanese
                         "eucjis2004": "euc_jis_2004", "jisx0213": "euc_jis_2004",  # Japanese
                         "eucjisx0213": "euc_jisx0213",  # Japanese
                         "euckr": "euc_kr", "korean": "euc_kr", "ksc5601": "euc_kr",  # Korean
                         "ksc56011987": "euc_kr", "ksx1001": "euc_kr",  # Korean
                         "gb2312": "gb2312", "chinese": "gb2312", "csiso58gb231280": "gb2312", "euccn": "gb2312",  # Simplified Chinese
                         "eucgb2312cn": "gb2312", "gb23121980": "gb2312", "gb231280": "gb2312",  # Simplified Chinese
                         "isoir58": "gb2312",  # Simplified Chinese
                         "gbk": "gbk", "936": "gbk", "cp936": "gbk", "ms936": "gbk",  # Unified Chinese
                         "gb18030": "gb18030", "gb180302000": "gb18030",  # Unified Chinese
                         "hz": "hz", "hzgb": "hz", "hzgb2312": "hz",  # Simplified Chinese
                         "iso2022jp": "iso2022_jp", "csiso2022jp": "iso2022_jp",  # Japanese
                         "iso2022jp1": "iso2022_jp_1",  # Japanese
                         "iso2022jp2": "iso2022_jp_2",  # Japanese, Korean, Simplified Chinese, Western Europe, Greek
                         "iso2022jp2004": "iso2022_jp_2004",  # Japanese
                         "iso2022jp3": "iso2022_jp_3",  # Japanese
                         "iso2022jpext": "iso2022_jp_ext",  # Japanese
                         "iso2022kr": "iso2022_kr", "csiso2022kr": "iso2022_kr",  # Korean
                         "latin1": "latin_1", "iso88591": "latin_1", "8859": "latin_1", "cp819": "latin_1",  # Western Europe
                         "819": "latin_1", "latin": "latin_1", "l1": "latin_1",  # Western Europe
                         "iso88592": "iso8859_2", "latin2": "iso8859_2", "l2": "iso8859_2",  # Central and Eastern Europe
                         "iso88593": "iso8859_3", "latin3": "iso8859_3", "l3": "iso8859_3",  # Esperanto, Maltese
                         "iso88594": "iso8859_4", "latin4": "iso8859_4", "l4": "iso8859_4",  # Baltic languages
                         "iso88595": "iso8859_5", "cyrillic": "iso8859_5",  # Bulgarian, Belorussian, Macedonian, Russian, Serbian
                         "iso88596": "iso8859_6", "arabic": "iso8859_6",  # Arabic
                         "iso88597": "iso8859_7", "greek": "iso8859_7", "greek8": "iso8859_7",  # Greek
                         "iso88598": "iso8859_8", "hebrew": "iso8859_8",  # Hebrew
                         "iso88599": "iso8859_9", "latin5": "iso8859_9", "l5": "iso8859_9",  # Turkish
                         "iso885910": "iso8859_10", "latin6": "iso8859_10", "l6": "iso8859_10",  # Nordic languages
                         "iso885911": "iso8859_11", "thai": "iso8859_11",  # Thai languages
                         "iso885913": "iso8859_13", "latin7": "iso8859_13", "l7": "iso8859_13",  # Baltic languages
                         "iso885914": "iso8859_14", "latin8": "iso8859_14", "l8": "iso8859_14",  # Celtic languages
                         "iso885915": "iso8859_15", "latin9": "iso8859_15", "l9": "iso8859_15",  # Western Europe
                         "iso885916": "iso8859_16", "latin10": "iso8859_16", "l10": "iso8859_16",  # South-Eastern Europe
                         "johab": "johab", "cp1361": "johab", "1361": "johab", "ms1361": "johab",  # Korean
                         "koi8r": "koi8_r",  # Russian
                         "koi8t": "koi8_t",  # Tajik
                         "koi8u": "koi8_u",  # Ukrainian
                         "kz1048": "kz1048", "strk10482002": "kz1048", "rk1048": "kz1048",  # Kazakh
                         "maccyrillic": "mac_cyrillic",  # Bulgarian, Belorussian, Macedonian, Russian, Serbian
                         "macgreek": "mac_greek",  # Greek
                         "maciceland": "mac_iceland",  # Icelandic
                         "maclatin2": "mac_latin2", "maccentraleurope": "mac_latin2", "maccenteuro": "mac_latin2",  # Central and Eastern Europe
                         "macroman": "mac_roman", "macintosh": "mac_roman",  # Western Europe
                         "macturkish": "mac_turkish",  # Turkish
                         "ptcp154": "ptcp154", "csptcp154": "ptcp154", "pt154": "ptcp154",  # Kazakh
                         "cp154": "ptcp154", "154": "ptcp154", "cyrillicasian": "ptcp154",  # Kazakh
                         "shiftjis": "shift_jis", "csshiftjis": "shift_jis", "sjis": "shift_jis",  # Japanese
                         "shiftjis2004": "shift_jis_2004", "sjis2004": "shift_jis_2004",  # Japanese
                         "shiftjisx0213": "shift_jisx0213", "sjisx0213": "shift_jisx0213",  # Japanese
                         "utf32": "utf_32", "u32": "utf_32",  # all languages
                         "utf32be": "utf_32_be",  # all languages
                         "utf32le": "utf_32_le",  # all languages
                         "utf16": "utf_16", "u16": "utf_16",  # all languages
                         "utf16be": "utf_16_be",  # all languages
                         "utf16le": "utf_16_le",  # all languages
                         "utf7": "utf_7", "u7": "utf_7", "unicode11utf7": "utf_7", "65000": "utf_7", "cp65000": "utf_7",  # all languages
                         "utf8": "utf_8", "u8": "utf_8", "utf": "utf_8", "65001": "utf_8", "cp65001": "utf_8",  # all languages
                         "utf8sig": "utf_8_sig",  # all languages
                         }


codec_languages = {"ascii": "English", "big5": "Traditional Chinese", "big5hkscs": "Traditional Chinese", "cp037": "English", "cp273": "German",
                   "cp424": "Hebrew", "cp437": "English, United States", "cp500": "Western Europe", "cp720": "Arabic", "cp737": "Greek",
                   "cp775": "Baltic languages", "cp850": "Western Europe", "cp852": "Central and Eastern Europe",
                   "cp855": "Bulgarian, Belarusian , Macedonian, Russian, Serbian", "cp856": "Hebrew", "cp857": "Turkish", "cp858": "Western Europe",
                   "cp860": "Portuguese", "cp861": "Icelandic", "cp862": "Hebrew", "cp863": "Canadian-French", "cp864": "Arabic",
                   "cp865": "Danish, Norwegian", "cp866": "Russian", "cp869": "Modern Greek", "cp874": "Thai", "cp875": "Greek", "cp932": "Japanese",
                   "cp949": "Korean", "cp950": "Traditional Chinese", "cp1006": "Urdu", "cp1026": "Turkish", "cp1125": "Ukrainian",
                   "cp1140": "Western Europe", "cp1250": "Central and Eastern Europe", "cp1251": "Bulgarian, Belarusian, Macedonian, Russian, Serbian",
                   "cp1252": "Western Europe", "cp1253": "Greek", "cp1254": "Turkish", "cp1255": "Hebrew", "cp1256": "Arabic", "cp1257": "Baltic languages",
                   "cp1258": "Vietnamese", "euc_jp": "Japanese", "euc_jis_2004": "Japanese", "euc_jisx0213": "Japanese", "euc_kr": "Korean",
                   "gb2312": "Simplified Chinese", "gbk": "Unified Chinese", "gb18030": "Unified Chinese", "hz": "Simplified Chinese",
                   "iso2022_jp": "Japanese", "iso2022_jp_1": "Japanese", "iso2022_jp_2": "Japanese, Korean, Simplified Chinese, Western Europe, Greek",
                   "iso2022_jp_2004": "Japanese", "iso2022_jp_3": "Japanese", "iso2022_jp_ext": "Japanese", "iso2022_kr": "Korean",
                   "latin_1": "Western Europe", "iso8859_2": "Central and Eastern Europe", "iso8859_3": "Esperanto, Maltese",
                   "iso8859_4": "Baltic languages", "iso8859_5": "Bulgarian, Belarusian, Macedonian, Russian, Serbian", "iso8859_6": "Arabic",
                   "iso8859_7": "Greek", "iso8859_8": "Hebrew", "iso8859_9": "Turkish", "iso8859_10": "Nordic languages", "iso8859_11": "Thai languages",
                   "iso8859_13": "Baltic languages", "iso8859_14": "Celtic languages", "iso8859_15": "Western Europe", "iso8859_16": "South-Eastern Europe",
                   "johab": "Korean", "koi8_r": "Russian", "koi8_t": "Tajik", "koi8_u": "Ukrainian", "kz1048": "Kazakh",
                   "mac_cyrillic": "Bulgarian, Belarusian, Macedonian, Russian, Serbian", "mac_greek": "Greek", "mac_iceland": "Icelandic",
                   "mac_latin2": "Central and Eastern Europe", "mac_roman": "Western Europe", "mac_turkish": "Turkish", "ptcp154": "Kazakh",
                   "shift_jis": "Japanese", "shift_jis_2004": "Japanese", "shift_jisx0213": "Japanese",
                   "utf_32": "all languages", "utf_32_be": "all languages", "utf_32_le": "all languages",
                   "utf_16": "all languages", "utf_16_be": "all languages", "utf_16_le": "all languages",
                   "utf_7": "all languages", "utf_8": "all languages", "utf_8_sig": "all languages",
                   }


def _disable_chardet_confidence_logging() -> None:
    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
    logging.getLogger('chardet.universaldetector').setLevel(logging.INFO)


_disable_chardet_confidence_logging()


# get_file_encoding{{{
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
    # get_file_encoding}}}
    detected = chardet.detect(raw_bytes)
    encoding = str(detected['encoding']).lower().replace('-', '_')
    confidence = detected['confidence']
    # locale.getpreferredencoding sometimes reports cp1252, but is cp850, so check with chcp
    if confidence < 0.95:
        encoding = get_system_preferred_encoding()
        lib_log_utils.log_warning(f'can not detect encoding from raw_bytes, returning system default encoding: {encoding}')

    return encoding


# get_system_preferred_encoding{{{
def get_system_preferred_encoding() -> str:
    """ returns the system preferred encoding in lowercase. Works on posix, windows and WINE
    On windows, the python default function "locale.getpreferredencoding" sometimes reports falsely cp1252 instead of cp850,
    therefore we check also with windows command "chcp" for the correct preferred codepage
    Note that the python codec name will be returned, such as : utf_8, utf_8_sig etc.
    see: https://docs.python.org/3/library/codecs.html#standard-encodings
    """
    # get_system_preferred_encoding}}}
    if lib_platform.is_platform_posix:
        return get_system_preferred_encoding_posix()
    elif lib_platform.is_platform_windows:
        return get_system_preferred_encoding_windows()
    else:   # pragma: no cover
        raise RuntimeError(f'Operating System {platform.system()} not supported')   # pragma: no cover


def get_system_preferred_encoding_posix() -> str:
    """
    Note that depending on different factors aliases of the codec name can be returned, such as : utf_8, utf8, etc.

    """
    os_encoding = locale.getpreferredencoding()
    os_encoding_simple = _simplify_codec_name(os_encoding)
    python_codec = codec_aliases_relaxed[os_encoding_simple]
    return python_codec


def get_system_preferred_encoding_windows() -> str:
    """
    >>> my_encoding = get_system_preferred_encoding_windows()
    >>> assert my_encoding == 'cp850' or my_encoding == 'utf_8'
    """

    # locale.getpreferredencoding sometimes reports cp1252, but in reality it is cp850, so we check with chcp again (especially when shell=True)

    preferred_os_encoding = locale.getpreferredencoding()

    if lib_platform.is_platform_windows_wine:   # pragma: no cover # no chcp command on wine
        lib_log_utils.log_warning('assuming encoding cp850 for WINE')   # pragma: no cover
        chcp_response = '850'                                           # pragma: no cover
    elif lib_platform.is_platform_posix:        # we called a wine program on linux probably
        chcp_response = '850'
    elif lib_platform.is_platform_windows:
        my_process = subprocess.Popen(['chcp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = my_process.communicate()
        chcp_response = stdout.decode(preferred_os_encoding)
    else:   # pragma: no cover
        lib_log_utils.log_warning('assuming encoding utf_8 for unknown operating system')   # pragma: no cover
        chcp_response = 'utf_8'  # pragma: no cover

    chcp_response_simple = _simplify_codec_name(chcp_response)

    if chcp_response_simple in codec_aliases_relaxed:
        return codec_aliases_relaxed[chcp_response_simple]

    lib_log_utils.log_warning(f'can not find the chcp response "{chcp_response}" in my list of valid encodings')
    lib_log_utils.log_warning('can not detect windows encoding with chcp, assuming cp850')
    return 'cp850'


# get_language_by_codec_name{{{
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
    # get_language_by_codec_name}}}
    codec_name_simple = _simplify_codec_name(codec_name)
    try:
        python_codec_name = codec_aliases_relaxed[codec_name_simple]
    except KeyError:
        raise KeyError(f'codec "{codec_name}" not found')
    try:
        language = codec_languages[python_codec_name]
    except KeyError:    # pragma: no cover
        raise KeyError(f'language for codec "{python_codec_name}" not found')   # pragma: no cover
    return language


def _simplify_codec_name(codec_name: str) -> str:
    """
    reduce the variations of codec names, because it's easier for comparison.

    >>> assert _simplify_codec_name('UTF8') == 'utf8'
    >>> assert _simplify_codec_name('UTF-8') == 'utf8'
    >>> assert _simplify_codec_name('UTF_8') == 'utf8'
    """
    simplified_codec_name = codec_name.lower().replace('-', '_')
    simplified_codec_name = simplified_codec_name.replace('_', '')
    return simplified_codec_name


if __name__ == "__main__":
    print(b'this is a library only, the executable is named "lib_detect_encoding_cli.py"', file=sys.stderr)

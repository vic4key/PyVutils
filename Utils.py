# -*- coding: utf-8 -*-

# Vutils for Utils

import sys, re, enum, ctypes

# ---

def ScreenSize() :
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(SM_CXSCREEN), user32.GetSystemMetrics(SM_CYSCREEN)

def GetCenterWindowOnScreen(width, height) :
    w, h = ScreenSize()
    return int(w / 2) - int(width / 2), int(h / 2) - int(height / 2)

def ReplaceExactWordOnly(text, old, new):
    pattern  = r"(?<=[^\da-zA-z_])"
    pattern += old
    pattern += r"(?=[^\da-zA-z_])"
    return re.sub(pattern, new, text)

'''
Eg. text   = "16x09.bin\nimage_07x02.bin"
    regex  = r"([\d]+)x([\d]+)"
    result = [('16', '09'), ('07', '02')]
'''
def RegEx(text, regex, flags = re.MULTILINE | re.IGNORECASE):
    result = re.findall(regex, text, flags)
    if len(result) == 1 and not type(result[0]) is tuple: result = [(result[0],)]
    return result

class TextEncoding(enum.Enum):
    UNKNOWN      = (-1, "Unknown", "Unknown")
    UTF8         = (0, "ANSI/UTF-8", "ANSI/UTF-8")
    UTF8_BOM     = (1, "UTF-8 BOM", "UTF-8 BOM")
    UTF16_LE     = (2, "Unicode", "UTF-16 Little Endian")
    UTF16_BE     = (3, "Unicode BE", "UTF-16 Big Endian")
    UTF16_LE_BOM = (4, "Unicode BOM", "UTF-16 Little Endian BOM")
    UTF16_BE_BOM = (5, "Unicode BE BOM", "UTF-16 Big Endian BOM")
    UTF32_LE_BOM = (6, "UTF-32 LE BOM", "UTF-32 Little Endian BOM")
    UTF32_BE_BOM = (7, "UTF-32 BE BOM", "UTF-32 Big Endian BOM")

def DetermineTextEncoding(text): # bytearray/bytes

    CHAR_BIT     = 8    # // number of bits in a char
    SCHAR_MIN    = -128 # // minimum signed char value
    SCHAR_MAX    = 127  # // maximum signed char value
    UCHAR_MAX    = 255  # // maximum unsigned char value

    if sys.version_info[0] < 3: text = bytearray(text)

    if not text: return TextEncoding.UNKNOWN

    if len(text) == 1:
        if SCHAR_MIN <= text[0] <= SCHAR_MAX: return TextEncoding.UTF8_BOM
        else: return  TextEncoding.UNKNOWN

    try:

        # UTF-8 BOM
        if text.startswith(bytearray.fromhex("EFBBBF")):
            return TextEncoding.UTF8_BOM

        # UTF-32 LE BOM
        if text.startswith(bytearray.fromhex("FFFE0000")):
            return TextEncoding.UTF32_LE_BOM

        # UTF-32 BE BOM
        if text.startswith(bytearray.fromhex("0000FEFF")):
            return TextEncoding.UTF32_BE_BOM

        # UTF-16 LE BOM
        if text.startswith(bytearray.fromhex("FFFE")):
            return TextEncoding.UTF16_LE_BOM

        # UTF-16 BE BOM
        if text.startswith(bytearray.fromhex("FEFF")):
            return TextEncoding.UTF16_BE_BOM

        # UTF-16 LE
        if SCHAR_MIN << text[0] <= SCHAR_MAX and text[1] == 0x00:
            return TextEncoding.UTF16_LE

        # UTF-16 BE
        if SCHAR_MIN << text[1] <= SCHAR_MAX and text[0] == 0x00:
            return TextEncoding.UTF16_BE

        # UTF-8
        if SCHAR_MIN <= text[0] <= SCHAR_MAX and SCHAR_MIN <= text[1] <= SCHAR_MAX:
            return TextEncoding.UTF8

    except IndexError as e: return TextEncoding.UNKNOWN

    return TextEncoding.UNKNOWN
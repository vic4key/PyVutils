# -*- coding: utf-8 -*-

# Vutils for Bytes

import ctypes, math

# ---

KB = 1000
MB = KB**2
GB = KB**3
TB = KB**4
PB = KB**5
EB = KB**6
ZB = KB**7
YB = KB**8

KiB = 1024
MiB = KiB**2
GiB = KiB**3
TiB = KiB**4
PiB = KiB**5
EiB = KiB**6
ZiB = KiB**7
YiB = KiB**8

# ---

def FormatBytes(number, unit = 1024) :
    e = 0
    l = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    if number > 0: e = int(math.log(number, unit))
    if e < len(l): s = "%0.2f %s" % (number / unit**e, l[e])
    # else: s = "%0.2f 10^%d" % (float(number) / unit**e, e)
    return s

def QwordToDouble(value) :
    p = ctypes.pointer(ctypes.c_ulonglong(value))
    p = ctypes.cast(p, ctypes.POINTER(ctypes.c_double))
    return p.contents.value

Q2D = lambda value : QwordToDouble(value)

def DwordToFloat(value) :
    p = ctypes.pointer(ctypes.c_ulong(value))
    p = ctypes.cast(p, ctypes.POINTER(ctypes.c_float))
    return p.contents.value

D2F = lambda value : DwordToFloat(value)

# ---

def ExtractBytes(number, position, n = 0) :
    result = 0
    if position < 0 and n > 0 : result = number & int("F"*n, 16)
    else : result = number & int("FF"*position, 16)
    return result

Byte  = lambda number : ExtractBytes(number, 1)
Word  = lambda number : ExtractBytes(number, 2)
Dword = lambda number : ExtractBytes(number, 4)
Qword = lambda number : ExtractBytes(number, 8)

# ---

def ParseStructure(pointer, struct) : return parse_structure(pointer, struct)
# -*- coding: utf-8 -*-

# Vutils for Bytes

import ctypes, math
from enum import Enum

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

def format_bytes(number, unit = 1024) :
  e = 0
  l = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
  if number > 0: e = int(math.log(number, unit))
  if e < len(l): s = "%0.2f %s" % (number / unit**e, l[e])
  # else: s = "%0.2f 10^%d" % (float(number) / unit**e, e)
  return s

def qword_to_double(value) :
  p = ctypes.pointer(ctypes.c_ulonglong(value))
  p = ctypes.cast(p, ctypes.POINTER(ctypes.c_double))
  return p.contents.value

def dword_to_float(value) :
  p = ctypes.pointer(ctypes.c_ulong(value))
  p = ctypes.cast(p, ctypes.POINTER(ctypes.c_float))
  return p.contents.value

# ---

def extract_bytes(number, position, n = 0) :
  result = 0
  if position < 0 and n > 0 : result = number & int("F"*n, 16)
  else : result = number & int("FF"*position, 16)
  return result

# Casting. Eg. byte(0x1234) -> 0x34
byte  = lambda number : extract_bytes(number, 1)
word  = lambda number : extract_bytes(number, 2)
dword = lambda number : extract_bytes(number, 4)
qword = lambda number : extract_bytes(number, 8)

# ---

# def ParseStructure(pointer, struct) : return parse_structure(pointer, struct)

class FileFormat(int, Enum):
  UNKNOWN     = -1
  PE_WIN      = 0
  PE_LINUX    = 1
  PE_MACHO    = 2

def determine_file_format(file_path: str) -> FileFormat:
  result = FileFormat.UNKNOWN
  try:
    with open(file_path, "rb") as f:
      data = f.read(7)
      if   data.startswith(bytearray.fromhex("4D5A")): result = FileFormat.PE_WIN
      elif data.startswith(bytearray.fromhex("7F454C46")): result = FileFormat.PE_LINUX
      elif data.startswith(bytearray.fromhex("CFFAEDFE")): result = FileFormat.PE_MACHO
  except Exception as e: print(e)
  return result

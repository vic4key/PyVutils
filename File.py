# -*- coding: utf-8 -*-

# Vutils for File/Directory

import os, stat, glob, re

from . import Utils

# ---

def Read(file_path, mode = "rb"):
    file = open(file_path, mode)
    data = file.read()
    file.close()
    return data

def Write(file_path, data, mode = "wb"):
    file = open(file_path, mode)
    file.write(data)
    file.close()
    return

def Log(filePath, text):
    file = open(filePath, "a+")
    file.write(text + "\n")
    file.close()
    return

# ---

def ExtractFileDirectory(filePath): return os.path.split(filePath)[0]

def ExtractFileName(filePath): return os.path.split(filePath)[1]

def ExtractFileExtension(filePath, includedDOT = False):
    s = os.path.splitext(filePath)[1]
    if not includedDOT : s = s[1:]
    return s

def IsFileExists(filePath): return os.path.isfile(filePath)

def IsDirectoryExists(directory): return os.path.isdir(directory)

def NormalizePath(path, includedLastSlash = False):
    s = path.replace("\\\\", os.path.sep).replace("\\", os.path.sep).replace("//", os.path.sep).replace("/", os.path.sep)
    if includedLastSlash: s += os.path.sep
    return s

# ---

# LS Recusive
#
# Eg. for a callback function
# def fnFSCallback(filePath, fileDirectory, fileName):
#     print("`%s` - `%s` - `%s`" % (filePath, fileDirectory, fileName))
#     return
#
# File.LSRecursive(R".", fnFSCallback, ["txt"])

LSR_DEPTH_MAX = -1
LSR_DEPTH_PARENT = 0
LSR_DEPTH_CURRENT = -1

def LSRecursive(directory, fnCallback, extensions = [], depth = LSR_DEPTH_MAX):
    global LSR_DEPTH_CURRENT

    if depth != LSR_DEPTH_MAX and LSR_DEPTH_CURRENT > depth:
        LSR_DEPTH_CURRENT = 0
        return False

    LSR_DEPTH_CURRENT += 1

    uExtensions = []
    if len(extensions): uExtensions = list(map(lambda extension : extension.upper(), extensions))

    pattern = os.path.join(directory, "*")

    for filePath in glob.glob(pattern):
        try:
            mode = os.stat(filePath)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                # if not filePath.startswith("\\"): # comment for LAN sharing path
                if not LSRecursive(filePath, fnCallback, extensions, depth): break
            elif stat.S_ISREG(mode):
                fileName = ExtractFileName(filePath)
                if len(uExtensions):
                    fileExtension = ExtractFileExtension(filePath, False).upper()
                    if fileExtension in uExtensions : fnCallback(filePath, directory, fileName)
                else : fnCallback(filePath, directory, fileName)
            else : pass # Unknown file type
        except WindowsError as e : pass
        except Exception as e : print(e)
    pass

    LSR_DEPTH_CURRENT = 0

    return True

def DetermineEncoding(filePath):
    f = open(filePath, "rb")
    data = f.read(7) # a reasonable number of bytes
    f.close()
    return Utils.DetermineTextEncoding(data)

def CleanFileName(file_name):
    invalid = '<>:"/\|?*+'
    for char in invalid: file_name = file_name.replace(char, '')
    return file_name

# -*- coding: utf-8 -*-

# Vutils for File/Directory

import os, stat

# ---

def ReadFile(file_path, mode = "rb"):
    file = open(file_path, mode)
    data = file.read()
    file.close()
    return data


def WriteFile(file_path, data, mode = "wb"):
    file = open(file_path, mode)
    file.write(data)
    file.close()
    return

def WriteLog(filePath, text):
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

def Slash(directory):
    if directory[-1] != '\\' : directory += "\\"
    return directory

# ---

# LS Recusive
#
# Eg. for a callback function
# def fnFSCallback(filePath, fileDirectory, fileName):
#     print("`%s` - `%s` - `%s`" % (filePath, fileDirectory, fileName))
#     return

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
    if len(extensions): uExtensions = map(lambda extension : extension.upper(), extensions)
    l = os.listdir(directory)

    for e in l:
        try:
            filePath = os.path.join(directory, e)
            mode = os.stat(filePath)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                if not LSRecursive(filePath, fnCallback, extensions, depth): break
            elif stat.S_ISREG(mode):
                if len(uExtensions):
                    fileExtension = ExtractFileExtension(filePath, False).upper()
                    if fileExtension in uExtensions : fnCallback(filePath, directory, e)
                else : fnCallback(filePath, directory, e)
            else : pass # Unknown file type
        except Exception as e : print(e)
    pass

    LSR_DEPTH_CURRENT = 0

    return True
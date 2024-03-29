# -*- coding: utf-8 -*-

# Vutils for File/Directory

import os, stat, glob

from . import Utils

# ---

def read_file(file_path, mode = "rb"):
    file = open(file_path, mode)
    data = file.read()
    file.close()
    return data

def write_file(file_path, data, mode = "wb"):
    file = open(file_path, mode)
    file.write(data)
    file.close()
    return

def log_file(file_path, text):
    file = open(file_path, "a+")
    file.write(text + "\n")
    file.close()
    return

# ---

def extract_file_directory(file_path, included_last_slash = True):
    result = os.path.split(file_path)[0]
    if included_last_slash: result += os.path.sep
    return result

def extract_file_name(file_path, included_extension = True):
    result = os.path.basename(file_path)
    if not included_extension: result = os.path.splitext(result)[0]
    return result

def extract_file_extension(file_path, included_dot = False):
    result = os.path.splitext(file_path)[1]
    if not included_dot : result = result[1:]
    return result

def is_file_exists(file_path): return os.path.isfile(file_path)

def is_directory_exists(directory): return os.path.isdir(directory)

def normalize_path(path, included_last_slash = True):
    s = path.replace("\\", os.path.sep).replace("//", os.path.sep).replace("/", os.path.sep)
    if included_last_slash: s += os.path.sep
    return s

# ---

# LS Recusive

''' Eg. for a callback function
def fn(file_path, file_directory, file_name):
    print("`%s` - `%s` - `%s`" % (file_path, file_directory, file_name))
    return

File.recursive_directory(".", fn, ["txt"])
'''

LSR_DEPTH_MAX = -1
LSR_DEPTH_PARENT = 0
LSR_DEPTH_CURRENT = -1

def recursive_directory(directory, fn, extensions = [], depth = LSR_DEPTH_MAX):
    global LSR_DEPTH_CURRENT

    if depth != LSR_DEPTH_MAX and LSR_DEPTH_CURRENT > depth:
        LSR_DEPTH_CURRENT = 0
        return False

    LSR_DEPTH_CURRENT += 1

    list_extensions = []
    if len(extensions): list_extensions = list(map(lambda extension : extension.upper(), extensions))

    pattern = os.path.join(directory, "*")

    for file_path in glob.glob(pattern):
        try:
            mode = os.stat(file_path)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                # if not file_path.startswith("\\"): # comment for LAN sharing path
                if not recursive_directory(file_path, fn, extensions, depth): break
            elif stat.S_ISREG(mode):
                file_name = extract_file_name(file_path)
                if len(list_extensions):
                    extension = extract_file_extension(file_path, False).upper()
                    if extension in list_extensions : fn(file_path, directory, file_name)
                else : fn(file_path, directory, file_name)
            else : pass # Unknown file type
        except WindowsError as e : pass
        except Exception as e : print(e)
    pass

    LSR_DEPTH_CURRENT = 0

    return True

def determine_encoding(file_path):
    f = open(file_path, "rb")
    data = f.read(7) # a reasonable number of bytes
    f.close()
    return Utils.determine_text_encoding(data)

FILE_NAME_FORBIDDEN_CHARS = "\\/:?\"<>|"

def correct_file_name(file_name: str, replacement_char = '-'):
    for char in FILE_NAME_FORBIDDEN_CHARS: file_name = file_name.replace(char, replacement_char)
    return file_name

def is_file_name_valid(file_name: str):
    for char in FILE_NAME_FORBIDDEN_CHARS:
        if file_name.find(char) != -1:
            return False
    return True

def pickle_save(file_path: str, object) -> bool:
    try:
        import pickle
        with open(file_path, "wb") as f:
            pickle.dump(object, f)
    except Exception as e:
        print(e)
        return False
    return True

def pickle_load(file_path: str):
    object = None
    try:
        import pickle
        with open(file_path, "rb") as f:
            object = pickle.load(f)
    except Exception as e:
        print(e)
        return None
    return object

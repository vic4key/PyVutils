# -*- coding: utf-8 -*-

# Vutils for Others

import traceback
from . import FS

# ---

def log_exception(obj) :
    IDLE_WIDTH = 80

    print("")
    print(" Exception Infomation ".center(IDLE_WIDTH, "*"))
    print("")

    frames = traceback.format_exc().split("\n")

    exception, = frames[-2:-1]
    if len(exception.strip().split(":")) < 2 :
        idx = frames.index(exception)
        frames.remove(exception)
        frames.insert(idx, "BuitinError: " + exception)
    pass

    frame_number = 0

    for frame in frames:
        frame = frame.strip()
        if len(frame) == 0 : continue
        if frame.find("File \"") == 0 :
            info = frame.split(",")
            if len(info) :
                frame_number += 1
                fileName, line_number, func_name = info
                print("%d. '%s' %s at %s : " % (
                    frame_number,
                    FS.extract_file_name(fileName.strip())[:-1],
                    func_name.strip(),
                    line_number.strip(),
                ))
            pass
        else :
            if frame.find("Error: ") != -1 :
                print("E. '%s'" % frame)
            pass
        pass
    pass

    print("")
    print("".center(IDLE_WIDTH, "*"))
    print("")

    return

from functools import lru_cache
cache = lru_cache(maxsize=None)

def __display_hook_hexify(item):
    type_name = type(item).__name__
    if   type_name == "bool": print(item)
    elif type_name in ["int", "long"]: print("0x%X" % item)
    elif type_name != "NoneType": print(repr(item))
    else: pass

__sys_displayhook = None

def console_hexify(enabled = True):
    global __sys_displayhook
    import sys
    if enabled:
        __sys_displayhook = sys.displayhook
        sys.displayhook = __display_hook_hexify
    elif not __sys_displayhook is None:
        sys.displayhook = __sys_displayhook
        __sys_displayhook = None

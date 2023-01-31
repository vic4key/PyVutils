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

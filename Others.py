# -*- coding: utf-8 -*-

# Vutils for Others

import traceback

# ---

def LogException(obj) :
    IDLE_WIDTH = 80

    print("")
    print(" Exception Infomation ".center(IDLE_WIDTH, "*"))
    print("")

    result = ""

    frames = traceback.format_exc().split("\n")

    exception, = frames[-2:-1]
    if len(exception.strip().split(":")) < 2 :
        idx = frames.index(exception)
        frames.remove(exception)
        frames.insert(idx, "BuitinError: " + exception)
    pass

    frameNumber = 0

    for frame in frames:
        frame = frame.strip()
        if len(frame) == 0 : continue
        if frame.find("File \"") == 0 :
            info = frame.split(",")
            if len(info) :
                frameNumber += 1
                fileName, lineNumber, funcName = info
                print("%d. '%s' %s at %s : " % (
                    frameNumber,
                    ExtractFileName(fileName.strip())[:-1],
                    funcName.strip(),
                    lineNumber.strip(),
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
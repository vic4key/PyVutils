# -*- coding: utf-8 -*-

# Vutils for Utils

import ctypes, re

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
    return re.findall(regex, text, flags)
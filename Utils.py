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
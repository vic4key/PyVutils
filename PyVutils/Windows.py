# -*- coding: utf-8 -*-

# Vutils for Windows

import win32api, win32security

# ---

def adjust_privileges(privileges, enable=True):
    # https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants
    flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id = win32security.LookupPrivilegeValue(None, privileges)
    if enable: new_privileges = [(id, win32security.SE_PRIVILEGE_ENABLED)]
    else: new_privileges = [(id, 0)]
    win32security.AdjustTokenPrivileges(token, 0, new_privileges)
    return

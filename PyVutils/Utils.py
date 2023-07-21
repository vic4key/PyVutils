# -*- coding: utf-8 -*-

# Vutils for Utils

import ctypes, time

# ---

def get_screen_size() :
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(SM_CXSCREEN), user32.GetSystemMetrics(SM_CYSCREEN)

def get_center_window_on_screen(width, height) :
    w, h = get_screen_size()
    return int(w / 2) - int(width / 2), int(h / 2) - int(height / 2)

def profiling(fn):
  def _fn_wrapper(*args, **kwargs):
    start_time = time.perf_counter()
    result = fn(*args, **kwargs)
    delta_time = time.perf_counter() - start_time
    print("%s(...) -> %.3fs" % (fn.__qualname__, delta_time))
    return result
  return _fn_wrapper

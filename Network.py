# -*- coding: utf-8 -*-

# Vutils for Network

import os, mechanize, cookielib

# ---

# https://mechanize.readthedocs.io/en/latest/

# Example:
# browser = Network.Browser()
# browser.open("http://viclab.biz/")
# print(browser.title())
# for form in browser.forms(): print(form)

def Browser(headers = [], debug = False, robots = True, redirect = True, referer = True, equiv = True, cookieFile = "") :
    browser = mechanize.Browser()

    cookiejar = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookiejar)
    if len(cookieFile) > 0 and os.path.exists(cookieFile) : cookiejar.load(cookieFile)

    browser.set_handle_robots(robots)
    browser.set_handle_equiv(equiv)
    browser.set_handle_referer(referer)
    browser.set_handle_redirect(redirect)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)

    browser.addheaders = headers

    if debug :
        browser.set_debug_http(True)
        browser.set_debug_redirects(True)
        browser.set_debug_responses(True)
    pass

    return browser
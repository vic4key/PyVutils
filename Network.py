# -*- coding: utf-8 -*-

# Vutils for Network

import os, mechanize

try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib

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

# Proxy Server

# # Example: (remember to change the System/Browsers Proxy Settings of the machine to 127.0.0.1:8080)
#
# from pprint import *
# from email import message_from_string
#
# def fnCallback(self, data):
#     try:
#         s = data.decode("ascii", "ignore")
#         request, hdrs = s.split("\r\n", 1)
#         headers = dict(message_from_string(hdrs).items())
#         print(("[%s]" % request).center(120, "-"))
#         pprint(headers,)
#     except Exception as e: print("[exception]:", e)
#     return data
#
# proxy = Network.Proxy(proxy=("127.0.0.1", 8080), target=("vic.onl", 80), callback=(fnCallback, fnCallback), timeout=None, debug=True)
# proxy.start()

import socket
from threading import Thread

def fnDefaultCallback(instance, data): return data

PROXY_DEFAULT_NUM_CLIENTS = 100
PROXY_DEFAULT_BUFFER_SIZE = 500*1024 # 500KB

class _ProxyClient(Thread):
    def __init__(self, host, port, fn_callback, timeout, debug = False):
        super(_ProxyClient, self).__init__()

        self._debug = debug
        if self._debug : print("[ctor] %s => %08x" % (self.__class__.__name__, id(self)))

        self._server = None

        self._fn_callback = fn_callback

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server.settimeout(timeout)
        server.bind((host, port))
        server.listen(PROXY_DEFAULT_NUM_CLIENTS)

        self._client = server.accept()[0]

        return

    def __del__(self):
        if self._debug : print("[dtor] %s => %08x" % (self.__class__.__name__, id(self)))

    def run(self):
        while True:
            if self._server == None or self._client == None: break
            try:
                data = self._client.recv(PROXY_DEFAULT_BUFFER_SIZE)
                if not data: break

                data = self._fn_callback(self, data)

                self._server.sendall(data)
            except Exception as e:
                if self._debug: print("[exception] %s: %s" % (self.__class__.__name__, str(e)))
                break
        return

class _ProxyTarget(Thread):

    def __init__(self, host, port, fn_callback, timeout, debug = False):
        super(_ProxyTarget, self).__init__()

        self._debug = debug
        if self._debug : print("[ctor] %s => %08x" % (self.__class__.__name__, id(self)))

        self._client = None

        self._fn_callback = fn_callback

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.settimeout(timeout)
        self._server.connect((host, port))

        return

    def __del__(self):
        if self._debug : print("[dtor] %s => %08x" % (self.__class__.__name__, id(self)))

    def run(self):
        while True:
            if self._server == None or self._client == None: break
            try:
                data = self._server.recv(PROXY_DEFAULT_BUFFER_SIZE)
                if not data: break

                data = self._fn_callback(self, data)

                self._client.sendall(data)
            except Exception as e:
                if self._debug: print("[exception] %s: %s" % (self.__class__.__name__, str(e)))
                break
        return

class NetworkProxy(Thread):

    def __init__(self,
        proxy,
        target,
        callback = (fnDefaultCallback, fnDefaultCallback),
        timeout = None,
        debug = False):

        super(NetworkProxy, self).__init__()

        self._fn_client_callback, self._fn_server_callback = callback
        if self._fn_client_callback == None: self._fn_client_callback = fnDefaultCallback
        if self._fn_server_callback == None: self._fn_server_callback = fnDefaultCallback

        self._to_host, self._to_port = target
        self._from_host, self._from_port = proxy

        self._to_host = self._to_host.lower()
        self._from_host = self._from_host.lower()

        self._timeout = timeout
        self._debug = debug

        self._is_running = False

        return

    def run(self):

        while True:

            if self._debug :
                print("[proxy] %s:%d => %s:%d" % (
                    self._from_host, self._from_port, self._to_host, self._to_port))

            self._proxy_client = _ProxyClient(
                self._from_host,
                self._from_port,
                self._fn_client_callback,
                self._timeout,
                self._debug
            )

            self._proxy_target = _ProxyTarget(
                self._to_host,
                self._to_port,
                self._fn_server_callback,
                self._timeout,
                self._debug
            )

            self._proxy_client._server = self._proxy_target._server
            self._proxy_target._client = self._proxy_client._client

            self._proxy_target.start()
            self._proxy_client.start()

            self._is_running = True

        return
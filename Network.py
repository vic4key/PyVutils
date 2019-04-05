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

# Example (rememer to change the Proxy Settings of the machine to 127.0.0.1:1609)
#
# def fnCallback(self, data): return data
#
# proxier = Network.Proxier(("127.0.0.1", 1609), ("viclab.biz", 80), (fnCallback, fnCallback))
# proxier.start()

import socket
from threading import Thread

def fnDefaultCallback(instance, data):
    return data

PROXY_DEFAULT_NUM_CLIENTS = 100
PROXY_DEFAULT_BUFFER_SIZE = 5*1024 # 5KB

class ProxierClient(Thread):

    def __init__(self, host, port, fn_callback, debug = False):
        super(ProxierClient, self).__init__()

        self.server = None

        self.port = port
        self.host = host
        self.fn_callback = fn_callback

        self.debug = debug

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(PROXY_DEFAULT_NUM_CLIENTS)

        self.client = server.accept()[0]

        return

    def run(self):
        while True:
            if self.server == None or self.client == None: continue
            try:
                data = self.client.recv(PROXY_DEFAULT_BUFFER_SIZE)
                if data == None or len(data) == 0: continue

                data = self.fn_callback(self, data)

                self.server.sendall(data)
            except Exception as e:
                if self.debug: print("[EXCEPTION] Occurred in %s: %s" % (self.__class__, str(e)))
                break
        return

class ProxierServer(Thread):

    def __init__(self, host, port, fn_callback, debug = False):
        super(ProxierServer, self).__init__()

        self.client = None

        self.port = port
        self.host = host
        self.fn_callback = fn_callback

        self.debug = debug

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

        return

    def run(self):
        while True:
            if self.server == None or self.client == None: continue
            try:
                data = self.server.recv(PROXY_DEFAULT_BUFFER_SIZE)
                if data == None or len(data) == 0: continue

                data = self.fn_callback(self, data)

                self.client.sendall(data)
            except Exception as e:
                if self.debug: print("[EXCEPTION] Occurred in %s: %s" % (self.__class__, str(e)))
                break
        return

class Proxier(Thread):

    def __init__(self,
        local,
        server,
        callback = (fnDefaultCallback, fnDefaultCallback),
        debug = False):

        super(Proxier, self).__init__()

        from_host, from_port = local
        to_host, to_port = server
        fn_client_callback, fn_server_callback = callback

        if fn_client_callback == None: fn_client_callback = fnDefaultCallback
        if fn_server_callback == None: fn_server_callback = fnDefaultCallback

        self.from_host = from_host
        self.from_port = from_port
        self.fn_client_callback = fn_client_callback

        self.to_host = to_host
        self.to_port = to_port
        self.fn_server_callback = fn_server_callback

        self.is_running = False

        self.debug = debug

        return

    def run(self):
        while True:
            self.proxier_client = ProxierClient(
                self.from_host,
                self.from_port,
                self.fn_client_callback,
                self.debug
            )

            self.proxier_server = ProxierServer(
                self.to_host,
                self.to_port,
                self.fn_server_callback,
                self.debug
            )

            self.proxier_client.start()
            self.proxier_server.start()

            self.proxier_client.server = self.proxier_server.server
            self.proxier_server.client = self.proxier_client.client

            self.is_running = True
        pass

        return
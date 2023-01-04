# Remember to change the Proxy Settings
# And use system proxy settings instead of buitin in browsers

# https://github.com/benoitc/http-parser

import PyVutils as vu
from pprint import *
from email import message_from_string

def callback(self, data):
	try:
		s = data.decode("ascii", "ignore")
		request, hdrs = s.split("\r\n", 1)
		headers = dict(message_from_string(hdrs).items())
		print(("[%s]" % request).center(120, "-"))
		pprint(headers,)
	except Exception as e: print("[exception]:", e)
	return data

proxy = vu.NetworkProxy(
	proxy=("127.0.0.1", 8080),
	target=("vic.onl", 80),
	callback=(callback, callback),
	timeout=None,
	debug=True,
)

proxy.start()

'''
---------------------------------------[POST http://ocsp.comodoca.com/ HTTP/1.1]----------------------------------------
{'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'en-US,en;q=0.5',
 'Connection': 'keep-alive',
 'Content-Length': '83',
 'Content-Type': 'application/ocsp-request',
 'DNT': '1',
 'Host': 'ocsp.comodoca.com',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) '
               'Gecko/20100101 Firefox/74.0'}
----------------------------------------------------[HTTP/1.1 530 ]-----------------------------------------------------
{'CF-Cache-Status': 'MISS',
 'CF-RAY': '57c3d9f6eb20d1d7-HKG',
 'Cache-Control': 'max-age=6',
 'Connection': 'keep-alive',
 'Content-Length': '3833',
 'Content-Type': 'text/html; charset=UTF-8',
 'Date': 'Mon, 30 Mar 2020 18:21:37 GMT',
 'Expires': 'Mon, 30 Mar 2020 18:21:43 GMT',
 'Server': 'cloudflare',
 'Vary': 'Accept-Encoding'}
[exception]: not enough values to unpack (expected 2, got 1)
---------------------------------------[POST http://ocsp.comodoca.com/ HTTP/1.1]----------------------------------------
{'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'en-US,en;q=0.5',
 'Connection': 'keep-alive',
 'Content-Length': '83',
 'Content-Type': 'application/ocsp-request',
 'DNT': '1',
 'Host': 'ocsp.comodoca.com',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) '
               'Gecko/20100101 Firefox/74.0'}
----------------------------------------------------[HTTP/1.1 530 ]-----------------------------------------------------
{'CF-Cache-Status': 'MISS',
 'CF-RAY': '57c3d9f74bc0d1d7-HKG',
 'Cache-Control': 'max-age=6',
 'Connection': 'keep-alive',
 'Content-Length': '3833',
 'Content-Type': 'text/html; charset=UTF-8',
 'Date': 'Mon, 30 Mar 2020 18:21:37 GMT',
 'Expires': 'Mon, 30 Mar 2020 18:21:43 GMT',
 'Server': 'cloudflare',
 'Vary': 'Accept-Encoding'}
[exception]: not enough values to unpack (expected 2, got 1)
---------------------------------------------[GET http://vic.onl/ HTTP/1.1]---------------------------------------------
{'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'en-US,en;q=0.5',
 'Connection': 'keep-alive',
 'DNT': '1',
 'Host': 'vic.onl',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) '
               'Gecko/20100101 Firefox/74.0'}
---------------------------------------------------[HTTP/1.1 200 OK]----------------------------------------------------
{'CF-Cache-Status': 'DYNAMIC',
 'CF-RAY': '57c3da8f6d7c8542-HKG',
 'Connection': 'keep-alive',
 'Content-Encoding': 'gzip',
 'Content-Type': 'text/html; charset=UTF-8',
 'Date': 'Mon, 30 Mar 2020 18:22:04 GMT',
 'Server': 'cloudflare',
 'Transfer-Encoding': 'chunked',
 'Vary': 'Accept-Encoding,User-Agent',
 'X-Turbo-Charged-By': 'LiteSpeed',
 'alt-svc': 'h2=":443"; ma=60'}
---------------------------------------------------------[3f1]----------------------------------------------------------
{}
---------------------[GET http://vic.onl/libraries/Bootstrap-3.3.7/css/bootstrap.min.css HTTP/1.1]----------------------
{'Accept': 'text/css,*/*;q=0.1',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'en-US,en;q=0.5',
 'Connection': 'keep-alive',
 'DNT': '1',
 'Host': 'vic.onl',
 'Referer': 'http://vic.onl/',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) '
               'Gecko/20100101 Firefox/74.0'}
------------------[GET http://vic.onl/libraries/Bootstrap-3.3.7/css/bootstrap-theme.min.css HTTP/1.1]-------------------
{'Accept': 'text/css,*/*;q=0.1',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'en-US,en;q=0.5',
 'Connection': 'keep-alive',
 'DNT': '1',
 'Host': 'vic.onl',
 'Referer': 'http://vic.onl/',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) '
               'Gecko/20100101 Firefox/74.0'}
---------------------------------------------------[HTTP/1.1 200 OK]----------------------------------------------------
{'Accept-Ranges': 'bytes',
 'CF-Cache-Status': 'MISS',
 'CF-RAY': '57c3daa1edad8542-HKG',
 'Cache-Control': 'public, max-age=604800',
 'Connection': 'keep-alive',
 'Content-Encoding': 'gzip',
 'Content-Length': '19714',
 'Content-Type': 'text/css',
 'Date': 'Mon, 30 Mar 2020 18:22:05 GMT',
 'Expires': 'Mon, 06 Apr 2020 18:22:04 GMT',
 'Last-Modified': 'Sun, 18 Aug 2019 17:13:02 GMT',
 'Server': 'cloudflare',
 'Vary': 'Accept-Encoding,User-Agent',
 'X-Turbo-Charged-By': 'LiteSpeed',
 'alt-svc': 'h2=":443"; ma=60'}
[zgCpnNv4b;0+0+ia%Xe0)-csn
0{xCxu5M@;
m6m>7KgzfAO(8/INNKfPPF>~V`r_
@Dp
'''
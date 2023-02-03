import time, requests
import PyVutils as vu

URLS = [
	'http://www.foxnews.com/',
	'http://www.cnn.com/',
	'http://europe.wsj.com/',
	'http://www.foxnews.com/',
	'http://www.cnn.com/',
	'http://europe.wsj.com/',
	'http://www.foxnews.com/',
	'http://www.cnn.com/',
	'http://europe.wsj.com/',
	'http://www.foxnews.com/',
	'http://www.cnn.com/',
]

def req_url(url):
	return requests.get(url).status_code

if __name__ == "__main__":

	result = []

	print("[THREAD]".center(80, "-"))

	start_time = time.time()

	pool = vu.Pool(debug=True)
	pool.add_task_batch(req_url, [(url,) for url in URLS])
	result = pool.launch()

	print(len(result), result)
	print(f"{time.time() - start_time} seconds")

	print("[PROCESS]".center(80, "-"))

	start_time = time.time()

	pool = vu.Pool(debug=True)
	pool.add_task_batch(req_url, [(url,) for url in URLS])
	result = pool.launch()

	print(len(result), result)
	print(f"{time.time() - start_time} seconds")

	print("[SYNC]".center(80, "-"))

	start_time = time.time()

	result = [req_url(url) for url in URLS]

	print(len(result), result)
	print(f"{time.time() - start_time} seconds")

'''
------------------------------------[THREAD]------------------------------------
Summary:
	14 items
	4 threads
	3 items per thread
	2 items are combined to last 2 threads
	Threads:
		Thread#1: 3 items
		Thread#2: 3 items
		Thread#3: 4 items
		Thread#4: 4 items
	Thread 23440 is created
	Thread 2144 is created
	Thread 19472 is created
	Thread 19376 is created
	Thread 2144 is terminated
	Thread 23440 is terminated
	Thread 19376 is terminated
	Thread 19472 is terminated
14 [200, 200, 404, 200, 404, 200, 200, 200, 200, 200, 404, 200, 200, 200]
3.343101978302002 seconds
-----------------------------------[PROCESS]------------------------------------
Summary:
	14 items
	4 processes
	3 items per process
	2 items are combined to last 2 processes
	Processes:
		Process#1: 3 items
		Process#2: 3 items
		Process#3: 4 items
		Process#4: 4 items
	4 processes are created
	4 processes are terminated
14 [200, 200, 200, 200, 200, 404, 404, 200, 200, 200, 404, 200, 200, 200]
3.493217945098877 seconds
-------------------------------------[SYNC]-------------------------------------
14 [200, 200, 404, 200, 200, 200, 404, 200, 200, 200, 404, 200, 200, 200]
10.510623931884766 seconds
'''
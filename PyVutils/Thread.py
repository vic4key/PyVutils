import sys, os, threading
from multiprocessing import cpu_count

if sys.version_info >= (3, 0): from queue import Queue
else: from Queue import Queue

POOL_BATCH_RESULT = "POOL_BATCH_RESULT"

class Worker(threading.Thread):
    def __init__(self, args, debug = False):
        threading.Thread.__init__(self)
        self._fn, self._tasks, self._results = args
        self._debug = debug
        self.daemon = True
        return

    def run(self):

        if self._debug: print("\tThread %d is created" % self.ident)

        for task in self._tasks:
            try:
                ret = self._fn(*task)
                self._results.put(ret)
            except Exception as e:
                print(e)

        if self._debug: print("\tThread %d is terminated" % self.ident)

        return

class Pool:
    def __init__(self, nthreads = None, debug = False):
        self._debug = debug
        self._fn = None
        self._tasks = []
        self._results = Queue()
        self._nthreads = nthreads if not nthreads in [None, 0] else cpu_count()

    def add_task(self, fn, args):
        self._fn = fn
        self._tasks.append(args)
        return

    def add_task_batch(self, fn, listargs):
        self._fn = fn
        self._tasks.extend(listargs)
        return

    def launch(self):

        # distribute tasks to each thread

        num_list_args = len(self._tasks)
        if num_list_args == 0: return

        num_threads = self._nthreads
        if self._nthreads > num_list_args: num_threads = num_list_args

        num_items_per_threads = self._nthreads if self._nthreads < num_list_args else num_list_args

        num_items_per_threads = num_list_args // num_threads
        num_items_left = num_list_args % num_threads

        segments = []
        for i in range(0, num_threads):
            start = i * num_items_per_threads
            stop  = start + num_items_per_threads
            segments.append(stop)

        # balance tasks for all thread

        idx_segment_head_for_combination = len(segments) - num_items_left

        if num_items_left > 0:
            for i, _ in enumerate(segments[idx_segment_head_for_combination:]):
                segments[i + idx_segment_head_for_combination] += i + 1
        del segments[-1]
        segments.insert(0, 0)

        # summary tasks

        if self._debug: print(
            ("Summary:") +
            ("\n\t%d items" % num_list_args) +
            ("\n\t%d threads" % num_threads) +
            ("\n\t%d items per thread" % num_items_per_threads) +
            ("\n\t%d items are combined to last %d threads" % (num_items_left, num_items_left)) +
            ("\n\tThreads:"))

        # assign tasks to each thread

        threads = []

        for i, segment in enumerate(segments):

            start = segments[i]
            stop  = segments[i + 1] if i < num_threads - 1 else None

            batch_args = self._tasks[start:stop]

            if self._debug: print("\t\tThread#%d: %d items" % (i + 1, len(batch_args)))

            threads.append(Worker((self._fn, batch_args, self._results), self._debug))

        # run multi-threading

        result = []

        for thread in threads: thread.start()
        for thread in threads: thread.join()

        # combine results

        while not self._results.empty():
            ret = self._results.get()
            if type(ret) is dict and POOL_BATCH_RESULT in ret.keys():
                result.extend(ret[POOL_BATCH_RESULT])
            else: result.append(ret)

        return result

# Eg.

# from PyVutils import Thread

# def task(v1, v2, v3):
#     for v in range(0, 10000000): pass
#     return [v1, v2, v3]

# if __name__ == "__main__":
#     pool = Thread.Pool(debug=True)
#     pool.AddTaskBatch(task, [(i, i, i) for i in range(0, 14)])
#     result = pool.Launch()
#     print(result)

import sys, time, _thread, trace
from threading import Thread, Timer

class StoppableThread(Thread):
	"""
    A class that represents a stoppable thread of control.
    def run(*args): pass
	thread = StoppableThread(target=run)
	thread.start()
	do something
	thread.stop()
	"""

	def __init__(self, *args, **keywords):
		Thread.__init__(self, *args, **keywords)
		self.m_killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		Thread.start(self)

	def stop(self):
		self.m_killed = True

	def __run(self):
		# PYDEV DEBUGGER WARNING: sys.settrace() should not be used when the debugger is being used.
		# sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def global_trace(self, frame, why, arg):
		if why == "call":
			return self.local_trace
		else:
			return None

	def local_trace(self, frame, why, arg):
		if self.m_killed:
			if why == "line":
				raise SystemExit()
		return self.local_trace

class LoopingThread(object):
    '''
    Create a thread that running with a looping function
    '''
    m_interval = 0
    m_running  = False
    m_locking  = None
    m_callback = None

    def __init__(self, callback, interval = 0.01, *args, **kwargs): # 10ms
        assert type(callback).__name__ == "function", "The callback must be a function"
        self.m_callback = callback
        self.m_interval = interval
        self.m_args     = args
        self.m_kwargs   = kwargs
        self.m_running  = False
        self.m_locking  = _thread.allocate_lock()

    def start(self):
        self.m_running = True
        _thread.start_new_thread(LoopingThread.function, (self,))

    def stop(self):
        self.m_running = False

    @staticmethod
    def function(self):
        while self.m_running:
            self.m_locking.acquire()
            self.m_callback(*self.m_args, **self.m_kwargs)
            self.m_locking.release()
            time.sleep(self.m_interval)

class LoopingTimer(object):
    '''
    Create a timer that running with a looping function
    '''
    def __init__(self, callback, interval, *args, **kwargs):
        self.m_args     = args
        self.m_kwargs   = kwargs
        self.m_timer    = None
        self.m_running  = False
        self.m_interval = interval
        self.m_callback = callback
        self.start()

    def _run(self):
        self.m_running = False
        self.start()
        self.m_callback(*self.m_args, **self.m_kwargs)

    def start(self):
        if not self.m_running:
            self.m_timer = Timer(self.m_interval, self._run)
            self.m_timer.start()
            self.m_running = True

    def stop(self):
        self.m_timer.cancel()
        self.m_running = False

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

    def AddTask(self, fn, args):
        self._fn = fn
        self._tasks.append(args)
        return

    def AddTaskBatch(self, fn, listargs):
        self._fn = fn
        self._tasks.extend(listargs)
        return

    def Launch(self):

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
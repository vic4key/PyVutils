import sys, os, threading

if sys.version_info >= (3, 0): from queue import Queue
else: from Queue import Queue

POOL_BATCH_RESULT = "POOL_BATCH_RESULT"

class Worker(threading.Thread):
    def __init__(self, tasks, results):
        threading.Thread.__init__(self)
        self._results = results
        self._tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            fn, args, kwargs = self._tasks.get()
            try:
                ret = fn(*args, **kwargs)
                self._results.put(ret)
            except Exception as e:
                print(e)
            finally:
                self._tasks.task_done()
        return

class Pool:
    def __init__(self, nthreads = None):
        if nthreads in [None, 0]: nthreads = os.cpu_count()
        self._tasks = Queue(nthreads)
        self._results = Queue()
        for _ in range(nthreads): Worker(self._tasks, self._results)

    def AddTask(self, fn, *args, **kwargs):
        self._tasks.put((fn, args, kwargs))

    def AddTaskBatch(self, fn, listargs):
        for args in listargs: self.AddTask(fn, *args)

    def Launch(self):
        result = []

        self._tasks.join()

        while not self._results.empty():
            ret = self._results.get()
            if type(ret) is dict and POOL_BATCH_RESULT in ret.keys():
                result.extend(ret[POOL_BATCH_RESULT])
            else: result.append(ret)

        return result

# Eg.

# from PyVutils import Thread

# def task(v1, v2, v3):
#     print(f"task({v1}, {v2}, {v3})")
#     for v in range(0, 10000000): pass
#     return [v1, v2, v3]

# if __name__ == "__main__":
#     pool = Thread.Pool()
#     pool.AddTaskBatch(task, [(i, i, i) for i in range(0, 14)])
#     result = pool.Launch()
#     print(result)